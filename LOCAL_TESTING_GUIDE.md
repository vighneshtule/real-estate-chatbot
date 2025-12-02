# Local Testing Guide - Real Estate Chatbot

## Prerequisites

- Python 3.8+
- Node.js 14+
- Git
- Backend: Django, pandas, openai
- Frontend: React with axios

---

## 🔧 Backend Setup & Testing

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Create `.env` File for Backend

Create `backend/.env`:
```
OPENAI_API_KEY=your-openai-api-key-here
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### 3. Run Migrations

```bash
cd backend
python manage.py migrate
```

### 4. Start Backend Development Server

```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 5. Test Backend Health Check

Open your browser or use curl:
```bash
curl http://127.0.0.1:8000/api/health/
```

Expected response:
```json
{
  "status": "Backend is running with AI! 🤖"
}
```

---

## 🎨 Frontend Setup & Testing

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Create `.env` File for Frontend

Create `frontend/.env`:
```
REACT_APP_API_URL=http://127.0.0.1:8000
```

### 3. Start Frontend Development Server

```bash
cd frontend
npm start
```

The app should open automatically at `http://localhost:3000`

---

## 🧪 Testing File Upload Locally

### Step 1: Prepare Test Data

Use the sample file: `data/Sample_data.xlsx`

Or create your own Excel file with columns:
- `Area` or `Location` (string)
- `Price` or `Cost` (number)
- `Year` or `Date` (number)

Example:
```
| Area   | Price  | Year |
|--------|--------|------|
| Wakad  | 5000   | 2020 |
| Wakad  | 5500   | 2021 |
| Aundh  | 4800   | 2020 |
| Aundh  | 5200   | 2021 |
```

### Step 2: Upload File via Frontend

1. Open http://localhost:3000
2. Click "Choose File" button
3. Select `data/Sample_data.xlsx`
4. Wait for success message: "✅ File uploaded successfully!"

### Step 3: Check Console for Details

Open Browser DevTools (Press F12):
- Go to Console tab
- You should see:
  ```
  Uploading file to: http://127.0.0.1:8000/api/upload/
  File: Sample_data.xlsx, Size: XXXXX bytes
  Upload response: {message: "File uploaded successfully!", ...}
  ```

### Step 4: Test Analysis Query

1. In the "Ask Your Question" section, enter: `Analyze Wakad`
2. Click "🔍 Analyze" button
3. Wait for AI response (should see loading spinner)
4. Should see:
   - 🤖 AI Analysis summary
   - 📈 Price Trends chart
   - 📋 Detailed data table

---

## 🐛 Debugging Common Issues

### Issue: CORS Error in Console

**Error Message:**
```
Access to XMLHttpRequest at 'http://127.0.0.1:8000/api/upload/' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
1. Verify backend is running on `http://127.0.0.1:8000`
2. Check `frontend/.env` has correct `REACT_APP_API_URL`
3. Restart frontend: `npm start`

### Issue: File Upload Returns 400 Error

**Backend Response:**
```json
{"error": "No file uploaded"}
```

**Solution:**
1. Check file was selected (not empty)
2. Verify file format is `.xlsx`, `.xls`, or `.csv`
3. Check file size is under 100MB

### Issue: "Please upload a file first" After Upload

**Solution:**
1. Check browser console for upload errors
2. Look for API response in Network tab (DevTools → Network)
3. Ensure file has proper columns (area, price, year)

### Issue: AI Analysis Not Generating

**Solution:**
1. Verify `OPENAI_API_KEY` is set in backend `.env`
2. Check backend console for OpenAI API errors
3. Ensure API key has sufficient credits

### Issue: Backend Won't Start

**Error:**
```
ModuleNotFoundError: No module named 'django'
```

**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📊 Testing Different Scenarios

### Scenario 1: Simple CSV Upload

1. Create `test.csv`:
```csv
Area,Price,Year
Wakad,5000,2020
Wakad,5500,2021
Aundh,4800,2020
```

2. Upload via frontend
3. Query: "Analyze Wakad"

### Scenario 2: Large Excel File

1. Use `data/Sample_data.xlsx` (if available)
2. Upload and test multiple queries
3. Verify chart renders correctly

### Scenario 3: Multiple Areas

1. Upload file with 5+ different areas
2. Query each area separately
3. Verify correct filtering

---

## ✅ Pre-Deployment Testing Checklist

Before deploying to Render.com and Vercel:

- [ ] Backend runs locally without errors
- [ ] Frontend loads at http://localhost:3000
- [ ] File upload works with Excel file
- [ ] File upload works with CSV file
- [ ] Analysis query returns AI summary
- [ ] Chart renders correctly
- [ ] No CORS errors in console
- [ ] No 500 errors in backend
- [ ] Sample data displays in table
- [ ] OpenAI API is working (AI summary generates)

---

## 🚀 Switch to Production URLs

Once local testing passes:

### Backend - Switch to Render.com URL

Update `frontend/.env`:
```env
REACT_APP_API_URL=https://real-estate-chatbot-ev0r.onrender.com
```

Or use the default in `App.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://real-estate-chatbot-ev0r.onrender.com';
```

### Test in Development Mode

1. Stop local servers
2. Build frontend:
   ```bash
   cd frontend
   npm run build
   ```
3. Test built version:
   ```bash
   npm install -g serve
   serve -s build
   ```
4. Visit http://localhost:3000 and test with production backend

---

## 📋 API Response Examples

### Successful File Upload Response

```json
{
  "message": "File uploaded successfully!",
  "rows": 1000,
  "columns": ["Area", "Price", "Year", "BHK"],
  "sample_areas": ["Wakad", "Aundh", "Baner", "Viman Nagar", "Koregaon Park"]
}
```

### Successful Analysis Response

```json
{
  "summary": "🏘️ Real Estate Analysis for Wakad\n\n📊 Quick Stats:\n• Properties Analyzed: 125\n• Average Price: ₹5,250,000\n• Latest Data: 2024\n\n🤖 AI Analysis:\n[AI generated insights...]",
  "chart_data": [
    {"area": "Wakad", "year": 2020, "price": 5000},
    {"area": "Wakad", "year": 2021, "price": 5200},
    {"area": "Wakad", "year": 2022, "price": 5500}
  ],
  "table_data": [
    {"Area": "Wakad", "Price": 5000, "Year": 2020},
    {"Area": "Wakad", "Price": 5200, "Year": 2021}
  ]
}
```

---

## 💡 Quick Commands Reference

```bash
# Backend
cd backend
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000

# Frontend
cd frontend
npm install
npm start

# Build frontend
npm run build

# Test with production backend
REACT_APP_API_URL=https://real-estate-chatbot-ev0r.onrender.com npm start

# Backend health check
curl http://127.0.0.1:8000/api/health/

# Frontend production build
npm run build && serve -s build
```

---

## 🎯 Next Steps

1. **Test Locally** - Follow steps above
2. **Fix Any Issues** - Use debugging section
3. **Push to GitHub** - When all tests pass
4. **Deploy to Render & Vercel** - Auto-deploy on push
5. **Test in Production** - Visit deployed URLs
6. **Monitor Logs** - Check Render.com and Vercel dashboards

---

Good luck with your deployment! 🚀