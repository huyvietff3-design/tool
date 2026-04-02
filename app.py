import streamlit as st
import edge_tts
import asyncio
import os

# Cấu hình giao diện Web
st.set_page_config(page_title="AI Voice Generator", page_icon="🎙️")

st.title("🎙️ AI Text-to-Voice Tool")
st.markdown("Chuyển đổi văn bản thành giọng nói AI chất lượng cao (Microsoft Edge TTS).")

# Danh sách các giọng đọc tiếng Việt phổ biến
VOICES = {
    "Nam - Hoài My": "vi-VN-HoaiMyNeural",
    "Nữ - Nam Minh": "vi-VN-NamMinhNeural",
}

# Sidebar tùy chỉnh
st.sidebar.header("Cấu hình giọng nói")
selected_voice = st.sidebar.selectbox("Chọn giọng đọc:", list(VOICES.keys()))
speed = st.sidebar.slider("Tốc độ đọc:", 0.5, 2.0, 1.0, 0.1)

# Khu vực nhập liệu
text_input = st.text_area("Nhập văn bản bạn muốn chuyển đổi:", placeholder="Chào bạn, mình là AI trợ lý...", height=200)

async def generate_voice(text, voice, rate):
    # Định dạng tốc độ (ví dụ: +0%, -10%, +20%)
    rate_str = f"{'+' if rate >= 1 else ''}{int((rate-1)*100)}%"
    communicate = edge_tts.Communicate(text, VOICES[voice], rate=rate_str)
    output_file = "output.mp3"
    await communicate.save(output_file)
    return output_file

if st.button("Chuyển đổi & Nghe"):
    if text_input.strip() == "":
        st.warning("Vui lòng nhập văn bản!")
    else:
        with st.spinner("Đang tạo giọng nói AI..."):
            try:
                # Chạy hàm async trong Streamlit
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                audio_file = loop.run_until_complete(generate_voice(text_input, selected_voice, speed))
                
                # Hiển thị trình phát nhạc
                st.audio(audio_file, format="audio/mp3")
                
                # Nút tải về
                with open(audio_file, "rb") as f:
                    st.download_button("Tải file .mp3", f, file_name="ai_voice.mp3")
                
                # Dọn dẹp file tạm sau khi dùng (tùy chọn)
                # os.remove(audio_file)
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")

st.info("💡 Mẹo: Tool này chạy trên trình duyệt nên bạn có thể dùng trên cả điện thoại và máy tính.")