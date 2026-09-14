import streamlit as st
import sys
import io

# টার্মিনালের মতো ডার্ক থিম কনফিগারেশন
st.set_page_config(page_title="ArabiTerm Pro", page_icon="💻", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0c0c0c;
        color: #00ff66;
        font-family: 'Courier New', Courier, monospace;
    }
    input {
        background-color: #1a1a1a !important;
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    .stMarkdown p {
        color: #00ff66;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💻 ArabiTerm Pro - Terminal Edition")
st.write("--------------------------------------------------")

# কমান্ড হিস্ট্রি বজায় রাখা
if "history" not in st.session_state:
    st.session_state.history = []

# কমান্ড ইনপুট ফাংশন
def run_command():
    cmd = st.session_state.user_cmd
    if cmd.strip():
        if cmd.strip().lower() == "clear":
            st.session_state.history = []
        else:
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            try:
                exec(cmd)
                output = redirected_output.getvalue()
                st.session_state.history.append((cmd, output if output else "Done."))
            except Exception as e:
                st.session_state.history.append((cmd, f"Error: {e}"))
            finally:
                sys.stdout = old_stdout
        st.session_state.user_cmd = ""

# পুরোনো কমান্ড ও আউটপুট প্রদর্শন
for cmd, output in st.session_state.history:
    st.text(f">>> {cmd}")
    st.text(output)
    st.write("---")

# কমান্ড ইনপুট বক্স
st.text_input("Enter Command:", key="user_cmd", on_change=run_command, placeholder="e.g. print('Hello World')")
