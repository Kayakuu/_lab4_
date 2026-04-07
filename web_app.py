import streamlit as st
import time
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agent import graph, logger

# =================================================================
# CẤU HÌNH GIAO DIỆN CHUNG (RICH AESTHETICS)
# =================================================================
st.set_page_config(
    page_title="TravelBuddy AI - Chuyên gia du lịch",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS cho phong cách Modern, Premium & Vibrant
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Làm đẹp Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    /* Chat bubbles */
    .stChatMessage {
        background-color: #334155 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        border: 1px solid #475569 !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    .stChatMessage[data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    }

    /* Dashboard Cards */
    .metric-card {
        background: rgba(51, 65, 85, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #475569;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }
    
    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }
    
    .stChatInputContainer {
        padding-bottom: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# =================================================================
# SIDEBAR - BẢNG ĐIỀU KHIỂN & THỐNG KÊ (DASHBOARD)
# =================================================================
with st.sidebar:
    st.title("📊 CHỈ SỐ LIVE")
    st.markdown("---")
    
    # Nút xóa lịch sử
    if st.button("🗑️ Làm mới hành trình"):
        st.session_state.messages = []
        st.session_state.stats = {"latency": 0, "tokens": 0, "cost": 0}
        st.rerun()
    
    # Khởi tạo state cho thống kê nếu chưa có
    if "stats" not in st.session_state:
        st.session_state.stats = {"latency": 0, "tokens": 0, "cost": 0}
    
    # Hiển thị thẻ thống kê
    st.markdown(f"""
    <div class="metric-card">
        <p style='margin:0; font-size: 0.85rem; color: #94a3b8; font-weight: 600;'>⏱️ ĐỘ TRỄ PHẢN HỒI</p>
        <h2 style='margin:0; color: #3b82f6;'>{st.session_state.stats['latency']:.2f}s</h2>
    </div>
    <div class="metric-card">
        <p style='margin:0; font-size: 0.85rem; color: #94a3b8; font-weight: 600;'>🧩 TOKEN TIÊU THỤ</p>
        <h2 style='margin:0; color: #f59e0b;'>{st.session_state.stats['tokens']}</h2>
    </div>
    <div class="metric-card">
        <p style='margin:0; font-size: 0.85rem; color: #94a3b8; font-weight: 600;'>💸 PHÍ ƯỚC TÍNH (VND)</p>
        <h2 style='margin:0; color: #10b981;'>{st.session_state.stats['cost']:.2f}đ</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("🚀 Powered by LangGraph & OpenAI gpt-4o-mini")

# =================================================================
# CHÍNH - KHÔNG GIAN CHAT (MAIN CHAT AREA)
# =================================================================
st.title("✈️ TravelBuddy AI")
st.markdown("#### *Cùng bạn thiết kế những chuyến đi đáng nhớ!* 🌟")

# Khởi tạo lịch sử tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn cũ
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    avatar = "👤" if role == "user" else "✈️"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message.content)

# Ô nhập liệu của người dùng
if prompt := st.chat_input("Hôm nay bạn muốn vi vu ở đâu?"):
    # 1. Hiển thị tin nhắn người dùng
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    # 2. Xử lý qua Agent
    with st.chat_message("assistant", avatar="✈️"):
        message_placeholder = st.empty()
        message_placeholder.markdown("✈️ *Để mình suy nghĩ một chút nhé...*")
        
        # Cấu hình thread_id cho phiên
        config = {"configurable": {"thread_id": "streamlit_session"}}
        initial_state = {"messages": [HumanMessage(content=prompt)]}
        
        try:
            # Đo thời gian bắt đầu
            start_time = time.time()
            
            # Chạy LangGraph
            result = graph.invoke(initial_state, config=config)
            
            # Tính toán thống kê
            latency = time.time() - start_time
            final_msg = result["messages"][-1]
            
            # Lấy thông tin token/cost (Tận dụng metadata từ response)
            usage = getattr(final_msg, "usage_metadata", {})
            prompt_tokens = usage.get("input_tokens", 0)
            completion_tokens = usage.get("output_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
            
            cost_usd = (prompt_tokens * 0.15 / 1_000_000) + (completion_tokens * 0.60 / 1_000_000)
            cost_vnd = cost_usd * 25000
            
            # Cập nhật sidebar stats
            st.session_state.stats = {
                "latency": latency,
                "tokens": total_tokens,
                "cost": cost_vnd
            }
            
            # Hiển thị câu trả lời cuối cùng
            message_placeholder.markdown(final_msg.content)
            st.session_state.messages.append(AIMessage(content=final_msg.content))
            
            # Tự động reload để cập nhật sidebar
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra: {e}")
            logger.error(f"Streamlit Error: {e}")
