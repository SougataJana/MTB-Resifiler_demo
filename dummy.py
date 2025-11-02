# --- Block 1: Global CSS & helper ---
import streamlit as st
import base64
from pathlib import Path

def get_img_as_base64(file):
    try:
        p = Path(file)
        if not p.is_file(): return None
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    except: return None

def load_ui_css(image_file="background.jpg"):
    img = get_img_as_base64(image_file)
    image_style = f"""
        .stApp {{
            background-image: linear-gradient(to bottom, rgba(14,17,23,0.85), rgba(14,17,23,0.85)),
                             url("data:image/jpeg;base64,{img}");
            background-size: cover; background-position: center;
        }}
    """ if img else ""
    css = f"""
    <style>
    /* Fonts & base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    body {{ font-family: Inter, sans-serif; }}

    /* Header/title */
    .main-title {{ font-size: 2.6rem; font-weight: 800; text-align:left; color: #E6EEF6; margin: 0 0 0.3rem 0; }}
    .subtitle {{ color: #A0A0A0; margin-bottom: 1.2rem; }}

    /* Alerts (st.info etc) */
    [data-testid="stInfo"] {{ background-color: rgba(23,162,184,0.24); border-radius:8px; padding:0.7rem 1rem; color:#fff; }}

    /* Config card */
    .config-section {{
        background-color: rgba(30,35,48,0.7);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }}

    /* Fix gap between st.info and config card */
    .block-container > div:has(.config-section) {{
        margin-top: -0.45rem !important;
    }}

    /* Recommendation & small items */
    .recommendation-card {{ padding:0.9rem; border-radius:10px; background: rgba(23,162,184,0.08); border:1px solid rgba(23,162,184,0.12); }}
    .option-card {{ padding: 4px 8px; border-radius:6px; background: rgba(255,255,255,0.03); display:inline-block; margin:4px 6px 4px 0; }}

    /* compact config items */
    .current-config-summary {{ margin-top:0.8rem; display:flex; flex-wrap:wrap; gap:8px; }}
    .config-item {{ padding:6px 10px; border-radius:6px; border:1px solid rgba(255,255,255,0.04); background: rgba(255,255,255,0.02); color:#E0E0E0; font-weight:600; font-size:0.85rem; }}

    </style>
    {image_style}
    """
    st.markdown(css, unsafe_allow_html=True)

# call once
load_ui_css()
# --- end block 1 ---
# --- Block 2: Hero header ---
st.markdown('<div style="margin-top: 0.6rem;"></div>', unsafe_allow_html=True)
st.markdown('<div><h1 class="main-title"> MTB-Resifiler Flexible Pipeline Dashboard</h1></div>', unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Configure your MTB WGS analysis workflow and upload your data.</p>", unsafe_allow_html=True)
# --- end block 2 ---
# --- Block 3: Recommendation cards ---
st.markdown("### Key Areas for Pipeline Flexibility")
rec1, rec2, rec3 = st.columns(3, gap="large")

with rec1:
    st.markdown("""
    <div class="recommendation-card">
      <strong>🧬 Variant Caller</strong>
      <div style="font-size:0.9rem;color:#C8C8C8;margin-top:6px;">Choices impact accuracy — DeepVariant for hard cases.</div>
      <div style="margin-top:8px"><span class="option-card"><strong>GATK</strong></span><span class="option-card">DeepVariant</span><span class="option-card">FreeBayes</span></div>
    </div>
    """, unsafe_allow_html=True)

with rec2:
    st.markdown("""
    <div class="recommendation-card">
      <strong>🔬 Mutation Database</strong>
      <div style="font-size:0.9rem;color:#C8C8C8;margin-top:6px;">Relevant DBs change interpretation (clinical vs research).</div>
      <div style="margin-top:8px"><span class="option-card"><strong>In-House</strong></span><span class="option-card">WHO</span></div>
    </div>
    """, unsafe_allow_html=True)

with rec3:
    st.markdown("""
    <div class="recommendation-card">
      <strong>🗺️ Reference Genome</strong>
      <div style="font-size:0.9rem;color:#C8C8C8;margin-top:6px;">Pick lineage-specific refs for divergent strains.</div>
      <div style="margin-top:8px"><span class="option-card"><strong>H37Rv</strong></span><span class="option-card">Lineage 2</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
# --- end block 3 ---
st.markdown('<div class="config-section">', unsafe_allow_html=True)
st.subheader("Pipeline Configuration Options")

