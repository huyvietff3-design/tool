import streamlit as st
import requests

# --- 1. KHAI BÁO CẤU HÌNH (BẮT BUỘC) ---
st.set_page_config(page_title="Multi-Scanner Pro v2.5", page_icon="🕵️", layout="wide")

# --- 2. CSS GIAO DIỆN & HIỆU ỨNG ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #00FF41; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00F260, #0575E6);
        color: white; border: none; font-weight: bold;
        box-shadow: 0 0 15px #00F260; border-radius: 10px;
    }
    .stTextInput>div>div>input { background-color: #1a1c23; color: white; border: 1px solid #00FF41; }
</style>
""", unsafe_allow_html=True)

# PHẦN NHẠC PLAYLIST
st.sidebar.markdown("### 🎵 NHẠC NỀN")
playlist_id = st.sidebar.text_input("ID Playlist YouTube:", value="RDYvpWl-qdI0g")
iframe_music = f"""
    <div style="border-radius: 12px; overflow: hidden; border: 1px solid #FF0000;">
        <iframe width="100%" height="80" src="https://www.youtube.com/embed?listType=playlist&list={playlist_id}&autoplay=1" 
        frameborder="0" allow="autoplay"></iframe>
    </div>
"""
st.sidebar.markdown(iframe_music, unsafe_allow_html=True)

# PHẦN NÚT SUB YOUTUBE (GỌN GÀNG)
st.sidebar.markdown("---")
my_yt_url = "https://www.youtube.com/@TenCuaBan?sub_confirmation=1" # THAY LINK TẠI ĐÂY
st.sidebar.markdown(f"""
    <a href="{my_yt_url}" target="_blank" style="text-decoration: none;">
        <div style="background:#FF0000; color:white; padding:10px; border-radius:10px; text-align:center; font-weight:bold;">
            🔔 ĐĂNG KÝ KÊNH CỦA TÔI
        </div>
    </a>
""", unsafe_allow_html=True)

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🛡️ GLOBAL ACCOUNT SCANNER")
platform = st.selectbox("Chọn nền tảng để quét:", ["YouTube", "TikTok", "Roblox"])
username = st.text_input(f"Nhập Username {platform}:", placeholder="Ví dụ: MrBeast hoặc roblox_user")

# --- 5. XỬ LÝ LOGIC (PHẦN BẠN BỊ LỖI) ---
if st.button(f"RUN SCAN: {platform.upper()} ⚡"):
    if not username:
        st.warning("⚠️ Vui lòng nhập tên người dùng!")
    else:
        # Tự động làm sạch dấu @ để API không bị lỗi
        clean_name = username.replace("@", "")
        
        with st.spinner(f'🚀 Đang truy xuất dữ liệu {platform}...'):
            # --- XỬ LÝ YOUTUBE ---
            if platform == "YouTube":
                api_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/@{clean_name}&format=json"
                res = requests.get(api_url)
                if res.status_code == 200:
                    data = res.json()
                    col1, col2 = st.columns([1, 2])
                    with col1: st.image(data['thumbnail_url'], width=200)
                    with col2:
                        st.success(f"✅ Tên kênh: {data['author_name']}")
                        st.info(f"🔗 Link: [Bấm để xem kênh](https://www.youtube.com/@{clean_name})")
                else:
                    st.error("❌ Không tìm thấy kênh YouTube này!")

            # --- XỬ LÝ ROBLOX ---
            elif platform == "Roblox":
                post_url = "https://users.roblox.com/v1/usernames/users"
                payload = {"usernames": [clean_name], "excludeBannedUsers": True}
                res = requests.post(post_url, json=payload).json()
                
                if res.get('data') and len(res['data']) > 0:
                    u_id = res['data'][0]['id']
                    detail = requests.get(f"https://users.roblox.com/v1/users/{u_id}").json()
                    thumb = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={u_id}&size=420x420&format=Png").json()
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if thumb.get('data'): st.image(thumb['data'][0]['imageUrl'], width=180)
                    with col2:
                        st.success(f"✅ User: {detail['displayName']} (@{detail['name']})")
                        st.write(f"🆔 ID: `{u_id}`")
                        st.write(f"📅 Ngày tạo: {detail['created'][:10]}")
                else:
                    st.error("❌ Không tìm thấy User Roblox này!")

            # --- XỬ LÝ TIKTOK ---
            elif platform == "TikTok":
                tik_url = f"https://www.tikwm.com/api/user/info?unique_id={clean_name}"
                res = requests.get(tik_url).json()
                if res.get('code') == 0:
                    d = res['data']
                    col1, col2 = st.columns([1, 2])
                    with col1: st.image(d['user']['avatarLarger'], width=180)
                    with col2:
                        st.success(f"✅ Nick: {d['user']['nickname']}")
                        st.write(f"📊 Followers: {d['stats']['followerCount']:,}")
                        st.write(f"❤️ Tổng Tim: {d['stats']['heartCount']:,}")
                else:
                    st.error("❌ TikTok không tìm thấy người dùng này!")

st.markdown("---")
st.caption("Tool Mod by Hzmod | Giao diện Matrix Edition")
