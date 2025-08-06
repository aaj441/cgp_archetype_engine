
import streamlit as st
import json

st.set_page_config(page_title='CGP: Archetype Engine', layout='centered')
st.title("🧬 CGP – Waltz 4 Expansion")

vault = json.load(open("archetype_prompt_vault_waltz4.json"))
name = st.selectbox("Choose your current care archetype", list(vault.keys()))

if name:
    data = vault[name]
    st.markdown(f"### ✨ {name}")
    st.markdown(f"**Narrative:** {data['narrative']}")
    st.markdown(f"**Tone:** {data['tone']}")
    st.markdown(f"**Values:** {', '.join(data['values'])}")
    st.markdown(f"**Risks:** {', '.join(data['risks'])}")
    st.markdown(f"**Features:** {', '.join(data['features'])}")
    st.markdown(f"**Care Ritual:** {data['ritual']}")
    try:
        with open(f"{name}.pdf", "rb") as pdf_file:
            st.download_button("📄 Download Full Archetype PDF", data=pdf_file.read(), file_name=f"{name}.pdf")
    except FileNotFoundError:
        st.error("PDF not available.")
