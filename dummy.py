import streamlit as st
import base64
from pathlib import Path
import time  # Import time for simulation

# --- Page Configuration ---
st.set_page_config(
    page_title="MTB-Resifiler Flexible Pipeline",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Helper Function to load image as base64 ---
def get_img_as_base64(file):
    """Loads an image file and returns its base64 encoded string."""
    try:
        path = Path(file)
        if not path.is_file():
            st.warning(f"Background image '{file}' not found at path: {path.resolve()}. Using default background.")
            return None
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        st.error(f"Error loading background image '{file}': {e}")
        return None

# --- Load CSS and Background Image (CSS Injected, Refined Spacing) ---
def load_css_and_background(image_file="background.jpg"):
    """Loads CSS styles and optionally a background image, injecting them into Streamlit."""
    css_content = """
        /* Basic Reset & Font */
        body { font-family: 'Inter', sans-serif; }
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        .stApp { background-color: #0e1117; }

        /* --- Animations --- */
        @keyframes shimmer { 0% { background-position: -200% center; } 100% { background-position: 200% center; } }
        @keyframes draw-line { from { width: 0; } to { width: 300px; } }

        /* --- Text Colors --- */
        h2, h3, h4, h5, h6, p, .stMarkdown, label,
        .stTextInput > div > div > input, .stFileUploader label, .stExpander header label {
            color: #E0E0E0 !important;
        }

        /* --- Header Styles --- */
        .main-title {
            font-size: 3.2rem;
            font-weight: 800;
            text-align: center;
            padding-bottom: 15px;
            margin-top: 1rem;
            margin-bottom: 0.2rem;
            width: 100%;
            background: linear-gradient(120deg, #e0e0e0, #ffffff, #00BFFF, #e0e0e0);
            background-size: 200% auto;
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 4s linear infinite;
        }
        .main-title::after {
            content: '';
            display: block;
            width: 0px;
            height: 3px;
            background: linear-gradient(135deg, #00BFFF 0%, #e0e0e0 100%);
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            border-radius: 2px;
            animation: draw-line 1.2s ease-out 0.5s forwards;
        }

        /* --- Info/Warning/Success Boxes --- */
        [data-testid="stInfo"], [data-testid="stWarning"], [data-testid="stSuccess"], [data-testid="stError"] {
            border-radius: 6px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 0.8rem;
            border: none;
            color: #FFFFFF !important;
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
        }
        [data-testid="stInfo"] { background-color: rgba(23, 162, 184, 0.3); }

        /* --- Config Section Card --- */
        .config-section {
            background-color: rgba(30, 35, 48, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 1.2rem 1.8rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* 🧩 FIX: Remove unwanted empty card gap after st.info() */
        .block-container > div:has(.config-section) {
            margin-top: -0.5rem !important;
        }

        /* --- Pipeline Flow & Misc --- */
        .pipeline-flow-container {
            display: flex; align-items: center; justify-content: space-around;
            padding: 1rem 0; flex-wrap: wrap; margin-bottom: 1rem;
        }
        .pipeline-step {
            background-color: rgba(0, 123, 255, 0.2);
            border: 1px solid #007bff; border-radius: 8px;
            padding: 0.8rem 1rem; text-align: center;
            min-width: 140px; margin: 0.5rem;
        }
        .step-name { font-weight: 600; color: #E0E0E0 !important; font-size: 0.9rem; margin-bottom: 0.3rem; }
        .tool-name { font-size: 0.8rem; color: #00BFFF !important; font-style: italic; }

        footer {
            text-align: center; margin-top: 2.5rem; padding-top: 1rem;
            border-top: 1px solid #444; color: #A0A0A0; font-size: 0.9rem;
        }
    """

    img = get_img_as_base64(image_file)
    image_style = f"""
        .stApp {{
            background-image: linear-gradient(to bottom, rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.85)),
            url("data:image/jpeg;base64,{img}");
            background-size: cover; background-position: center;
            background-repeat: no-repeat; background-attachment: fixed;
        }}
    """ if img else ""

    st.markdown(f"<style>{css_content}{image_style}</style>", unsafe_allow_html=True)


# --- Define Pipeline Constants ---
PIPELINE_STEPS = [
    "1. Initial QC", "2. Read Trimming", "3. Alignment",
    "4. BAM Processing & QC", "5. Variant Calling",
    "6. Annotation", "7. Variant Filtering", "8. Summary & Visualization"
]

STANDARD_CONFIG = {
    "QC Tool": "FastQC",
    "Read Trimmer": "Trimmomatic",
    "Aligner": "BWA-MEM",
    "BAM Processing": "GATK + Samtools",
    "Variant Caller": "GATK HaplotypeCaller",
    "Annotation Tool": "SnpEff + Annovar",
    "Mutation Database": "In-House (AFF_Mtb)",
    "Reference Genome": "H37Rv (Standard)",
    "Visualization Tool": "R (maftools)"
}

OPTIONS = {
    "QC Tool": ["FastQC", "Fastp"],
    "Read Trimmer": ["Trimmomatic", "Fastp", "Cutadapt"],
    "Aligner": ["BWA-MEM", "Bowtie2"],
    "Variant Caller": ["GATK HaplotypeCaller", "DeepVariant (High Accuracy)", "FreeBayes"],
    "Annotation Tool": ["SnpEff + Annovar (MycoVarP)", "SnpEff Only", "Annovar Only"],
    "Mutation Database": ["In-House (AFF_Mtb)", "Latest WHO Catalogue", "Northeast Database"],
    "Reference Genome": ["H37Rv (Standard)", "Lineage 2 (Beijing)", "User Uploaded (Not Implemented)"],
    "Visualization Tool": ["R (maftools)", "None"]
}

# --- UI FUNCTIONS ---
def display_standard_flow():
    flow_html = '<div class="pipeline-flow-container">'
    steps_tools = [
        ("QC", "FastQC"), ("Trimming", "Trimmomatic"),
        ("Alignment", "BWA-MEM"), ("BAM Prep", "GATK/Samtools"),
        ("Variant Call", "GATK HaplotypeCaller"),
        ("Annotation", "SnpEff/Annovar"),
        ("Filtering", "SnpSift/Bedtools"),
        ("Visualize", "R (maftools)")
    ]
    for i, (step, tool) in enumerate(steps_tools):
        flow_html += f'<div class="pipeline-step"><div class="step-name">{step}</div><div class="tool-name">{tool}</div></div>'
        if i < len(steps_tools) - 1: flow_html += '<div class="flow-arrow">&rarr;</div>'
    flow_html += '</div>'
    st.markdown(flow_html, unsafe_allow_html=True)


def display_current_config_compact(config_dict):
    config_html = '<div class="current-config-summary"><div class="config-row">'
    for key in OPTIONS.keys():
        value = config_dict.get(key, "N/A")
        config_html += f'<div class="config-item"><span class="config-item-label">{key}:</span><span class="config-item-value">{value}</span></div>'
    config_html += '</div></div>'
    st.markdown(config_html, unsafe_allow_html=True)


# --- MAIN UI ---
load_css_and_background()
st.markdown('<h1 class="main-title">JANA MTB-Resifiler Flexible Pipeline Dashboard</h1>', unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Configure your MTB WGS analysis workflow and upload your data.</p>", unsafe_allow_html=True)

# --- Configuration Section ---
st.header("1. Pipeline Configuration")
st.info("You can choose your own combination")

with st.container():
    st.markdown('<div class="config-section">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    if 'config_mode' not in st.session_state:
        st.session_state.config_mode = "Standard (Recommended)"

    with col1:
        mode = st.radio(
            "Configuration Mode:",
            ("Standard (Recommended)", "Advanced (Custom)"),
            key="config_mode",
        )

    with col2:
        if st.session_state.config_mode == "Standard (Recommended)":
            st.info("Using the standard MycoVarP pipeline configuration.")
            display_current_config_compact(STANDARD_CONFIG)
        else:
            st.warning("Advanced Mode: Ensure selections are appropriate for your analysis.")
            temp_advanced_config = {}
            adv_cols = st.columns(3)
            col_idx = 0
            for key in OPTIONS.keys():
                opts = OPTIONS[key]
                with adv_cols[col_idx % 3]:
                    selected = st.selectbox(f"{key}:", opts, index=0)
                    temp_advanced_config[key] = selected
                col_idx += 1
            display_current_config_compact(temp_advanced_config)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("<footer>MycoVarP Flexible Pipeline Prototype - Developed by SciWhy Lab</footer>", unsafe_allow_html=True)
