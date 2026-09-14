import streamlit as st
import subprocess
import sys
import io

st.set_page_config(page_title="ArabiTerm Pro", page_icon="💻", layout="wide")

# টার্মাক্স ফ্রেমলেস ডার্ক থিম CSS
st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #000000 !important;
    }
    
    p, span, div, label, .stMarkdown {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 15px !important;
    }

    /* st.chat_input-এর পুরো স্ট্রাকচার থেকে বক্স ও বর্ডার গায়েব করা */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    
    [data-testid="stChatInput"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 15px !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* চ্যাট ইনপুটের ভেতরে থাকা সেন্ড বাটন অদৃশ্য করা */
    [data-testid="stChatInputSubmitButton"] {
        display: none !important;
    }

    header, footer, [data-testid="stHeader"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# হিস্ট্রি ট্র্যাকিং
if "history" not in st.session_state:
    st.session_state.history = []

# টার্মাক্সের মতো হুবহু ওয়েলকাম হেডার
if not st.session_state.history:
    welcome_text = """Welcome to ArabiTerm Pro!

Docs:       https://ArabiTerm-web.dev/docs
Donate:     https://ArabiTerm-web.dev/donate
Community:  https://ArabiTerm-web.dev/community

Working with packages:

 - Search:  pkg search <query>
 - Install: pkg install <package>
 - Upgrade: pkg upgrade

Subscribing to additional repositories:

 - Root:    pkg install root-repo
 - X11:     pkg install x11-repo

For fixing any repository issues,
try 'ArabiTerm-web-change-repo' command.

Report issues at https://ArabiTerm-web.dev/issues"""
    st.text(welcome_text)

# পূর্বে রান করা আদেশ ও আউটপুটসমূহ
for cmd_text, output_text in st.session_state.history:
    st.markdown(f"~ $ {cmd_text}", unsafe_allow_html=True)
    if output_text:
        st.text(output_text.strip())

# মোবাইল কিবোর্ডের Enter কাজ করার জন্য কাস্টমাইজড চ্যাট ইনপুট
user_cmd = st.chat_input("~ $ ")

if user_cmd:
    cmd = user_cmd.strip()
    if cmd.lower() == "clear":
        st.session_state.history = []
        st.rerun()
    else:
        output = ""
        
        # ১. AI Engine
        if cmd.startswith("ai "):
            prompt = cmd.split(" ", 1)[1]
            output = f"AI Output: {prompt}"
        
        # ২. JS Engine
        elif cmd.startswith("js ") or cmd.startswith("node "):
            js_code = cmd.split(" ", 1)[1]
            try:
                res = subprocess.run(["node", "-e", js_code], capture_output=True, text=True, timeout=10)
                output = res.stdout if res.stdout else res.stderr
            except Exception as e:
                output = f"JS Error: {e}"

        # ৩. Python Engine
        elif cmd.startswith("py ") or cmd.startswith("python "):
            py_code = cmd.split(" ", 1)[1]
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            try:
                exec(py_code)
                output = redirected_output.getvalue()
            except Exception as e:
                output = f"Python Error: {e}"
            finally:
                sys.stdout = old_stdout

        # ৪. Linux Shell Engine
        else:
            clean_cmd = cmd.split(" ", 1)[1] if (cmd.startswith("bash ") or cmd.startswith("sh ")) else cmd
            try:
                res = subprocess.run(clean_cmd, shell=True, capture_output=True, text=True, timeout=10)
                output = res.stdout if res.stdout else res.stderr
            except Exception as e:
                output = f"Shell Error: {e}"

        st.session_state.history.append((cmd, output if output else "Done."))
        st.rerun()
