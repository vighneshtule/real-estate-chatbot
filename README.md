# 🏘️ Real Estate Analysis Chatbot

A full-stack AI-powered real estate analytics platform that processes property data and provides intelligent insights using natural language queries.

**🌐 Live Demo:** 
- **Frontend:** https://real-estate-chatbot-hbzp.vercel.app/
- **Backend API:** https://real-estate-chatbot-ev0r.onrender.com/

---

## 📖 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [🏗️ Technology Stack](#️-technology-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
- [🔧 Detailed Setup](#-detailed-setup)
- [📡 API Documentation](#-api-documentation)
- [🧠 AI Integration](#-ai-integration)
- [🚢 Deployment](#-deployment)
- [🔐 Security](#-security)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## 🌟 Overview

The **Real Estate Analysis Chatbot** is a modern web application that helps users analyze real estate market data through intelligent queries. Upload your property dataset (Excel/CSV) and ask questions like:

> "Analyze Wakad" → Get AI-powered insights, price trends, and detailed analytics

### Key Capabilities
- 📊 Analyze property data by area/locality
- 🤖 AI-generated market insights using GPT-4o
- 📈 Interactive price trend charts
- 📋 Detailed data tables with filters
- 📤 Support for Excel (.xlsx, .xls) and CSV files
- 🎯 Up to 100MB file uploads

---

## ✨ Features

### 📤 File Upload
- Upload Excel (.xlsx, .xls) or CSV files
- Automatic column detection (Area, Price, Year)
- Support for files up to 100MB
- Sample area suggestions from uploaded data

### 🔍 Intelligent Analysis
- Natural language query processing
- Area-based data filtering
- Smart column detection (handles variations like "locality", "location", "region")
- Real-time analysis results

### 📊 Data Visualization
- **Price Trends Chart:** View price evolution over time
- **Interactive Charts:** Built with Recharts for responsive design
- **Data Tables:** Display detailed property information with formatting

### 🧠 AI-Powered Insights
- Integration with OpenAI GPT-4o-mini
- Context-aware market analysis
- Investment recommendations
- Trend analysis and market strength assessment
- Fallback to rule-based insights if API unavailable

### 🔐 Security
- CORS configured for cross-origin requests
- CSRF protection enabled
- Environment variables for sensitive data
- No hardcoded API keys

---

## 🏗️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, Bootstrap 5, Recharts, Axios |
| **Backend** | Django 5, Django REST Framework, pandas, openpyxl |
| **AI/ML** | OpenAI GPT-4o-mini |
| **Database** | SQLite (development), PostgreSQL (production-ready) |
| **File Processing** | pandas, openpyxl |
| **Deployment** | Vercel (frontend), Render.com (backend) |
| **Styling** | Bootstrap 5 CSS |

---

## 📂 Project Structure

```
real-estate-chatbot/
│
├── backend/                              # Django Backend
│   ├── realestate_backend/              # Project settings
│   │   ├── settings.py                  # Configuration & CORS
│   │   ├── urls.py                      # URL routing
│   │   ├── wsgi.py                      # WSGI application
│   │   └── asgi.py                      # ASGI application
│   │
│   ├── api/                             # API Application
│   │   ├── views.py                     # API endpoints
│   │   ├── urls.py                      # API routes
│   │   ├── models.py                    # Data models
│   │   └── migrations/                  # Database migrations
│   │
│   ├── manage.py                        # Django CLI
│   ├── requirements.txt                 # Python dependencies
│   └── db.sqlite3                       # Development database
│
├── frontend/                             # React Frontend
│   ├── public/                          # Static files
│   │   └── index.html                   # HTML entry point
│   │
│   ├── src/                             # Source code
│   │   ├── App.js                       # Main React component
│   │   ├── App.css                      # Application styles
│   │   ├── config.js                    # Configuration
│   │   ├── index.js                     # React entry point
│   │   └── .env                         # Environment variables
│   │
│   ├── package.json                     # Node dependencies
│   └── README.md                        # Frontend documentation
│
├── data/                                 # Sample datasets
│   └── Sample_data.xlsx                 # Example Excel file
│
├── docs/                                 # Documentation files
│   ├── LOCAL_TESTING_GUIDE.md          # Testing instructions
│   ├── SYNC_DEPLOYMENT_GUIDE.md        # Deployment guide
│   ├── QUICK_REFERENCE.md              # Quick reference card
│   └── SYNC_SUMMARY.md                 # Summary of changes
│
├── .gitignore                           # Git ignore rules
├── render.yaml                          # Render.com configuration
├── README.md                            # This file
├── CONTRIBUTING.md                      # Contribution guidelines
└── LICENSE                              # MIT License
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git
- (Optional) OpenAI API key for AI features

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/real-estate-chatbot.git
cd real-estate-chatbot
```

### 2️⃣ Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000
```

Backend runs at: **http://127.0.0.1:8000**

### 3️⃣ Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend

# Create .env file
echo "REACT_APP_API_URL=http://127.0.0.1:8000" > .env

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs at: **http://localhost:3000**

### 4️⃣ Test the Application

1. Open http://localhost:3000 in your browser
2. Upload `data/Sample_data.xlsx` 
3. Enter a query like "Analyze Wakad"
4. View results with AI insights, charts, and data

---

## 🔧 Detailed Setup

### Backend Configuration

**File: `backend/realestate_backend/settings.py`**

Key configurations:
- ✅ CORS enabled for frontend domain
- ✅ File upload limits: 100MB
- ✅ CSRF protection configured
- ✅ OpenAI integration ready

**Environment Variables:**

```env
# Required for production
OPENAI_API_KEY=sk-your-api-key
DEBUG=False

# Optional
DJANGO_SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
```

### Frontend Configuration

**File: `frontend/.env`**

```env
# Backend API URL
REACT_APP_API_URL=http://127.0.0.1:8000    # Development
REACT_APP_API_URL=https://your-backend.onrender.com  # Production
```

---

## 📡 API Documentation

### Health Check

```http
GET /api/health/
```

**Response:**
```json
{
  "status": "Backend is running with AI! 🤖"
}
```

### File Upload

```http
POST /api/upload/
Content-Type: multipart/form-data

file: <Excel or CSV file>
```

**Success Response (200):**
```json
{
  "message": "File uploaded successfully!",
  "rows": 1000,
  "columns": ["Area", "Price", "Year", "BHK"],
  "sample_areas": ["Wakad", "Aundh", "Baner", "Viman Nagar", "Koregaon Park"]
}
```

**Error Response (400):**
```json
{
  "error": "Please upload Excel (.xlsx, .xls) or CSV file"
}
```

### Analyze Query

```http
POST /api/analyze/
Content-Type: application/json

{
  "query": "Analyze Wakad"
}
```

**Success Response (200):**
```json
{
  "summary": "🏘️ Real Estate Analysis for Wakad\n\n📊 Quick Stats:\n• Properties Analyzed: 125\n• Average Price: ₹5,250,000\n• Latest Data: 2024\n\n🤖 AI Analysis:\n[Generated insights...]",
  "chart_data": [
    {
      "area": "Wakad",
      "year": 2020,
      "price": 5000
    },
    {
      "area": "Wakad",
      "year": 2021,
      "price": 5200
    }
  ],
  "table_data": [
    {
      "Area": "Wakad",
      "Price": 5000000,
      "Year": 2020,
      "BHK": 2
    }
  ]
}
```

**Error Response (400):**
```json
{
  "error": "Please upload a file first"
}
```

---

## 🧠 AI Integration

### OpenAI Setup

1. **Get API Key:**
   - Visit https://platform.openai.com/api-keys
   - Create new secret key
   - Copy and save securely

2. **Configure Backend:**
   ```env
   # backend/.env
   OPENAI_API_KEY=sk-your-actual-key
   ```

3. **How It Works:**
   - Extracts area data from uploaded file
   - Creates contextual prompt with statistics
   - Calls GPT-4o-mini for market analysis
   - Returns AI-generated insights with formatting

### Fallback Logic

If OpenAI API fails or key is missing:
- System falls back to rule-based analysis
- Provides basic market strength assessment
- No interruption to user experience

---

## 🚢 Deployment

### Frontend Deployment (Vercel)

1. **Connect Repository**
   - Push code to GitHub
   - Go to https://vercel.com
   - Import repository

2. **Configure Environment**
   - Settings → Environment Variables
   - Add: `REACT_APP_API_URL=https://your-backend-url`

3. **Deploy**
   - Vercel auto-deploys on push
   - Preview URL provided

### Backend Deployment (Render.com)

1. **Create Service**
   - Go to https://render.com
   - Create new "Web Service"
   - Connect GitHub repository

2. **Configure**
   - Build Command: `pip install -r requirements.txt && python manage.py migrate`
   - Start Command: `gunicorn realestate_backend.wsgi:application`
   - Add Environment Variables:
     ```
     OPENAI_API_KEY=your-key
     DEBUG=False
     ALLOWED_HOSTS=your-render-url.onrender.com
     ```

3. **Deploy**
   - Click Deploy
   - Monitor build in dashboard

### Post-Deployment Checklist

- [ ] Test file upload on production
- [ ] Verify AI insights generation
- [ ] Check CORS settings match frontend URL
- [ ] Monitor error logs
- [ ] Test all API endpoints

---

## 🔐 Security

### Best Practices

✅ **Do's:**
- Use environment variables for secrets
- Keep `.env` in `.gitignore`
- Rotate API keys regularly
- Use HTTPS in production
- Validate file uploads
- Implement rate limiting

❌ **Don'ts:**
- Hardcode API keys in code
- Commit `.env` files
- Use development keys in production
- Allow large file uploads without limits
- Skip CORS configuration
- Expose sensitive data in logs

### CORS Configuration

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.vercel.app",
    "https://your-backend.onrender.com",
]
CORS_ALLOW_ALL_ORIGINS = False  # Restrictive approach
```

### File Upload Security

- Maximum 100MB file size
- Only accept `.xlsx`, `.xls`, `.csv`
- Files stored in temporary memory
- No persistent file storage

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Steps

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Workflow

```bash
# Create branch
git checkout -b feature/your-feature

# Make changes and test locally
npm test              # Frontend
python manage.py test # Backend

# Commit and push
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature

# Create Pull Request on GitHub
```

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author & Contributors

**Original Author:** Vighnesh Tule
- GitHub: [@vighneshtule](https://github.com/vighneshtule)
- Email: vighnesh@example.com

**Contributors:** See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

---

## 🙏 Acknowledgments

- Django & Django REST Framework team
- React community
- OpenAI for GPT-4o API
- Render.com and Vercel for hosting
- Bootstrap for UI framework
- Recharts for visualization

---

## 📞 Support & Issues

### Need Help?

- 📖 **Documentation:** Check [docs/](docs/) folder
- 🐛 **Report Bug:** Open an issue on GitHub
- 💡 **Feature Request:** Create a new discussion
- 📧 **Contact:** vighnesh@example.com

### Common Issues

| Issue | Solution |
|-------|----------|
| CORS error | Check `CORS_ALLOWED_ORIGINS` in settings.py |
| File upload fails | Verify file format (.xlsx, .xls, .csv) |
| AI insights not showing | Check OpenAI API key and credits |
| Charts not displaying | Check browser console for errors |

---

## 🎯 Roadmap

- [ ] User authentication & accounts
- [ ] Saved analysis history
- [ ] Advanced filtering options
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Real-time data integration
- [ ] Predictive analytics
- [ ] Export to PDF

---

**Built with ❤️ for real estate professionals and data enthusiasts**

Owner : Vighnesh Tule
https://github.com/vighneshtule

**Last Updated:** December 2025

