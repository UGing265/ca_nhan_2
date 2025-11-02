import os

import streamlit as st

st.set_page_config(page_title="Code Viewer", layout="wide")

# --- CSS cho theme tối giống VSCode
st.markdown(
    """
    <style>
        body {
            background-color: #0e1117;
            color: #fafafa;
        }
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
            color: #58a6ff;
        }
        .stTextArea textarea {
            font-family: 'Fira Code', monospace;
            background-color: #161b22;
            color: #f0f6fc;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# --- Hàm đệ quy để hiển thị cây thư mục
def display_folder_tree(root_folder, base_path=""):
    items = []
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


# --- Layout 3 cột
col1, col2, col3 = st.columns([1.5, 3, 2])

# --- Cột trái: chọn folder + hiển thị cây thư mục
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

# --- Cột giữa: hiển thị code
with col2:
    st.header("🧑‍💻 Code Viewer")
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

# --- Cột phải: giữ nguyên bảng AI Review Panel
with col3:
    st.header("🤖 AI Review Panel")
    st.info("✅ Code viewer ready. Waiting for AI agent integration.")
