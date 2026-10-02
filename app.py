# ============================================================
#              SCHOOL OF SKILLS - MANAGEMENT SYSTEM
#                          app.py
#
# High-End Modern EdTech SaaS Web Application Architecture.
# All business logic, OOP domain entities, and data models
# reside in sos.py. This file manages user interface state,
# styling, rendering pipelines, and user interaction flows.
# ============================================================

# Import the core Streamlit library which powers our web dashboard interface
import streamlit as st
# Import date object from Python's standard datetime module for handling calendar dates
from datetime import date
# Import pandas library for tabular data structures and rendering structured dataframes
import pandas as pd
# Import base64 module to encode binary images into inline browser-compatible data URIs
import base64
# Import the operating system module to safely check for local file availability
import os
# Import random module for generating unique transaction and announcement IDs
import random

# Import all core OOP domain models and activities coordinator from sos.py
from sos import (
    SOS,                 # Central institution profile and details class
    Staff,               # Base class representing school staff members
    Teacher,             # Academic faculty sub-class specializing in subject delivery
    StudentCoordinator,  # Operational staff managing admissions and student guidance
    MediaTeam,           # Communications staff managing digital branding and events
    Accountant,          # Financial staff auditing tuition and fee collections
    Program,             # Academic course offering and syllabus tracking class
    Student,             # Enrolled learner entity holding profile, fees, and attendance
    Notice,              # Campus notice and bulletin announcement model
    SOSActivities        # Operational controller handling workflows and rule validations
)


# ============================================================
#                    PAGE CONFIGURATION
# ============================================================

# Configure Streamlit window title, icon, and full-width responsive viewport layout
st.set_page_config(
    page_title="SOS - School Of Skills",                     # Title displayed in the browser tab
    page_icon="🏫",                                          # Favicon emoji displayed in the browser tab
    layout="wide",                                           # Set layout mode to utilize the full display width
    initial_sidebar_state="expanded"                         # Keep the left navigation panel open by default
)


# ============================================================
#                    SMALL DESIGN HELPERS
# ============================================================

# Helper function to read the local logo file and encode it as a Base64 string for HTML embedding
def get_logo_as_base64():
    # Verify that the logo image file exists on the local file system before opening
    if not os.path.exists("logo.png"):
        # Return None gracefully if the file is absent so the application does not crash
        return None
    # Open the logo file in binary read mode to extract its raw binary data
    with open("logo.png", "rb") as logo_file:
        # Read file bytes, encode into base64, and decode as an ASCII string for inline HTML use
        return base64.b64encode(logo_file.read()).decode("utf-8")


# Helper function to generate a modern, accessible pill-shaped tag badge with custom colors
def badge(text, bg_color="#EEF2FF", text_color="#3730A3", border_color="transparent"):
    # Return a stylized HTML span element configured with padding, border radius, and colors
    return (
        f'<span style="background-color:{bg_color}; color:{text_color}; '
        f'border: 1px solid {border_color}; '
        f'padding: 3px 10px; border-radius: 9999px; font-size: 0.76rem; '
        f'font-weight: 600; letter-spacing: 0.02em; display: inline-flex; '
        f'align-items: center; white-space: nowrap;">{text}</span>'
    )


# Color mapping dictionary defining modern soft-pastel backgrounds and high-contrast text for staff roles
ROLE_BADGE_STYLES = {
    # Styling for Teacher role: soft terracotta badge
    "Teacher": {"bg": "rgba(224, 94, 62, 0.12)", "text": "#C84B29", "border": "rgba(224, 94, 62, 0.25)"},
    # Styling for Student Coordinator: soft crimson red badge
    "Student Coordinator": {"bg": "rgba(220, 38, 38, 0.12)", "text": "#DC2626", "border": "rgba(220, 38, 38, 0.25)"},
    # Styling for Media Team: soft purple badge
    "Media Team": {"bg": "rgba(168, 85, 247, 0.12)", "text": "#7E22CE", "border": "rgba(168, 85, 247, 0.25)"},
    # Styling for Accountant: soft amber badge
    "Accountant": {"bg": "rgba(245, 158, 11, 0.12)", "text": "#B45309", "border": "rgba(245, 158, 11, 0.25)"}
}

# Color mapping dictionary defining modern badge styles for student enrollment status
STATUS_BADGE_STYLES = {
    # Active enrolled student: vibrant emerald badge
    "Active": {"bg": "rgba(16, 185, 129, 0.12)", "text": "#047857", "border": "rgba(16, 185, 129, 0.25)"},
    # Inactive or unenrolled student: warm slate badge
    "Not Enrolled": {"bg": "rgba(100, 116, 139, 0.12)", "text": "#475569", "border": "rgba(100, 116, 139, 0.25)"}
}

# Color mapping dictionary defining modern badge styles for tuition fee payment statuses
FEE_STATUS_BADGE_STYLES = {
    # Fully paid: emerald green indicating cleared status
    "Fully Paid": {"bg": "rgba(16, 185, 129, 0.12)", "text": "#047857", "border": "rgba(16, 185, 129, 0.25)"},
    # Partially paid: warm amber indicating installments pending
    "Partially Paid": {"bg": "rgba(245, 158, 11, 0.12)", "text": "#B45309", "border": "rgba(245, 158, 11, 0.25)"},
    # Unpaid: soft coral red indicating overdue tuition
    "Unpaid": {"bg": "rgba(239, 68, 68, 0.12)", "text": "#B91C1C", "border": "rgba(239, 68, 68, 0.25)"},
    # Not applicable: neutral grey for non-tuition profiles
    "Not Applicable": {"bg": "rgba(148, 163, 184, 0.12)", "text": "#64748B", "border": "rgba(148, 163, 184, 0.25)"}
}

# Color mapping dictionary defining modern badge styles for announcement categories
NOTICE_CATEGORY_STYLES = {
    # Urgent alert: soft red container with bold crimson text
    "Urgent": {"bg": "rgba(239, 68, 68, 0.12)", "text": "#B91C1C", "border": "rgba(239, 68, 68, 0.3)"},
    # Campus event: modern sky blue container with deep royal blue text
    "Event": {"bg": "rgba(14, 165, 233, 0.12)", "text": "#0369A1", "border": "rgba(14, 165, 233, 0.3)"},
    # General notice: modern teal container with dark teal text
    "General": {"bg": "rgba(20, 184, 166, 0.12)", "text": "#0F766E", "border": "rgba(20, 184, 166, 0.3)"},
    # Examination notice: golden amber container with deep amber text
    "Exam": {"bg": "rgba(245, 158, 11, 0.12)", "text": "#B45309", "border": "rgba(245, 158, 11, 0.3)"}
}


# Helper function to render object detail dictionaries as a clean, styled specification list
def render_details(details):
    # Iterate through each key-value pair in the provided entity dictionary
    for key, value in details.items():
        # Check if the attribute is Staff Role and matches a known style definition
        if key == "Role" and value in ROLE_BADGE_STYLES:
            # Extract badge color specifications for this staff role
            s = ROLE_BADGE_STYLES[value]
            # Render key along with the styled pill badge
            st.markdown(f"**{key}:** {badge(value, s['bg'], s['text'], s['border'])}", unsafe_allow_html=True)
        # Check if the attribute is Enrollment Status and matches a known style definition
        elif key == "Status" and value in STATUS_BADGE_STYLES:
            # Extract badge color specifications for this status
            s = STATUS_BADGE_STYLES[value]
            # Render key along with the styled pill badge
            st.markdown(f"**{key}:** {badge(value, s['bg'], s['text'], s['border'])}", unsafe_allow_html=True)
        # Check if the attribute is Fee Status and matches a known style definition
        elif key == "Fee Status" and value in FEE_STATUS_BADGE_STYLES:
            # Extract badge color specifications for this fee status
            s = FEE_STATUS_BADGE_STYLES[value]
            # Render key along with the styled pill badge
            st.markdown(f"**{key}:** {badge(value, s['bg'], s['text'], s['border'])}", unsafe_allow_html=True)
        # Standard fallback for general attributes (strings, numbers, dates)
        else:
            # Render label and value as clean markdown text
            st.write(f"**{key}:** {value}")


# Helper function to generate an ultra-modern, theme-responsive SaaS KPI card container
def kpi_card(title, value, subtitle, icon, accent_color="#DC2626"):
    # Build clean HTML card markup without leading line indentation to prevent markdown pre-block formatting
    html_markup = (
        f'<div style="background-color: var(--secondary-background-color); '
        f'border: 1px solid rgba(148, 163, 184, 0.18); border-radius: 16px; '
        f'padding: 20px 22px; position: relative; overflow: hidden; '
        f'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03); transition: transform 0.18s ease, box-shadow 0.18s ease;">'
        f'<div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: {accent_color};"></div>'
        f'<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">'
        f'<span style="font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; opacity: 0.72;">{title}</span>'
        f'<div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(148, 163, 184, 0.12); '
        f'display: flex; align-items: center; justify-content: center; font-size: 1.15rem;">{icon}</div>'
        f'</div>'
        f'<div style="font-size: 2.1rem; font-weight: 800; line-height: 1.1; margin-bottom: 6px; letter-spacing: -0.02em;">{value}</div>'
        f'<div style="font-size: 0.8rem; opacity: 0.75; display: flex; align-items: center; gap: 4px;">'
        f'<span style="color: {accent_color}; font-weight: 600;">●</span> {subtitle}'
        f'</div>'
        f'</div>'
    )
    # Output the styled HTML string to Streamlit's markdown renderer
    st.markdown(html_markup, unsafe_allow_html=True)


# ============================================================
#                    GLOBAL SAAS STYLING (CSS)
# ============================================================

