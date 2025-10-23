# 🚀 CGP Archetype Engine - Deployment Guide

## Overview

This Streamlit app can be deployed to various platforms. **Railway is the recommended platform** for Streamlit apps due to native support for long-running web processes.

---

## ✅ Railway Deployment (RECOMMENDED)

Railway is perfect for Streamlit apps and provides the best experience.

### Prerequisites
- [Railway account](https://railway.app/) (free tier available)
- GitHub repository connected

### Deployment Steps

1. **Connect Repository to Railway:**
   - Go to [railway.app](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select this repository

2. **Railway Auto-Detects Configuration:**
   - Railway will automatically detect `railway.toml` and `Procfile`
   - It will use Nixpacks to build the Python environment
   - Dependencies from `requirements.txt` will be installed

3. **Environment Variables (Optional):**
   - No environment variables required for basic deployment
   - If needed, add them in Railway Dashboard → Variables

4. **Deploy:**
   - Railway automatically deploys on push to main branch
   - You'll get a public URL like: `https://your-app.up.railway.app`

### Railway Configuration Files
- `railway.toml` - Railway-specific configuration
- `Procfile` - Defines the web process start command
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version (3.11.7)
- `.streamlit/config.toml` - Streamlit server configuration

### Troubleshooting Railway

**Issue: App crashes on startup**
- Check logs in Railway dashboard
- Ensure all PDF files and JSON files are committed to the repository
- Verify `archetype_prompt_vault_waltz4.json` exists

**Issue: Port binding errors**
- Railway automatically provides `$PORT` environment variable
- Procfile already configured to use `$PORT`

**Issue: Build fails**
- Check that `requirements.txt` has correct package versions
- Verify Python version in `runtime.txt` is supported

---

## ⚠️ Vercel Deployment (NOT RECOMMENDED)

**Why Vercel isn't ideal for Streamlit:**
- Vercel is designed for **static sites and serverless functions** (max 10-60 second execution time)
- Streamlit requires a **long-running WebSocket connection**
- Vercel's architecture conflicts with Streamlit's stateful nature

### Alternative Options for Vercel

#### Option 1: Use Streamlit Community Cloud Instead
- [share.streamlit.io](https://share.streamlit.io/) - Free hosting for Streamlit apps
- Simply connect your GitHub repository
- Purpose-built for Streamlit

#### Option 2: Rewrite as a Static Site (Major Refactor)
If you must use Vercel, you'd need to:
1. Convert the app to Next.js or pure HTML/CSS/JS
2. Make it a static site or use Vercel serverless functions
3. This would require a complete rewrite

#### Option 3: Deploy Streamlit Elsewhere, Proxy via Vercel
1. Deploy Streamlit on Railway or Streamlit Cloud
2. Use Vercel as a reverse proxy (not worth the complexity)

### Vercel Configuration (Experimental)
A `vercel.json` is included, but it **will not work reliably** due to:
- 10-second timeout on Hobby plan (60s on Pro)
- No WebSocket support in serverless functions
- Stateless execution model

---

## 🌟 Streamlit Community Cloud (ALTERNATIVE RECOMMENDATION)

### Why Use Streamlit Community Cloud?
- ✅ Free tier available
- ✅ Purpose-built for Streamlit apps
- ✅ Automatic deploys from GitHub
- ✅ Built-in secrets management
- ✅ No configuration files needed

### Deployment Steps

1. **Go to Streamlit Community Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io/)
   - Sign in with GitHub

2. **Deploy Your App:**
   - Click "New app"
   - Select your repository: `aaj441/cgp_archetype_engine`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Done!**
   - Your app will be live at: `https://[your-app-name].streamlit.app`
   - Auto-deploys on every push to main branch

---

## 🐳 Docker Deployment (Advanced)

For custom hosting (AWS, GCP, Azure, DigitalOcean):

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

### Build and Run
```bash
docker build -t cgp-archetype-engine .
docker run -p 8501:8501 cgp-archetype-engine
```

---

## 📋 Deployment Checklist

Before deploying, ensure:
- [ ] All PDF files are committed (`Connector.pdf`, `Fighter.pdf`, etc.)
- [ ] JSON vault file exists: `archetype_prompt_vault_waltz4.json`
- [ ] `requirements.txt` is present
- [ ] `.streamlit/config.toml` is configured
- [ ] Git repository is up to date

---

## 🔧 Configuration Files Explained

### `requirements.txt`
Lists Python dependencies (Streamlit)

### `Procfile`
Tells Railway/Heroku how to start the web process:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

### `runtime.txt`
Specifies Python version:
```
python-3.11.7
```

### `.streamlit/config.toml`
Streamlit server configuration:
- Headless mode (no browser auto-open)
- Port 8501 (can be overridden by $PORT)
- CORS disabled for deployment
- Custom theme colors

### `railway.toml`
Railway-specific configuration:
- Build strategy (Nixpacks)
- Start command
- Restart policy

---

## 🆘 Common Deployment Issues

### Issue: "File not found: archetype_prompt_vault_waltz4.json"
**Solution:** Ensure the JSON file is committed to Git:
```bash
git add archetype_prompt_vault_waltz4.json
git commit -m "Add archetype vault"
git push
```

### Issue: "PDF not available" error in app
**Solution:** Ensure all PDF files are committed:
```bash
git add *.pdf
git commit -m "Add archetype PDFs"
git push
```

### Issue: App works locally but fails on deployment
**Solution:** Check that:
1. File paths are relative (not absolute)
2. All dependencies are in `requirements.txt`
3. Python version matches `runtime.txt`

### Issue: Port binding errors
**Solution:** Ensure your start command uses `$PORT` environment variable:
```bash
streamlit run app.py --server.port=$PORT
```

---

## 🎯 Recommended Deployment Strategy

**For Public/Production Use:**
1. **First Choice:** Railway (best Streamlit support, free tier)
2. **Second Choice:** Streamlit Community Cloud (free, Streamlit-native)
3. **Third Choice:** Docker on cloud provider (AWS ECS, Google Cloud Run)

**Avoid:**
- Vercel (not designed for Streamlit)
- Netlify (same limitations as Vercel)
- GitHub Pages (static only)

---

## 📊 Platform Comparison

| Platform | Cost | Streamlit Support | Ease of Setup | Auto-Deploy | WebSockets |
|----------|------|-------------------|---------------|-------------|------------|
| **Railway** | Free tier → $5/mo | ✅ Excellent | ⭐⭐⭐⭐⭐ | ✅ Yes | ✅ Yes |
| **Streamlit Cloud** | Free tier → $20/mo | ✅ Native | ⭐⭐⭐⭐⭐ | ✅ Yes | ✅ Yes |
| **Vercel** | Free tier → $20/mo | ❌ Poor | ⭐⭐⭐ | ✅ Yes | ❌ No |
| **Docker (Cloud)** | $5-50/mo | ✅ Excellent | ⭐⭐ | ⚙️ Manual | ✅ Yes |

---

## 🔗 Helpful Links

- [Railway Documentation](https://docs.railway.app/)
- [Streamlit Community Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Deployment Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy)
- [Railway Streamlit Template](https://railway.app/template/streamlit)

---

## 📝 Need Help?

If deployment fails:
1. Check the platform's build logs
2. Verify all files are committed to Git
3. Ensure `requirements.txt` has correct versions
4. Try deploying to Railway first (most forgiving)

**Repository:** `https://github.com/aaj441/cgp_archetype_engine`
**Branch:** `claude/ritual-union-design-011CUMHLL9bYWYYbQMGQYcjY`
