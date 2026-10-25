import streamlit as st
import pandas as pd
from google import genai
import time

# ==============================================================================
# 1. CẤU HÌNH TRANG WEB STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Blooming Season - Mùa Xuân Sớm Mai",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. GIAO DIỆN TÙY BIẾN CSS (THEME MÙA XUÂN SỚM MAI)
# ==============================================================================
st.markdown("""
""", unsafe_allow_html=True)

# ==============================================================================
# 3. KNOWLEDGE BASE & SYSTEM PROMPT TỪ BÁO CÁO STEM
# ==============================================================================
SYSTEM_INSTRUCTION = """
Bạn là Blooming Bot - Trợ lý AI đại diện cho dự án STEM nước hoa "Sớm Xuân" (thương hiệu Blooming Season).
Slogan của dự án: "Hương thơm của những khởi đầu an lành".
Ý nghĩa câu chuyện:
- "Sớm": Khoảnh khắc ban mai khi sương chưa tan, gió se mát chuyển dần sang ấm áp; hương thơm biến chuyển từ thanh mát (Sen hồng), qua ngọt dịu (Trà nhài), đến ấm sâu (Đàn hương).
- "Xuân": Mùa của sự bắt đầu, búp non chồi biếc, mang lại cảm giác bình an và thư thái.

Dữ liệu hóa học & Nốt hương:
1. Pinky Lotus (Hương đầu, max 5%): Chứa Methyl palmitate, dẫn xuất Linoleic acid. Hương thơm mát, nhẹ, trong trẻo.
2. Green Tea (Hương giữa, max 4%): Chứa Linalool, geraniol. Mang lại sự tỉnh táo, thanh lọc tinh thần.
3. Jasmine (Hương giữa, max 4%): Chứa Benzyl acetate, linalool, alpha-farnesene. Lưu ý: Mùi hoa nhài tỏa rất mạnh, trong các mẫu thử nếu tỷ lệ cao sẽ dễ lấn át các nốt khác nên cần cân đối cẩn thận.
4. Sandalwood (Hương cuối, max 5%): Chứa alpha-santalol và beta-santalol. Gỗ ngọt ấm, giữ mùi bền bỉ trên 12 giờ.
5. Dung môi: Cồn 96 độ và nước cất (tối thiểu 85% thể tích). Nước cất tối đa không vượt quá 20% dung môi để tránh kết tủa, đục dung dịch.

Các mẫu thử nghiệm thực tế:
- Mẫu B2 (Mầm Xuân - Tối ưu vòng 2): Điểm cảm quan 4.505/5.0 (Vượt trội +0.2 so với vòng 1). Tỷ lệ: Lotus 3.0%, Green Tea 3.5%, Jasmine 4.0%, Sandalwood 4.5%.
- Mẫu B (Vòng 1): 4.305 điểm.
- Mẫu C (Vòng 1): 4.015 điểm.

Phong cách trả lời: Nhã nhặn, ấm áp, đậm chất mùa xuân, giải thích kiến thức khoa học/hóa học chuẩn xác theo báo cáo và gợi ý mùi hương tinh tế cho người dùng.
"""

# ==============================================================================
# 4. KHỞI TẠO CLIENT GEMINI TỪ STREAMLIT SECRETS
# ==============================================================================
def init_gemini_client():
    if "GEMINI_API_KEY" in st.secrets:
        return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    return None

client = init_gemini_client()

# ==============================================================================
# 5. PHẦN BANNER GIỚI THIỆU (HERO SECTION)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #FFF0F5 0%, #F0FDF4 100%) !important;
    color: #374151 !important;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.note-box { 
    background: #F9FAFB; 
    border-left: 4px solid #10B981; 
    padding: 12px 16px; 
    border-radius: 0 12px 12px 0; 
    margin-bottom: 12px; 
} 

html, body, [class*="css"], .stApp, p, span, div, li, label, .stMarkdown { 
    color: #1F2937 !important; 
} 

h1, h2, h3, h4, h5, h6, .stHeading, [data-testid="stHeader"] { 
    color: #9D174D !important; 
} 

.stCaption, small { 
    color: #4B5563 !important; 
} 

