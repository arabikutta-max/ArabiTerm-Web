import streamlit as st
import subprocess
import sys
import io

st.set_page_config(page_title="ArabiTerm Pro", page_icon="💻", layout="wide")

# পুরো পেজের মার্জিন ও স্ক্রোলবার ক্লিন করার সিএসএস
st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        padding: 0 !important;
    }
    header, footer, [data-testid="stHeader"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = [
        "Welcome to ArabiTerm Pro!",
        "",
        "Docs:      https://termux.dev/docs",
        "Donate:    https://termux.dev/donate",
        "Community: https://termux.dev/community",
        "",
        "Working with engines:",
        "  - Linux Shell:  apt update, ls, pwd, whoami",
        "  - JavaScript:   js console.log('Hello JS')",
        "  - Python:       py print('Hello Python')",
        "  - AI Engine:    ai What is termux?",
        "",
        "Type 'clear' to reset terminal screen.",
        ""
    ]

# ব্যাকএন্ড থেকে কমান্ড প্রসেসিং
if "cmd" in st.query_params:
    cmd = st.query_params["cmd"]
    st.query_params.clear()
    
    if cmd.strip().lower() == "clear":
        st.session_state.history = []
    else:
        st.session_state.history.append(f"$ {cmd}")
        output = ""
        
        # ১. AI Assistant Engine
        if cmd.startswith("ai "):
            prompt = cmd.split(" ", 1)[1]
            output = f"AI Bot: Processed prompt '{prompt}'"
            
        # ২. JavaScript Engine
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
            try:
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                output = res.stdout if res.stdout else res.stderr
            except Exception as e:
                output = f"Shell Error: {e}"
                
        if output.strip():
            for line in output.strip().split("\n"):
                st.session_state.history.append(line)

# টার্মিনালের হিস্ট্রি সাজানো
formatted_history = "\n".join(st.session_state.history)

# Termux এর মতো সম্পূর্ণ খোলা ফিল্ড HTML/JS ইন্টারফেস
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    html, body {{
        background-color: #000000;
        color: #ffffff;
        font-family: 'Courier New', monospace;
        font-size: 15px;
        margin: 0;
        padding: 8px;
        height: 100vh;
        width: 100vw;
        box-sizing: border-box;
        cursor: text;
    }}
    #terminal-field {{
        white-space: pre-wrap;
        word-break: break-all;
        color: #ffffff;
        margin-bottom: 5px;
    }}
    .input-line {{
        display: flex;
        align-items: center;
    }}
    .prompt {{
        color: #00ff00;
        font-weight: bold;
        margin-right: 8px;
    }}
    #cmd-input {{
        background: transparent !important;
        border: none !important;
        outline: none !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 15px !important;
        flex-grow: 1;
        padding: 0;
        margin: 0;
        caret-color: #00ff00;
    }}
</style>
</head>
<body onclick="document.getElementById('cmd-input').focus()">

<div id="terminal-field"></div>

<div class="input-line">
    <span class="prompt">$</span>
    <input type="text" id="cmd-input" autofocus autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" />
</div>

<script>
    const historyText = {repr(formatted_history)};
    document.getElementById("terminal-field").innerText = historyText;
    
    const input = document.getElementById("cmd-input");
    
    // অটোমেটিক ফোকাস এবং স্ক্রোল ডাউন
    window.onload = function() {{
        input.focus();
        window.scrollTo(0, document.body.scrollHeight);
    }};

    input.addEventListener("keydown", function(e) {{
        if (e.key === "Enter") {{
            e.preventDefault();
            const val = input.value;
            if (val.trim() !== "") {{
                const url = new URL(window.parent.location.href);
                url.searchParams.set("cmd", val);
                window.parent.location.href = url.href;
            }}
        }}
    }});
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=1000, scrolling=True)
