import streamlit as st

# পেজ টাইটেল ও কনফিগারেশন
st.set_page_config(page_title="ArabiTerm Pro AI", page_icon="💻", layout="centered")

st.title("🚀 ArabiTerm Pro v2.0 AI Edition")
st.subheader("Developed by Arabi")
st.write("---")

# লগইন সিস্টেম
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.header("🔒 System Authentication")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "123":
            st.session_state.logged_in = True
            st.success("Access Granted! Welcome Admin.")
            st.rerun()
        else:
            st.error("Invalid Username or Password!")
else:
    st.sidebar.success("Status: Connected to Server")
    st.sidebar.info("Developer: Arabi")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # কমান্ড প্রম্পট ও এআই ইন্টারফেস
    st.markdown("### ⚡ Interactive Control Panel")
    command = st.text_input("What would you like to do? (Enter command)")

    # AI Auto-correct 
    corrections = {"lss": "ls", "cleer": "clear", "pwwd": "pwd", "exitt": "exit"}
    
    if st.button("Run Command"):
        if command:
            cmd_word = command.split()[0].lower()
            if cmd_word in corrections:
                fixed_cmd = corrections[cmd_word]
                st.warning(f"[AI Engine]: Auto-corrected typo '{command}' -> '{fixed_cmd}'")
                command = fixed_cmd

            # Safety Shield Check
            if "rm -rf" in command:
                st.error("[ArabiTerm AI Shield]: CRITICAL SECURITY RISK! Command Blocked.")
            else:
                st.code(f"Executing: {command}\n[System]: Command processed successfully.", language="bash")
