import json
import streamlit as st
from streamlit_google_auth import Authenticate

st.set_page_config(page_title="LSM - Hệ Thống Học Tập", layout="wide")

# 1. TẠO FILE TẠM CẤU HÌNH GOOGLE OAUTH
credentials_dict = {
    "web": {
        "client_id": st.secrets["google_oauth"]["client_id"],
        "client_secret": st.secrets["google_oauth"]["client_secret"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [st.secrets["google_oauth"]["redirect_uri"]]
    }
}

with open("google_creds.json", "w") as f:
    json.dump(credentials_dict, f)

# KHỞI TẠO AUTHENTICATOR
authenticator = Authenticate(
    secret_credentials_path="google_creds.json",
    cookie_name="lsm_google_auth_cookie",
    cookie_key="chuoi_bi_mat_random_123456",
    cookie_expiry_days=30
)

# 2. KHỞI TẠO DỮ LIỆU APP (13 lớp)
if "users" not in st.session_state:
    st.session_state.users = {}

if "classes" not in st.session_state:
    st.session_state.classes = {f"Lớp 7A{i}": [] for i in range(1, 14)}

if "lessons" not in st.session_state:
    st.session_state.lessons = [
        {
            "title": "Bài 1: Tập hợp các số hữu tỉ",
            "duration": "15 phút",
            "video_url": "https://www.youtube.com/watch?v=x534MglTm8o",
            "desc": "Khái niệm số hữu tỉ, biểu diễn số hữu tỉ trên trục số."
        }
    ]

# Kiểm tra trạng thái đăng nhập Google
authenticator.check_authenticity()

# --- MÀN HÌNH CHƯA ĐĂNG NHẬP ---
if not st.session_state.get('connected', False):
    st.title("🎓 LSM - Hệ Thống Học Tập")
    st.write("Vui lòng đăng nhập bằng tài khoản Google để tiếp tục.")
    
    authorization_url = authenticator.get_authorization_url()
    st.markdown(f'''
        <a href="{authorization_url}" target="_self" style="
            background-color: #4285F4;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            display: inline-block;
        ">🌐 Đăng nhập bằng Google</a>
    ''', unsafe_allow_html=True)

# --- SAU KHI ĐĂNG NHẬP GOOGLE THÀNH CÔNG ---
else:
    user_info = st.session_state.get('user_info', {})
    user_email = user_info.get('email', '').strip().lower()
    user_name = user_info.get('name', 'Người dùng')

    if user_email not in st.session_state.users:
        st.warning(f"Xin chào **{user_name}**! Đây là lần đầu bạn đăng nhập.")
        role = st.radio("Vui lòng xác nhận vai trò của bạn:", ["Học sinh", "Giáo viên"])
        if st.button("Xác nhận"):
            st.session_state.users[user_email] = {
                "name": user_name,
                "role": role
            }
            st.rerun()
        st.stop()

    current_user = st.session_state.users[user_email]
    user_role = current_user["role"]

    st.sidebar.title("📌 Menu")
    st.sidebar.write(f"Xin chào: **{user_name}**")
    st.sidebar.write(f"Email: `{user_email}`")
    st.sidebar.write(f"Vai trò: **{user_role}**")
    
    if st.sidebar.button("Đăng Xuất"):
        authenticator.logout()
        st.rerun()

    if user_role == "Giáo viên":
        st.title("👨‍🏫 Trang Quản Lý Dành Cho Giáo Viên")
        
        tab_classes, tab_add_lesson = st.tabs(["🏫 Quản Lý Lớp Học & Thêm Học Sinh", "➕ Thêm Bài Học Mới"])
        
        with tab_classes:
            st.subheader("Quản lý danh sách lớp")
            selected_class = st.selectbox("Chọn lớp học:", list(st.session_state.classes.keys()))
            
            st.markdown("---")
            st.write("### 🔍 Thêm Học Sinh Vào Lớp Bằng Gmail")
            search_email = st.text_input("Nhập Gmail học sinh:").strip().lower()
            
            if st.button("Tìm & Thêm Vào Lớp"):
                if search_email in st.session_state.users:
                    student_info = st.session_state.users[search_email]
                    if student_info["role"] == "Học sinh":
                        if search_email not in st.session_state.classes[selected_class]:
                            st.session_state.classes[selected_class].append(search_email)
                            st.success(f"Đã thêm học sinh **{student_info['name']}** ({search_email}) vào {selected_class}!")
                            st.rerun()
                        else:
                            st.warning("Học sinh này đã có trong lớp rồi!")
                    else:
                        st.error("Email này thuộc tài khoản Giáo viên!")
                else:
                    st.error("Không tìm thấy Email! Học sinh cần bấm nút Đăng nhập bằng Google trên trang web 1 lần.")

            st.markdown("---")
            st.write(f"### 📋 Danh sách học sinh thuộc {selected_class}")
            student_list = st.session_state.classes[selected_class]
            if student_list:
                table_data = []
                for email in student_list:
                    info = st.session_state.users.get(email, {})
                    table_data.append({
                        "Họ và Tên": info.get("name", "Chưa cập nhật"),
                        "Email": email
                    })
                st.table(table_data)
            else:
                st.info("Lớp này chưa có học sinh nào.")

        with tab_add_lesson:
            st.subheader("Tạo bài học mới")
            new_title = st.text_input("Tên bài học")
            new_duration = st.text_input("Thời lượng (ví dụ: 20 phút)")
            new_video = st.text_input("Link YouTube bài giảng")
            new_desc = st.text_area("Tóm tắt nội dung bài học")
            
            if st.button("Đăng Bài Học"):
                if new_title and new_video:
                    st.session_state.lessons.append({
                        "title": new_title,
                        "duration": new_duration if new_duration else "Chưa xác định",
                        "video_url": new_video,
                        "desc": new_desc
                    })
                    st.success("Đã thêm bài học mới thành công!")
                else:
                    st.warning("Vui lòng nhập Tên bài học và Link YouTube!")

    else:
        st.title("📖 Màn Hình Học Tập - Học Sinh")
        lesson_titles = [l["title"] for l in st.session_state.lessons]
        selected_title = st.selectbox("Chọn bài học:", lesson_titles)
        selected_lesson = next(l for l in st.session_state.lessons if l["title"] == selected_title)
        
        st.subheader(selected_lesson["title"])
        st.caption(f"Thời lượng: {selected_lesson['duration']}")
        st.video(selected_lesson["video_url"])
        st.write("**Tóm tắt bài học:**")
        st.write(selected_lesson["desc"])
