# BÁO CÁO KẾT QUẢ KIỂM THỬ (TEST RESULTS) — TRAVELBUDDY AI

**Người thực hiện:** [Nguyễn Tiến Huy Hoàng]
**Ngày thực hiện:** 2026-04-08
**Mô hình sử dụng:** OpenAI gpt-4o-mini

---

### **Test 1 — Direct Answer (Chào hỏi/Tư vấn chung)**
*   **User Input:** "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."
*   **Kỳ vọng:** Agent phản hồi thân thiện, hỏi thêm thông tin, chưa gọi tool.
*   **Kết quả thực tế:** 
    > Chào bạn! Có rất nhiều điểm đến thú vị ở Việt Nam. Bạn có thể cân nhắc đến Hà Nội, Hồ Chí Minh, Đà Nẵng hoặc Phú Quốc. Bạn thích khám phá thành phố nào nhất? Hoặc bạn có ý tưởng nào về lịch trình chưa?
*   **Nhật ký kỹ thuật (Console Log):**
    - Độ trễ: 1.07 giây
    - Token: 712 input + 44 output = 756 total
    - Chi phí: ~3.15 VND
    - Gọi Tool: Không

---

### **Test 2 — Single Tool Call (Tra cứu một chiều)**
*   **User Input:** "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"
*   **Kỳ vọng:** Gọi `search_flights`, liệt kê danh sách chuyến bay và hyperlink.
*   **Kết quả thực tế:**
    > Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng mà bạn có thể tham khảo:
    > 1. **Vietnam Airlines** [Link](https://www.vietnamairlines.com/) | Giá: 1.450.000 VND | Giờ khởi hành: 06:00
    > 2. **VietJet Air** [Link](https://www.vietjetair.com/) | Giá: 890.000 VND | Giờ khởi hành: 08:30
    > ... (Xem thêm trong giao diện)
*   **Nhật ký kỹ thuật (Console Log):**
    - Độ trễ: 1.09 giây
    - Token: 731 input + 25 output = 756 total
    - Chi phí: ~3.12 VND
    - Gọi Tool: `search_flights`

---

### **Test 3 — Multi-Step Tool Chaining (Chuỗi hành động phức tạp)**
*   **User Input:** "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"
*   **Kỳ vọng:** Gọi Flight -> Hotel -> Budget. Tính toán tổng chi phí và đề xuất.
*   **Kết quả thực tế:**
    > ... (Tìm thấy chuyến bay 1.100.000 VND và khách sạn 200.000 VND/đêm)
    > **Tổng chi phí: 1.500.000 VND**
    > **Dư ngân sách: 3.500.000 VND** cho các hoạt động khác.
*   **Nhật ký kỹ thuật (Console Log):**
    - Độ trễ: 2.91 giây
    - Token: 741 input + 56 output = 797 total
    - Chi phí: ~3.62 VND
    - Gọi Tool: `search_flights`, `search_hotels`, `calculate_budget`

---

### **Test 4 — Missing Info / Clarification (Hỏi lại thông tin thiếu)**
*   **User Input:** "Tôi muốn đặt khách sạn"
*   **Kỳ vọng:** Không gọi tool ngay, hỏi lại khách về thành phố.
*   **Kết quả thực tế:**
    > TravelBuddy hiện tại chỉ hỗ trợ đặt phòng khách sạn tại Hà Nội, Hồ Chí Minh, Đà Nẵng hoặc Phú Quốc. Bạn muốn ở thành phố nào?
*   **Nhật ký kỹ thuật (Console Log):**
    - Độ trễ: 2.15 giây
    - Token: 722 input + 62 output = 784 total
    - Chi phí: ~3.64 VND
    - Gọi Tool: Không

---

### **Test 5 — Guardrail / Refusal (Chặn yêu cầu ngoài lề)**
*   **User Input:** "Giải giúp tôi bài tập lập trình Python về linked list"
*   **Kỳ vọng:** Từ chối lịch sự theo ràng buộc hệ thống.
*   **Kết quả thực tế:**
    > TravelBuddy hiện tại chỉ hỗ trợ đặt vé máy bay, phòng khách sạn và quản lý ngân sách thôi nè! Nếu bạn có kế hoạch du lịch... mình rất vui lòng giúp bạn!
*   **Nhật ký kỹ thuật (Console Log):**
    - Độ trễ: 2.00 giây
    - Token: 727 input + 69 output = 796 total
    - Chi phí: ~3.76 VND
    - Gọi Tool: Không

---

### **KẾT LUẬN**
- Agent vượt qua 100% các bài kiểm thử.
- Tính năng **Fail-fast** (từ chối địa điểm lạ) và **Hyperlink** hoạt động ổn định.
- Tốc độ phản hồi trung bình: **1.8 giây/truy vấn**.
