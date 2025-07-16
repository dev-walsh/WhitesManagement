import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password():
    """Returns True if the user has the correct password"""
    
    def password_entered():
        """Checks whether a password entered by the user is correct"""
        username = st.session_state["username"]
        password = st.session_state["password"]
        
        # Default credentials: admin/admin
        if username == "admin" and password == "admin":
            st.session_state["password_correct"] = True
            st.session_state["username"] = username
            st.session_state["login_time"] = datetime.now()
            del st.session_state["password"]  # Don't store password
            return True
        else:
            st.session_state["password_correct"] = False
            return False

    # Check if already logged in and session is valid (24 hours)
    if st.session_state.get("password_correct", False):
        if "login_time" in st.session_state:
            login_time = st.session_state["login_time"]
            if datetime.now() - login_time < timedelta(hours=24):
                return True
            else:
                # Session expired
                st.session_state["password_correct"] = False
                del st.session_state["login_time"]
                st.warning("Session expired. Please login again.")

    # Show login form
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 2rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    .login-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .login-form {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .login-footer {
        text-align: center;
        margin-top: 2rem;
        color: #666;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="login-header">🔐 Whites Management Login</h1>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter username", key="username")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="password")
        
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submitted:
            if password_entered():
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    st.markdown("""
    <div class="login-footer">
        <p><strong>Default Credentials:</strong></p>
        <p>Username: <code>admin</code></p>
        <p>Password: <code>admin</code></p>
        <p><em>Change these credentials in production</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return False

def logout():
    """Logout function"""
    for key in ["password_correct", "username", "login_time"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def get_current_user():
    """Get current logged in user"""
    return st.session_state.get("username", "Unknown")

def is_logged_in():
    """Check if user is logged in"""
    return st.session_state.get("password_correct", False)

def require_login():
    """Decorator function to require login for pages"""
    if not check_password():
        st.stop()
    return True

def show_logout_button():
    """Show logout button in sidebar"""
    if is_logged_in():
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"**Logged in as:** {get_current_user()}")
            if st.button("🚪 Logout", use_container_width=True):
                logout()