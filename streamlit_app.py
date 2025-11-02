import json
import os

import streamlit as st
from agents.workflow import run_code_review_workflow

# ---------------------- CẤU HÌNH CHUNG ----------------------
st.set_page_config(page_title="Code Viewer", layout="wide")

# ---------------------- CSS THEME HACKATHON SEAL ----------------------
st.markdown(
    """
<style>
/* Nền gradient + ảnh SEAL */
[data-testid="stAppViewContainer"] {
    background-image:
        linear-gradient(to bottom, rgba(0, 0, 0, 0.85) 0%, rgba(0, 0, 0, 0.55) 40%, rgba(0, 30, 60, 0.25) 70%, rgba(0, 60, 120, 0.1) 100%),
        radial-gradient(circle at center, rgba(0, 80, 150, 0.4), rgba(0, 10, 25, 0.95)),
        url("https://scontent.fsgn2-9.fna.fbcdn.net/v/t39.30808-6/557621112_775914388598180_6880016187368726812_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeErLU3ZBSWMlBW7qpwVnVa9jTKqKsvQIdyNMqoqy9Ah3LZKeuNUEWTsMdO6-VXxcnyHW0TT1y904Bi0bOIRVSNi&_nc_ohc=H1kcYJlN8EgQ7kNvwGBa1wf&_nc_oc=AdmPJ-EekjmeRXgd8wW543OWDTmd4C1gtSsUHZWT_GZ-hJxPmls1oRl2Xn1mvaF9NEg&_nc_zt=23&_nc_ht=scontent.fsgn2-9.fna&_nc_gid=adwffAKIjE1nAThlkk0omg&oh=00_Afj_VUYNiR2h-YqjN3PhHHvEOaibt08m0a2rm1wlUjXYUg&oe=690CBB13");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Làm mờ nhẹ vùng nội dung */
.block-container {
    background: rgba(0, 0, 0, 0.6);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 0 30px rgba(0, 100, 255, 0.3);
}

/* Tiêu đề chính */
h1, h2, h3 {
    color: #58a6ff !important;
    text-shadow: 0px 0px 10px #0ff;
}

/* Nút & text */
.stButton>button {
    background-color: rgba(0, 60, 150, 0.9);
    color: #ffffff;
    border-radius: 10px;
    border: 1px solid #0ff;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #0ff;
    color: #000;
    transform: scale(1.05);
}

/* Textarea code viewer */
.stTextArea textarea {
    font-family: 'Fira Code', monospace;
    background-color: rgba(10, 25, 40, 0.9);
    color: #f0f6fc;
    border-radius: 10px;
    box-shadow: inset 0 0 10px rgba(0, 255, 255, 0.3);
}

/* File & Folder */
.folder {
    font-weight: 600;
    color: #58a6ff;
    cursor: pointer;
}
.file {
    color: #c9d1d9;
    margin-left: 1.5em;
    cursor: pointer;
}
.file:hover {
    color: #00ffff;
    text-shadow: 0px 0px 5px #00ffff;
}

/* Panel phải (AI Review) */
[data-testid="stSidebar"], .css-1d391kg {
    background: rgba(0, 0, 0, 0.8);
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------- HÀM HIỂN THỊ CÂY THƯ MỤC ----------------------
def display_folder_tree(root_folder, base_path=""):
    try:
        for item in sorted(os.listdir(root_folder)):
            item_path = os.path.join(root_folder, item)
            rel_path = os.path.relpath(item_path, base_path)
            if os.path.isdir(item_path):
                with st.expander(f"📁 {item}", expanded=False):
                    display_folder_tree(item_path, base_path)
            else:
                if item.endswith(".py"):
                    if st.button(f"📄 {item}", key=rel_path):
                        st.session_state["selected_file"] = item_path
    except Exception as e:
        st.warning(f"Không thể đọc thư mục: {e}")


# ---------------------- GIAO DIỆN CHÍNH ----------------------
col1, col2, col3 = st.columns([1.5, 3, 2])

# --- Cột 1: Explorer ---
with col1:
    st.header("🗂️ Explorer")
    folder_path = st.text_input(
        "Nhập đường dẫn đến thư mục:",
        value="",
        placeholder="VD: C:\\Users\\MSII\\Downloads\\ca_nhan_2-feature-project",
    )

    if folder_path and os.path.exists(folder_path):
        st.success("✅ Thư mục hợp lệ, đang hiển thị cấu trúc...")
        display_folder_tree(folder_path, folder_path)
    else:
        st.info("💡 Nhập đường dẫn hợp lệ để hiển thị các file.")

# --- Cột 2: Code Viewer ---
with col2:
    st.header("👨‍💻 Code Viewer")
    if "selected_file" in st.session_state:
        file_path = st.session_state["selected_file"]
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            st.text_area("📜 Nội dung file:", code, height=600)
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}")
    else:
        st.info("📁 Chọn một file .py từ bên trái để xem nội dung.")

# --- Cột 3: AI Review Panel ---
with col3:
    st.header("🤖 AI Review Panel")
    st.info(
        "✅ Code viewer ready. Use the controls below to run the Review/Repair agents."
    )

    # If a file is selected, allow agent actions
    if "selected_file" in st.session_state:
        selected = st.session_state["selected_file"]
        st.write(f"Selected: `{selected}`")

        # language selection (basic)
        ext = os.path.splitext(selected)[1].lower()
        language = st.selectbox(
            "Language",
            options=["python", "javascript", "java"],
            index=0 if ext == ".py" else 1,
        )

        if st.button("▶️ Run Review & Repair Agent"):
            try:
                with open(selected, "r", encoding="utf-8") as f:
                    code_to_run = f.read()
            except Exception as e:
                st.error(f"Không thể đọc file: {e}")
                code_to_run = None

            if code_to_run is not None:
                with st.spinner("Running agents..."):
                    review_results, repaired = run_code_review_workflow(
                        code_to_run, language
                    )

                # show review results (JSON) and human-friendly list
                st.subheader("Review Results (raw JSON)")
                st.code(
                    json.dumps(review_results, indent=2, ensure_ascii=False),
                    language="json",
                )

                if review_results:
                    st.subheader("Detected Issues")
                    for idx, issue in enumerate(review_results, start=1):
                        st.markdown(
                            f"**{idx}. {issue.get('issue_type','Issue')}** — severity: {issue.get('severity')}"
                        )
                        st.text(f"Line: {issue.get('line')} — {issue.get('context')}")
                        st.write(issue.get("description"))
                else:
                    st.success("No issues found by the Review Agent.")

                # show repaired code if available
                if repaired:
                    st.subheader("Repaired Code")
                    st.code(repaired, language=language)
                    st.download_button(
                        "Download repaired code",
                        data=repaired,
                        file_name=f"repaired{os.path.splitext(selected)[1]}",
                    )
                else:
                    st.info("No repaired code produced.")
    else:
        st.info(
            "📁 Chọn một file .py từ Explorer bên trái để xem và cho agent chạy review."
        )
