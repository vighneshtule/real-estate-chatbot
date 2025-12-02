#!/bin/bash
# Quick Sync Verification Script for Real Estate Chatbot
# This script tests that frontend and backend are properly synchronized

echo "🔍 Real Estate Chatbot - Sync Verification Script"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to check if a file exists and has content
check_file() {
    if [ -f "$1" ]; then
        if grep -q "$2" "$1"; then
            echo -e "${GREEN}✓${NC} $3"
            ((CHECKS_PASSED++))
            return 0
        else
            echo -e "${RED}✗${NC} $3 (content not found)"
            ((CHECKS_FAILED++))
            return 1
        fi
    else
        echo -e "${RED}✗${NC} $3 (file not found: $1)"
        ((CHECKS_FAILED++))
        return 1
    fi
}

echo "📋 Backend Configuration Checks"
echo "--------------------------------"

# Check settings.py
check_file "backend/realestate_backend/settings.py" "CORS_ALLOWED_ORIGINS" "CORS Origins configured"
check_file "backend/realestate_backend/settings.py" "real-estate-chatbot-kappa.vercel.app" "Frontend URL in CORS"
check_file "backend/realestate_backend/settings.py" "CSRF_TRUSTED_ORIGINS" "CSRF origins configured"
check_file "backend/realestate_backend/settings.py" "MEDIA_URL" "Media file handling configured"
check_file "backend/realestate_backend/settings.py" "FILE_UPLOAD_MAX_MEMORY_SIZE" "File upload size limit set"

# Check urls.py
check_file "backend/realestate_backend/urls.py" "static" "Media file serving configured"

# Check requirements.txt
check_file "backend/requirements.txt" "django-cors-headers" "django-cors-headers installed"
check_file "backend/requirements.txt" "djangorestframework" "djangorestframework installed"
check_file "backend/requirements.txt" "gunicorn" "gunicorn installed for production"

echo ""
echo "📋 Frontend Configuration Checks"
echo "--------------------------------"

# Check App.js
check_file "frontend/src/App.js" "API_BASE_URL = process.env.REACT_APP_API_URL" "API_BASE_URL uses environment variable"
check_file "frontend/src/App.js" "real-estate-chatbot-ev0r.onrender.com" "Backend URL configured as fallback"
check_file "frontend/src/App.js" "timeout: 30000" "Upload timeout configured"
check_file "frontend/src/App.js" "console.log" "Console logging added for debugging"

# Check .env file exists
if [ -f "frontend/.env" ]; then
    if grep -q "REACT_APP_API_URL" "frontend/.env"; then
        echo -e "${GREEN}✓${NC} .env file configured with API URL"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} .env file exists but missing REACT_APP_API_URL"
        ((CHECKS_FAILED++))
    fi
else
    echo -e "${YELLOW}⚠${NC} .env file not found (needed for production)"
    ((CHECKS_FAILED++))
fi

# Check config.js
check_file "frontend/src/config.js" "backendURL" "config.js created with backend URL"

echo ""
echo "📋 Security Checks"
echo "-------------------"

# Check .gitignore
check_file ".gitignore" ".env" ".env files excluded from git"
check_file ".gitignore" "__pycache__" "Python cache excluded"
check_file ".gitignore" "node_modules" "node_modules excluded"

# Check CORS is restricted
if grep -q "CORS_ALLOW_ALL_ORIGINS = False" "backend/realestate_backend/settings.py"; then
    echo -e "${GREEN}✓${NC} CORS is restricted to specific origins (secure)"
    ((CHECKS_PASSED++))
else
    echo -e "${RED}✗${NC} CORS might be allowing all origins (security risk)"
    ((CHECKS_FAILED++))
fi

echo ""
echo "📋 Git & Deployment Checks"
echo "---------------------------"

# Check if git repo exists
if [ -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git repository initialized"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Git repository not initialized"
fi

# Check for render.yaml
if [ -f "render.yaml" ]; then
    echo -e "${GREEN}✓${NC} render.yaml found for Render.com deployment"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} render.yaml not found (optional for Render.com)"
fi

echo ""
echo "📊 Summary"
echo "==========="
echo -e "Checks Passed: ${GREEN}$CHECKS_PASSED${NC}"
echo -e "Checks Failed: ${RED}$CHECKS_FAILED${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Your frontend and backend are properly synchronized.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run local tests: See LOCAL_TESTING_GUIDE.md"
    echo "2. Push to GitHub: git add . && git commit -m 'Sync frontend and backend' && git push"
    echo "3. Monitor deployments in Render.com and Vercel dashboards"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please review the issues above.${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check SYNC_DEPLOYMENT_GUIDE.md for detailed instructions"
    echo "2. Review the files mentioned in the failed checks"
    echo "3. Ensure all configuration files are in place"
    exit 1
fi