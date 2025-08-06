
import streamlit as st
import json

st.set_page_config(page_title='Care Genome Engine', layout='centered')
st.title("🧬 CGP Archetype Engine")

vault = json.load(open("archetype_prompt_vault_full.json"))
name = st.selectbox("Choose an archetype", list(vault.keys()))

if name:
    data = vault[name]
    st.markdown(f"### Narrative:\n{data['narrative']}")
    st.write("**Tone:**", data['tone'])
    st.write("**Values:**", ', '.join(data['values']))
    st.write("**Risks:**", ', '.join(data['risks']))
    st.write("**Features:**", ', '.join(data['features']))
    st.write("**CMS Tags:**", ', '.join(data['cms_tags']))
    with open(f"{name}.pdf", "rb") as pdf_file:
        st.download_button("📄 Download Full PDF", data=pdf_file.read(), file_name=f"{name}.pdf")
