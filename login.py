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
            st.session_state["current_user"] = username
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

    # Modern login page with mobile-responsive design
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        color: #e0e6ed !important;
        min-height: 100vh !important;
    }
    
    /* Hide default Streamlit elements that might create empty containers */
    .stApp > header {
        display: none !important;
    }
    
    /* Hide any empty containers at the top */
    .stApp > div:empty {
        display: none !important;
    }
    
    /* Hide default Streamlit containers */
    .stApp > div:first-child:empty {
        display: none !important;
    }
    
    /* Hide any potential empty sidebar containers */
    .stSidebar > div:empty {
        display: none !important;
    }
    
    /* Remove any default padding/margins that might create empty space */
    .stApp > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2.5rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 50%, #2196f3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        color: #b0bec5;
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #e0e6ed !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2196f3 !important;
        box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(33, 150, 243, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 32px rgba(33, 150, 243, 0.4) !important;
    }
    
    .login-footer {
        text-align: center;
        margin-top: 2rem;
        color: #b0bec5;
        font-size: 0.9rem;
        background: rgba(255, 255, 255, 0.02);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .login-footer code {
        background: rgba(33, 150, 243, 0.2);
        color: #64b5f6;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
    }
    
    @media (max-width: 768px) {
        .login-container {
            margin: 1rem;
            padding: 1.5rem;
        }
        
        .login-title {
            font-size: 2rem;
        }
        
        .login-subtitle {
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input {
            padding: 0.875rem !important;
        }
        
        .stButton > button {
            padding: 0.875rem 1.5rem !important;
            font-size: 1rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('''
    <div class="login-header">
        <div class="login-title">🔐 Whites Management</div>
        <div class="login-subtitle">Enter your credentials to access the system</div>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username", key="username")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="password")
        
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if password_entered():
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
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
    for key in ["password_correct", "current_user", "login_time"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def get_current_user():
    """Get current logged in user"""
    return st.session_state.get("current_user", "Unknown")

def is_logged_in():
    """Check if user is logged in"""
    return st.session_state.get("password_correct", False)

def require_login():
    """Decorator function to require login for pages"""
    if not check_password():
        st.stop()
    return True

def show_logout_button():
    """Show modern logout button in sidebar"""
    if is_logged_in():
        st.markdown("""
        <style>
        .logout-section {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(244, 67, 54, 0.3);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            margin-top: 1rem;
        }
        .logout-user {
            color: #e0e6ed;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="logout-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="logout-user">👤 {get_current_user()}</div>', unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True, key="logout-btn"):
            logout()
        st.markdown('</div>', unsafe_allow_html=True)