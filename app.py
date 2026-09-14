import streamlit as st
import json

# Config trang web
st.set_page_config(
    page_title="LSM - Learning Management System",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 1. KHỞI TẠO DỮ LIỆU MẪU (CURRICULUM)
# -----------------------------------------------------------------------------
GRADE_7_SUBJECTS = [
    {
        "id": "toan-7",
        "name": "Toán học 7",
        "lessons": [
            {
                "id": "toan-7-bai-1",
                "title": "Bài 1: Tập hợp các số hữu tỉ",
                "video_url": "https://www.youtube.com/watch?v=X30wO8T08U4",
                "duration": "15 phút",
                "description": "Khái niệm số hữu tỉ, biểu diễn số hữu tỉ trên trục số."
            },
            {
                "id": "toan-7-bai-2",
                "title": "Bài 2: Cộng, trừ số hữu tỉ",
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "duration": "18 phút",
                "description": "Các quy tắc cộng, trừ số hữu tỉ và bài tập áp dụng."
            }
        ]
    },
    {
        "id": "van-7",
        "name": "Ngữ văn 7",
        "lessons": [
            {
                "id": "van-7-bai-1",
                "title": "Bài 1: Mạch cảm xúc trong bài thơ",
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "duration": "12 phút",
                "description": "Tìm hiểu mạch cảm xúc và cấu trúc các tác phẩm thơ Lớp 7."
            }
        ]
    }
]

# -----------------------------------------------------------------------------
# 2. KHỞI TẠO SESSION STATE (Tương đương State trong React)
# -----------------------------------------------------------------------------
if "users_db" not in st.session_state:
    st.session_state.users_db = {}  # Lưu thông tin tài khoản đăng ký trên bộ nhớ
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "selected_grade" not in st.session_state:
    st.session_state.selected_grade = 7
if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = []
if "lesson_notes" not in st.session_state:
    st.session_state.lesson_notes = {}
if "active_lesson" not in st.session_state:
    st.session_state.active_lesson = GRADE_7_SUBJECTS[0]["lessons"][0]


# -----------------------------------------------------------------------------
# 3. MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ THỦ CÔNG
# -----------------------------------------------------------------------------
def render_auth_screen():
    st.markdown("<h2 style='text-align: center;'>🎓 LSM - Đăng Nhập Hệ Thống Học Tập</h2>", unsafe_allow_html=True)
    
    tab_login, tab_register = st.tabs(["Đăng Nhập", "Đăng Ký Tài Khoản Mới"])
    
    # Tab Đăng nhập
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Địa chỉ Email")
            password = st.text_input("Mật khẩu", type="password")
            submit_login = st.form_submit_button("Đăng Nhập")
            
            if submit_login:
                user = st.session_state.users_db.get(email.strip().lower())
                if user and user["password"] == password.strip():
                    st.session_state.current_user = user
                    st.success(f"Chào mừng {user['name']} đã quay trở lại!")
                    st.rerun()
                else:
                    st.error("Email hoặc mật khẩu không chính xác!")

    # Tab Đăng ký
    with tab_register:
        with st.form("register_form"):
            name = st.text_input("Họ và Tên thật")
            email = st.text_input("Email của bạn")
            password = st.text_input("Mật khẩu", type="password")
            submit_register = st.form_submit_button("Tạo Tài Khoản & Học Ngay")
            
            if submit_register:
                email_clean = email.strip().lower()
                if not name.strip() or not email_clean or not password.strip():
                    st.error("Vui lòng điền đầy đủ tất cả thông tin!")
                elif email_clean in st.session_state.users_db:
                    st.error("Email này đã được đăng ký!")
                else:
                    new_user = {
                        "name": name.strip(),
                        "email": email_clean,
                        "password": password.strip()
                    }
                    st.session_state.users_db[email_clean] = new_user
                    st.session_state.current_user = new_user
                    st.success("Đăng ký thành công!")
                    st.rerun()


# -----------------------------------------------------------------------------
# 4. GIAO DIỆN CHÍNH HỌC TẬP (LMS HUB)
# -----------------------------------------------------------------------------
def render_main_app():
    user = st.session_state.current_user
    
    # Thanh điều hướng (Header)
    col_head1, col_head2, col_head3 = st.columns([2, 2, 1])
    with col_head1:
        st.title("📚 LSM Learning")
    with col_head2:
        st.write(f"👋 Xin chào, **{user['name']}**")
        grade = st.selectbox("Khối lớp:", [6, 7, 8, 9], index=1)
        st.session_state.selected_grade = grade
    with col_head3:
        if st.button("Đăng xuất"):
            st.session_state.current_user = None
            st.rerun()
            
    st.divider()

    # Bố cục chính: Cột trái (Sidebar Môn học) & Cột phải (Xem Bài học & Trợ lý AI)
    col_sidebar, col_main = st.columns([1, 2.5])

    # --- CỘT TRÁI: DẠNG SIDEBAR MÔN HỌC ---
    with col_sidebar:
        st.subheader(" Danh mục Môn học")
        
        # Tìm kiếm bài học
        search_query = st.text_input("🔍 Tìm bài học...", placeholder="Nhập từ khóa...")
        
        if search_query.strip():
            st.caption("Kết quả tìm kiếm:")
            for sub in GRADE_7_SUBJECTS:
                for les in sub["lessons"]:
                    if search_query.lower() in les["title"].lower():
                        if st.button(f"📌 {les['title']}", key=f"search_{les['id']}"):
                            st.session_state.active_lesson = les
                            st.rerun()
        else:
            for subject in GRADE_7_SUBJECTS:
                with st.expander(f"📘 {subject['name']}", expanded=True):
                    for lesson in subject["lessons"]:
                        is_done = lesson["id"] in st.session_state.completed_lessons
                        status_icon = "✅" if is_done else "📖"
                        
                        if st.button(f"{status_icon} {lesson['title']}", key=lesson["id"]):
                            st.session_state.active_lesson = lesson
                            st.rerun()

    # --- CỘT PHẢI: VIDEO PLAYER, GHI CHÚ & TRỢ LÝ AI ---
    with col_main:
        active_lesson = st.session_state.active_lesson
        st.subheader(active_lesson["title"])
        st.caption(f"Thời lượng: {active_lesson['duration']} | Môn học thuộc Khối {st.session_state.selected_grade}")
        
        # Video bài giảng (Nhúng YouTube)
        st.video(active_lesson["video_url"])
        
        # Mô tả bài học & Đánh dấu hoàn thành
        col_desc, col_check = st.columns([3, 1])
        with col_desc:
            st.write(f"**Tóm tắt bài học:** {active_lesson['description']}")
        with col_check:
            lesson_id = active_lesson["id"]
            is_completed = lesson_id in st.session_state.completed_lessons
            if st.checkbox("Đã hoàn thành", value=is_completed):
                if lesson_id not in st.session_state.completed_lessons:
                    st.session_state.completed_lessons.append(lesson_id)
            else:
                if lesson_id in st.session_state.completed_lessons:
                    st.session_state.completed_lessons.remove(lesson_id)

        st.divider()

        # Phần Tabs cho Ghi chú & Trợ lý AI
        tab_notes, tab_ai = st.tabs(["📝 Ghi chú bài học", "🤖 Gia sư AI Gemini"])
        
        with tab_notes:
            current_note = st.session_state.lesson_notes.get(active_lesson["id"], "")
            note_input = st.text_area("Viết ghi chú của bạn tại đây:", value=current_note, height=120)
            if st.button("Lưu Ghi Chú"):
                st.session_state.lesson_notes[active_lesson["id"]] = note_input
                st.success("Đã lưu ghi chú thành công!")

        with tab_ai:
            st.write("🤖 **Hỏi đáp cùng Trợ lý AI về bài học này:**")
            ai_prompt = st.text_input("Nhập câu hỏi của bạn:", placeholder="VD: Giải thích thêm cho em về số hữu tỉ...")
            if st.button("Gửi câu hỏi"):
                if ai_prompt.strip():
                    st.info(f"**Gia sư AI:** Bài học '{active_lesson['title']}' rất quan trọng. Về câu hỏi '{ai_prompt}', em cần nhớ khái niệm số hữu tỉ là số viết được dưới dạng phân số a/b (với a, b ∈ Z, b ≠ 0).")
                else:
                    st.warning("Vui lòng nhập nội dung câu hỏi.")


# -----------------------------------------------------------------------------
# 5. ĐIỀU HƯỚNG LUỒNG CHÍNH (MAIN ENTRY POINT)
# -----------------------------------------------------------------------------
def main():
    if st.session_state.current_user is None:
        render_auth_screen()
    else:
        render_main_app()

if __name__ == "__main__":
    main()
