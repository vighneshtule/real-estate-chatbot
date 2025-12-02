# 🤝 Contributing to Real Estate Analysis Chatbot

Thank you for your interest in contributing to the Real Estate Analysis Chatbot! This document provides guidelines and instructions for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Workflow](#-development-workflow)
- [Making Changes](#-making-changes)
- [Coding Standards](#-coding-standards)
- [Testing](#-testing)
- [Commit Guidelines](#-commit-guidelines)
- [Pull Request Process](#-pull-request-process)
- [Reporting Issues](#-reporting-issues)
- [Feature Requests](#-feature-requests)
- [Documentation](#-documentation)

---

## 🎯 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- ✅ Be respectful and constructive
- ✅ Provide helpful feedback
- ✅ Focus on the code, not the person
- ✅ Welcome diverse perspectives
- ✅ Report violations to the maintainers

**Unacceptable behavior includes:** harassment, discrimination, or disruptive conduct.

---

## 🚀 Getting Started

### Prerequisites

Before you start, ensure you have:

- **Python 3.8+** - For backend development
- **Node.js 14+** - For frontend development
- **Git** - For version control
- **GitHub Account** - To fork and submit PRs
- **Code Editor** - VS Code, PyCharm, or similar

### 1. Fork the Repository

Click the **Fork** button on the GitHub repository to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/real-estate-chatbot.git
cd real-estate-chatbot
```

### 3. Add Upstream Remote

```bash
git remote add upstream https://github.com/vighneshtule/real-estate-chatbot.git
git fetch upstream
```

### 4. Set Up Development Environment

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-test-key" > .env
python manage.py migrate
```

**Frontend:**
```bash
cd frontend
npm install
echo "REACT_APP_API_URL=http://127.0.0.1:8000" > .env
```

---

## 💻 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions
- `chore/` - Maintenance tasks

**Examples:**
```bash
git checkout -b feature/add-export-to-pdf
git checkout -b fix/cors-configuration
git checkout -b docs/update-api-docs
```

### 2. Make Your Changes

Follow the coding standards in the next section.

### 3. Test Locally

**Backend:**
```bash
cd backend
python manage.py test
python manage.py runserver 0.0.0.0:8000
```

**Frontend:**
```bash
cd frontend
npm test
npm start
```

### 4. Commit Your Changes

See [Commit Guidelines](#commit-guidelines) section.

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

Go to the original repository and click **New Pull Request**.

---

## ✏️ Making Changes

### Backend Changes (Django/Python)

**File Organization:**
```
backend/
├── api/
│   ├── views.py          # API endpoints
│   ├── urls.py           # URL routing
│   ├── models.py         # Database models
│   ├── serializers.py    # DRF serializers (if added)
│   └── tests.py          # Unit tests
└── realestate_backend/
    ├── settings.py       # Configuration
    └── urls.py           # Main URL routing
```

**Adding a New Endpoint:**

```python
# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def new_endpoint(request):
    """
    Description of what this endpoint does.
    
    Request:
        - param1: Description
        - param2: Description
    
    Response:
        - result: Description
    """
    try:
        # Implementation
        return Response({'result': 'success'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
```

**Register in urls.py:**
```python
# api/urls.py
urlpatterns = [
    path('new-endpoint/', views.new_endpoint, name='new_endpoint'),
]
```

### Frontend Changes (React/JavaScript)

**File Organization:**
```
frontend/src/
├── App.js              # Main component
├── App.css             # Styles
├── config.js           # Configuration
├── index.js            # Entry point
└── components/         # Reusable components (if added)
```

**Creating a New Component:**

```javascript
// Example: frontend/src/components/AnalysisChart.js
import React from 'react';
import './AnalysisChart.css';

/**
 * AnalysisChart Component
 * 
 * Displays price trends for real estate areas
 * 
 * @param {Array} data - Array of chart data points
 * @param {String} title - Chart title
 * @returns {JSX} Rendered chart component
 */
const AnalysisChart = ({ data, title }) => {
  return (
    <div className="analysis-chart">
      <h3>{title}</h3>
      {/* Component logic */}
    </div>
  );
};

export default AnalysisChart;
```

**Update App.js to use it:**
```javascript
import AnalysisChart from './components/AnalysisChart';

// In render/return:
<AnalysisChart data={chartData} title="Price Trends" />
```

---

## 🎨 Coding Standards

### Python (Backend)

**Style Guide:** PEP 8

```python
# ✅ Good
def analyze_real_estate_data(area_name, price_data):
    """
    Analyze real estate data for a specific area.
    
    Args:
        area_name (str): Name of the area
        price_data (list): List of price values
    
    Returns:
        dict: Analysis results with summary and statistics
    """
    if not area_name or not price_data:
        raise ValueError("area_name and price_data are required")
    
    average_price = sum(price_data) / len(price_data)
    return {
        'area': area_name,
        'average_price': average_price,
        'count': len(price_data)
    }


# ❌ Bad
def analyze(a, p):
    return {'area': a, 'avg': sum(p)/len(p)}
```

**Key Rules:**
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use meaningful variable names
- Write docstrings for all functions and classes
- Use type hints where possible
- Follow PEP 8 style guide

**Imports Order:**
```python
# Standard library
import os
import json

# Third-party
from django.conf import settings
from rest_framework import status

# Local
from api.models import Property
```

### JavaScript (Frontend)

**Style Guide:** Airbnb JavaScript Style Guide

```javascript
// ✅ Good
const analyzeMarketData = (areaName, priceData) => {
  if (!areaName || !priceData.length) {
    throw new Error('areaName and priceData are required');
  }

  const averagePrice = priceData.reduce((a, b) => a + b) / priceData.length;
  
  return {
    area: areaName,
    averagePrice,
    count: priceData.length
  };
};

// ❌ Bad
const analyze = (a, p) => ({
  area: a,
  avg: p.reduce((x,y)=>x+y)/p.length
});
```

**Key Rules:**
- Use `const` by default, `let` when reassignment is needed
- Use arrow functions
- Use destructuring where possible
- Use meaningful variable names
- Write JSDoc comments for functions
- Use camelCase for variables and functions
- Use PascalCase for components and classes

**Example JSDoc:**
```javascript
/**
 * Fetches analysis data from backend API
 * @param {String} query - User's search query
 * @returns {Promise<Object>} Analysis results
 * @throws {Error} If API request fails
 */
const fetchAnalysis = async (query) => {
  // Implementation
};
```

### Comments & Documentation

```python
# ✅ Good - Explains WHY, not WHAT
# We retry the API call up to 3 times because it can be
# temporarily unavailable during peak hours
for attempt in range(3):
    try:
        return call_api()
    except APIError:
        continue

# ❌ Bad - Obvious from code
# Loop 3 times
for i in range(3):
    try:
        result = call_api()  # Call API
    except APIError:  # Catch error
        pass  # Continue
```

---

## 🧪 Testing

### Backend Testing

**Create Tests:**
```python
# backend/api/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class FileUploadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_upload_excel_file(self):
        """Test uploading an Excel file"""
        with open('data/Sample_data.xlsx', 'rb') as file:
            response = self.client.post(
                '/api/upload/',
                {'file': file},
                format='multipart'
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('rows', response.data)
    
    def test_upload_invalid_file(self):
        """Test uploading an invalid file type"""
        with open('test.txt', 'rb') as file:
            response = self.client.post(
                '/api/upload/',
                {'file': file},
                format='multipart'
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

**Run Tests:**
```bash
cd backend
python manage.py test
python manage.py test api.tests.FileUploadTestCase
```

### Frontend Testing

**Create Tests:**
```javascript
// frontend/src/App.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  test('renders file upload button', () => {
    render(<App />);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    expect(uploadButton).toBeInTheDocument();
  });

  test('displays error when no file selected', () => {
    render(<App />);
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    fireEvent.click(analyzeButton);
    
    expect(screen.getByText(/upload a file first/i)).toBeInTheDocument();
  });
});
```

**Run Tests:**
```bash
cd frontend
npm test
npm test -- --coverage  # With coverage report
```

---

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons)
- **refactor**: Code refactoring without changing functionality
- **test**: Adding or updating tests
- **chore**: Build process, dependencies, etc.

### Examples

```bash
# Feature
git commit -m "feat(api): add export to PDF endpoint"

# Bug fix
git commit -m "fix(cors): allow frontend requests from vercel domain"

# Documentation
git commit -m "docs(readme): update deployment instructions"

# Test
git commit -m "test(upload): add validation for file size limit"
```

### Detailed Commit

```
feat(chart): add price trend visualization

- Implement Recharts LineChart component
- Add data aggregation by year
- Format price values with currency symbol
- Add responsive design for mobile devices

Closes #42
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update your branch:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests:**
   ```bash
   # Backend
   cd backend && python manage.py test
   
   # Frontend
   cd frontend && npm test
   ```

3. **Check code quality:**
   ```bash
   # Python
   pip install flake8
   flake8 backend/
   
   # JavaScript
   npm install eslint
   npx eslint frontend/src/
   ```

### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Testing
Describe how you tested this change:
- [ ] Local testing completed
- [ ] Unit tests added
- [ ] Integration tests passed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
- [ ] `.env` files not included
- [ ] API keys not exposed

## Screenshots (if applicable)
Add screenshots of UI changes
```

### Review Process

PRs will be reviewed for:
- ✅ Code quality and standards
- ✅ Test coverage
- ✅ Documentation
- ✅ Security implications
- ✅ Performance impact

Maintainers may request changes before merging.

---

## 🐛 Reporting Issues

### Bug Report Template

```markdown
## Description
Clear description of the bug.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: Windows/Mac/Linux
- Python Version: 3.8/3.9/3.10
- Node Version: 14/16/18
- Browser: Chrome/Firefox/Safari

## Screenshots
Attach relevant screenshots.

## Additional Context
Any other context about the problem.
```

### Issue Labels

When submitting issues, use appropriate labels:
- `bug` - Something isn't working
- `enhancement` - Request for improvement
- `documentation` - Docs need updating
- `good first issue` - Good for newcomers
- `help wanted` - Need assistance

---

## 💡 Feature Requests

### Feature Request Template

```markdown
## Description
Clear description of the desired feature.

## Use Case
Why would this feature be useful?

## Proposed Solution
How should this be implemented?

## Alternatives
Any alternative approaches considered?

## Additional Context
Any other relevant information.
```

---

## 📚 Documentation

### Updating Documentation

1. **README.md** - For major changes and setup instructions
2. **CONTRIBUTING.md** - For contribution guidelines
3. **Code Comments** - For implementation details
4. **Docstrings** - For function documentation

### Documentation Style

**Python Docstring Example:**
```python
def upload_file(request):
    """
    Handle file upload for real estate data.
    
    Accepts Excel (.xlsx, .xls) or CSV files and stores
    in session for analysis.
    
    Args:
        request (HttpRequest): The HTTP request object with
            uploaded file in request.FILES['file']
    
    Returns:
        Response: JSON response with file info:
            - message (str): Success message
            - rows (int): Number of data rows
            - columns (list): Column names
            - sample_areas (list): Sample area values
    
    Raises:
        ValidationError: If file format is unsupported
        ValueError: If file is empty or corrupted
    
    Example:
        >>> response = client.post('/api/upload/', {'file': file})
        >>> response.status_code
        200
    """
    pass
```

**JavaScript JSDoc Example:**
```javascript
/**
 * Process and filter real estate data
 * 
 * Filters the uploaded dataset by area and calculates
 * statistics for analysis.
 * 
 * @param {Array<Object>} data - Raw data with area, price, year
 * @param {String} areaName - Area to filter by
 * @returns {Object} Filtered data with statistics
 * @returns {Object.average} Average price in area
 * @returns {Object.count} Number of properties
 * @returns {Object.records} Filtered records
 * 
 * @throws {TypeError} If data is not an array
 * @throws {Error} If areaName is empty
 * 
 * @example
 * const stats = processData(data, 'Wakad');
 * console.log(stats.average); // 5250000
 */
const processData = (data, areaName) => {
  // Implementation
};
```

---

## 🔒 Security Guidelines

When contributing:

- ❌ Never commit API keys or secrets
- ❌ Never hardcode credentials
- ✅ Use environment variables for secrets
- ✅ Validate all user inputs
- ✅ Sanitize data before processing
- ✅ Use HTTPS in production
- ✅ Follow security best practices

### Security Checklist

- [ ] No secrets in code
- [ ] Input validation implemented
- [ ] SQL injection protected (Django ORM used)
- [ ] XSS protection (React auto-escapes)
- [ ] CSRF tokens included (Django)
- [ ] File upload validation
- [ ] Error messages don't leak info

---

## 📞 Getting Help

- **Documentation:** Check [docs/](../docs/) folder
- **Discussions:** GitHub Discussions tab
- **Issues:** Search existing issues first
- **Email:** vighnesh@example.com

---

## 🎁 Recognition

Contributors will be:
- Listed in README.md contributors section
- Given credit in release notes
- Mentioned in project acknowledgments

---

## 📋 Quick Reference

### Common Commands

```bash
# Update your branch
git fetch upstream
git rebase upstream/main

# Create and switch to feature branch
git checkout -b feature/your-feature

# Stage and commit changes
git add .
git commit -m "feat(scope): description"

# Push to your fork
git push origin feature/your-feature

# Pull latest from upstream
git pull upstream main

# Clean up local branches
git branch -d feature/your-feature
```

### Running Project Locally

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py runserver 0.0.0.0:8000

# Terminal 2 - Frontend
cd frontend
npm start
```

### Testing Commands

```bash
# Backend tests
cd backend && python manage.py test

# Frontend tests
cd frontend && npm test

# Code quality
flake8 backend/
npx eslint frontend/src/
```

---

## 🚀 Ready to Contribute?

1. **Read** this guide thoroughly
2. **Fork** the repository
3. **Create** a feature branch
4. **Make** your changes
5. **Test** locally
6. **Commit** with clear messages
7. **Push** to your fork
8. **Create** a Pull Request

**We look forward to your contributions! 🎉**

---

**Last Updated:** December 2025

**Questions?** Open an issue or start a discussion!