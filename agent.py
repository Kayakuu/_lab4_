import os
import logging
from typing import Annotated, TypedDict, List, Dict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from tools import search_flights, search_hotels, calculate_budget

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agent.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TravelBuddy")

load_dotenv()

with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT: str = f.read()

# 2. Khai báo State với Type Hints
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# 3. Khởi tạo LLM và Tools
api_key: str = os.getenv("OPENAI_API_KEY") or ""

tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key,
    temperature=0
)
llm_with_tools = llm.bind_tools(tools_list)

import time
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage

# 4. Agent Node (Nút xử lý của Agent)
def agent_node(state: AgentState, config: RunnableConfig) -> dict:
    messages: List[BaseMessage] = state["messages"]
    
    # Ghi nhận User Input vào Log (Lấy tin nhắn cuối cùng của người dùng)
    user_input = next((m.content for m in reversed(messages) if isinstance(m, HumanMessage)), "None")
    logger.info(f">>> USER INPUT: {user_input}")
    
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    start_time = time.time()
    logger.info("Bạn chờ tôi chút...")
    
    try:
        # Gọi OpenAI (LangChain tự động xử lý tool calling)
        response = llm_with_tools.invoke(messages)
    except Exception as e:
        logger.error(f"LỖI KẾT NỐI API: {str(e)}")
        # Fallback: Trả về thông báo bảo trì
        return {
            "messages": [AIMessage(content="🔧 Thật xin lỗi bạn, hệ thống TravelBuddy đang được bảo trì. Bạn vui lòng quay lại sau ít phút nữa nhé! ✨")]
        }
    
    # Log metrics cho report
    latency = time.time() - start_time
    usage = getattr(response, "usage_metadata", {})
    prompt_tokens = usage.get("input_tokens", 0)
    completion_tokens = usage.get("output_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)
    
    cost_usd = (prompt_tokens * 0.15 / 1_000_000) + (completion_tokens * 0.60 / 1_000_000)
    cost_vnd = cost_usd * 25000
    
    logger.info(f"--- METRICS: Latency {latency:.2f}s | Tokens {total_tokens} | Cost ~{cost_vnd:.1f} VND ---")
    
    if response.tool_calls:
        for tc in response.tool_calls:
            logger.info(f"Yêu cầu gọi tool: {tc['name']}")
    
    return {"messages": [response]}

# 5. Xây dựng Graph
memory = MemorySaver()
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

# Biên dịch Graph với checkpointer (Bộ nhớ)
graph = builder.compile(checkpointer=memory)

# 6. Chat loop (Vòng lặp trò chuyện)
if __name__ == "__main__":
    logger.info("TravelBuddy đã sẵn sàng phục vụ.")
    print("=" * 60)
    print("TravelBuddy – Trợ lý Du lịch OpenAI (LOGGING ENABLED)")
    print("    Gõ 'quit', 'exit' hoặc 'q' để kết thúc")
    print("=" * 60)
    
    # Cấu hình thread_id cho phiên làm việc hiện tại
    config = {"configurable": {"thread_id": "session_1"}}

    while True:
        try:
            user_input: str = input("\nBạn: ").strip()
            if not user_input or user_input.lower() in ("quit", "exit", "q"):
                logger.info("Kết thúc phiên làm việc.")
                break
            
            logger.info(f"Người dùng hỏi: {user_input}")
            
            # Gửi input mới vào, LangGraph sẽ tự động lấy lịch sử cũ ra dựa trên thread_id
            initial_state = {"messages": [HumanMessage(content=user_input)]}
            result = graph.invoke(initial_state, config=config)
            
            final_message: BaseMessage = result["messages"][-1]
            print(f"\nTravelBuddy:\n{final_message.content}")
            
        except Exception as e:
            logger.error(f"Đã xảy ra lỗi thực thi: {str(e)}")
            print(f"❌ Lỗi: {e}")
