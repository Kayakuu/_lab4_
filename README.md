# ✈️ TravelBuddy - Trợ lý Du lịch thông minh (Lab 4)

Dự án này ứng dụng **LangGraph** để xây dựng một Agent có khả năng lập kế hoạch du lịch tự động. Thay vì chỉ trả lời văn bản đơn thuần, Agent biết cách kết nối nhiều công cụ dữ liệu để đưa ra một phương án hoàn chỉnh (Vé máy bay + Khách sạn + Ngân sách).

## Các tính năng chính
- Agent thông minh: Tự động điều phối công cụ (Flight -> Hotel -> Budget) dựa trên context.
- Dữ liệu thực tế: Gợi ý kèm hyperlink chính xác từ database.
- Quản lý ngân sách: Tự động parse chi phí và đưa ra cảnh báo số dư.
- Hệ thống Logging: Theo dõi latency, token và cost thực tế cho mỗi request.

### 3. Giao diện & Trải nghiệm (web_app.py)
- Dashboard theo dõi chi tiết tài chính và hiệu năng ngay trên Sidebar.
- Phản hồi bằng Markdown với Hyperlink giúp người dùng đặt vé trực tiếp tại website hãng.

## 🚀 Hướng dẫn khởi chạy
1. Cài đặt: `pip install -r requirements.txt`
2. Cấu hình: Dán OpenAI API Key vào file `.env`.
3. Chạy Web: `streamlit run web_app.py`
4. Chạy Console: `python agent.py`

---
**📂 Deliverables:** Bài nộp bao gồm `agent.py`, `tools.py`, `system_prompt.txt` (XML format), và báo cáo kết quả `test_results.md`.
