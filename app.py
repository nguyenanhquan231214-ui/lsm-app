import streamlit as st

st.set_page_config(page_title="LSM - Hệ Thống Học Tập", layout="wide")

# 1. KHỞI TẠO DỮ LIỆU APP (13 lớp)
if "users" not in st.session_state:
    # Tài khoản mẫu có sẵn để test nhanh
    st.session_state.users = {
        "gv@gmail.com": {"name": "Thầy Giáo Mẫu", "role": "Giáo viên", "pass": "123"},
        "hs@gmail.com": {"name": "Học Sinh Mẫu", "role": "Học sinh", "pass": "123"}
    }

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

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# --- MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ ---
if not st.session_state.current_user:
    st.title("🎓 LSM - Hệ Thống Học Tập")
    
    tab_login, tab_register = st.tabs(["🔑 Đăng Nhập", "📝 Đăng Ký Tài Khoản"])
    
    with tab_login:
        email_login = st.text_input("Email:").strip().lower()
        pass_login = st.text_input("Mật khẩu:", type="password")
        
        if st.button("Đăng Nhập"):
            if email_login in st.session_state.users:
                user = st.session_state.users[email_login]
                if user["pass"] == pass_login:
                    st.session_state.current_user = {**user, "email": email_login}
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Sai mật khẩu!")
            else:
                st.error("Email chưa được đăng ký!")
                
    with tab_register:
        reg_name = st.text_input("Họ và Tên:")
        reg_email = st.text_input("Email đăng ký:").strip().lower()
        reg_pass = st.text_input("Tạo Mật khẩu:", type="password")
        reg_role = st.radio("Vai trò:", ["Học sinh", "Giáo viên"])
        
        if st.button("Tạo Tài Khoản"):
            if reg_email and reg_pass and reg_name:
                if reg_email not in st.session_state.users:
                    st.session_state.users[reg_email] = {
                        "name": reg_name,
                        "role": reg_role,
                        "pass": reg_pass
                    }
                    st.success("Đăng ký thành công! Hãy chuyển sang tab Đăng Nhập.")
                else:
                    st.warning("Email này đã tồn tại!")
            else:
                st.warning("Vui lòng điền đầy đủ thông tin!")

# --- GIAO DIỆN SAU KHI ĐĂNG NHẬP ---
else:
    user = st.session_state.current_user
    user_role = user["role"]

    st.sidebar.title("📌 Menu")
    st.sidebar.write(f"Xin chào: **{user['name']}**")
    st.sidebar.write(f"Email: `{user['email']}`")
    st.sidebar.write(f"Vai trò: **{user_role}**")
    
    if st.sidebar.button("Đăng Xuất"):
        st.session_state.current_user = None
        st.rerun()

    # GIAO DIỆN GIÁO VIÊN
    if user_role == "Giáo viên":
        st.title("👨‍🏫 Trang Quản Lý Dành Cho Giáo Viên")
        tab_classes, tab_add_lesson = st.tabs(["🏫 Quản Lý Lớp Học & Thêm Học Sinh", "➕ Thêm Bài Học Mới"])
        
        with tab_classes:
            st.subheader("Quản lý danh sách lớp")
            selected_class = st.selectbox("Chọn lớp học:", list(st.session_state.classes.keys()))
            
            st.markdown("---")
            st.write("### 🔍 Thêm Học Sinh Vào Lớp Bằng Email")
            search_email = st.text_input("Nhập Email học sinh:").strip().lower()
            
            if st.button("Tìm & Thêm Vào Lớp"):
                if search_email in st.session_state.users:
                    student_info = st.session_state.users[search_email]
                    if student_info["role"] == "Học sinh":
                        if search_email not in st.session_state.classes[selected_class]:
                            st.session_state.classes[selected_class].append(search_email)
                            st.success(f"Đã thêm **{student_info['name']}** vào {selected_class}!")
                            st.rerun()
                        else:
                            st.warning("Học sinh này đã có trong lớp!")
                    else:
                        st.error("Email này là tài khoản Giáo viên!")
                else:
                    st.error("Không tìm thấy Email! Học sinh cần Đăng ký tài khoản trước.")

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
                    st.success("Đã thêm bài học thành công!")
                else:
                    st.warning("Vui lòng nhập Tên bài học và Link YouTube!")

    # GIAO DIỆN HỌC SINH
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
