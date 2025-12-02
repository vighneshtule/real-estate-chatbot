# Real Estate Chatbot - Frontend & Backend Synchronization Guide

## ✅ Changes Made for Frontend-Backend Synchronization

### Backend Changes (Django)

#### 1. **settings.py** - CORS & File Upload Configuration
- ✅ Updated `CORS_ALLOWED_ORIGINS` to include your deployed frontend URL:
  - `https://real-estate-chatbot-kappa.vercel.app`
  - `https://real-estate-chatbot-ev0r.onrender.com`
  - Localhost URLs for development
- ✅ Set `CORS_ALLOW_ALL_ORIGINS = False` for better security
- ✅ Added `CSRF_TRUSTED_ORIGINS` for cross-domain CSRF protection
- ✅ Configured media file handling:
  - `MEDIA_URL = '/media/'`
  - `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`
- ✅ Increased file upload limits to 100MB:
  - `FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600`
  - `DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600`

#### 2. **urls.py** - Media File Serving
- ✅ Added static media file serving for production and development
- ✅ Ensures uploaded files are accessible via `/media/` URL

### Frontend Changes (React)

#### 1. **App.js** - API Configuration
- ✅ Updated `API_BASE_URL` to use deployed backend:
  ```javascript
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://real-estate-chatbot-ev0r.onrender.com';
  ```
- ✅ Enhanced file upload handler with:
  - Better error logging and debugging
  - 30-second timeout for large files
  - Improved error messages
  - Console logging for troubleshooting

#### 2. **.env** - Environment Variables
- ✅ Created `.env` file with backend URL:
  ```
  REACT_APP_API_URL=https://real-estate-chatbot-ev0r.onrender.com
  ```

#### 3. **config.js** - Centralized Configuration
- ✅ Created config file for easy backend URL management

---

## 🚀 Deployment Checklist

### Before Pushing to Production:

- [ ] Verify `.env` file is in `.gitignore` (to avoid exposing sensitive data)
- [ ] Test file upload locally with both Excel and CSV files
- [ ] Test all API endpoints work correctly
- [ ] Verify CORS errors are resolved in browser console
- [ ] Check that uploaded files are processed correctly

### Render.com Backend Deployment:

1. **Environment Variables** - Set in Render dashboard:
   ```
   OPENAI_API_KEY=your-api-key-here
   DEBUG=False (for production)
   ```

2. **Requirements.txt** - Ensure all dependencies are listed:
   ```
   Django==5.0
   djangorestframework
   django-cors-headers
   pandas
   openpyxl
   openai
   gunicorn
   ```

3. **Render Build Settings**:
   - Build Command: `pip install -r requirements.txt && python manage.py migrate`
   - Start Command: `gunicorn realestate_backend.wsgi:application`

### Vercel Frontend Deployment:

1. **Environment Variables** - Set in Vercel dashboard:
   ```
   REACT_APP_API_URL=https://real-estate-chatbot-ev0r.onrender.com
   ```

2. **Build Settings**:
   - Build Command: `npm run build`
   - Start Command: `npm start`
   - Output Directory: `build`

---

## 🔧 Troubleshooting File Upload Issues

### If upload still fails:

1. **Check Browser Console**:
   - Open DevTools (F12)
   - Go to Console tab
   - Try uploading a file and check for error messages
   - Look for CORS errors or network failures

2. **Check Backend Logs**:
   - View Render.com logs: https://dashboard.render.com/
   - Check for file upload errors and API response messages

3. **Verify File Format**:
   - Ensure file is `.xlsx`, `.xls`, or `.csv`
   - File size should be under 100MB
   - File should have proper columns (area, price, year)

4. **Check CORS Headers**:
   - Frontend URL must match exactly in `CORS_ALLOWED_ORIGINS`
   - Protocol (https/http) and domain must match perfectly

### Common Issues & Solutions:

| Issue | Solution |
|-------|----------|
| "CORS error" in console | Verify frontend URL in `CORS_ALLOWED_ORIGINS` |
| "File upload failed" | Check file format is .xlsx, .xls, or .csv |
| "No file uploaded" error | Ensure file input has `accept=".xlsx,.xls,.csv"` |
| Backend not responding | Check Render.com is running and API_BASE_URL is correct |
| Timeout during upload | Increase timeout or check file size |

---

## 📋 API Endpoints

### File Upload
- **URL**: `POST https://real-estate-chatbot-ev0r.onrender.com/api/upload/`
- **Headers**: `Content-Type: multipart/form-data`
- **Body**: `file` (multipart file)
- **Response**: 
  ```json
  {
    "message": "File uploaded successfully!",
    "rows": 100,
    "columns": ["area", "price", "year"],
    "sample_areas": ["Wakad", "Aundh", "Baner"]
  }
  ```

### Analyze Query
- **URL**: `POST https://real-estate-chatbot-ev0r.onrender.com/api/analyze/`
- **Headers**: `Content-Type: application/json`
- **Body**: 
  ```json
  {
    "query": "Analyze Wakad"
  }
  ```
- **Response**: 
  ```json
  {
    "summary": "AI analysis text...",
    "chart_data": [...],
    "table_data": [...]
  }
  ```

### Health Check
- **URL**: `GET https://real-estate-chatbot-ev0r.onrender.com/api/health/`

---

## 🔐 Security Notes

- ✅ CORS is now restricted to specific origins only
- ✅ CSRF protection enabled for cross-domain requests
- ⚠️ In production, change `DEBUG = False` in settings.py
- ⚠️ Never commit `.env` files with sensitive data
- ⚠️ Use environment variables for all API keys

---

## 📝 Next Steps

1. **Push Changes to GitHub**:
   ```bash
   git add .
   git commit -m "Sync frontend and backend for production"
   git push origin main
   ```

2. **Deploy Backend**:
   - Render.com will auto-deploy from GitHub
   - Monitor deployment in Render dashboard

3. **Deploy Frontend**:
   - Vercel will auto-deploy from GitHub
   - Verify deployment completed successfully

4. **Test Integration**:
   - Visit: https://real-estate-chatbot-kappa.vercel.app/
   - Upload a test Excel file
   - Test an analysis query
   - Check browser console for any errors

---

## 📞 Support

If issues persist:
1. Check the browser DevTools Console (F12)
2. Check Render.com backend logs
3. Verify environment variables are set correctly
4. Ensure file format is correct (Excel or CSV)
