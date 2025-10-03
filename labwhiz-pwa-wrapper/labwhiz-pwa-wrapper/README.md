
# LabWhiz PWA Wrapper

This is a minimal, production-ready Progressive Web App wrapper for LabWhiz (Streamlit-based). It provides installability, an app icon, and an offline fallback for the shell.

## Quick Start (5–10 minutes)

1. **Edit the app URL:**
   - Open `index.html` and replace the `src` of the `<iframe>` with your Streamlit URL.
   - Current placeholder: `https://your-streamlit-app-url.example.com/?embed=true`

2. **Deploy:**
   - Push this folder to a GitHub repo.
   - Connect the repo to **Netlify** (or Vercel). Default settings are fine.

3. **Test PWA:**
   - Open the deployed URL in Chrome.
   - Open DevTools → Lighthouse → Run PWA audits (optional).
   - You should see an **Install** prompt or the browser's install menu.

4. **Optional: custom domain**
   - Point your domain (e.g., `app.labwhiz.xyz`) to Netlify.
   - The PWA will auto-update via the service worker.

### Notes

- The service worker caches the app shell and serves an `offline.html` fallback.
- The embedded Streamlit app runs on another domain and cannot be cached by this service worker (browser security). The calculators require internet to function.
- You can change theme color and icons in `manifest.json` and `/icons/`.
- For an **Install** button, use the one provided in `index.html` (handled by `install.js`).

Enjoy!
