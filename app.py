import streamlit as st
import sys
import io
import subprocess

st.set_page_config(page_title="ArabiTerm Pro", page_icon="💻", layout="wide")

# Termux এর মতো ক্লিন ব্ল্যাক অ্যান্ড হোয়াইট থিম CSS
st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
    }
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
        font-size: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

def run_command():
    cmd = st.session_state.current_cmd.strip()
    if cmd:
        if cmd.lower() == "clear":
            st.session_state.history = []
        else:
            output = ""
            
            # ১. AI Assistant
            if cmd.startswith("ai "):
                prompt = cmd.split(" ", 1)[1]
                output = f"AI Bot: Analyzing prompt '{prompt}'...\n(API Key সেটআপ করলে এখানে AI সরাসরি রেসপন্স দেবে)"
            
            # ২. JavaScript / Node.js
            elif cmd.startswith("js ") or cmd.startswith("node "):
                js_code = cmd.split(" ", 1)[1]
                try:
                    res = subprocess.run(["node", "-e", js_code], capture_output=True, text=True, timeout=10)
                    output = res.stdout if res.stdout else res.stderr
                except Exception as e:
                    output = f"JS Error: {e}"

            # ৩. C Programming
            elif cmd.startswith("c "):
                c_code = cmd.split(" ", 1)[1]
                try:
                    with open("temp.c", "w") as f:
                        f.write(c_code)
                    compile_res = subprocess.run(["gcc", "temp.c", "-o", "temp_c"], capture_output=True, text=True)
                    if compile_res.returncode == 0:
                        run_res = subprocess.run(["./temp_c"], capture_output=True, text=True, timeout=10)
                        output = run_res.stdout if run_res.stdout else run_res.stderr
                    else:
                        output = compile_res.stderr
                except Exception as e:
                    output = f"C Execution Error: {e}"

            # ৪. C++ Programming
            elif cmd.startswith("cpp ") or cmd.startswith("c++ "):
                cpp_code = cmd.split(" ", 1)[1]
                try:
                    with open("temp.cpp", "w") as f:
                        f.write(cpp_code)
                    compile_res = subprocess.run(["g++", "temp.cpp", "-o", "temp_cpp"], capture_output=True, text=True)
                    if compile_res.returncode == 0:
                        run_res = subprocess.run(["./temp_cpp"], capture_output=True, text=True, timeout=10)
                        output = run_res.stdout if run_res.stdout else run_res.stderr
                    else:
                        output = compile_res.stderr
                except Exception as e:
                    output = f"C++ Execution Error: {e}"

            # ৫. Python Exec Engine
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

            # ৬. Linux Shell Commands (Default)
            else:
                clean_cmd = cmd.split(" ", 1)[1] if (cmd.startswith("bash ") or cmd.startswith("sh ")) else cmd
                try:
                    res = subprocess.run(clean_cmd, shell=True, capture_output=True, text=True, timeout=10)
                    output = res.stdout if res.stdout else res.stderr
                except Exception as e:
                    output = f"Linux Shell Error: {e}"

            st.session_state.history.append((cmd, output if output else "Done."))
        st.session_state.current_cmd = ""

# Termux স্টাইলের ওয়েলকাম হেডার
st.text("Welcome to ArabiTerm Pro All-in-One Engine!")
st.text("")
st.text("Supported Engines & Syntax:")
st.text(" - Linux Shell:  ls, pwd, whoami, uname -a, cat")
st.text(" - JavaScript:   js console.log('Hello JS')")
st.text(" - Python:       py print('Hello Python')")
st.text(" - C Code:       c #include<stdio.h>\nint main(){printf(\"Hello C\");return 0;}")
st.text(" - C++ Code:     cpp #include<iostream>\nint main(){std::cout<<\"Hello C++\";return 0;}")
st.text(" - AI Assistant: ai Write a python script for sorting")
st.text("")
st.text("For fixing screen issues, type 'clear' command.")
st.text("")

# আউটপুট হিস্ট্রি প্রদর্শন
for cmd_text, output_text in st.session_state.history:
    st.text(f"$ {cmd_text}")
    if output_text:
        st.text(output_text.strip())

# Termux ইনপুট প্রম্পট ($ )
st.text_input("$ ", key="current_cmd", on_change=run_command, placeholder="")
