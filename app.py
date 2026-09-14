import streamlit as st
import subprocess
import sys
import io

st.set_page_config(page_title="ArabiTerm Pro", page_icon="💻", layout="wide")

# ব্যাকগ্রাউন্ড ও বক্স গায়েব করার কাস্টম স্টাইল
st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* স্ট্রিমলিট ইনপুট বক্সের সীমানা ও ব্যাকগ্রাউন্ড পুরোপুরি গায়েব করা */
    div[data-baseweb="input"], div[data-baseweb="input"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    input {
        background-color: transparent !important;
        color: #ffffff !important;
        border: none !important;
        outline: none !important;
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
    }
    
    input:focus {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    .stMarkdown p, div[data-testid="stText"] {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
    }

    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# হিস্ট্রি সেশন ইনিশিয়ালাইজেশন
if "history" not in st.session_state:
    st.session_state.history = []

def process_command():
    cmd = st.session_state.user_cmd.strip()
    if cmd:
        if cmd.lower() == "clear":
            st.session_state.history = []
        else:
            output = ""
            
            # ১. AI Assistant
            if cmd.startswith("ai "):
                prompt = cmd.split(" ", 1)[1]
                output = f"AI Bot Response for: '{prompt}'"
            
            # ২. JavaScript / Node.js
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

            # ৪. Linux Shell Engine (Default)
            else:
                clean_cmd = cmd.split(" ", 1)[1] if (cmd.startswith("bash ") or cmd.startswith("sh ")) else cmd
                try:
                    res = subprocess.run(clean_cmd, shell=True, capture_output=True, text=True, timeout=10)
                    output = res.stdout if res.stdout else res.stderr
                except Exception as e:
                    output = f"Linux Shell Error: {e}"

            st.session_state.history.append((cmd, output if output else "Done."))
        
        st.session_state.user_cmd = ""

# টার্মাক্স স্টাইল ওয়েলকাম হেডার
if not st.session_state.history:
    st.text("Welcome to ArabiTerm Pro!")
    st.text("")
    st.text("Docs:      https://termux.dev/docs")
    st.text("Donate:    https://termux.dev/donate")
    st.text("Community: https://termux.dev/community")
    st.text("")
    st.text("Working with packages:")
    st.text("  - Linux Shell:  apt update, ls, pwd, whoami")
    st.text("  - JavaScript:   js console.log('Hello JS')")
    st.text("  - Python:       py print('Hello Python')")
    st.text("  - AI Engine:    ai What is termux?")
    st.text("")
    st.text("Type 'clear' to reset terminal history.")
    st.text("")

# পূর্বের কমান্ড ও আউটপুটসমূহ টার্মিনাল ফ্লোতে দেখানো
for cmd_text, output_text in st.session_state.history:
    st.text(f"$ {cmd_text}")
    if output_text:
        st.text(output_text.strip())

# ফর্ম ব্যবহার করা হয়েছে যেন কিবোর্ডের Enter চাপলেই সাবমিট হয়
with st.form(key="term_form", clear_on_submit=True):
    st.text_input("$ ", key="user_cmd", placeholder="")
    # বাটনটি অদৃশ্য রাখা হয়েছে, কিবোর্ডের Enter দিয়েই ট্র্রিগার হবে
    submitted = st.form_submit_button("", on_click=process_command)

