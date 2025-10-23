import streamlit as st
import json
import os

# Page configuration
st.set_page_config(
    page_title='CGP: Archetype Engine',
    layout='centered',
    page_icon='🧬',
    menu_items={
        'About': "CGP Archetype Engine - Waltz 4 Expansion\n\nExplore care archetypes designed for personalized support."
    }
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .archetype-card {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 1rem;
    }
    .stSelectbox label {
        font-size: 1.1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-header'>", unsafe_allow_html=True)
st.title("🧬 CGP – Waltz 4 Expansion")
st.caption("Discover your care archetype and explore personalized support pathways")
st.markdown("</div>", unsafe_allow_html=True)

# Load archetype data with error handling
@st.cache_data
def load_archetype_data():
    vault_path = "archetype_prompt_vault_waltz4.json"
    try:
        with open(vault_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ Data file not found: {vault_path}")
        st.info("Please ensure 'archetype_prompt_vault_waltz4.json' is in the root directory.")
        return {}
    except json.JSONDecodeError:
        st.error("❌ Error reading archetype data (invalid JSON format)")
        return {}

vault = load_archetype_data()

if not vault:
    st.stop()

# Archetype selection
st.markdown("### Choose Your Current Care Archetype")
archetype_names = list(vault.keys())
name = st.selectbox(
    "Select an archetype to explore:",
    archetype_names,
    label_visibility="collapsed"
)

# Display archetype details
if name:
    data = vault[name]

    # Archetype header
    st.markdown(f"## ✨ {name}")

    # Create columns for better layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Narrative
        st.markdown("### 📖 Narrative")
        st.write(data.get('narrative', 'No narrative available.'))

        # Tone
        st.markdown("### 🎭 Tone")
        st.write(data.get('tone', 'No tone information available.'))

    with col2:
        # Values
        st.markdown("### 💎 Values")
        values = data.get('values', [])
        if values:
            for value in values:
                st.markdown(f"- {value}")
        else:
            st.write("No values listed.")

    # Risks
    st.markdown("### ⚠️ Risks")
    risks = data.get('risks', [])
    if risks:
        for risk in risks:
            st.markdown(f"- {risk}")
    else:
        st.write("No risks identified.")

    # Features
    st.markdown("### 🌟 Features")
    features = data.get('features', [])
    if features:
        for feature in features:
            st.markdown(f"- {feature}")
    else:
        st.write("No features listed.")

    # Care Ritual
    st.markdown("### 🕯️ Care Ritual")
    st.info(data.get('ritual', 'No ritual available.'))

    # PDF Download
    st.markdown("---")
    pdf_path = f"{name}.pdf"
    if os.path.exists(pdf_path):
        try:
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="📄 Download Full Archetype PDF",
                    data=pdf_bytes,
                    file_name=f"{name}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error loading PDF: {e}")
    else:
        st.warning(f"📄 PDF not available for {name}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>Part of the Aaron OS ecosystem • CGP: Waltz 4 Expansion</p>
    <p>🔗 <a href='https://github.com/aaj441/cgp_archetype_engine' target='_blank'>GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)
