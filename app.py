import streamlit as st

st.set_page_config(page_title="LSM - Hệ Thống Học Tập", layout="wide")

# Khởi tạo dữ liệu bài học mẫu trong Session State
if "lessons" not in st.session_state:
    st.session_state.lessons = [
        {
            "title": "Bài 1: Tập hợp các số hữu tỉ",
            "duration": "15 phút",
            "video_url": "https://www.youtube.com/watch?v=x534MglTm8o",
            "desc": "Khái niệm số hữu tỉ, biểu diễn số hữu tỉ trên trục số."
        }
    ]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# --- MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ ---
if not st.session_state.logged_in:
    st.title("🎓 LSM - Đăng Nhập Hệ Thống Học Tập")
    
    tab_login, tab_register = st.tabs(["Đăng Nhập", "Đăng Ký Tài Khoản Mới"])
    
    with tab_register:
        reg_email = st.text_input("Địa chỉ Email", key="reg_email")
        reg_pass = st.text_input("Mật khẩu", type="password", key="reg_pass")
        reg_role = st.selectbox("Bạn là:", ["Học sinh", "Giáo viên"], key="reg_role")
        
        if st.button("Đăng Ký"):
            if reg_email and reg_pass:
                st.session_state[f"user_{reg_email}"] = {"pass": reg_pass, "role": reg_role}
                st.success(f"Đăng ký thành công tài khoản {reg_role}! Vui lòng sang tab Đăng Nhập.")
            else:
                st.error("Vui lòng điền đầy đủ thông tin!")

    with tab_login:
        login_email = st.text_input("Địa chỉ Email", key="login_email")
        login_pass = st.text_input("Mật khẩu", type="password", key="login_pass")
        
        if st.button("Đăng Nhập"):
            user_data = st.session_state.get(f"user_{login_email}")
            if user_data and user_data["pass"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.user_role = user_data["role"]
                st.session_state.user_email = login_email
                st.rerun()
            else:
                st.error("Email hoặc mật khẩu không chính xác!")

# --- MÀN HÌNH SAU KHI ĐĂNG NHẬP ---
else:
    # Thanh bên Sidebar
    st.sidebar.title("📌 Menu")
    st.sidebar.write(f"Xin chào: **{st.session_state.user_email}**")
    st.sidebar.write(f"Vai trò: **{st.session_state.user_role}**")
    
    if st.sidebar.button("Đăng Xoát / Đăng Xuất"):
        st.session_state.logged_in = False
        st.rerun()

    # 1. GIAO DIỆN GIÁO VIÊN
    if st.session_state.user_role == "Giáo viên":
        st.title("👨‍🏫 Trang Quản Lý Dành Cho Giáo Viên")
        
        tab_add, tab_list = st.tabs(["➕ Thêm Bài Học Mới", "📚 Danh Sách Bài Học"])
        
        with tab_add:
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

        with tab_list:
            st.subheader("Các bài học hiện có trên hệ thống")
            for idx, lesson in enumerate(st.session_state.lessons):
                st.write(f"**{idx + 1}. {lesson['title']}** - ({lesson['duration']})")
                st.caption(f"Link: {lesson['video_url']}")

    # 2. GIAO DIỆN HỌC SINH
    else:
        st.title("📖 Màn Hình Học Tập - Học Sinh")
        
        # Chọn bài học
        lesson_titles = [l["title"] for l in st.session_state.lessons]
        selected_title = st.selectbox("Chọn bài học:", lesson_titles)
        
        # Tìm thông tin bài học được chọn
        selected_lesson = next(l for l in st.session_state.lessons if l["title"] == selected_title)
        
        st.subheader(selected_lesson["title"])
        st.caption(f"Thời lượng: {selected_lesson['duration']}")
        
        # Hiển thị Video YouTube
        st.video(selected_lesson["video_url"])
        
        st.write("**Tóm tắt bài học:**")
        st.write(selected_lesson["desc"])
