from langchain_core.tools import tool
from typing import Dict, List, Tuple, Optional

import logging

# Mock Database
AIRLINE_WEBSITES: Dict[str, str] = {
    "Vietnam Airlines": "https://www.vietnamairlines.com/",
    "VietJet Air": "https://www.vietjetair.com/",
    "Bamboo Airways": "https://www.bambooairways.com/",
}

FLIGHTS_DB: Dict[Tuple[str, str], List[Dict]] = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1200000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1100000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1600000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1300000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3200000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1300000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650000, "class": "economy"},
    ],
}

HOTELS_DB: Dict[str, List[Dict]] = {
    "Đà Nẵng": [
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6, "website": "https://memoryhostel.com/"},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350000, "area": "An Thượng", "rating": 4.7, "website": "https://christinas.vn/"},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3500000, "area": "Bãi Dài", "rating": 4.4, "website": "https://vinpearl.com/"},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1500000, "area": "Bãi Trường", "rating": 4.2, "website": "https://melia.com/"},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.0, "website": "https://lahanaresort.com/"},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200000, "area": "Dương Đông", "rating": 4.5, "website": "https://9stationhostel.com/"},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2800000, "area": "Quận 1", "rating": 4.3, "website": "https://rexhotelsaigon.com/"},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1400000, "area": "Quận 1", "rating": 4.1, "website": "https://libertycentral.com/"},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550000, "area": "Quận 3", "rating": 4.4, "website": "https://cochinzen.com/"},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180000, "area": "Quận 1", "rating": 4.6, "website": "https://commonroom.vn/"},
    ],
}

def format_currency(amount: int) -> str:
    """Hàm hỗ trợ format tiền tệ có dấu phân cách."""
    return "{:,}".format(amount).replace(",", ".") + " VND"

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố. Trình bày Hyperlink nếu có.
    """
    try:
        flights = FLIGHTS_DB.get((origin, destination))
        
        if not flights:
            flights = FLIGHTS_DB.get((destination, origin))
            if flights:
                msg = f"Không tìm thấy chuyến bay trực tiếp từ {origin} đi {destination}. Dưới đây là chiều ngược lại:\n"
            else:
                return f"Xin lỗi, hiện TravelBuddy chưa có dữ liệu chuyến bay giữa {origin} và {destination}."
        else:
            msg = f"Danh sách chuyến bay từ {origin} đến {destination} (✈️ Click vào tên hãng để đặt vé):\n"

        for f in flights:
            price_str = format_currency(f['price'])
            airline_name = f['airline']
            # Gắn link hãng hàng không
            website = AIRLINE_WEBSITES.get(airline_name, "#")
            msg += f"- [{airline_name}]({website}) | Khởi hành: {f['departure']} | Hạng: {f['class']} | Giá: {price_str}\n"
        
        return msg
    except Exception as e:
        return f"Đã xảy ra lỗi khi tra cứu chuyến bay: {str(e)}"

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố. Trình bày Hyperlink nếu có.
    """
    try:
        hotels = HOTELS_DB.get(city)
        if not hotels:
            return f"Hiện TravelBuddy chưa có dữ liệu khách sạn tại {city}."

        filtered_hotels = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
        
        if not filtered_hotels:
            return f"Không tìm thấy khách sạn tại {city} có giá dưới {format_currency(max_price_per_night)}. Hãy thử tăng ngân sách."

        sorted_hotels = sorted(filtered_hotels, key=lambda x: x['rating'], reverse=True)

        msg = f"Danh sách khách sạn tại {city} dưới {format_currency(max_price_per_night)} (🏨 Click tên khách sạn để xem thêm):\n"
        for h in sorted_hotels:
            price_str = format_currency(h['price_per_night'])
            website = h.get("website", "#")
            msg += f"- [{h['name']}]({website}) ({h['stars']} sao) | Khu vực: {h['area']} | Đánh giá: {h['rating']} | Giá: {price_str}/đêm\n"
        
        return msg
    except Exception as e:
        return f"Đã xảy ra lỗi khi tìm kiếm khách sạn: {str(e)}"

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả định dạng 'tên_khoản:số_tiền,tên_khoản:số_tiền'
    """
    try:
        expense_items: List[Tuple[str, int]] = []
        total_expense: int = 0
        
        parts: List[str] = expenses.split(',')
        for part in parts:
            if ':' in part:
                name_cost = part.split(':')
                name: str = name_cost[0].strip()
                cost: int = int(name_cost[1].strip())
                expense_items.append((name, cost))
                total_expense += cost
        
        remaining: int = total_budget - total_expense
        
        msg = "--- CHI TIẾT NGÂN SÁCH ---\n"
        for name, cost in expense_items:
            msg += f"- {name}: {format_currency(cost)}\n"
        
        msg += f"------------------------\n"
        msg += f"Tổng chi phí: {format_currency(total_expense)}\n"
        msg += f"Ngân sách ban đầu: {format_currency(total_budget)}\n"
        if remaining >= 0:
            msg += f"Còn lại: {format_currency(remaining)}\n"
        else:
            msg += f"Còn thiếu: {format_currency(abs(remaining))} (⚠️ Bạn đã vượt ngân sách!)\n"
        
        return msg
    except Exception as e:
        return f"Lỗi định dạng expenses. (Chi tiết lỗi: {str(e)})"
