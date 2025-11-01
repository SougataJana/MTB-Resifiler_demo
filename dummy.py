import streamlit as st
import base64
from pathlib import Path
import time # Import time for simulation

# --- Page Configuration ---
st.set_page_config(
    page_title="MTB-Resifiler Flexible Pipeline",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Helper Function to load image as base64 ---
# @st.cache_data
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
    # --- Define CSS Content Here ---
    # (CSS content remains the same as the previous version with visual intro cards)
    css_content = """
        /* Basic Reset & Font */
        body { font-family: 'Inter', sans-serif; }
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        .stApp { background-color: #0e1117; } /* Fallback background */

        /* --- Animations --- */
        @keyframes shimmer { 0% { background-position: -200% center; } 100% { background-position: 200% center; } }
        @keyframes draw-line { from { width: 0; } to { width: 300px; } }

        /* --- Text Colors --- */
        h2, h3, h4, h5, h6, p, .stMarkdown, label, .stTextInput > div > div > input, .stFileUploader label, .stExpander header label { color: #E0E0E0 !important; }
        a { color: #3498db !important; }
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] .stRadio > label, [data-testid="stSidebar"] .stSelectbox > label, [data-testid="stSidebar"] .stInfo, [data-testid="stSidebar"] .stWarning, [data-testid="stSidebar"] .stMarkdown { color: #212529 !important; }

        /* --- Header Styles --- */
        .main-title { font-size: 3.2rem; font-weight: 800; position: relative; text-align: center; padding-bottom: 15px; margin-top: 1rem; margin-bottom: 0.2rem; width: 100%; background: linear-gradient(120deg, #e0e0e0, #ffffff, #00BFFF, #e0e0e0); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; animation: shimmer 4s linear infinite; display: block; }
        .main-title::after { content: ''; display: block; width: 0px; height: 3px; background: linear-gradient(135deg, #00BFFF 0%, #e0e0e0 100%); position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); border-radius: 2px; animation: draw-line 1.2s ease-out 0.5s forwards; }
        p.subtitle { text-align: center; color: #A0A0A0; margin-top: 0px; margin-bottom: 1.5rem; }
        h2 { color: #E0E0E0 !important; margin-top: 1.5rem; margin-bottom: 0.8rem; border-bottom: 1px solid #444; padding-bottom: 4px; font-weight: 600; }
        h3 { color: #C8C8C8 !important; margin-top: 1.2rem; margin-bottom: 0.6rem; font-weight: 500; }

        /* --- Component Styles --- */
        .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #444; gap: 12px; padding-bottom: 0; margin-bottom: 1rem; }
        .stTabs [data-baseweb="tab"] { color: #A0A0A0 !important; padding: 10px 15px; border: none; border-bottom: 3px solid transparent; transition: all 0.2s ease-in-out; background-color: transparent; margin-bottom: -1px; font-weight: 500; }
        .stTabs [data-baseweb="tab"]:hover { background-color: rgba(255, 255, 255, 0.05); color: #E0E0E0 !important; }
        .stTabs [aria-selected="true"] { color: #00BFFF !important; border-bottom: 3px solid #00BFFF !important; font-weight: 600; }
        .stExpander { background-color: rgba(30, 35, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(8px); border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .stExpander header { background-color: rgba(40, 45, 60, 0.8); border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #E0E0E0 !important; font-weight: 600; padding: 10px 15px; border-top-left-radius: 8px; border-top-right-radius: 8px; }
        .stExpander header svg { fill: #E0E0E0 !important; }
        .stExpander div[data-testid="stExpanderDetails"] { color: #C8C8C8 !important; padding: 15px; }
        .stTextInput label, .stSelectbox label, .stRadio label { color: #E0E0E0 !important; font-weight: 500; margin-bottom: 0.2rem; }
        .stTextInput > div > div > input, .stSelectbox > div > div { border-radius: 6px !important; border: 1px solid #555 !important; background-color: rgba(14, 17, 23, 0.5) !important; color: #E0E0E0 !important; }
        .stSelectbox svg { fill: #A0A0A0 !important; }
        .stRadio > label > div { color: #E0E0E0 !important; }
        .config-section { background-color: rgba(30, 35, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 1.2rem 1.8rem; margin-bottom: 1.5rem; backdrop-filter: blur(8px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .stButton > button { border-radius: 6px; padding: 10px 24px; font-weight: 600; transition: all 0.2s ease; border: 1px solid transparent; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stButton > button:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); }
        .stButton > button[kind="primary"] { background-color: #007bff; color: white; border-color: #007bff; }
        .stButton > button[kind="primary"]:hover:not(:disabled) { background-color: #0056b3; border-color: #0056b3; }
        .stButton > button:disabled { background-color: #495057; border-color: #495057; color: #adb5bd; opacity: 0.7; cursor: not-allowed; }
        [data-testid="stInfo"], [data-testid="stWarning"], [data-testid="stSuccess"], [data-testid="stError"] { border-radius: 6px; padding: 0.8rem 1.2rem; margin-bottom: 0.8rem; border: none; color: #FFFFFF !important; background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(5px); }
        [data-testid="stSuccess"] { background-color: rgba(40, 167, 69, 0.3); } /* Green tint */
        [data-testid="stWarning"] { background-color: rgba(255, 193, 7, 0.3); } /* Yellow tint */
        [data-testid="stError"] { background-color: rgba(220, 53, 69, 0.3); } /* Red tint */
        [data-testid="stInfo"] { background-color: rgba(23, 162, 184, 0.3); } /* Blue tint */
        .block-container { padding-top: 2rem; padding-bottom: 1rem; padding-left: 2rem; padding-right: 2rem; }
        footer { text-align: center; margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid #444; color: #A0A0A0; font-size: 0.9rem; }

        /* --- Styles for Standard Pipeline Flow --- */
        .pipeline-flow-container { display: flex; align-items: center; justify-content: space-around; padding: 1rem 0; overflow-x: auto; flex-wrap: wrap; margin-bottom: 1rem; }
        .pipeline-step { background-color: rgba(0, 123, 255, 0.2); border: 1px solid #007bff; border-radius: 8px; padding: 0.8rem 1rem; text-align: center; min-width: 140px; margin: 0.5rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .step-name { font-weight: 600; color: #E0E0E0 !important; font-size: 0.9rem; margin-bottom: 0.3rem; white-space: nowrap; }
        .tool-name { font-size: 0.8rem; color: #00BFFF !important; font-style: italic; white-space: normal; }
        .flow-arrow { font-size: 1.5rem; color: #A0A0A0; margin: 0 0.2rem; }
        @media (max-width: 1200px) { .flow-arrow { display: none; } }

        /* --- Styles for Compact Current Config Display --- */
        .current-config-summary { margin-top: 1rem; border-top: 1px dashed #555; padding-top: 1rem; }
        .config-row { display: flex; flex-wrap: wrap; gap: 0.8rem; margin-bottom: 0.5rem; }
        .config-item { display: flex; align-items: baseline; background-color: rgba(255, 255, 255, 0.05); padding: 4px 8px; border-radius: 4px; border: 1px solid rgba(255, 255, 255, 0.1); }
        .config-item-label { font-size: 0.8rem; color: #A0A0A0 !important; margin-right: 0.4rem; font-weight: 500; }
        .config-item-value { font-size: 0.85rem; color: #E0E0E0 !important; font-weight: 600; }

        /* <<< Styles for Intro Recommendation Cards >>> */
        .recommendation-card { background-color: rgba(23, 162, 184, 0.15); border: 1px solid #17a2b8; border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1rem; height: 100%; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .recommendation-header { display: flex; align-items: center; margin-bottom: 0.6rem; }
        .recommendation-icon { font-size: 1.5rem; margin-right: 0.8rem; }
        .recommendation-title { font-size: 1.1rem; font-weight: 600; color: #17a2b8 !important; margin: 0; }
        .recommendation-text { font-size: 0.9rem; color: #C8C8C8 !important; line-height: 1.5; margin-bottom: 0.8rem; }
        .recommendation-text strong { color: #E0E0E0 !important; font-weight: 600; }

        /* <<< Styles for Option Sub-Cards >>> */
        .option-list { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
        .option-card { background-color: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 4px; padding: 4px 8px; font-size: 0.8rem; color: #B0C4DE !important; white-space: nowrap; }
        .option-card strong { color: #FFD700 !important; font-weight: 600; }

    """ # End of CSS string

    img = get_img_as_base64(image_file)
    image_style = f"""
        .stApp {{
            background-image: linear-gradient(to bottom, rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.85)), url("data:image/jpeg;base64,{img}");
            background-size: cover; background-position: center;
            background-repeat: no-repeat; background-attachment: fixed;
        }}
    """ if img else ""

    st.markdown(f'<style>{css_content}{image_style}</style>', unsafe_allow_html=True)


# === IMPORTANT: Define Constants BASED ON MycoVarP PPT ===
# --- Pipeline Steps (Refined from MycoVarP PPT) ---
PIPELINE_STEPS = [
    "1. Initial QC",            # FastQC (Slide 19)
    "2. Read Trimming",         # Trimmomatic (Slide 20)
    "3. Alignment",             # BWA (Slide 21)
    "4. BAM Processing & QC",   # GATK SortSam, Samtools Depth/Coverage (Slide 22), GATK Prep (Slide 25)
    "5. Variant Calling",       # GATK HaplotypeCaller (Slide 25)
    "6. Annotation",            # SnpEff, Annovar (Slides 26, 29)
    "7. Variant Filtering",     # SnpSift (AFF, DP, Synonymous), Bedtools (PE/PPE) (Slides 27, 28)
    "8. Summary & Visualization" # Annovar Summary + R/maftools (Slide 29) - RENAMED
]
# --- Default/Standard MycoVarP Pipeline Configuration ---
STANDARD_CONFIG = {
    "QC Tool": "FastQC",
    "Read Trimmer": "Trimmomatic",
    "Aligner": "BWA-MEM",
    "BAM Processing": "GATK + Samtools",
    "Variant Caller": "GATK HaplotypeCaller",
    "Annotation Tool": "SnpEff + Annovar",
    "Mutation Database": "In-House (AFF_Mtb)", # RENAMED Key
    # REMOVED Filtering Strategy from standard display config if needed, or keep for internal logic
    # "Filtering Strategy": "MycoVarP Standard (AF<=0.01, DP>10, Non-Syn, Excl. PE/PPE)",
    "Reference Genome": "H37Rv (Standard)",
    "Visualization Tool": "R (maftools)"
}
# --- Available Options for Advanced Mode (Updated DB Options) ---
OPTIONS = {
    "QC Tool": ["FastQC", "Fastp"],
    "Read Trimmer": ["Trimmomatic", "Fastp", "Cutadapt"],
    "Aligner": ["BWA-MEM", "Bowtie2"],
    "Variant Caller": ["GATK HaplotypeCaller", "DeepVariant (High Accuracy)", "FreeBayes"],
    "Annotation Tool": ["SnpEff + Annovar (MycoVarP)", "SnpEff Only", "Annovar Only"],
    "Mutation Database": ["In-House (AFF_Mtb)", "Latest WHO Catalogue", "Northeast Database"], # RENAMED Key, REMOVED None
    # REMOVED Filtering Strategy from options
    # "Filtering Strategy": ["MycoVarP Standard", "GATK Hard Filtering", "Minimal (QC Only)", "Custom (Not Implemented)"],
    "Reference Genome": ["H37Rv (Standard)", "Lineage 2 (Beijing)", "User Uploaded (Not Implemented)"],
    "Visualization Tool": ["R (maftools)", "None"]
}
# === End of Constant Definitions ===

# --- Function to Display Standard Pipeline Flow ---
# ... (display_standard_flow function remains the same) ...
def display_standard_flow():
    """Generates HTML to visually represent the standard MycoVarP pipeline flow."""
    flow_html = '<div class="pipeline-flow-container">'
    # Adjusted to reflect removal of explicit filtering strategy config if needed
    steps_tools = [
        ("QC", STANDARD_CONFIG["QC Tool"]),
        ("Trimming", STANDARD_CONFIG["Read Trimmer"]),
        ("Alignment", STANDARD_CONFIG["Aligner"]),
        ("BAM Prep", "GATK/Samtools"),
        ("Variant Call", STANDARD_CONFIG["Variant Caller"]),
        ("Annotation", "SnpEff/Annovar"),
        ("Filtering", "SnpSift/Bedtools"), # Uses DB implicitly
        ("Visualize", STANDARD_CONFIG["Visualization Tool"])
    ]
    for i, (step, tool) in enumerate(steps_tools):
        flow_html += f'<div class="pipeline-step"><div class="step-name">{step}</div><div class="tool-name">{tool}</div></div>'
        if i < len(steps_tools) - 1: flow_html += '<div class="flow-arrow">&rarr;</div>'
    flow_html += '</div>'
    st.markdown(flow_html, unsafe_allow_html=True)

# --- Function to Display Current Config Compactly ---
def display_current_config_compact(config_dict):
    """Generates HTML for a compact horizontal display of the current config."""
    config_html = '<div class="current-config-summary"><div class="config-row">'
    # Use the keys from OPTIONS to ensure consistent order/display
    # This automatically excludes the removed 'Filtering Strategy'
    for key in OPTIONS.keys():
        value = config_dict.get(key, "N/A") # Get value from current config
        display_value = str(value)
        if len(display_value) > 30: display_value = display_value[:27] + "..."
        config_html += f'<div class="config-item"><span class="config-item-label">{key}:</span><span class="config-item-value">{display_value}</span></div>'
    config_html += '</div></div>'
    st.markdown(config_html, unsafe_allow_html=True)

# --- Load UI ---
load_css_and_background()

# --- Main Application Area ---
st.markdown('<h1 class="main-title">  JANA MTB-Resifiler Flexible Pipeline Dashboard</h1>', unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Configure your MTB WGS analysis workflow and upload your data.</p>", unsafe_allow_html=True)

# --- Visual Intro Recommendations Section ---
st.markdown("### Key Areas for Pipeline Flexibility")
st.markdown(
    """
    While the **Standard Configuration** provides a validated workflow, **Advanced Mode** allows customization in critical areas:
    """, unsafe_allow_html=True)

rec_col1, rec_col2, rec_col3 = st.columns(3)

# Function to generate option cards HTML
def generate_option_cards(options_list, standard_value):
    cards_html = '<div class="option-list">'
    for option in options_list:
        if option == standard_value: cards_html += f'<div class="option-card"><strong>{option}</strong></div>'
        else: cards_html += f'<div class="option-card">{option}</div>'
    cards_html += '</div>'
    return cards_html

with rec_col1:
    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-header">
                <span class="recommendation-icon">🧬</span>
                <h4 class="recommendation-title">Variant Caller</h4>
            </div>
            <p class="recommendation-text">
                Core of variant discovery. Choices impact <strong>accuracy</strong>, especially for challenging regions or variant types (e.g., DeepVariant).
            </p>
            {generate_option_cards(OPTIONS["Variant Caller"], STANDARD_CONFIG["Variant Caller"])}
        </div>
        """, unsafe_allow_html=True
    )

with rec_col2:
    # UPDATED: Use the new DB options and key
    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-header">
                <span class="recommendation-icon">🔬</span>
                <h4 class="recommendation-title">Mutation Database</h4>
            </div>
            <p class="recommendation-text">
                Crucial for the final <strong>interpretation</strong> (drug resistance). Use databases relevant to your study goals (clinical vs. research).
            </p>
             {generate_option_cards(OPTIONS["Mutation Database"], STANDARD_CONFIG["Mutation Database"])}
        </div>
        """, unsafe_allow_html=True
    )

with rec_col3:
    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-header">
                <span class="recommendation-icon">🗺️</span>
                <h4 class="recommendation-title">Reference Genome</h4>
            </div>
            <p class="recommendation-text">
                Affects <strong>alignment quality</strong>. Aligning to the most appropriate reference (e.g., specific lineage) improves accuracy for divergent strains.
            </p>
             {generate_option_cards(OPTIONS["Reference Genome"], STANDARD_CONFIG["Reference Genome"])}
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("---") # Separator after recommendations
# --- End of Visual Intro Section ---


# --- Configuration Section ---
# --- Configuration Section (from Dashboard) ---
st.markdown("""
<div class="config-section">
<h3>1. Pipeline Configuration</h3>
</div>
""", unsafe_allow_html=True)

# No `st.container()` here — start content immediately
config_col1, config_col2 = st.columns([1, 3])
current_config_display = {}

with config_col1:
    if 'config_mode' not in st.session_state:
        st.session_state.config_mode = "Standard (Recommended)"
    mode = st.radio(
        "Configuration Mode:",
        ("Standard (Recommended)", "Advanced (Custom)"),
        key="config_mode",
        help="Choose 'Standard' for the validated MycoVarP workflow or 'Advanced' to customize."
    )

with config_col2:
    if st.session_state.config_mode == "Standard (Recommended)":
        st.info("Using the standard MycoVarP pipeline configuration.")
        current_config_display = STANDARD_CONFIG
        display_current_config_compact(current_config_display)

    else:
        st.warning("Advanced Mode: Ensure selections are appropriate for your analysis.")
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        cols = [adv_col1, adv_col2, adv_col3]
        col_idx = 0
        temp_advanced_config = {}
        for key in OPTIONS.keys():
            opts = OPTIONS[key]
            standard_val = STANDARD_CONFIG.get(key)
            with cols[col_idx % len(cols)]:
                default_index = 0
                if standard_val and standard_val in opts:
                    default_index = opts.index(standard_val)
                session_key = f"advanced_{key.lower().replace('/', '').replace(' ', '_').replace('.', '').replace('(','').replace(')','')}"
                if session_key not in st.session_state:
                    st.session_state[session_key] = opts[default_index]
                selected_option = st.selectbox(
                    f"{key}:", opts,
                    index=opts.index(st.session_state[session_key]),
                    key=f"sb_{session_key}",
                    help=f"Choose the desired option for {key}."
                )
                st.session_state[session_key] = selected_option
                temp_advanced_config[key] = selected_option
            col_idx += 1
        current_config_display = temp_advanced_config
        display_current_config_compact(current_config_display)


# --- File Uploader ---
st.header("2. Upload Data")
# ... (File uploader code remains the same) ...
with st.expander("Upload Paired-End FASTQ Files", expanded=True):
    uploaded_files = st.file_uploader( "Select FASTQ files (.fastq.gz, .fq.gz)", type=['gz'], accept_multiple_files=True, label_visibility="collapsed" )
    if uploaded_files:
        if len(uploaded_files) == 2:
            st.success(f"✔️ {uploaded_files[0].name} and {uploaded_files[1].name} ready.")
            st.text_input("Sample Name (Auto-detected)", value="Sample_ABC", disabled=True)
        else: st.warning("⚠️ Please upload exactly two paired-end FASTQ files.")
    else: st.info("⬆️ Upload your paired-end FASTQ files (.gz format) to begin analysis.")

st.markdown("---")

# --- Pipeline Steps Display (Using Tabs) ---
st.header("3. Run Pipeline Workflow")
# ... (Rest of the pipeline steps display code remains the same, but references to 'Filtering Strategy' are removed) ...
if 'current_step_index' not in st.session_state: st.session_state.current_step_index = 0
files_ready = uploaded_files and len(uploaded_files) == 2

# --- Display Visual Flow ONLY if Standard Mode and Files Ready ---
if files_ready and 'config_mode' in st.session_state and st.session_state.config_mode == "Standard (Recommended)":
     st.markdown("**Standard Workflow Overview:**")
     display_standard_flow() # Display flow here
     st.markdown("---") # Add separator

# --- Display Tabs only if files are ready ---
if not files_ready:
    st.info("Please upload your paired-end FASTQ files in Step 2 above to view and run the pipeline workflow.")
else:
    # --- Determine Current Configuration for Tabs ---
    current_run_config_for_tabs = {}
    if 'config_mode' in st.session_state and st.session_state.config_mode == "Standard (Recommended)":
        current_run_config_for_tabs = STANDARD_CONFIG
    else:
        for key_opt in OPTIONS.keys(): # Use current OPTIONS keys
            session_key_opt = f"advanced_{key_opt.lower().replace('/', '').replace(' ', '_').replace('.', '').replace('(','').replace(')','')}"
            current_run_config_for_tabs[key_opt] = st.session_state.get(session_key_opt, STANDARD_CONFIG.get(key_opt, "N/A")) # Fallback to standard
    # --- End Determine Current Configuration ---

    tabs = st.tabs(PIPELINE_STEPS)
    for i, step_name in enumerate(PIPELINE_STEPS):
        with tabs[i]:
            st.markdown(f"<h3 style='margin-top: 0.5rem; margin-bottom: 0.8rem;'>{step_name}</h3>", unsafe_allow_html=True)

            # --- Tab Content Logic ---
            if i > st.session_state.current_step_index:
                st.warning("⏳ Complete previous steps to proceed.")
                st.markdown("**Upcoming Configuration:**")
                # UPDATED: Removed Filtering Strategy, Renamed DB key
                if i == 4: st.write(f"- Variant Caller: *{current_run_config_for_tabs.get('Variant Caller', 'N/A')}*")
                if i == 5: st.write(f"- Annotation Tool: *{current_run_config_for_tabs.get('Annotation Tool', 'N/A')}*")
                if i == 6:
                    st.write(f"- Mutation Database: *{current_run_config_for_tabs.get('Mutation Database', 'N/A')}*")
                    # Filtering strategy is implicit now or part of Annotation step config
                if i == 7: st.write(f"- Visualization Tool: *{current_run_config_for_tabs.get('Visualization Tool', 'N/A')}*")

            elif i < st.session_state.current_step_index:
                st.success("✅ Step completed.")
                st.write(f"Outputs for {step_name} would appear here.")
                if st.button("Go to Current Step", key=f"jump_{i}"): st.rerun()

            else: # Current Step
                st.info("▶️ This is the current step.")
                st.markdown("**Configuration for this step:**")
                config_lines = []
                # UPDATED: Removed Filtering Strategy, Renamed DB key
                if i == 0:
                     config_lines.append(f"- QC Tool: *{current_run_config_for_tabs.get('QC Tool', 'N/A')}*")
                     config_lines.append(f"- Reference Genome (used later): *{current_run_config_for_tabs.get('Reference Genome', 'N/A')}*")
                elif i == 1: config_lines.append(f"- Read Trimmer: *{current_run_config_for_tabs.get('Read Trimmer', 'N/A')}*")
                elif i == 2: config_lines.append(f"- Aligner: *{current_run_config_for_tabs.get('Aligner', 'N/A')}*")
                elif i == 3: config_lines.append(f"- BAM Processing: *{current_run_config_for_tabs.get('BAM Processing', 'N/A')}*")
                elif i == 4: config_lines.append(f"- Variant Caller: *{current_run_config_for_tabs.get('Variant Caller', 'N/A')}*")
                elif i == 5: config_lines.append(f"- Annotation Tool: *{current_run_config_for_tabs.get('Annotation Tool', 'N/A')}*")
                elif i == 6: # Variant Filtering Step now uses DB
                     config_lines.append(f"- Mutation Database: *{current_run_config_for_tabs.get('Mutation Database', 'N/A')}*")
                     # Implicitly uses standard filtering params unless overridden by advanced logic later
                     config_lines.append("- Applying Standard MycoVarP Filters (DP, Synonymous, PE/PPE etc.)")
                elif i == 7:
                    config_lines.append(f"- Visualization Tool: *{current_run_config_for_tabs.get('Visualization Tool', 'N/A')}*")
                    config_lines.append("Generating final summaries and plots.")
                if config_lines: st.markdown("\n".join(config_lines))

                button_label = f"Run {step_name}"
                if i == len(PIPELINE_STEPS) - 1: button_label = "Generate Final Summary"
                files_still_ready = uploaded_files and len(uploaded_files) == 2
                if st.button(button_label, type="primary", key=f"run_{i}", use_container_width=True, disabled=not files_still_ready):
                    with st.spinner(f"Simulating {step_name}... Please wait."):
                        time.sleep(1)
                        if i < len(PIPELINE_STEPS) - 1: st.session_state.current_step_index += 1
                        st.rerun()
                elif not files_still_ready: st.caption("File upload seems incomplete. Cannot run step.")


# --- Footer ---
st.markdown("---")
st.markdown("<footer>MycoVarP Flexible Pipeline Prototype - Developed by SciWhy Lab - For Demonstration Purposes Only</footer>", unsafe_allow_html=True)

