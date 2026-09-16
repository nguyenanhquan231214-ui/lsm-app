import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="LSM - Hệ Thống Học Tập", layout="wide")

# 1. KẾT NỐI GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

def load_users():
    try:
        # TTL=0 để luôn làm mới dữ liệu từ Google Sheets
        df = conn.read(ttl=0)
        return df
    except Exception:
        return pd.DataFrame(columns=["Name", "Email", "Password", "Role"])

def save_user(name, email, password, role):
    df = load_users()
    new_user = pd.DataFrame([{
        "Name": name.strip(),
        "Email": email.strip().lower(),
        "Password": str(password).strip(),
        "Role": role.strip()
    }])
    updated_df = pd.concat([df, new_user], ignore_index=True)
    conn.update(data=updated_df)

# 2. KHỞI TẠO BÀI HỌC VÀ LỚP HỌC (13 LỚP)
if "lessons" not in st.session_state:
    st.session_state.lessons = [
        {
            "title": "Bài 1: Tập hợp các số hữu tỉ",
            "duration": "15 phút",
            "video_url": "https://www.youtube.com/watch?v=x534MglTm8o",
            "desc": "Khái niệm số hữu tỉ, biểu diễn số hữu tỉ trên trục số."
        }
    ]

if "classes" not in st.session_state:
    st.session_state.classes = {f"Lớp 7A{i}": [] for i in range(1, 14)}

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# --- MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ ---
if not st.session_state.current_user:
    st.title("🎓 LSM - Hệ Thống Học Tập")
    
    tab_login, tab_register = st.tabs(["🔑 Đăng Nhập", "📝 Đăng Ký Tài Khoản"])
    
    with tab_login:
        email_login = st.text_input("Email:").strip().lower()
        pass_login = st.text_input("Mật khẩu:", type="password").strip()
        
        if st.button("Đăng Nhập"):
            df_users = load_users()
            if not df_users.empty:
                # Chuẩn hóa dữ liệu để so sánh
                df_users['Clean_Email'] = df_users['Email'].astype(str).str.strip().str.lower()
                df_users['Clean_Pass'] = df_users['Password'].astype(str).str.strip()
                
                user_match = df_users[(df_users['Clean_Email'] == email_login) & (df_users['Clean_Pass'] == pass_login)]
                
                if not user_match.empty:
                    user_info = user_match.iloc[0]
                    st.session_state.current_user = {
                        "name": str(user_info["Name"]).strip(),
                        "email": str(user_info["Clean_Email"]),
                        "role": str(user_info["Role"]).strip()
                    }
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Sai Email hoặc Mật khẩu!")
            else:
                st.error("Chưa có tài khoản nào trên hệ thống. Vui lòng Đăng ký!")
                
    with tab_register:
        reg_name = st.text_input("Họ và Tên:").strip()
        reg_email = st.text_input("Email đăng ký:").strip().lower()
        reg_pass = st.text_input("Tạo Mật khẩu:", type="password").strip()
        reg_role = st.radio("Vai trò:", ["Học sinh", "Giáo viên"])
        
        if st.button("Tạo Tài Khoản"):
            if reg_email and reg_pass and reg_name:
                df_users = load_users()
                if not df_users.empty:
                    existing_emails = df_users['Email'].astype(str).str.strip().str.lower().values
                else:
                    existing_emails = []
                    
                if reg_email in existing_emails:
                    st.warning("Email này đã được đăng ký rồi!")
                else:
                    save_user(reg_name, reg_email, reg_pass, reg_role)
                    st.success("Đã đăng ký thành công! Hãy chuyển sang tab Đăng Nhập.")
            else:
                st.warning("Vui lòng điền đầy đủ thông tin!")

# --- MÀN HÌNH SAU KHI ĐĂNG NHẬP ---
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
                df_users = load_users()
                if not df_users.empty:
                    # Chuẩn hóa dữ liệu tìm kiếm
                    df_users['Clean_Email'] = df_users['Email'].astype(str).str.strip().str.lower()
                    df_users['Clean_Role'] = df_users['Role'].astype(str).str.strip()
                    
                    target_email = search_email
                    student_match = df_users[(df_users['Clean_Email'] == target_email) & (df_users['Clean_Role'] == 'Học sinh')]
                    
                    if not student_match.empty:
                        student_name = str(student_match.iloc[0]["Name"]).strip()
                        current_class_emails = [s['email'] for s in st.session_state.classes[selected_class]]
                        
                        if target_email not in current_class_emails:
                            st.session_state.classes[selected_class].append({"name": student_name, "email": target_email})
                            st.success(f"Đã thêm học sinh **{student_name}** vào {selected_class}!")
                            st.rerun()
                        else:
                            st.warning("Học sinh này đã có trong lớp rồi!")
                    else:
                        st.error("Không tìm thấy Email! Hãy đảm bảo tài khoản đã đăng ký và chọn vai trò 'Học sinh'.")
                else:
                    st.error("Chưa có dữ liệu học sinh nào trên hệ thống.")

            st.markdown("---")
            st.write(f"### 📋 Danh sách học sinh thuộc {selected_class}")
            student_list = st.session_state.classes[selected_class]
            if student_list:
                st.table(pd.DataFrame(student_list))
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