[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span, [data-testid="stChatMessageContent"] { 
    color: #1F2937 !important; 
} 

[data-testid="stChatInput"] textarea { 
    color: #111827 !important; 
    -webkit-text-fill-color: #111827 !important; 
}

/* Khóa nền khung viền ngoài của ô nhập */
[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #F472B6 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

/* Khóa nền và chữ của vùng gõ văn bản */
[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Chữ mờ gợi ý (placeholder) */
[data-testid="stChatInput"] textarea::placeholder {
    color: #9CA3AF !important;
    -webkit-text-fill-color: #9CA3AF !important;
}

/* Nút gửi (icon mũi tên) luôn giữ màu hồng sen */
[data-testid="stChatInput"] button {
    color: #9D174D !important;
    background: transparent !important;
}

[data-testid="stTable"], [data-testid="stDataFrame"], table {
    background-color: #FFFFFF !important;
    color: #1F2937 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Ép nền các ô tiêu đề và nội dung */
th, td {
    background-color: #FFFFFF !important;
    color: #1F2937 !important;
    border-color: #F3E8FF !important;
}

/* Dòng tiêu đề bảng có màu nền hồng phấn nhẹ */
th {
    background-color: #FFF0F5 !important;
    color: #9D174D !important;
}

/* Khóa nền trắng và định dạng bảng HTML */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    background-color: #FFFFFF !important;
    color: #1F2937 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    margin-bottom: 1.2rem !important;
    font-size: 0.9rem !important;
}

th, td {
    padding: 10px 12px !important;
    border: 1px solid #F3E8FF !important;
    text-align: center !important;
    color: #1F2937 !important;
}

th:first-child, td:first-child {
    text-align: left !important; /* Căn trái cột Tiêu chí */
}

th {
    background-color: #FFF0F5 !important;
    color: #9D174D !important;
    font-weight: 600 !important;
}

/* Khóa ô nhập tin nhắn và nút gửi luôn sáng rõ */
[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #F472B6 !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #9CA3AF !important;
    -webkit-text-fill-color: #9CA3AF !important;
}

[data-testid="stChatInput"] button {
    color: #9D174D !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. BỐ CỤC NỘI DUNG (2 CỘT CHÍNH)
# ==============================================================================
col_content, col_chat = st.columns([1.1, 0.9], gap="large")

with col_content:
    # --- PHẦN 1: BỘ SƯU TẬP MẪU THỬ ---
    st.subheader("🌸 Bộ Sưu Tập Mẫu Thử Nghiệm")
    st.caption("Kết quả nghiên cứu thực nghiệm và tinh chỉnh qua 2 vòng pha chế của nhóm dự án STEM")
    
    # Mẫu B2 Tối Ưu
    st.markdown("""
    <div style="padding: 15px; border-left: 5px solid #db2777; background-color: #fdf2f4; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #9d174d; margin: 0 0 5px 0;">🌿 Mầm Xuân (Mẫu B2 - Tối Ưu Hóa)</h4>
        <p style="color: #b45309; font-weight: bold; margin: 0 0 8px 0;">⭐ 4.505 / 5.0 (Xuất sắc)</p>
        <p style="color: #374151; margin: 0 0 8px 0; font-size: 14px;"><b>Cảm quan:</b> Tươi mới, trong trẻo và thanh thoát. Là phiên bản tối ưu xuất sắc (+0.2 điểm so với mẫu B), cân bằng tuyệt hảo giữa 3 tầng hương.</p>
        <p style="color: #374151; margin: 0; font-size: 13px;"><b>Công thức:</b> Pinky Lotus (3.0%) • Green Tea (3.5%) • Jasmine (4.0%) • Sandalwood (4.5%)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mẫu Đối chiếu B & C
    col_b, col_c = st.columns(2)
    with col_b:
        st.markdown("""
        <div style="padding: 12px; background-color: #f9fafb; border-radius: 5px; border: 1px solid #e5e7eb; height: 100%;">
            <h5 style="color: #4b5563; margin: 0 0 5px 0;">Mẫu B (Vòng 1)</h5>
            <p style="color: #059669; font-weight: bold; margin: 0 0 5px 0; font-size: 14px;">4.305 / 5.0</p>
            <p style="color: #6b7280; font-size: 13px; margin: 0;">Sảng khoái, cân bằng, độ lưu hương tốt. Nền tảng phát triển nên B2.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_c:
        st.markdown("""
        <div style="padding: 12px; background-color: #f9fafb; border-radius: 5px; border: 1px solid #e5e7eb; height: 100%;">
            <h5 style="color: #4b5563; margin: 0 0 5px 0;">Mẫu C (Vòng 1)</h5>
            <p style="color: #059669; font-weight: bold; margin: 0 0 5px 0; font-size: 14px;">4.015 / 5.0</p>
            <p style="color: #6b7280; font-size: 13px; margin: 0;">Hạ Jasmine xuống 0.5% làm nốt đệm, mùi thanh khiết, êm dịu trên da.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- PHẦN 2: BẢNG ĐÁNH GIÁ CẢM QUAN CỦA HỘI ĐỒNG ---
    st.subheader("📊 Bảng Đánh Giá Cảm Quan Từ Hội Đồng")
    eval_data = {
        "Tiêu Chí Đánh Giá": [
            "Phù hợp mùa xuân",
            "Cân bằng ba tầng hương",
            "Độ dễ chịu",
            "Độ rõ tầng hương",
            "Độ lưu mùi",
            "ĐIỂM TỔNG HỢP CÓ TRỌNG SỐ"
        ],
        "Trọng Số": [0.25, 0.25, 0.20, 0.15, 0.15, 1.00],
        "Mẫu A": [4.2, 3.6, 3.8, 3.7, 3.4, 3.775],
        "Mẫu B": [4.6, 4.3, 4.4, 4.1, 3.9, 4.305],
        "Mẫu C": [4.1, 3.8, 3.9, 4.2, 4.2, 4.015],
        "Mẫu B2 (Tối Ưu)": [4.8, 4.5, 4.6, 4.3, 4.1, 4.505]
    }
    df_eval = pd.DataFrame(eval_data)
    # Xuất Styler thành HTML tĩnh kèm highlight điểm số tối ưu và độ chính xác thập phân
    table_html = df_eval.style.highlight_max(
        subset=["Mẫu A", "Mẫu B", "Mẫu C", "Mẫu B2 (Tối Ưu)"],
        color="#FCE7F3",
        axis=1
    ).format(precision=3).hide(axis="index").to_html()

    # Hiển thị trực tiếp dưới dạng HTML
    st.markdown(table_html, unsafe_allow_html=True)

    # --- PHẦN 3: NỐT HƯƠNG TINH TUÝ & AN TOÀN ---
    st.subheader("🌿 Nốt Hương Tinh Tuý & Giới Hạn An Toàn")
    note_col1, note_col2 = st.columns(2)
    with note_col1:
        st.markdown("""
        🪷 **Pinky Lotus (Hương Đầu - Max 5%)**<br>
        <span style="font-size: 13px; color: #4b5563;">• Methyl palmitate: Mùi ngọt thanh nhẹ, dịu dàng, tựa giọt sương sớm đọng trên mặt hồ.</span><br><br>
        🍵 **Green Tea (Hương Giữa - Max 4%)**<br>
        <span style="font-size: 13px; color: #4b5563;">• Linalool & Geraniol: Vị trà khô trong trẻo, mang lại sự tỉnh táo, thanh lọc tinh thần.</span>
        """, unsafe_allow_html=True)
    with note_col2:
        st.markdown("""
        🌼 **Jasmine (Hương Giữa - Max 4%)**<br>
        <span style="font-size: 13px; color: #4b5563;">• Benzyl acetate & Farnesene: Nốt hoa trắng ngát, thư thái; tạo mùi trà ướp hoa nhài thân thuộc.</span><br><br>
        🪵 **Sandalwood (Hương Cuối - Max 5%)**<br>
        <span style="font-size: 13px; color: #4b5563;">• α- & β-Santalol: Gỗ ấm sâu, bền mùi, lưu giữ hương thơm như làn khói ấm đầu năm.</span>
        """, unsafe_allow_html=True)

with col_chat:
    # --- PHẦN 4: CHATBOT BLOOMING BOT (GEMINI FLASH) ---
    st.subheader("💬 Blooming Bot - Trợ Lý Mùi Hương")
    st.caption("Khám phá mùi hương Sớm Xuân hoặc nhận tư vấn phù hợp với tâm trạng của bạn 24/7.")
    
    chat_container = st.container(height=580)
    
    # Khởi tạo phiên trò chuyện trong Session State
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chào bạn! Mình là **Blooming Bot** đến từ dự án *Sớm Xuân* 🌸. Bạn đang tìm kiếm cảm giác mùi hương thế nào cho ngày hôm nay?"
            }
        ]
        
    # Hiển thị các tin nhắn đã có
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    # Tiếp nhận input từ người dùng
    if user_input := st.chat_input("Nhập cảm xúc, câu hỏi về thành phần hoặc mẫu B2..."):
        # 1. Lưu và hiển thị ngay tin nhắn của người dùng
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
                
        # 2. Xử lý gọi API Gemini (Tối ưu tốc độ + Streaming + Retry khi quá tải)
        if client:
            with chat_container:
                with st.chat_message("assistant"):
                    status_placeholder = st.empty()
                    message_placeholder = st.empty()
                    max_retries = 3
                    wait_time = 2  # Thời gian chờ ban đầu (giây)
                    bot_reply = ""
                    
                    # --- TỐI ƯU 1: Cấu hình System Instruction riêng & giới hạn token ---
                    generation_config = {
                        "system_instruction": SYSTEM_INSTRUCTION,
                        "max_output_tokens": 600,  # Giới hạn độ dài câu trả lời ngắn gọn, tinh tế
                        "temperature": 0.7
                    }
                    
                    # --- TỐI ƯU 2: Sliding Window - Chỉ lấy 6 tin nhắn gần nhất ---
                    recent_messages = st.session_state.messages[-6:]
                    contents_payload = [f"{m['role'].upper()}: {m['content']}" for m in recent_messages]
                    
                    for attempt in range(1, max_retries + 1):
                        try:
                            status_placeholder.markdown(
                                f"🌸 *Blooming Bot đang suy nghĩ...* *(Lần thử {attempt}/{max_retries})*" 
                                if attempt > 1 else "🌸 *Blooming Bot đang suy nghĩ...*"
                            )
                            
                            # --- TỐI ƯU 3: Gọi Stream để chữ hiển thị ngay tức thì ---
                            response_stream = client.models.generate_content_stream(
                                model="gemini-3.8-flash",
                                contents=contents_payload,
                                config=generation_config
                            )
                            
                            def stream_generator():
                                for chunk in response_stream:
                                    if chunk.text:
                                        yield chunk.text
                                        
                            # Xóa thông báo chờ ngay khi luồng dữ liệu bắt đầu trả về
                            status_placeholder.empty()
                            bot_reply = message_placeholder.write_stream(stream_generator())
                            break  # Thành công -> thoát vòng lặp retry
                            
                        except Exception as e:
                            err_str = str(e).lower()
                            # Bắt lỗi quá tải, nghẽn mạng hoặc chạm quota
                            is_spike = any(k in err_str for k in ["429", "503", "resourceexhausted", "quota", "overloaded", "demand"])
                            
                            if attempt < max_retries and is_spike:
                                for remaining in range(wait_time, 0, -1):
                                    status_placeholder.warning(
                                        f"⏳ **Lượng truy cập AI đang tăng cao.** Đang kết nối lại sau **{remaining}s** (Lần {attempt}/{max_retries})..."
                                    )
                                    time.sleep(1)
                                wait_time *= 2  # Exponential backoff: 2s -> 4s -> 8s
                            else:
                                status_placeholder.empty()
                                bot_reply = (
                                    "⚠️ *Máy chủ AI hiện đang chịu tải rất lớn từ nhiều lượt truy cập cùng lúc.* "
                                    "Bạn vui lòng chờ khoảng 1-2 phút rồi gửi lại câu hỏi giúp mình nhé!"
                                    if is_spike else f"Đã xảy ra sự cố khi kết nối mô hình: {str(e)}"
                                )
                                message_placeholder.markdown(bot_reply)
                                break
                                
                    # Lưu tin nhắn của bot vào lịch sử hội thoại
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        else:
            with chat_container:
                with st.chat_message("assistant"):
                    st.warning("Vui lòng cấu hình khóa bí mật `GEMINI_API_KEY` trong Streamlit Secrets để kích hoạt Bot.")

# ==============================================================================
# 7. CHÂN TRANG (FOOTER)
# ==============================================================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 13px; padding-bottom: 20px;">
    Dự án STEM Nước Hoa Sớm Xuân • Nhóm thực hiện: Xuân Đức, Hà Anh, Hoàng Bảo, Quốc Triệu, Tấn Phúc, Minh Nhật, Gia Cát, Thiên Phúc, Xuân Hy, Lê Vy, Minh Thy, Quế Chi.
</div>
""", unsafe_allow_html=True)