# Inject global SaaS stylesheet enforcing modern typography, sleek sidebar navigation, and card aesthetics
st.markdown(
    """
    <style>
        /* Import Plus Jakarta Sans web font from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        /* Import Material Symbols Rounded font directly to ensure icon ligatures always resolve */
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

        /* Apply modern typography font specifically to text and heading tags */
        html, body, p, h1, h2, h3, h4, h5, h6, label {
            /* Set font family to Plus Jakarta Sans with standard sans-serif fallbacks */
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Protect all icon containers from having their font-family overridden */
        .material-symbols-rounded,
        .material-symbols-outlined,
        [data-testid*="Icon"],
        [data-testid="stIconMaterial"],
        [data-testid="stExpanderToggleIcon"],
        span[data-testid="stIconMaterial"] {
            /* Enforce Material Symbols Rounded font so glyphs render as icons and never as text */
            font-family: 'Material Symbols Rounded', 'Material Icons' !important;
            /* Ensure font-style is normal */
            font-style: normal !important;
            /* Set display mode to inline-block for proper alignment */
            display: inline-block !important;
            /* Prevent unwanted text wrapping on icon glyphs */
            white-space: nowrap !important;
            /* Ensure left-to-right rendering direction */
            direction: ltr !important;
            /* Enable font ligature rendering */
            -webkit-font-feature-settings: 'liga' !important;
            /* Enable antialiased smoothing for crisp icon edges */
            -webkit-font-smoothing: antialiased !important;
        }

        /* ------------------- MODERN DARK SLATE SIDEBAR ------------------- */
        /* ------------------- MODERN RED & WHITE SIDEBAR ------------------- */
        /* Style the left sidebar background as an elegant deep red slate panel */
        section[data-testid="stSidebar"] {
            /* Background color set to deep crimson slate */
            background-color: #170707 !important;
            /* Subtle red border for clean separation */
            border-right: 1px solid rgba(220, 38, 38, 0.18) !important;
        }

        /* Pull the sidebar content up closer to the top and flex container to push footer down */
        section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
            /* Reduce top padding from 4rem to 1rem to move logo higher up */
            padding-top: 1rem !important;
            /* Flex layout to organize sidebar vertically */
            display: flex !important;
            /* Stack elements vertically */
            flex-direction: column !important;
            /* Extend to near full screen height so footer sticks to bottom */
            min-height: calc(100vh - 2rem) !important;
        }

        /* Sidebar collapse toggle button icon styling */
        button[data-testid="stSidebarCollapseButton"] {
            /* Color the collapse button in muted slate */
            color: #94A3B8 !important;
            /* Transparent background */
            background: transparent !important;
        }

        /* Hover effect on sidebar collapse button */
        button[data-testid="stSidebarCollapseButton"]:hover {
            /* Highlight collapse button icon in white on hover */
            color: #FFFFFF !important;
            /* Soft translucent hover background */
            background: rgba(255, 255, 255, 0.08) !important;
        }

        /* Enforce light text contrast for paragraphs and labels in the dark sidebar */
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            /* Set text color to near-white */
            color: #F8FAFC !important;
        }

        /* ------------------- MODERN RED SELECTION BUBBLES IN SIDEBAR ------------------- */
        /* Style the outer circular selection bubble container */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child,
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child {
            /* Fixed width for circular bubble */
            width: 18px !important;
            /* Fixed height for circular bubble */
            height: 18px !important;
            /* Minimum width to prevent shrinking */
            min-width: 18px !important;
            /* Minimum height to prevent shrinking */
            min-height: 18px !important;
            /* Perfect circular boundary */
            border-radius: 50% !important;
            /* Dark red boundary for unselected bubble */
            border: 2px solid #7F1D1D !important;
            /* Dark burgundy interior fill */
            background-color: rgba(23, 7, 7, 0.8) !important;
            /* Flex layout to center inner dot */
            display: flex !important;
            /* Center dot horizontally */
            align-items: center !important;
            /* Center dot vertically */
            justify-content: center !important;
            /* Spacing between bubble and menu text */
            margin-right: 12px !important;
            /* Left margin alignment */
            margin-left: 2px !important;
            /* Smooth color and shadow transitions */
            transition: all 0.18s ease !important;
            /* Proper box-sizing */
            box-sizing: border-box !important;
        }

        /* Hover effect on unselected bubble */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover [data-baseweb="radio"] > div:first-child,
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover > div:first-child {
            /* Glow bubble border to soft coral red on hover */
            border-color: #F87171 !important;
            /* Soft ambient glow shadow around bubble */
            box-shadow: 0 0 8px rgba(248, 113, 113, 0.45) !important;
        }

        /* Active / Selected circular bubble */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) [data-baseweb="radio"] > div:first-child,
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) > div:first-child {
            /* Vibrant brand red border for selected bubble */
            border-color: #DC2626 !important;
            /* Solid brand red fill for selected bubble */
            background-color: #DC2626 !important;
            /* High-end glowing red shadow around the selected bubble */
            box-shadow: 0 0 10px rgba(220, 38, 38, 0.7) !important;
        }

        /* Inner white dot inside the active selection bubble */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) [data-baseweb="radio"] > div:first-child > div,
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) > div:first-child > div {
            /* 6px inner dot width */
            width: 6px !important;
            /* 6px inner dot height */
            height: 6px !important;
            /* Round shape for inner dot */
            border-radius: 50% !important;
            /* Pure white fill for inner dot */
            background-color: #FFFFFF !important;
        }

        /* Hide the raw native HTML radio input to keep custom styling crisp */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label input[type="radio"] {
            /* Transparent opacity */
            opacity: 0 !important;
            /* Zero width */
            width: 0 !important;
            /* Absolute off-screen position */
            position: absolute !important;
        }

        /* ------------------- SIDEBAR NAVIGATION TILES ------------------- */
        /* Style sidebar radio navigation buttons into interactive navigation tiles */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {
            /* Full width nav item */
            width: 100% !important;
            /* Rounded corners for menu capsule */
            border-radius: 12px !important;
            /* Padding around each menu option */
            padding: 10px 14px !important;
            /* Vertical spacing between menu options */
            margin-bottom: 6px !important;
            /* Smooth transition on hover and selection */
            transition: all 0.16s ease !important;
            /* Default transparent border */
            border: 1px solid transparent !important;
            /* Pointer cursor on hover */
            cursor: pointer !important;
            /* Flex layout to align items cleanly */
            display: flex !important;
            /* Center elements vertically */
            align-items: center !important;
            /* Transparent background by default */
            background-color: transparent !important;
            /* Proper box-sizing */
            box-sizing: border-box !important;
        }

        /* Sidebar nav label text color */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label p {
            /* Muted slate text for unselected navigation options */
            color: #94A3B8 !important;
            /* Standard navigation font size */
            font-size: 0.94rem !important;
            /* Medium font weight for legibility */
            font-weight: 500 !important;
            /* Margin reset */
            margin: 0 !important;
            /* Padding reset */
            padding: 0 !important;
            /* Smooth transition for text color */
            transition: color 0.15s ease !important;
        }

        /* Hover animation for inactive sidebar menu options */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
            /* Soft white background tint on hover */
            background-color: rgba(255, 255, 255, 0.06) !important;
            /* Slight horizontal slide on hover */
            transform: translateX(3px) !important;
        }

        /* Light up text on hover */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover p {
            /* White text on hover */
            color: #FFFFFF !important;
        }

        /* Active sidebar navigation item highlighting with sleek left border */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
            /* Gradient background highlight for active menu item */
            background: linear-gradient(90deg, rgba(220, 38, 38, 0.25) 0%, rgba(220, 38, 38, 0.05) 100%) !important;
            /* Soft red border around active item */
            border: 1px solid rgba(220, 38, 38, 0.35) !important;
            /* Vibrant crimson red accent line on left border */
            border-left: 3px solid #DC2626 !important;
        }

        /* Active menu option text styling */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
            /* Crisp white text for active tab */
            color: #FFFFFF !important;
            /* Bold font weight for active tab */
            font-weight: 700 !important;
        }

        /* ------------------- MODERN RED BUTTON ELEVATION ------------------- */
        /* Transform primary action buttons into modern red gradient capsules with smooth shadows */
        .stButton > button[kind="primary"], .stButton > button {
            /* High-end brand red gradient background */
            background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%) !important;
            /* White text inside button */
            color: #FFFFFF !important;
            /* Capsule pill shape border radius */
            border-radius: 9999px !important;
            /* Bold button text weight */
            font-weight: 600 !important;
            /* Button font size */
            font-size: 0.88rem !important;
            /* Button padding */
            padding: 0.55rem 1.4rem !important;
            /* Remove default borders */
            border: none !important;
            /* Subtle glow shadow */
            box-shadow: 0 4px 14px rgba(220, 38, 38, 0.3) !important;
            /* Smooth easing transition */
            transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        /* Hover elevation effect for primary buttons */
        .stButton > button:hover {
            /* Darker red gradient on hover */
            background: linear-gradient(135deg, #B91C1C 0%, #991B1B 100%) !important;
            /* White text on hover */
            color: #FFFFFF !important;
            /* Lift up by 2px on hover */
            transform: translateY(-2px) !important;
            /* Deepen red shadow on hover */
            box-shadow: 0 8px 20px rgba(220, 38, 38, 0.45) !important;
        }

        /* Active click compression effect for tactile feedback */
        .stButton > button:active {
            /* Reset vertical lift on click */
            transform: translateY(0px) !important;
        }

        /* ------------------- MODERN CARDS & EXPANDERS ------------------- */
        /* Enhance Streamlit expander containers to render as floating cards */
        div[data-testid="stExpander"] {
            /* Use theme secondary background color */
            background-color: var(--secondary-background-color) !important;
            /* Subtle 1px card border */
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            /* Rounded card corners */
            border-radius: 14px !important;
            /* Soft ambient card shadow */
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
            /* Smooth transition on hover */
            transition: all 0.18s ease !important;
            /* Spacing below expander card */
            margin-bottom: 12px !important;
            /* Prevent content overflow */
            overflow: hidden !important;
        }

        /* Expander header summary row */
        div[data-testid="stExpander"] summary {
            /* Padding inside expander header */
            padding: 12px 16px !important;
            /* Rounded corners */
            border-radius: 14px !important;
        }

        /* Expander header text */
        div[data-testid="stExpander"] summary p {
            /* Semibold title */
            font-weight: 600 !important;
            /* Font size */
            font-size: 0.95rem !important;
        }

        /* Expander chevron arrow icon spacing */
        div[data-testid="stExpander"] summary [data-testid="stIconMaterial"] {
            /* Ensure proper icon font */
            font-family: 'Material Symbols Rounded', 'Material Icons' !important;
            /* Spacing between arrow icon and title text */
            margin-right: 8px !important;
        }

        /* Hover lift and glow effect for expander cards */
        div[data-testid="stExpander"]:hover {
            /* Brand red border tint on hover */
            border-color: rgba(220, 38, 38, 0.45) !important;
            /* Elevated shadow on hover */
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06) !important;
        }

        /* ------------------- SEGMENTED PILL TABS ------------------- */
        /* Transform tab list into a modern segmented bar */
        div[data-baseweb="tab-list"] {
            gap: 6px !important;
            background-color: var(--secondary-background-color) !important;
            padding: 5px !important;
            border-radius: 12px !important;
            border: 1px solid rgba(148, 163, 184, 0.15) !important;
            margin-bottom: 22px !important;
        }

        /* Individual tab pill styling */
        button[data-baseweb="tab"] {
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 8px 18px !important;
            border: none !important;
            transition: all 0.15s ease !important;
        }

        /* Selected active tab styling with brand red accent background */
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #DC2626 !important;
            color: #FFFFFF !important;
            box-shadow: 0 2px 8px rgba(220, 38, 38, 0.35) !important;
        }

        /* Remove default flat underline bar underneath tabs */
        div[data-baseweb="tab-highlight"] {
            display: none !important;
        }

        /* ------------------- FORM INPUTS & SELECTBOXES ------------------- */
        /* Add modern rounded borders and transitions to form inputs */
        div[data-baseweb="input"], div[data-baseweb="select"] {
            border-radius: 10px !important;
            transition: border-color 0.15s ease !important;
        }

        /* ------------------- PAGE TITLES & HEADINGS ------------------- */
        /* Clean typography hierarchy for primary headings */
        h1 {
            font-weight: 800 !important;
            letter-spacing: -0.025em !important;
            font-size: 1.85rem !important;
            margin-bottom: 0.4rem !important;
        }

        h2, h3 {
            font-weight: 700 !important;
            letter-spacing: -0.015em !important;
        }
    </style>
    """,
    unsafe_allow_html=True # Permit custom CSS tags to be parsed directly by the browser
)


