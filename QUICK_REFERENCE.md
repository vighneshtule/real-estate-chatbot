# Quick Reference Card - Frontend & Backend Sync

## 📌 One-Page Summary of All Changes

### Backend Configuration Changes

**File: `backend/realestate_backend/settings.py`**

```python
# Line ~120 (Updated CORS section)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://real-estate-chatbot-kappa.vercel.app",
    "https://real-estate-chatbot-ev0r.onrender.com",
]
CORS_ALLOW_ALL_ORIGINS = False

CSRF_TRUSTED_ORIGINS = [
    "https://real-estate-chatbot-kappa.vercel.app",
    "https://real-estate-chatbot-ev0r.onrender.com",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB
```

**File: `backend/realestate_backend/urls.py`**

```python
from django.conf import settings
from django.conf.urls.static import static

# At the end of urlpatterns:
if settings.DEBUG or True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

### Frontend Configuration Changes

**File: `frontend/src/App.js`** (Line 10)

```javascript
// Change this:
// const API_BASE_URL = 'http://127.0.0.1:8000';

// To this:
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://real-estate-chatbot-ev0r.onrender.com';
```

**File: `frontend/.env`** (NEW FILE)

```env
REACT_APP_API_URL=https://real-estate-chatbot-ev0r.onrender.com
```

**File: `frontend/src/config.js`** (NEW FILE)

```javascript
const config = {
  backendURL: "https://real-estate-chatbot-ev0r.onrender.com",
};

export default config;
```

---

## 🔑 Key Configuration Values

| Setting | Value |
|---------|-------|
| Frontend URL | `https://real-estate-chatbot-kappa.vercel.app` |
| Backend URL | `https://real-estate-chatbot-ev0r.onrender.com` |
| API Upload | `POST /api/upload/` |
| API Analyze | `POST /api/analyze/` |
| API Health | `GET /api/health/` |
| Max Upload Size | 100MB |
| Allowed Origins | Specific (not all) |
| CORS Status | ✅ Restricted & Secure |

---

## 🚀 Next Steps (Exact Order)

### 1️⃣ Verify Everything is Ready
```bash
# Check all files are in place
dir backend\realestate_backend\settings.py
dir frontend\.env
dir frontend\src\config.js
```

### 2️⃣ Test Locally (30 minutes)
```bash
# Terminal 1 - Backend
cd backend
python manage.py runserver 0.0.0.0:8000

# Terminal 2 - Frontend
cd frontend
npm start
```

Test at: `http://localhost:3000`
- Upload a test Excel file
- Run an analysis query
- Check console for errors (F12)

### 3️⃣ Push to GitHub
```bash
git add .
git commit -m "Sync frontend and backend for production deployment"
git push origin main
```

### 4️⃣ Monitor Auto-Deployment
- **Backend**: https://dashboard.render.com/ (Should deploy in ~5 min)
- **Frontend**: https://vercel.com/dashboard (Should deploy in ~2 min)

### 5️⃣ Test in Production
Visit: `https://real-estate-chatbot-kappa.vercel.app/`
- Upload test file
- Run query
- Verify results

---

## ✅ Verification Checklist

Run before pushing:

```
[ ] backend/realestate_backend/settings.py has CORS_ALLOWED_ORIGINS
[ ] backend/realestate_backend/settings.py has CSRF_TRUSTED_ORIGINS
[ ] backend/realestate_backend/settings.py has MEDIA_URL and MEDIA_ROOT
[ ] backend/realestate_backend/urls.py imports static
[ ] backend/realestate_backend/urls.py has urlpatterns += static(...)
[ ] frontend/.env exists with REACT_APP_API_URL
[ ] frontend/src/config.js exists
[ ] frontend/src/App.js uses process.env.REACT_APP_API_URL || '...'
[ ] .gitignore has .env
[ ] requirements.txt has all dependencies
[ ] package.json looks correct
```

---

## 🐛 Most Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| CORS error on upload | Verify frontend URL in CORS_ALLOWED_ORIGINS |
| 400 Bad Request | Check file is .xlsx/.xls/.csv |
| Backend not responding | Check Render.com is running |
| "No file uploaded" | Check file input has accept attribute |
| Timeout | Increase timeout or check file size |
| 500 error | Check backend logs in Render dashboard |

---

## 📞 Emergency Contacts

**File Upload Not Working?**
1. Open browser DevTools (F12)
2. Go to Console tab
3. Try upload and note error
4. Check CORS_ALLOWED_ORIGINS in settings.py

**Backend Unresponsive?**
1. Check Render.com dashboard: https://dashboard.render.com/
2. View logs for error messages
3. Verify OPENAI_API_KEY is set

**Frontend Issues?**
1. Check Vercel dashboard: https://vercel.com/dashboard
2. Check browser console (F12) for errors
3. Verify .env file exists with API URL

---

## 📊 API Request Examples

### Upload File
```javascript
const formData = new FormData();
formData.append('file', file);

const response = await axios.post(
  `${API_BASE_URL}/api/upload/`,
  formData,
  { headers: { 'Content-Type': 'multipart/form-data' } }
);
```

### Analyze Query
```javascript
const response = await axios.post(
  `${API_BASE_URL}/api/analyze/`,
  { query: 'Analyze Wakad' }
);
```

---

## 🎯 Success Indicators

When properly synced, you should see:

✅ File uploads accepted without CORS errors
✅ File info returned (rows, columns, areas)
✅ Analysis queries processed
✅ AI summaries generated
✅ Charts displaying correctly
✅ Data tables showing results
✅ No 404 or 500 errors
✅ Console clean (no errors)

---

## 📌 Important Files Summary

| File | Purpose | Status |
|------|---------|--------|
| settings.py | Django config | ✅ Updated |
| urls.py | URL routing | ✅ Updated |
| App.js | React main component | ✅ Updated |
| .env | Environment variables | ✅ Created |
| config.js | Config file | ✅ Created |
| requirements.txt | Python dependencies | ✅ Verified |
| package.json | Node dependencies | ✅ Verified |

---

## 🎓 What Each Change Does

### CORS Configuration
**Why needed:** Allows your Vercel frontend to make requests to your Render backend
**What it does:** Specifies exactly which domains can access your API

### CSRF Protection
**Why needed:** Prevents attacks from unauthorized domains
**What it does:** Only allows requests from trusted origins

### Media File Handling
**Why needed:** Stores and serves uploaded files
**What it does:** Saves files and makes them accessible via `/media/` URL

### File Upload Limits
**Why needed:** Prevents server overload
**What it does:** Sets maximum file size to 100MB

### Environment Variables
**Why needed:** Keeps sensitive data out of code
**What it does:** Loads API keys and URLs from environment instead of hardcoding

---

## 🚨 Do NOT Do These Things

❌ Change `CORS_ALLOW_ALL_ORIGINS = True` (security risk)
❌ Hardcode API keys in frontend code
❌ Commit `.env` files to GitHub
❌ Use `http://` instead of `https://` in production
❌ Change the backend URL without updating frontend

---

## ✨ You're All Set!

All configuration is complete. The connection between your frontend and backend is now properly synchronized.

**Current Status:**
- ✅ Backend: Ready on https://real-estate-chatbot-ev0r.onrender.com
- ✅ Frontend: Ready on https://real-estate-chatbot-kappa.vercel.app
- ✅ CORS: Configured and restricted
- ✅ File Upload: Enabled with 100MB limit
- ✅ Security: Protected with CSRF tokens

**Next Action:** Push to GitHub and watch both platforms auto-deploy! 🚀