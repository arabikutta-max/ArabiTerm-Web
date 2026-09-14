import streamlit as st
import subprocess
import sys
import io

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="ArabiTerm Pro", page_icon="💻", layout="wide")

# ২. ডার্ক মিনিমালিস্ট ও ফ্রেমলেস টার্মিনাল CSS
st.markdown("""
    <style>
    /* পুরো পেজের ব্যাকগ্রাউন্ড কুচকুচে কালো */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #000000 !important;
    }
    
    /* টেক্সটের কালার ধবধবে উজ্জ্বল সাদা */
    p, span, div, label, .stMarkdown {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
    }
    
    /* ইনপুট বক্সের সাদা ব্যাকগ্রাউন্ড ও বর্ডার পুরোপুরি অদৃশ্য করা */
    div[data-baseweb="input"], div[data-baseweb="input"] > div {
        background-color: #000000 !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* টাইপিং টেক্সটের রঙ সবুজ */
    input {
        background-color: #000000 !important;
        color: #00ff00 !important;
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

    /* সাবমিট বাটন পুরোপুরি গায়েব করা */
    div[data-testid="stFormSubmitButton"], button {
        display: none !important;
    }

    /* স্ট্রিমলিটের ডিফল্ট হেডার ও ফুটার হাইড করা */
    header, footer, [data-testid="stHeader"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ৩. হিস্ট্রি সেশন ট্র্যাকিং
if "history" not in st.session_state:
    st.session_state.history = []

# ৪. কমান্ড প্রসেসিং ও এক্সিকিউটর ফাংশন
def run_command():
    cmd = st.session_state.user_cmd.strip()
    if cmd:
        if cmd.lower() == "clear":
            st.session_state.history = []
        else:
            output = ""
            
            # (ক) AI Assistant Engine
            if cmd.startswith("ai "):
                prompt = cmd.split(" ", 1)[1]
                output = f"AI Bot Response: Processed prompt '{prompt}'"
            
            # (খ) JavaScript / Node.js Engine
            elif cmd.startswith("js ") or cmd.startswith("node "):
                js_code = cmd.split(" ", 1)[1]
                try:
                    res = subprocess.run(["node", "-e", js_code], capture_output=True, text=True, timeout=10)
                    output = res.stdout if res.stdout else res.stderr
                except Exception as e:
                    output = f"JS Execution Error: {e}"

            # (গ) Python Engine
            elif cmd.startswith("py ") or cmd.startswith("python "):
                py_code = cmd.split(" ", 1)[1]
                old_stdout = sys.stdout
                redirected_output = sys.stdout = io.StringIO()
                try:
                    exec(py_code)
                    output = redirected_output.getvalue()
                except Exception as e:
                    output = f"Python Execution Error: {e}"
                finally:
                    sys.stdout = old_stdout

            # (ঘ) Linux Shell Engine (Default)
            else:
                clean_cmd = cmd.split(" ", 1)[1] if (cmd.startswith("bash ") or cmd.startswith("sh ")) else cmd
                try:
                    res = subprocess.run(clean_cmd, shell=True, capture_output=True, text=True, timeout=10)
                    output = res.stdout if res.stdout else res.stderr
                except Exception as e:
                    output = f"Shell Error: {e}"

            st.session_state.history.append((cmd, output if output else "Done."))
        
        st.session_state.user_cmd = ""

# ৫. ক্লিন হেডার
if not st.session_state.history:
    st.text("ArabiTerm Pro Terminal Engine")
    st.text("--------------------------------------------------")

# ৬. টার্মিনাল আউটপুট সাজানো
for cmd_text, output_text in st.session_state.history:
    st.markdown(f"<span style='color:#00ff00; font-weight:bold;'>$</span> {cmd_text}", unsafe_allow_html=True)
    if output_text:
        st.text(output_text.strip())

# ৭. ইনপুট প্রম্পট (কোনো দৃশ্যমান বাটন বা বক্সের বর্ডার থাকবে না, Enter দিলে কাজ করবে)
with st.form(key="arabi_term_form", clear_on_submit=True):
    col1, col2 = st.columns([0.03, 0.97])
    with col1:
        st.markdown("<span style='color:#00ff00; font-weight:bold; font-size:18px;'>$</span>", unsafe_allow_html=True)
    with col2:
        st.text_input("", key="user_cmd", placeholder="", label_visibility="collapsed")
    
    st.form_submit_button("", on_click=run_command)