# ============================================================
#                    INITIAL SEED DATA
# ============================================================

# Check session state version (v8) to ensure seed data populates cleanly once per session
if st.session_state.get("data_seed_version") != 8:

    # 1. Reset and initialize academic Programs list (Courses requested by institution)
    Program.programs_list = [] # Clear any existing in-memory programs list
    Program.trash_list = []    # Clear any existing programs trash bin

    # Seed Program 1: DSA - Data Scientist And Analyst curriculum (6 months, 70000/-)
    p_dsa = Program(
        "P201", "DSA - Data Scientist And Analyst", "Tech", "6 months",
        70000, "Vyshak"
    )

    # Seed Program 2: HR - Human Resource curriculum (4 months, 50000/-)
    p_hr = Program(
        "P202", "HR - Human Resource", "Management", "4 months",
        50000, "Diya"
    )

    # Seed Program 3: FAD - Fashion Design curriculum (6 months, 80000/-)
    p_fad = Program(
        "P203", "FAD - Fashion Design", "Design", "6 months",
        80000, "Shahma C.P"
    )

    # Seed Program 4: AI - Agent K curriculum (6 months, 80000/-)
    p_ai = Program(
        "P204", "AI - Agent K", "Tech", "6 months",
        80000, "Rinshin"
    )

    # Seed Program 5: Spoken English curriculum (3 months, 25000/- with mentor Ashraf)
    p_se = Program(
        "P205", "Spoken English", "Language", "3 months",
        25000, "Ashraf"
    )

    # 2. Reset and initialize Staff members (Configured with newly designated faculty & HR team)
    Staff.staff_list = [] # Clear any existing staff records
    Staff.trash_list = [] # Clear any existing staff trash records

    # Academic Faculty Members — Teachers & Mentors
    t1 = Teacher("S101", "Vyshak", "9999900001", "vyshak@sos.com", "DSA - Data Scientist And Analyst", date(2022, 6, 1))
    t2 = Teacher("S102", "Shahma C.P", "9999900002", "shahma@sos.com", "FAD - Fashion Design", date(2023, 2, 15))
    t3 = Teacher("S103", "Rinshin", "9999900003", "rinshin@sos.com", "AI - Agent K", date(2021, 11, 10))
    t4 = Teacher("S104", "Ashraf", "9999900004", "ashraf@sos.com", "Spoken English", date(2023, 5, 20))
    t5 = Teacher("S105", "Diya", "9999900005", "diya@sos.com", "HR - Human Resource", date(2022, 9, 1))

    # HR, Student Coordination, Media, and Accounts personnel
    sc1 = StudentCoordinator("S106", "Soniya", "9999900006", "soniya@sos.com", "HR & Admissions", date(2023, 7, 12))
    sc2 = StudentCoordinator("S107", "Rahul Nair", "9999900007", "rahul@sos.com", "Admissions", date(2023, 1, 15))
    mt1 = MediaTeam("S108", "Fathima K", "9999900008", "fathima@sos.com", "Media", date(2023, 3, 10))
    ac1 = Accountant("S109", "Suresh Babu", "9999900009", "suresh@sos.com", "Accounts", date(2021, 8, 20))

    # Seed baseline attendance for staff members across recent dates
    for staff_member in Staff.staff_list:
        staff_member.mark_attendance(date(2026, 9, 20), True)
        staff_member.mark_attendance(date(2026, 9, 21), staff_member.staff_id not in ["S102", "S106"])

    # 3. Reset and initialize Students (Distributed across all 5 programs)
    Student.students_list = [] # Clear any existing student records
    Student.trash_list = []    # Clear any existing student trash records

    # --- Program 1: DSA - Data Scientist And Analyst (Teacher: Vyshak, Fee: 70,000) ---
    s1 = Student("ST301", "Marco Joseph", "9888800001", "marco@sos.com", 19, "Calicut")
    s1.enroll("DSA - Data Scientist And Analyst", "Batch A", "Vyshak", date(2026, 1, 5), 70000)
    s1.pay_fee(70000, "UPI / GPay")
    s1.mark_attendance(date(2026, 9, 20), True)
    s1.mark_attendance(date(2026, 9, 21), True)

    s2 = Student("ST302", "Ayesha R", "9888800002", "ayesha@sos.com", 21, "Kochi")
    s2.enroll("DSA - Data Scientist And Analyst", "Batch A", "Vyshak", date(2026, 1, 8), 70000)
    s2.pay_fee(40000, "Net Banking")
    s2.mark_attendance(date(2026, 9, 20), True)
    s2.mark_attendance(date(2026, 9, 21), False)

    s3 = Student("ST303", "Bilal Ahmed", "9888800003", "bilal@sos.com", 22, "Malappuram")
    s3.enroll("DSA - Data Scientist And Analyst", "Batch B", "Vyshak", date(2026, 1, 10), 70000)
    s3.mark_attendance(date(2026, 9, 20), True)
    s3.mark_attendance(date(2026, 9, 21), True)

    # --- Program 2: HR - Human Resource (Teacher: Diya, Fee: 50,000) ---
    s4 = Student("ST304", "Devika Suresh", "9888800004", "devika@sos.com", 20, "Calicut")
    s4.enroll("HR - Human Resource", "Batch A", "Diya", date(2026, 1, 12), 50000)
    s4.pay_fee(50000, "Debit / Credit Card")
    s4.mark_attendance(date(2026, 9, 20), False)
    s4.mark_attendance(date(2026, 9, 21), True)

    s5 = Student("ST305", "Farhan Ali", "9888800005", "farhan@sos.com", 23, "Kannur")
    s5.enroll("HR - Human Resource", "Batch A", "Diya", date(2026, 2, 1), 50000)
    s5.pay_fee(25000, "Cash")
    s5.mark_attendance(date(2026, 9, 20), True)
    s5.mark_attendance(date(2026, 9, 21), True)

    s6 = Student("ST306", "Gopika Mohan", "9888800006", "gopika@sos.com", 20, "Thrissur")
    s6.enroll("HR - Human Resource", "Batch B", "Diya", date(2026, 2, 3), 50000)
    s6.pay_fee(50000, "UPI / GPay")
    s6.mark_attendance(date(2026, 9, 20), True)
    s6.mark_attendance(date(2026, 9, 21), True)

    # --- Program 3: FAD - Fashion Design (Teacher: Shahma C.P, Fee: 80,000) ---
    s7 = Student("ST307", "Harish Kumar", "9888800007", "harish@sos.com", 22, "Palakkad")
    s7.enroll("FAD - Fashion Design", "Batch A", "Shahma C.P", date(2026, 2, 5), 80000)
    s7.pay_fee(45000, "Cash")
    s7.mark_attendance(date(2026, 9, 20), False)
    s7.mark_attendance(date(2026, 9, 21), True)

    s8 = Student("ST308", "Ishaan Verma", "9888800008", "ishaan@sos.com", 24, "Calicut")
    s8.enroll("FAD - Fashion Design", "Batch A", "Shahma C.P", date(2026, 2, 7), 80000)
    s8.pay_fee(80000, "UPI / GPay")
    s8.mark_attendance(date(2026, 9, 20), True)
    s8.mark_attendance(date(2026, 9, 21), True)

    s9 = Student("ST309", "Jaseela Banu", "9888800009", "jaseela@sos.com", 21, "Wayanad")
    s9.enroll("FAD - Fashion Design", "Batch B", "Shahma C.P", date(2026, 1, 10), 80000)
    s9.mark_attendance(date(2026, 9, 20), True)
    s9.mark_attendance(date(2026, 9, 21), True)

    # --- Program 4: AI - Agent K (Teacher: Rinshin, Fee: 80,000) ---
    s10 = Student("ST310", "Kevin Thomas", "9888800010", "kevin@sos.com", 22, "Kottayam")
    s10.enroll("AI - Agent K", "Batch A", "Rinshin", date(2026, 1, 11), 80000)
    s10.pay_fee(50000, "Cash")
    s10.mark_attendance(date(2026, 9, 20), True)
    s10.mark_attendance(date(2026, 9, 21), False)

    s11 = Student("ST311", "Lakshmi Priya", "9888800011", "lakshmi@sos.com", 20, "Calicut")
    s11.enroll("AI - Agent K", "Batch A", "Rinshin", date(2026, 1, 12), 80000)
    s11.pay_fee(80000, "Debit / Credit Card")
    s11.mark_attendance(date(2026, 9, 20), True)
    s11.mark_attendance(date(2026, 9, 21), True)

    s12 = Student("ST312", "Mohammed Rayan", "9888800012", "rayan@sos.com", 23, "Malappuram")
    s12.enroll("AI - Agent K", "Batch B", "Rinshin", date(2026, 1, 15), 80000)
    s12.pay_fee(80000, "UPI / GPay")
    s12.mark_attendance(date(2026, 9, 20), False)
    s12.mark_attendance(date(2026, 9, 21), True)

    # --- Program 5: Spoken English (Mentor: Ashraf, Fee: 25,000) ---
    s13 = Student("ST313", "Nihal Basheer", "9888800013", "nihal@sos.com", 21, "Calicut")
    s13.enroll("Spoken English", "Batch A", "Ashraf", date(2026, 2, 10), 25000)
    s13.pay_fee(25000, "UPI / GPay")
    s13.mark_attendance(date(2026, 9, 20), True)
    s13.mark_attendance(date(2026, 9, 21), True)

    s14 = Student("ST314", "Ranya Fathima", "9888800014", "ranya@sos.com", 19, "Kozhikode")
    s14.enroll("Spoken English", "Batch A", "Ashraf", date(2026, 2, 12), 25000)
    s14.pay_fee(15000, "Cash")
    s14.mark_attendance(date(2026, 9, 20), True)
    s14.mark_attendance(date(2026, 9, 21), True)

    # 4. Campus Notices — Seed ONLY 1 single sample notice as specifically requested
    Notice.notices_list = [] # Ensure notices repository starts clean
    Notice(
        "N101",                                      # Identifier for this sample notice
        "🎉 2026 Batch Orientation & Welcome Day",    # Headline of the announcement
        "Event",                                     # Category tag for styling
        "The official orientation session for all new batches will be held this Saturday at 10:00 AM in the Main Seminar Hall.", # Announcement body
        date(2026, 9, 22),                           # Date posted
        "Director"                                   # Issuer of the announcement
    )

    # Store seed version flag 8 in session state so re-running the script preserves updated data
    st.session_state.data_seed_version = 8


