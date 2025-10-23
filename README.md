# 🧬 CGP Archetype Engine

A Streamlit-based care archetype selection system for the CGP: Waltz 4 Expansion project. Users can explore different personality-based care plans and download detailed archetype guides.

## 🚀 Quick Deploy

### Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/aaj441/cgp_archetype_engine)

### Streamlit Community Cloud
Visit [share.streamlit.io](https://share.streamlit.io/) and connect this repository.

## 📦 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Visit http://localhost:8501

## 🏗️ Project Structure

```
cgp_archetype_engine/
├── app.py                              # Main Streamlit application
├── archetype_prompt_vault_waltz4.json  # Archetype data
├── *.pdf                               # Archetype PDF downloads
├── requirements.txt                    # Python dependencies
├── Procfile                            # Railway/Heroku start command
├── railway.toml                        # Railway configuration
├── .streamlit/config.toml              # Streamlit settings
└── DEPLOYMENT_GUIDE.md                 # Full deployment documentation
```

## 🌟 Features

- **7 Care Archetypes:** Connector, Fighter, Griefwalker, Nurturer, Seeker, Self-Protector, Solo Architect
- **Interactive Selection:** Dropdown menu with instant archetype details
- **PDF Downloads:** Full archetype guides available for download
- **Responsive Design:** Clean, centered layout optimized for all devices

## 🎨 Archetypes

- **Connector:** Relationship-focused care
- **Fighter:** Advocacy and resilience
- **Griefwalker:** Emotional processing and loss navigation
- **Nurturer:** Compassionate support
- **Seeker:** Growth-oriented exploration
- **Self-Protector:** Boundary maintenance
- **Solo Architect:** Independent care design

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment instructions for Railway, Vercel, Streamlit Cloud, and Docker
- **[RITUAL_UNION_BEST_PRACTICES.md](RITUAL_UNION_BEST_PRACTICES.md)** - Modern app development best practices for neurodivergent-friendly design
- **[TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)** - Detailed technical specifications for the Ritual-Union expansion

## 🔧 Configuration

The app uses configuration files for deployment:
- `requirements.txt` - Python dependencies (Streamlit 1.29.0)
- `Procfile` - Process definition for Railway/Heroku
- `runtime.txt` - Python version (3.11.7)
- `.streamlit/config.toml` - Streamlit server settings and theme

## 🚢 Deployment Status

**Recommended Platforms:**
- ✅ Railway (best for Streamlit, long-running processes)
- ✅ Streamlit Community Cloud (free, Streamlit-native hosting)
- ⚠️ Vercel (not recommended - designed for static sites/serverless, not Streamlit)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 🤝 Contributing

This project is part of the Aaron OS ecosystem and Ritual-Union development.

## 📄 License

Proprietary - Part of the CGP (Care Guidance Protocols) project.

---

**Current Branch:** `claude/ritual-union-design-011CUMHLL9bYWYYbQMGQYcjY`
