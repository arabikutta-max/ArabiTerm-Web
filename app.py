import streamlit as st
import sys
import io

st.set_page_config(page_title="ArabiTerm Pro", page_icon="💻", layout="wide")

# বক্স ছাড়া ফুল স্ক্রিন টার্মিনাল স্টাইল
st.markdown("""
    <style>
    /* পুরো স্ক্রিন কালো */
    .stApp {
        background-color: #000000;
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    /* ইনপুট বক্সের বর্ডার ও ব্যাকগ্রাউন্ড গায়েব করা */
    div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    input {
        background-color: transparent !important;
        color: #00ff00 !important;
        border: none !important;
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
    }
    /* ডিভাইডার লাইন সরিয়ে ফেলা */
    hr {
        display: none;
    }
    .stMarkdown p {
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# হিস্ট্রি ট্র্যাক করা
if "history" not in st.session_state:
    st.session_state.history = []

def run_command():
    cmd = st.session_state.current_cmd
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
        st.session_state.current_cmd = ""

# শিরোনাম
st.write("ArabiTerm Pro Terminal [Version 2.0]")
st.write("Type 'clear' to reset terminal history.")
st.write("--------------------------------------------------")

# পূর্বের লাইন বাই লাইন আউটপুট দেখানো
line_num = 1
for cmd, output in st.session_state.history:
    st.text(f"Line {line_num}: >>> {cmd}")
    if output:
        st.text(output)
    line_num += 1

# নতুন ইনপুট দেওয়ার লাইন (বক্স ছাড়া)
current_label = f"Line {line_num}: >>>"
st.text_input(current_label, key="current_cmd", on_change=run_command, placeholder="Enter or paste command here...")