# Ensure shared SOSActivities coordination instance exists in Streamlit session memory
if "activities" not in st.session_state:
    st.session_state.activities = SOSActivities() # Instantiate primary activity coordinator


# ============================================================
#                    HIGH-END MODERN SIDEBAR
# ============================================================

# Fetch base64-encoded logo string for embedding into our modern sidebar header
sidebar_logo_b64 = get_logo_as_base64()

# Construct HTML for sidebar header branding
if sidebar_logo_b64:
    sidebar_brand_html = (
        f'<div style="display: flex; align-items: center; gap: 12px; padding: 14px 6px 18px 6px; '
        f'border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 16px;">'
        f'<img src="data:image/png;base64,{sidebar_logo_b64}" '
        f'style="height: 42px; width: 42px; object-fit: contain; border-radius: 10px; background: #FFFFFF; padding: 4px;">'
        # Text wrapper for institute title
        f'<div>'
        # Prominent bold brand title: SOS - School Of Skills
        f'<div style="font-weight: 800; font-size: 1.05rem; color: #FFFFFF; letter-spacing: -0.01em;">SOS - School Of Skills</div>'
        # Close text wrapper
        f'</div>'
        f'</div>'
    )
else:
    sidebar_brand_html = (
        f'<div style="display: flex; align-items: center; gap: 12px; padding: 14px 6px 18px 6px; '
        f'border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 16px;">'
        f'<div style="height: 42px; width: 42px; border-radius: 10px; background: #4F46E5; '
        f'display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">🏫</div>'
        # Text wrapper for fallback institute title
        f'<div>'
        # Prominent bold brand title: SOS - School Of Skills
        f'<div style="font-weight: 800; font-size: 1.05rem; color: #FFFFFF; letter-spacing: -0.01em;">SOS - School Of Skills</div>'
        # Close text wrapper
        f'</div>'
        f'</div>'
    )

# Render the styled brand header in the sidebar
st.sidebar.markdown(sidebar_brand_html, unsafe_allow_html=True)

# Render navigation section category divider
st.sidebar.markdown(
    '<div style="font-size: 0.68rem; font-weight: 700; color: #64748B; text-transform: uppercase; '
    'letter-spacing: 0.08em; padding: 0 8px 6px 8px;">Workspace Modules</div>',
    unsafe_allow_html=True
)

# Render modern radio button navigation menu with concise, elegant page titles
menu = st.sidebar.radio(
    "Select Module",
    # List of all primary application modules accessible in the sidebar
    [
        "🏠 Home",
        "🏫 School Details",
        "👥 Staff",
        "🎓 Programs",
        "👨‍🎓 Students",
        "✅ Attendance",
        "💰 Fees",
        "📊 Analytics"
    ],
    label_visibility="collapsed" # Hide the default label to keep layout ultra-clean
)

# Build modern Admin Profile footer tile pinned to the bottom of the sidebar via auto top margin
admin_profile_html = (
    # Container with margin-top auto to push tile to bottom of the flex sidebar column
    f'<div style="margin-top: auto; padding-top: 24px; '
    # Subtle top border line separating navigation items from the admin profile
    f'border-top: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 12px; '
    # Flex container aligning avatar circle and status labels horizontally
    f'display: flex; align-items: center; gap: 12px; padding-left: 6px;">'
    # Avatar badge with brand red gradient background and bold white initials
    f'<div style="width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%); '
    # Centering avatar initials inside circle
    f'display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.88rem; color: white; flex-shrink: 0;">AD</div>'
    # Wrapper div for admin name and status tag
    f'<div>'
    # Bold admin user label
    f'<div style="font-size: 0.85rem; font-weight: 700; color: #F8FAFC;">Admin Desk</div>'
    # Green live status indicator tag
    f'<div style="font-size: 0.72rem; color: #10B981; display: flex; align-items: center; gap: 4px;">'
    # Green glowing status indicator dot
    f'<span style="height: 6px; width: 6px; border-radius: 50%; background: #10B981; display: inline-block;"></span> Online &bull; Active'
    # Close status tag
    f'</div>'
    # Close text wrapper
    f'</div>'
    # Close main tile container
    f'</div>'
)
# Output the pinned admin profile tile into the sidebar
st.sidebar.markdown(admin_profile_html, unsafe_allow_html=True)


# ============================================================
#                         HOME PAGE
# ============================================================

