import streamlit as st

st.set_page_config(page_title="LSM - Hệ Thống Học Tập", layout="wide")

# 1. KHỞI TẠO DỮ LIỆU
if "users" not in st.session_state:
    # Danh sách người dùng hệ thống
    st.session_state.users = {
        "gv@gmail.com": {"pass": "123", "role": "Giáo viên", "name": "Thầy Giáo A"},
        "hs1@gmail.com": {"pass": "123", "role": "Học sinh", "name": "Nguyễn Văn A"},
        "hs2@gmail.com": {"pass": "123", "role": "Học sinh", "name": "Trần Thị B"}
    }

if "classes" not in st.session_state:
    # Quản lý lớp học (Lưu danh sách email học sinh thuộc từng lớp)
    st.session_state.classes = {
        "Lớp 7A1": [],
        "Lớp 7A2": []
         "Lớp 7A3": [],
        "Lớp 7A4": []
         "Lớp 7A5": [],
        "Lớp 7A6": []
         "Lớp 7A7": [],
        "Lớp 7A8": []
         "Lớp 7A9": [],
        "Lớp 7A10": []
         "Lớp 7A11": [],
        "Lớp 7A12": []
         "Lớp 7A13": [],
    }

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
        reg_name = st.text_input("Họ và Tên", key="reg_name")
        reg_email = st.text_input("Địa chỉ Email", key="reg_email")
        reg_pass = st.text_input("Mật khẩu", type="password", key="reg_pass")
        reg_role = st.selectbox("Bạn là:", ["Học sinh", "Giáo viên"], key="reg_role")
        
        if st.button("Đăng Ký"):
            if reg_email and reg_pass and reg_name:
                st.session_state.users[reg_email] = {
                    "pass": reg_pass, 
                    "role": reg_role, 
                    "name": reg_name
                }
                st.success(f"Đăng ký thành công! Hãy đọc Email ({reg_email}) cho Giáo viên để được thêm vào lớp.")
            else:
                st.error("Vui lòng điền đầy đủ thông tin!")

    with tab_login:
        login_email = st.text_input("Địa chỉ Email", key="login_email")
        login_pass = st.text_input("Mật khẩu", type="password", key="login_pass")
        
        if st.button("Đăng Nhập"):
            user = st.session_state.users.get(login_email)
            if user and user["pass"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.user_role = user["role"]
                st.session_state.user_email = login_email
                st.session_state.user_name = user["name"]
                st.rerun()
            else:
                st.error("Email hoặc mật khẩu không chính xác!")

# --- MÀN HÌNH SAU KHI ĐĂNG NHẬP ---
else:
    st.sidebar.title("📌 Menu")
    st.sidebar.write(f"Xin chào: **{st.session_state.user_name}**")
    st.sidebar.write(f"Email: `{st.session_state.user_email}`")
    st.sidebar.write(f"Vai trò: **{st.session_state.user_role}**")
    
    if st.sidebar.button("Đăng Xuất"):
        st.session_state.logged_in = False
        st.rerun()

    # 1. GIAO DIỆN GIÁO VIÊN
    if st.session_state.user_role == "Giáo viên":
        st.title("👨‍🏫 Trang Quản Lý Dành Cho Giáo Viên")
        
        tab_classes, tab_add_lesson = st.tabs(["🏫 Quản Lý Lớp Học & Thêm Học Sinh", "➕ Thêm Bài Học Mới"])
        
        # TAB QUẢN LÝ LỚP
        with tab_classes:
            st.subheader("Quản lý danh sách lớp")
            
            # Chọn lớp học
            selected_class = st.selectbox("Chọn lớp học:", list(st.session_state.classes.keys()))
            
            # Ô TÌM KIẾM & THÊM HỌC SINH BẰNG EMAIL
            st.markdown("---")
            st.write("### 🔍 Thêm Học Sinh Vào Lớp Bằng Email")
            search_email = st.text_input("Nhập Email học sinh cung cấp:").strip()
            
            if st.button("Tìm & Thêm Vào Lớp"):
                # Kiểm tra email có trong hệ thống không
                if search_email in st.session_state.users:
                    student_info = st.session_state.users[search_email]
                    
                    if student_info["role"] == "Học sinh":
                        # Kiểm tra xem đã có trong lớp chưa
                        if search_email not in st.session_state.classes[selected_class]:
                            st.session_state.classes[selected_class].append(search_email)
                            st.success(f"Đã thêm học sinh **{student_info['name']}** ({search_email}) vào {selected_class}!")
                            st.rerun()
                        else:
                            st.warning("Học sinh này đã có trong lớp rồi!")
                    else:
                        st.error("Email này thuộc tài khoản Giáo viên, không thể thêm vào lớp học sinh!")
                else:
                    st.error("Không tìm thấy Email này! Hãy chắc chắn Học sinh đã Đăng ký tài khoản.")

            # HIỂN THỊ DANH SÁCH HỌC SINH TRONG LỚP
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

        # TAB THÊM BÀI HỌC
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

    # 2. GIAO DIỆN HỌC SINH
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