if menu == "🏠 Home":

    # Fetch Base64 logo for the Hero Bar
    logo_base64 = get_logo_as_base64()

    # Build image tag if available, or fall back to sleek graphic badge
    if logo_base64:
        hero_logo = (
            f'<img src="data:image/png;base64,{logo_base64}" '
            f'style="height: 60px; width: 60px; object-fit: contain; border-radius: 12px; background: white; padding: 6px; '
            f'box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);">'
        )
    else:
        hero_logo = (
            '<div style="height: 60px; width: 60px; border-radius: 12px; '
            'background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%); display: flex; align-items: center; '
            'justify-content: center; font-size: 1.8rem; box-shadow: 0 4px 14px rgba(220, 38, 38, 0.3);">🏫</div>'
        )

    # Render a high-end brand Red & White Top App Bar with live session indicator
    hero_banner_html = (
        f'<div style="background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%); '
        f'border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 18px; padding: 24px 30px; '
        f'display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; '
        f'box-shadow: 0 10px 25px rgba(220, 38, 38, 0.25);">'
        f'<div style="display: flex; align-items: center; gap: 20px;">'
        f'{hero_logo}'
        # Container wrapping the institution title text
        f'<div>'
        # Display clean prominent title: SOS - School Of Skills in pure white
        f'<div style="color: #FFFFFF; font-size: 1.65rem; font-weight: 800; letter-spacing: -0.02em;">SOS - School Of Skills</div>'
        # Close title container div
        f'</div>'
        f'</div>'
        f'<div style="display: flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.18); '
        f'border: 1px solid rgba(255, 255, 255, 0.4); padding: 8px 14px; border-radius: 9999px;">'
        f'<span style="height: 8px; width: 8px; border-radius: 50%; background: #FFFFFF;"></span>'
        f'<span style="color: #FFFFFF; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.02em;">2026 SESSION LIVE</span>'
        f'</div>'
        f'</div>'
    )
    st.markdown(hero_banner_html, unsafe_allow_html=True)

    # ---------------- Calculate Global Analytics Metrics ----------------
    total_students = len(Student.students_list) # Count active student records
    total_staff = len(Staff.staff_list)       # Count active staff records
    total_programs = len(Program.programs_list) # Count active academic programs

    # Sum total tuition fee revenue collected across all students
    total_fees_collected = 0
    for student in Student.students_list:
        total_fees_collected += student.student_details()["Fees Paid"]

    # ---------------- High-End 4-Column KPI Stat Cards ----------------
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    with col_kpi1:
        # Total Students Metric Card with Brand Red Accent
        kpi_card("Total Students", total_students, "Active Enrolled", "👨‍🎓", "#DC2626")

    with col_kpi2:
        # Total Faculty & Staff Metric Card with Teal Accent
        kpi_card("Faculty & Staff", total_staff, "Academics & Ops", "👥", "#0EA5E9")

    with col_kpi3:
        # Total Programs Metric Card with Amber Accent
        kpi_card("Active Programs", total_programs, "Live Curriculums", "🎓", "#F59E0B")

    with col_kpi4:
        # Total Revenue Collected Metric Card with Emerald Accent
        kpi_card("Fees Collected", f"₹{total_fees_collected:,}", "Audited YTD", "💳", "#10B981")

    # Spacing divider between metric cards and main dashboard sections
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # ---------------- Dashboard Content: Active Programs & Campus Notice Board ----------------
    col_programs, col_notices = st.columns([1, 1])

    with col_programs:
        # Section header for active educational programs
        st.subheader("🎓 Active Programs")

        # Check if programs have been created in the system
        if Program.programs_list:
            for program in Program.programs_list:
                # Calculate enrolled count badge
                enrolled_count = program.enrolled_count()
                # Create an enrolled learner count pill badge for this curriculum with red brand colors
                count_pill = badge(f"{enrolled_count} Students", "rgba(220, 38, 38, 0.12)", "#DC2626", "rgba(220, 38, 38, 0.25)")
                # Generate category pill badge for this academic program
                dept_pill = badge(program.category, "rgba(148, 163, 184, 0.12)", "#64748B")

                # Build clean HTML card for each curriculum
                prog_card_html = (
                    f'<div style="background-color: var(--secondary-background-color); '
                    f'border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 14px; '
                    f'padding: 16px 20px; margin-bottom: 12px; transition: transform 0.15s ease; '
                    f'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);">'
                    f'<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">'
                    f'<div>'
                    f'<div style="font-weight: 700; font-size: 1.02rem;">{program.program_name}</div>'
                    f'<div style="font-size: 0.8rem; opacity: 0.72; margin-top: 2px;">Faculty Lead: <strong>{program.teacher}</strong></div>'
                    f'</div>'
                    f'{count_pill}'
                    f'</div>'
                    f'<div style="display: flex; gap: 8px; align-items: center; margin-top: 10px; font-size: 0.8rem; opacity: 0.8;">'
                    f'<span>⏱️ {program.duration}</span> &bull; <span>💵 ₹{program.fees:,}</span> &bull; {dept_pill}'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(prog_card_html, unsafe_allow_html=True)
        else:
            st.warning("No active programs found. Create your first program in the Programs tab.")

    with col_notices:
        # Section header for campus bulletin and announcements
        st.subheader("📢 Campus Notice Board")

        # Retrieve notices list from domain class
        all_notices = Notice.get_all_notices()

        # Collapsible card container for posting new announcements
        with st.expander("➕ Post New Notice"):
            n_title = st.text_input("Notice Title", placeholder="e.g. Workshop on Generative AI", key="home_notice_title")
            col_nc1, col_nc2 = st.columns(2)
            with col_nc1:
                n_cat = st.selectbox("Category", ["General", "Urgent", "Event", "Exam"], key="home_notice_cat")
            with col_nc2:
                n_by = st.text_input("Issued By", value="Administration", key="home_notice_by")
            n_content = st.text_area("Announcement Body", placeholder="Enter announcement text...", key="home_notice_content")

            # Action button to record and publish the announcement
            if st.button("Publish Announcement", type="primary", key="btn_publish_home_notice"):
                if n_title and n_content:
                    n_id = f"N{random.randint(100, 999)}" # Generate unique notice ID
                    Notice(n_id, n_title, n_cat, n_content, date.today(), n_by) # Instantiate domain model
                    st.success("Notice published successfully!")
                    st.rerun() # Refresh page to show newly published notice
                else:
                    st.warning("Please provide both a notice title and details.")

        # If no announcements exist, display informational notification
        if not all_notices:
            st.info("No active notices currently posted.")
        else:
            # Render notice cards for all active announcements
            for n in list(all_notices):
                # Retrieve category pill styling or fall back to neutral
                c_style = NOTICE_CATEGORY_STYLES.get(n.category, {"bg": "#EEF2FF", "text": "#4F46E5", "border": "transparent"})
                cat_badge_html = badge(n.category, c_style["bg"], c_style["text"], c_style["border"])
                clean_content = n.content.replace("\n", "<br>") # Clean newlines into HTML breaks

                # Build clean HTML notice card without leading indentation spaces
                notice_card_html = (
                    f'<div style="background-color: var(--secondary-background-color); '
                    f'border: 1px solid rgba(148, 163, 184, 0.2); border-left: 4px solid {c_style["text"]}; '
                    f'border-radius: 12px; padding: 16px 18px; margin-bottom: 10px; '
                    f'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);">'
                    f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
                    f'<span style="font-weight: 700; font-size: 0.98rem;">{n.title}</span>'
                    f'{cat_badge_html}'
                    f'</div>'
                    f'<div style="font-size: 0.88rem; line-height: 1.5; margin-bottom: 10px; opacity: 0.9;">{clean_content}</div>'
                    f'<div style="font-size: 0.76rem; opacity: 0.65; display: flex; justify-content: space-between; align-items: center;">'
                    f'<span>📅 {n.posted_date} &bull; ✍️ {n.posted_by}</span>'
                    f'<span style="font-family: monospace; font-size: 0.72rem; opacity: 0.7;">ID: #{n.notice_id}</span>'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(notice_card_html, unsafe_allow_html=True)

                # Modern inline delete action button
                col_del_n, _ = st.columns([1, 4])
                with col_del_n:
                    if st.button("🗑️ Delete", key=f"del_notice_{n.notice_id}"):
                        Notice.delete_notice(n.notice_id) # Remove notice from master list
                        st.rerun() # Refresh to update dashboard immediately


# ============================================================
#                     SCHOOL DETAILS
# ============================================================

elif menu == "🏫 School Details":

    # Primary page title
    st.title("🏫 Campus Profile & Accreditation")
    st.caption("Official institution credentials, campus address, and affiliation parameters.")

    # Retrieve official school details from SOS domain model
    school = SOS()
    details = school.school_details()

    # Render a hero card for the institution profile
    st.markdown(
        f'<div style="background-color: var(--secondary-background-color); '
        f'border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 16px; padding: 24px; '
        f'margin-bottom: 20px; box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);">'
        # Campus institution icon container with brand red background
        f'<div style="width: 52px; height: 52px; border-radius: 12px; background: rgba(220, 38, 38, 0.12); '
        # Align icon center
        f'display: flex; align-items: center; justify-content: center; font-size: 1.8rem;">🏛️</div>'
        f'<div>'
        f'<div style="font-size: 1.35rem; font-weight: 800;">{details.get("School Name", "School of Skills")}</div>'
        f'<div style="font-size: 0.85rem; opacity: 0.75;">Established: {details.get("Established", 2026)} &bull; Affiliation: {details.get("Affiliation", "Kerala State Skill Development")}</div>'
        f'</div>'
        f'</div>'
        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 0.92rem;">'
        f'<div><strong>📍 Campus Location:</strong> {details.get("Address", "Calicut, Kerala")}</div>'
        f'<div><strong>📞 Primary Hotline:</strong> {details.get("Phone", "+91 9876543210")}</div>'
        f'<div><strong>✉️ Official Email:</strong> {details.get("Email", "info@schoolofskills.com")}</div>'
        f'<div><strong>🌐 Official Website:</strong> {details.get("Website", "https://schoolofskills.com")}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ============================================================
#                         STAFF
# ============================================================

elif menu == "👥 Staff":

    # Page header with title and subtitle
    st.title("👥 Faculty & Operations Team")
    st.caption("Manage teachers, academic coordinators, media producers, and finance accountants.")

    # Modern segmented tabs for viewing, adding, and managing trash
    tab_view, tab_add, tab_trash = st.tabs(
        ["📋 Faculty Directory", "➕ Onboard New Staff", "🗑️ Recycle Bin"]
    )

    # ---------------- TAB 1: Faculty Directory ----------------
    with tab_view:

        # Search bar and role filter
        col_s1, col_s2 = st.columns([2, 1])
        with col_s1:
            search_name = st.text_input("🔍 Search Staff by Name", placeholder="Type a staff member's name...", key="staff_search")
        with col_s2:
            role_filter = st.selectbox("Filter by Role", ["All Roles", "Teacher", "Student Coordinator", "Media Team", "Accountant"], key="filter_staff_role")

        # Determine which staff to display based on search and role filters
        if search_name:
            displayed_staff = Staff.search_staff(search_name)
        else:
            displayed_staff = Staff.display_all_staff()

        if role_filter != "All Roles":
            displayed_staff = [s for s in displayed_staff if s.role == role_filter]

        st.caption(f"Showing **{len(displayed_staff)}** of **{len(Staff.staff_list)}** staff members")

        if displayed_staff:
            for staff in list(displayed_staff):
                r_style = ROLE_BADGE_STYLES.get(staff.role, {"bg": "#EEF2FF", "text": "#4F46E5", "border": "transparent"})
                role_pill = badge(staff.role, r_style["bg"], r_style["text"], r_style["border"])

                with st.expander(f"{staff.name} — {staff.role} ({staff.department})"):
                    col_det, col_act = st.columns([3, 1])
                    with col_det:
                        render_details(staff.staff_details())
                    with col_act:
                        # Move to trash soft-delete action button
                        if st.button("🗑️ Move to Trash", key=f"trash_staff_{staff.staff_id}"):
                            staff.move_to_trash()
                            st.rerun()
        else:
            st.warning("No staff found matching the filter criteria.")

    # ---------------- TAB 2: Onboard New Staff ----------------
    with tab_add:
        st.subheader("➕ Onboard New Staff Member")

        col_stf1, col_stf2 = st.columns(2)
        with col_stf1:
            staff_id = st.text_input("Staff ID", placeholder="e.g. S115")
            name = st.text_input("Full Name", placeholder="e.g. Dr. Maya Pillai")
            role = st.selectbox("Functional Role", ["Teacher", "Student Coordinator", "Media Team", "Accountant"])

        with col_stf2:
            phone = st.text_input("Contact Number", placeholder="e.g. 9876543210")
            email = st.text_input("Work Email", placeholder="e.g. maya@sos.com")
            program_names = [p.program_name for p in Program.programs_list]
            if program_names:
                department = st.selectbox("Department / Subject Area", program_names)
            else:
                department = st.text_input("Department / Subject Area", placeholder="Tech / Business")

        joining_date = st.date_input("Joining Date", value=date.today())

        if st.button("Register Staff Member", type="primary"):
            if not staff_id or not name or not phone or not email:
                st.warning("Please fill all required fields before submitting.")
            else:
                duplicate = any(s.staff_id == staff_id for s in Staff.staff_list)
                if duplicate:
                    st.error("A staff member with this Staff ID already exists.")
                else:
                    if role == "Teacher":
                        Teacher(staff_id, name, phone, email, department, joining_date)
                    elif role == "Student Coordinator":
                        StudentCoordinator(staff_id, name, phone, email, department, joining_date)
                    elif role == "Media Team":
                        MediaTeam(staff_id, name, phone, email, department, joining_date)
                    else:
                        Accountant(staff_id, name, phone, email, department, joining_date)
                    st.success(f"Staff member '{name}' onboarded successfully as {role}!")

    # ---------------- TAB 3: Staff Trash Bin ----------------
    with tab_trash:
        trashed_staff = Staff.display_trash()
        if not trashed_staff:
            st.info("Recycle Bin is currently empty.")
        else:
            for staff in list(trashed_staff):
                with st.expander(f"{staff.name} ({staff.staff_id})"):
                    render_details(staff.staff_details())
                    col_r, col_d = st.columns(2)
                    with col_r:
                        if st.button("♻️ Restore Staff", key=f"restore_staff_{staff.staff_id}"):
                            staff.restore_from_trash()
                            st.rerun()
                    with col_d:
                        if st.button("❌ Permanently Delete", key=f"delete_perm_staff_{staff.staff_id}"):
                            staff.delete_permanently()
                            st.rerun()


# ============================================================
#                         PROGRAMS
# ============================================================

elif menu == "🎓 Programs":

    # Page header with title and subtitle
    st.title("🎓 Academic Programs & Curriculums")
    st.caption("Manage subjects, course fee structures, durations, and assigned faculty leads.")

    # Modern segmented tabs for viewing, adding, and managing trash
    tab_view_prog, tab_add_prog, tab_trash_prog = st.tabs(
        ["📋 Active Programs", "➕ Create Program", "🗑️ Recycle Bin"]
    )

    # ---------------- TAB 1: Active Programs ----------------
    with tab_view_prog:
        if Program.programs_list:
            for program in list(Program.programs_list):
                # Create an expandable card showing program name, program ID, and category
                with st.expander(f"📘 {program.program_name} ({program.program_id}) — {program.category}"):
                    details = program.program_details()
                    render_details(details)

                    # Show enrolled students roster under this program
                    roster = program.enrolled_students()
                    st.markdown("**Enrolled Students:**")
                    if roster:
                        st.write(", ".join(roster))
                    else:
                        st.caption("No students enrolled in this program yet.")

                    # Move program to trash button
                    if st.button("🗑️ Move to Trash", key=f"trash_prog_{program.program_id}"):
                        program.move_to_trash()
                        st.rerun()
        else:
            st.warning("No active academic programs found. Use the Create Program tab to add one.")

    # ---------------- TAB 2: Create Program (No start/end dates) ----------------
    with tab_add_prog:
        st.subheader("➕ Launch a New Academic Program")

        col_pr1, col_pr2 = st.columns(2)
        with col_pr1:
            prog_id = st.text_input("Program ID", placeholder="e.g. P204")
            prog_name = st.text_input("Program Name", placeholder="e.g. Cybersecurity Essentials")
            department = st.selectbox("Department", ["Tech", "Business", "Design", "Media"])

        with col_pr2:
            duration = st.text_input("Curriculum Duration", placeholder="e.g. 3 months")
            fees = st.number_input("Tuition Fee (₹)", min_value=0, step=1000, value=25000)

            # Assign teacher dropdown
            teachers = [s.name for s in Staff.staff_list if s.role == "Teacher"]
            if teachers:
                teacher = st.selectbox("Assigned Faculty Lead", teachers)
            else:
                teacher = st.text_input("Assigned Faculty Lead", placeholder="Faculty Name")

        if st.button("Create Program", type="primary"):
            if not prog_id or not prog_name or not duration:
                st.warning("Please complete all required fields.")
            else:
                duplicate = any(p.program_id == prog_id for p in Program.programs_list)
                if duplicate:
                    st.error("A program with this ID already exists.")
                else:
                    Program(prog_id, prog_name, department, duration, fees, teacher)
                    st.success(f"Program '{prog_name}' created successfully!")

    # ---------------- TAB 3: Programs Trash Bin ----------------
    with tab_trash_prog:
        trashed_programs = Program.display_trash()
        if not trashed_programs:
            st.info("Recycle Bin is currently empty.")
        else:
            for prog in list(trashed_programs):
                with st.expander(f"{prog.program_name} ({prog.program_id})"):
                    render_details(prog.program_details())
                    col_pr_r, col_pr_d = st.columns(2)
                    with col_pr_r:
                        if st.button("♻️ Restore Program", key=f"restore_prog_{prog.program_id}"):
                            prog.restore_from_trash()
                            st.rerun()
                    with col_pr_d:
                        if st.button("❌ Permanently Delete", key=f"delete_perm_prog_{prog.program_id}"):
                            prog.delete_permanently()
                            st.rerun()


# ============================================================
#                        STUDENTS
# ============================================================

elif menu == "👨‍🎓 Students":

    # Page header with title and subtitle
    st.title("👨‍🎓 Student Directory & Enrollment")
    st.caption("Manage student registrations, academic batch assignments, fees, and profiles.")

    # Modern segmented tabs
    tab_view_stu, tab_enroll_stu, tab_trash_stu = st.tabs(
        ["📋 Student Directory", "➕ Enroll New Student", "🗑️ Recycle Bin"]
    )

    # ---------------- TAB 1: Student Directory with Smart Filters ----------------
    with tab_view_stu:

        st.subheader("🎯 Filter Student Directory")
        col_sf1, col_sf2, col_sf3 = st.columns(3)

        with col_sf1:
            filter_prog = st.selectbox(
                "Filter by Program",
                ["All Programs"] + [p.program_name for p in Program.programs_list],
                key="stu_filter_prog"
            )

        with col_sf2:
            all_batches = sorted(list({s.get_batch() for s in Student.students_list if s.get_batch() != "-"}))
            filter_batch = st.selectbox(
                "Filter by Batch / Section",
                ["All Batches"] + all_batches,
                key="stu_filter_batch"
            )

        with col_sf3:
            filter_fee = st.selectbox(
                "Filter by Fee Status",
                ["All Fee Statuses", "Fully Paid", "Partially Paid", "Unpaid"],
                key="stu_filter_fee"
            )

        # Filter students based on selected parameters
        filtered_students = list(Student.students_list)

        if filter_prog != "All Programs":
            filtered_students = [s for s in filtered_students if s.get_program() == filter_prog]

        if filter_batch != "All Batches":
            filtered_students = [s for s in filtered_students if s.get_batch() == filter_batch]

        if filter_fee != "All Fee Statuses":
            filtered_students = [s for s in filtered_students if s.get_fee_status() == filter_fee]

        st.caption(f"Showing **{len(filtered_students)}** of **{len(Student.students_list)}** students")

        if filtered_students:
            for student in filtered_students:
                fee_stat = student.get_fee_status()
                f_style = FEE_STATUS_BADGE_STYLES.get(fee_stat, {"bg": "#EEF2FF", "text": "#4F46E5", "border": "transparent"})
                fee_badge = badge(fee_stat, f_style["bg"], f_style["text"], f_style["border"])

                with st.expander(f"{student.name} ({student.student_id}) — {student.get_program()} [{student.get_batch()}]"):
                    col_sd1, col_sd2 = st.columns([3, 1])
                    with col_sd1:
                        render_details(student.student_details())
                    with col_sd2:
                        if st.button("🗑️ Move to Trash", key=f"trash_student_{student.student_id}"):
                            student.move_to_trash()
                            st.rerun()
        else:
            st.warning("No students found matching the selected filter criteria.")

    # ---------------- TAB 2: Enroll New Student ----------------
    with tab_enroll_stu:
        if not Program.programs_list:
            st.warning("No programs available. Please launch a program before enrolling students.")
        else:
            st.subheader("Learner Profile")
            col_en1, col_en2 = st.columns(2)

            with col_en1:
                student_id = st.text_input("Student ID", placeholder="e.g. ST315")
                name = st.text_input("Student Full Name", placeholder="e.g. Rahul Sharma")
                phone = st.text_input("Phone Number", placeholder="e.g. 9888800015")
                email = st.text_input("Email Address", placeholder="e.g. rahul@sos.com")

            with col_en2:
                age = st.number_input("Age", min_value=14, max_value=80, value=20)
                address = st.text_input("City / Residential Address", placeholder="e.g. Calicut")

                program_options = {f"{p.program_id} - {p.program_name}": p for p in Program.programs_list}
                selected_program_label = st.selectbox("Select Program", list(program_options.keys()))
                program = program_options[selected_program_label]

                batch = st.text_input("Batch / Section", placeholder="e.g. Batch A")
                total_fees = st.number_input("Tuition Fee (₹)", min_value=0, step=1000, value=int(program.fees))

            if st.button("Enroll Student", type="primary"):
                if not student_id or not name or not phone or not batch:
                    st.warning("Please fill all required learner and enrollment fields.")
                else:
                    duplicate = any(s.student_id == student_id for s in Student.students_list)
                    if duplicate:
                        st.error("A student with this ID already exists.")
                    else:
                        new_student = Student(student_id, name, phone, email, age, address)
                        success, message = st.session_state.activities.enroll_student(
                            new_student, program, batch, program.teacher, date.today(), total_fees
                        )
                        if success:
                            st.success(f"Student '{name}' successfully enrolled in {program.program_name}!")
                        else:
                            st.error(message)

    # ---------------- TAB 3: Students Trash Bin ----------------
    with tab_trash_stu:
        trashed_students = Student.display_trash()
        if not trashed_students:
            st.info("Recycle Bin is currently empty.")
        else:
            for student in list(trashed_students):
                with st.expander(f"{student.name} ({student.student_id})"):
                    render_details(student.student_details())
                    col_st_r, col_st_d = st.columns(2)
                    with col_st_r:
                        if st.button("♻️ Restore Student", key=f"restore_student_{student.student_id}"):
                            student.restore_from_trash()
                            st.rerun()
                    with col_st_d:
                        if st.button("❌ Permanently Delete", key=f"delete_perm_student_{student.student_id}"):
                            student.delete_permanently()
                            st.rerun()


# ============================================================
#                       ATTENDANCE
# ============================================================

elif menu == "✅ Attendance":

    # Page header with title and subtitle
    st.title("✅ Attendance Hub")
    st.caption("Track daily classroom presence, audit staff logs, and mark bulk attendance in 1 click.")

    # Modern segmented tabs for Student vs Staff Attendance
    tab_stu_att, tab_stf_att = st.tabs(
        ["👨‍🎓 Student Attendance", "👥 Staff Attendance"]
    )

    # ---------------- TAB 1: Student Attendance ----------------
    with tab_stu_att:

        if "student_att_msg" in st.session_state:
            st.success(st.session_state.pop("student_att_msg"))

        enrolled_students = Student.get_enrolled_students()

        if not enrolled_students:
            st.warning("No enrolled students found. Please enroll students first.")
        else:
            # 1. Overview Table with Filters
            st.subheader("📊 Class Attendance Overview")
            col_af1, col_af2 = st.columns(2)

            with col_af1:
                att_prog_filter = st.selectbox(
                    "Filter by Program",
                    ["All Programs"] + [p.program_name for p in Program.programs_list],
                    key="att_prog_filter"
                )

            with col_af2:
                all_batches = sorted(list({s.get_batch() for s in enrolled_students if s.get_batch() != "-"}))
                att_batch_filter = st.selectbox(
                    "Filter by Batch",
                    ["All Batches"] + all_batches,
                    key="att_batch_filter"
                )

            table_students = enrolled_students
            if att_prog_filter != "All Programs":
                table_students = [s for s in table_students if s.get_program() == att_prog_filter]
            if att_batch_filter != "All Batches":
                table_students = [s for s in table_students if s.get_batch() == att_batch_filter]

            student_rows = []
            for s in table_students:
                summary = s.get_attendance_summary()
                student_rows.append({
                    "Student ID": s.student_id,
                    "Name": s.name,
                    "Program": s.get_program(),
                    "Batch": s.get_batch(),
                    "Total Days": summary["total_days"],
                    "Present Days": summary["present_days"],
                    "Absent Days": summary["absent_days"],
                    "Attendance Rate": f"{summary['percentage']}%"
                })

            if student_rows:
                st.dataframe(pd.DataFrame(student_rows), width="stretch", hide_index=True)
            else:
                st.info("No students match the selected filter.")

            st.divider()

            # 2. Mode Selector: 1-Click Bulk Class Attendance vs Individual
            att_mode = st.radio(
                "Attendance Mode",
                ["⚡ 1-Click Bulk Class Attendance", "✍️ Individual Student Attendance"],
                horizontal=True,
                key="student_att_mode"
            )

            # MODE A: 1-Click Bulk Attendance
            if att_mode == "⚡ 1-Click Bulk Class Attendance":
                st.subheader("⚡ 1-Click Bulk Class Attendance")
                col_bp, col_bb, col_bd = st.columns([2, 2, 1])

                with col_bp:
                    bulk_prog = st.selectbox("Select Program", [p.program_name for p in Program.programs_list], key="bulk_att_prog")
                with col_bb:
                    prog_batches = sorted(list({s.get_batch() for s in enrolled_students if s.get_program() == bulk_prog and s.get_batch() != "-"}))
                    bulk_batch = st.selectbox("Select Batch", prog_batches if prog_batches else ["All"], key="bulk_att_batch")
                with col_bd:
                    bulk_date = st.date_input("Attendance Date", value=date.today(), key="bulk_att_date")

                batch_students = [
                    s for s in enrolled_students
                    if s.get_program() == bulk_prog and (bulk_batch == "All" or s.get_batch() == bulk_batch)
                ]

                if not batch_students:
                    st.info("No students found in this program and batch.")
                else:
                    st.write(f"Roster for **{bulk_prog}** — **{bulk_batch}** ({len(batch_students)} students):")
                    unmarked_checks = {}
                    already_marked_count = 0

                    for s_obj in batch_students:
                        c_name, c_chk = st.columns([3, 1])
                        with c_name:
                            st.write(f"🧑‍🎓 **{s_obj.name}** ({s_obj.student_id})")
                        with c_chk:
                            if s_obj.has_attendance_marked(bulk_date):
                                already_marked_count += 1
                                st.caption("✅ Marked")
                            else:
                                is_p = st.checkbox("Present", value=True, key=f"chk_{s_obj.student_id}_{bulk_date}")
                                unmarked_checks[s_obj] = is_p

                    if already_marked_count == len(batch_students):
                        st.info(f"Attendance for all students in this batch is already recorded for {bulk_date}.")
                    else:
                        if st.button("💾 Save Batch Attendance", type="primary", key="btn_save_bulk_att"):
                            status_list = list(unmarked_checks.items())
                            marked, skipped = st.session_state.activities.mark_bulk_attendance(status_list, bulk_date)
                            st.session_state.student_att_msg = f"Batch attendance saved for {marked} student(s) on {bulk_date}!"
                            st.rerun()

            # MODE B: Individual Student Attendance
            else:
                st.subheader("✍️ Mark Individual Student Attendance")
                student_options = {
                    f"{student.student_id} - {student.name} ({student.get_program()} [{student.get_batch()}])": student
                    for student in enrolled_students
                }

                col_sp, col_sd, col_ss = st.columns([2, 1, 1])
                with col_sp:
                    selected_student_key = st.selectbox("Select Student", list(student_options.keys()), key="att_student_select")
                    student = student_options[selected_student_key]
                with col_sd:
                    att_date = st.date_input("Date", value=date.today(), key="student_att_date")
                with col_ss:
                    present = st.radio("Status", ["Present", "Absent"], horizontal=True, key="student_att_status") == "Present"

                if st.button("Record Attendance", type="primary", key="btn_mark_student_att"):
                    success, message = st.session_state.activities.mark_attendance(student, att_date, present)
                    if success:
                        st.session_state.student_att_msg = message
                        st.rerun()
                    else:
                        st.error(message)

                summary = student.get_attendance_summary()
                st.info(
                    f"**{student.name}** &bull; Total: **{summary['total_days']}** | "
                    f"Present: **{summary['present_days']}** | Absent: **{summary['absent_days']}** | "
                    f"Rate: **{summary['percentage']}%**"
                )

                with st.expander(f"📜 Attendance History for {student.name}"):
                    records = student.get_attendance_records()
                    if not records:
                        st.write("No attendance records marked yet.")
                    else:
                        rec_rows = [
                            {"Date": r["date"], "Status": "✅ Present" if r["present"] else "❌ Absent"}
                            for r in reversed(records)
                        ]
                        st.dataframe(pd.DataFrame(rec_rows), width="stretch", hide_index=True)

    # ---------------- TAB 2: Staff Attendance ----------------
    with tab_stf_att:
        if "staff_att_msg" in st.session_state:
            st.success(st.session_state.pop("staff_att_msg"))

        active_staff = Staff.display_all_staff()

        if not active_staff:
            st.warning("No staff members found.")
        else:
            st.subheader("📊 Staff Attendance Overview")
            staff_att_rows = []
            for s in active_staff:
                summary = s.get_attendance_summary()
                staff_att_rows.append({
                    "Staff ID": s.staff_id,
                    "Name": s.name,
                    "Role": s.role,
                    "Department": s.department,
                    "Total Days": summary["total_days"],
                    "Present Days": summary["present_days"],
                    "Absent Days": summary["absent_days"],
                    "Attendance Rate": f"{summary['percentage']}%"
                })

            st.dataframe(pd.DataFrame(staff_att_rows), width="stretch", hide_index=True)

            st.divider()

            st.subheader("✍️ Record Staff Attendance")
            staff_options = {f"{stf.staff_id} - {stf.name} ({stf.role})": stf for stf in active_staff}

            col_stp, col_std, col_sts = st.columns([2, 1, 1])
            with col_stp:
                selected_staff_key = st.selectbox("Select Staff Member", list(staff_options.keys()), key="att_staff_select")
                selected_staff = staff_options[selected_staff_key]
            with col_std:
                stf_att_date = st.date_input("Date", value=date.today(), key="staff_att_date")
            with col_sts:
                stf_present = st.radio("Status", ["Present", "Absent"], horizontal=True, key="staff_att_status") == "Present"

            if st.button("Record Staff Attendance", type="primary", key="btn_mark_staff_att"):
                success, message = st.session_state.activities.mark_staff_attendance(selected_staff, stf_att_date, stf_present)
                if success:
                    st.session_state.staff_att_msg = message
                    st.rerun()
                else:
                    st.error(message)

            summary = selected_staff.get_attendance_summary()
            st.info(
                f"**{selected_staff.name}** ({selected_staff.role}) &bull; Total: **{summary['total_days']}** | "
                f"Present: **{summary['present_days']}** | Absent: **{summary['absent_days']}** | "
                f"Rate: **{summary['percentage']}%**"
            )

            with st.expander(f"📜 Attendance History for {selected_staff.name}"):
                records = selected_staff.get_attendance_records()
                if not records:
                    st.write("No attendance records marked yet.")
                else:
                    rec_rows = [
                        {"Date": r["date"], "Status": "✅ Present" if r["present"] else "❌ Absent"}
                        for r in reversed(records)
                    ]
                    st.dataframe(pd.DataFrame(rec_rows), width="stretch", hide_index=True)


# ============================================================
#                          FEES
# ============================================================

elif menu == "💰 Fees":

    # Page header with title and subtitle
    st.title("💰 Tuition Fees & Digital Invoicing")
    st.caption("Audit fee collections, record payments across multiple modes, and issue digital receipts.")

    # Success alert if fee was recently processed
    if "fee_success_msg" in st.session_state:
        st.success(st.session_state.pop("fee_success_msg"))

    # ---------------- Digital Receipt Card (if recently collected) ----------------
    if "last_receipt" in st.session_state:
        rc = st.session_state.last_receipt
        r_info = rc["receipt"]
        receipt_id_badge = badge(f"RECEIPT #{r_info['receipt_id']}", "rgba(16, 185, 129, 0.15)", "#047857", "rgba(16, 185, 129, 0.3)")
        # Render payment method pill badge with brand red accent
        pay_mode_badge = badge(r_info['mode'], "rgba(220, 38, 38, 0.15)", "#DC2626", "rgba(220, 38, 38, 0.3)")

        # Render ultra-modern, high-end digital receipt card
        receipt_html = (
            f'<div style="background-color: var(--secondary-background-color); '
            f'border: 2px solid #10B981; border-radius: 16px; padding: 24px 28px; '
            f'margin-bottom: 24px; box-shadow: 0 10px 25px rgba(16, 185, 129, 0.12);">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; '
            f'border-bottom: 1px dashed rgba(148, 163, 184, 0.3); padding-bottom: 14px; margin-bottom: 16px;">'
            f'<div>'
            f'<div style="font-size: 1.15rem; font-weight: 800; color: #10B981; letter-spacing: 0.02em;">🧾 OFFICIAL PAYMENT RECEIPT</div>'
            f'<div style="font-size: 0.8rem; opacity: 0.7;">School of Skills — Calicut Campus &bull; Accounts Department</div>'
            f'</div>'
            f'<div>{receipt_id_badge}</div>'
            f'</div>'
            f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.92rem; margin-bottom: 18px;">'
            f'<div><strong>Student Name:</strong> {rc["student_name"]} ({rc["student_id"]})</div>'
            f'<div><strong>Transaction Date:</strong> {r_info["date"]}</div>'
            f'<div><strong>Enrolled Program:</strong> {rc["program"]} [{rc["batch"]}]</div>'
            f'<div><strong>Payment Mode:</strong> {pay_mode_badge}</div>'
            f'</div>'
            f'<div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); '
            f'border-radius: 10px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;">'
            f'<span style="font-weight: 700; font-size: 1.05rem;">Amount Received:</span>'
            f'<span style="font-size: 1.5rem; font-weight: 800; color: #10B981;">₹{r_info["amount"]:,}</span>'
            f'</div>'
            f'<div style="margin-top: 12px; font-size: 0.88rem; opacity: 0.75; display: flex; justify-content: space-between;">'
            f'<span>Remaining Tuition Balance: <strong>₹{r_info["due_after"]:,}</strong></span>'
            f'<span>Status: <strong style="color: #10B981;">Verified & Cleared</strong></span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(receipt_html, unsafe_allow_html=True)

        if st.button("✖️ Dismiss Receipt Card", key="btn_dismiss_receipt"):
            del st.session_state.last_receipt
            st.rerun()

    # ---------------- Smart Filters for Fees ----------------
    st.subheader("🎯 Filter Fee Collections")
    col_ff1, col_ff2 = st.columns(2)

    with col_ff1:
        fee_prog_filter = st.selectbox(
            "Filter by Program",
            ["All Programs"] + [p.program_name for p in Program.programs_list],
            key="fee_filter_prog"
        )
    with col_ff2:
        enrolled_all = Student.get_enrolled_students()
        fee_batches = sorted(list({s.get_batch() for s in enrolled_all if s.get_batch() != "-"}))
        fee_batch_filter = st.selectbox(
            "Filter by Batch / Section",
            ["All Batches"] + fee_batches,
            key="fee_filter_batch"
        )

    pending_students = Student.get_pending_fee_students()
    paid_students = Student.get_fully_paid_students()

    if fee_prog_filter != "All Programs":
        pending_students = [s for s in pending_students if s.get_program() == fee_prog_filter]
        paid_students = [s for s in paid_students if s.get_program() == fee_prog_filter]

    if fee_batch_filter != "All Batches":
        pending_students = [s for s in pending_students if s.get_batch() == fee_batch_filter]
        paid_students = [s for s in paid_students if s.get_batch() == fee_batch_filter]

    # Calculate pending dues total
    total_pending_amount = sum(s.get_fee_due() for s in pending_students)
    total_paid_count = len(paid_students)

    # High-end 2-Column Fee KPI Cards
    col_fc1, col_fc2 = st.columns(2)
    with col_fc1:
        kpi_card("Pending Tuition", f"₹{total_pending_amount:,}", f"{len(pending_students)} Students with dues", "⏳", "#EF4444")
    with col_fc2:
        kpi_card("Fully Cleared", f"{total_paid_count} Students", "100% Tuition paid", "✅", "#10B981")

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # ---------------- Pending and Paid Tables ----------------
    col_tab_pend, col_tab_paid = st.columns(2)

    with col_tab_pend:
        st.subheader("🔴 Outstanding Dues")
        if pending_students:
            pending_rows = []
            for student in pending_students:
                pending_rows.append({
                    "Student ID": student.student_id,
                    "Name": student.name,
                    "Program": student.get_program(),
                    "Due Amount": f"₹{student.get_fee_due():,}"
                })
            st.dataframe(pd.DataFrame(pending_rows), width="stretch", hide_index=True)
        else:
            st.success("All students in this filtered view have cleared their fees!")

    with col_tab_paid:
        st.subheader("🟢 Cleared Accounts")
        if paid_students:
            paid_rows = []
            for student in paid_students:
                paid_rows.append({
                    "Student ID": student.student_id,
                    "Name": student.name,
                    "Program": student.get_program(),
                    "Total Paid": f"₹{student.student_details()['Fees Paid']:,}"
                })
            st.dataframe(pd.DataFrame(paid_rows), width="stretch", hide_index=True)
        else:
            st.info("No students in this filtered category have fully paid yet.")

    st.divider()

    # ---------------- Collect Fee & Issue Receipt Form ----------------
    st.subheader("💵 Collect Payment & Issue Receipt")

    all_pending = Student.get_pending_fee_students()

    if not all_pending:
        st.info("No outstanding dues pending across the institution.")
    else:
        student_options = {
            f"{student.student_id} - {student.name} ({student.get_program()} [{student.get_batch()}]) — Due: ₹{student.get_fee_due():,}": student
            for student in all_pending
        }

        col_cp1, col_cp2 = st.columns(2)
        with col_cp1:
            selected_key = st.selectbox("Select Student with Due Balance", list(student_options.keys()), key="collect_student_select")
            student_to_pay = student_options[selected_key]
            current_due = student_to_pay.get_fee_due()
            st.info(f"Outstanding Balance for **{student_to_pay.name}**: **₹{current_due:,}**")

        with col_cp2:
            pay_mode = st.selectbox("Payment Method", ["UPI / GPay", "Cash", "Debit / Credit Card", "Net Banking"], key="collect_pay_mode")
            amount_to_pay = st.number_input("Amount to Collect (₹)", min_value=1, max_value=current_due, step=500, value=current_due)

        if st.button("Collect Fee & Generate Receipt", type="primary", key="btn_collect_fee"):
            success, receipt, message = st.session_state.activities.collect_fee(student_to_pay, amount_to_pay, payment_mode=pay_mode)
            if success:
                st.session_state.last_receipt = {
                    "receipt": receipt,
                    "student_name": student_to_pay.name,
                    "student_id": student_to_pay.student_id,
                    "program": student_to_pay.get_program(),
                    "batch": student_to_pay.get_batch()
                }
                st.session_state.fee_success_msg = message
                st.rerun()
            else:
                st.error(message)

    st.divider()

    # ---------------- Payment History & Receipts Lookup ----------------
    with st.expander("📜 Audit Historical Payment Receipts"):
        all_enrolled = Student.get_enrolled_students()
        if not all_enrolled:
            st.write("No enrolled students found.")
        else:
            opt_history = {f"{s.student_id} - {s.name} ({s.get_program()})": s for s in all_enrolled}
            hist_student_key = st.selectbox("Select Student to Audit", list(opt_history.keys()), key="audit_student_select")
            hist_student = opt_history[hist_student_key]

            history = hist_student.get_payment_history()
            if not history:
                st.info(f"No payment receipts recorded yet for {hist_student.name}.")
            else:
                hist_rows = [
                    {
                        "Receipt ID": r["receipt_id"],
                        "Date": r["date"],
                        "Amount (₹)": f"₹{r['amount']:,}",
                        "Payment Mode": r["mode"],
                        "Remaining Due (₹)": f"₹{r['due_after']:,}"
                    }
                    for r in reversed(history)
                ]
                # Render DataFrame of historical transaction receipts
                st.dataframe(pd.DataFrame(hist_rows), width="stretch", hide_index=True)


# ============================================================
#                      VISUAL ANALYTICS
# ============================================================

# Check if user selected the Analytics module from the sidebar
elif menu == "📊 Analytics":

    # Render primary page heading title
    st.title("📊 Campus Analytics & Interactive Insights")
    # Display informative subtitle explaining the analytics scope
    st.caption("Visual reporting on fee realization efficiency, batch attendance trends, and curriculum capacity.")

    # Retrieve list of all actively enrolled student objects
    enrolled_students = Student.get_enrolled_students()

    # Guard clause: check if any students have been enrolled yet
    if not enrolled_students:
        # Inform the user to enroll students first if none exist
        st.warning("No enrolled students found. Please enroll students to populate visual analytics.")
    else:
        # ---------------- 1. Financial Realization Metrics ----------------
        # Section subheading for Financial Realization Analytics
        st.subheader("💳 Fee Recovery & Collection Efficiency")

        # Sum cumulative billed tuition across all enrolled students
        total_billed = sum(s.student_details()["Total Fees"] for s in enrolled_students)
        # Sum cumulative fees collected to date
        total_collected = sum(s.student_details()["Fees Paid"] for s in enrolled_students)
        # Calculate remaining unpaid tuition dues across all students
        total_pending = total_billed - total_collected
        # Calculate collection efficiency percentage (safeguard against division by zero)
        collection_rate = round((total_collected / total_billed * 100), 1) if total_billed > 0 else 0

        # Create 4 responsive columns for the financial KPI cards
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            # Metric card for total billed tuition with brand red accent
            kpi_card("Total Billed", f"₹{total_billed:,}", "Gross Contracted", "📑", "#DC2626")
        with col_m2:
            # Metric card for total collected revenue
            kpi_card("Collected Revenue", f"₹{total_collected:,}", "Realized Cashflow", "💰", "#10B981")
        with col_m3:
            # Metric card for outstanding tuition dues
            kpi_card("Outstanding Dues", f"₹{total_pending:,}", "Pending Recovery", "⏳", "#EF4444")
        with col_m4:
            # Metric card for overall collection recovery rate
            kpi_card("Recovery Rate", f"{collection_rate}%", "Collection Efficiency", "📈", "#06B6D4")

        # Spacing div
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Build data rows comparing Collected vs Pending fees per Program
        fee_by_prog = []
        # Loop through each offered academic program
        for p in Program.programs_list:
            # Filter enrolled students belonging to this program
            p_students = [s for s in enrolled_students if s.get_program() == p.program_name]
            # Sum fees paid by students in this program
            p_paid = sum(s.student_details()["Fees Paid"] for s in p_students)
            # Sum dues pending for students in this program
            p_due = sum(s.get_fee_due() for s in p_students)
            # Append structured dictionary row for this program
            fee_by_prog.append({
                "Program": p.program_name,
                "Collected (₹)": p_paid,
                "Pending Due (₹)": p_due
            })

        # If fee comparison rows exist
        if fee_by_prog:
            # Create Pandas DataFrame with Program as index for clean chart labels
            df_fee_prog = pd.DataFrame(fee_by_prog).set_index("Program")
            # Explanatory chart title
            st.write("**Tuition Realization by Academic Program (Collected vs Due):**")
            # Render interactive bar chart with emerald for collected and coral for pending
            st.bar_chart(df_fee_prog, color=["#10B981", "#EF4444"], width="stretch")
        else:
            # Display informational notification if no fee data is recorded
            st.info("No fee realization data available to chart.")

        # Divider separating financial section from attendance section
        st.divider()

        # ---------------- 2. Attendance Trends & Batch Comparisons ----------------
        # Section subheading for Attendance Trends
        st.subheader("📅 Attendance Analytics & Class Performance")

        # Count students in good academic standing with attendance >= 75%
        high_att_count = sum(1 for s in enrolled_students if s.get_attendance_summary()["percentage"] >= 75)
        # Count students with attendance below the 75% minimum threshold
        low_att_count = len(enrolled_students) - high_att_count

        # Create two columns for attendance health indicator cards
        col_ah1, col_ah2 = st.columns(2)
        with col_ah1:
            # Metric card for students in good standing (>= 75%)
            kpi_card("Good Standing (≥75%)", f"{high_att_count} Students", "Regular Attendance", "🟢", "#10B981")
        with col_ah2:
            # Metric card for students requiring follow-up (< 75%)
            kpi_card("Attendance Alert (<75%)", f"{low_att_count} Students", "Requires Academic Notice", "🔴", "#F59E0B")

        # Spacing div
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Build attendance comparison dataset across batches and programs
        batch_att_data = []
        # Loop through each academic program
        for p in Program.programs_list:
            # Find distinct batches in this program
            batches_in_p = sorted(list({s.get_batch() for s in enrolled_students if s.get_program() == p.program_name and s.get_batch() != "-"}))
            # Loop through each batch
            for b in batches_in_p:
                # Filter students in this specific program and batch
                b_students = [s for s in enrolled_students if s.get_program() == p.program_name and s.get_batch() == b]
                # Calculate average attendance percentage for this batch
                if b_students:
                    avg_att = round(sum(s.get_attendance_summary()["percentage"] for s in b_students) / len(b_students), 1)
                else:
                    avg_att = 0
                # Append row dictionary for this class
                batch_att_data.append({
                    "Class": f"{p.program_name} [{b}]",
                    "Average Attendance (%)": avg_att
                })

        # If batch attendance records exist
        if batch_att_data:
            # Convert to DataFrame indexed by Class name
            df_batch_att = pd.DataFrame(batch_att_data).set_index("Class")
            # Explanatory chart title
            st.write("**Average Attendance Rate by Class & Section:**")
            # Render interactive bar chart showing attendance rate per class in brand red
            st.bar_chart(df_batch_att, color="#DC2626", width="stretch")
        else:
            # Display informational notification if no batch attendance data exists
            st.info("No batch attendance records available to chart.")

        # Divider separating attendance section from enrollment section
        st.divider()

        # ---------------- 3. Curriculum Popularity & Distribution ----------------
        # Section subheading for Student Distribution Analytics
        st.subheader("🎓 Curriculum Popularity & Student Enrollment Density")

        # Build list of student counts per program
        prog_density = []
        # Loop through all programs in catalog
        for p in Program.programs_list:
            # Append program name and live enrolled student count
            prog_density.append({
                "Program Name": p.program_name,
                "Enrolled Learners": p.enrolled_count()
            })

        # If program density records exist
        if prog_density:
            # Convert to DataFrame indexed by Program Name
            df_density = pd.DataFrame(prog_density).set_index("Program Name")
            # Explanatory chart title
            st.write("**Learner Enrollment Density across Offered Programs:**")
            # Render interactive bar chart of enrollment counts in ruby red
            st.bar_chart(df_density, color="#E11D48", width="stretch")
        else:
            # Display informational notification if no program density records exist
            st.info("No curriculum enrollment records available to chart.")
