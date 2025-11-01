# Development Workflow Guide

This document outlines the proper development workflow for maintaining code here while running in different environments.

## 🏗️ Development Setup

### Local Development (This Machine)
- **Environment**: PROD (contractordemo credentials)  
- **Purpose**: Code development, automation testing, locator verification
- **Safety**: READ-ONLY - Never submit/save data in PROD
- **Configuration**: `OSC_ENV=prod` in `.env` file

### Org Laptop Production Use
- **Environment**: QA (ContractorQA credentials)
- **Purpose**: Actual business operations, data submission, saving
- **Safety**: Full operations allowed
- **Configuration**: `OSC_ENV=qa` in `.env` file

## 🔄 Workflow Process

### 1. Development Phase (This Machine)
```bash
# Ensure PROD environment
echo "OSC_ENV=prod" >> .env

# Validate environment
python scripts/osc/check_environment.py

# Develop and test automation (READ-ONLY)
python scripts/osc/verify_dashboard.py

# Commit and push changes
git add .
git commit -m "feat: add new automation feature"
git push origin main
```

### 2. Deployment Phase (Org Laptop)
```bash
# Pull latest changes
git pull origin main

# Switch to QA environment
echo "OSC_ENV=qa" >> .env

# Validate environment
python scripts/osc/check_environment.py

# Run automation with full operations
python scripts/osc/verify_dashboard.py
```

## ⚠️ Safety Guidelines

### PROD Environment (Development)
- ✅ Navigate pages, inspect elements
- ✅ Test login flows, verify selectors
- ✅ Take screenshots, capture logs
- ❌ **NEVER** submit forms with data
- ❌ **NEVER** save applications/quotes
- ❌ **NEVER** modify any business data

### QA Environment (Org Laptop)
- ✅ All development activities
- ✅ Submit applications and quotes
- ✅ Save and modify business data
- ✅ Full end-to-end testing

## 🔧 Environment Validation

Always run environment check before automation:
```bash
python scripts/osc/check_environment.py
```

This will show:
- Current environment (prod/qa)
- Safety status (read-only vs full operations)
- Active credentials
- Environment-specific warnings

## 📁 File Organization

### Environment-Specific Files
- `.env` - Environment configuration (not committed)
- `config/osc/config.py` - Environment-aware credential management

### Shared Code (Version Controlled)
- `locators/osc/` - Element selectors
- `pages/osc/` - Page objects
- `scripts/osc/` - Automation scripts
- `core/` - Framework components

## 🚀 Quick Commands

```bash
# Check environment
make check-env  # or python scripts/osc/check_environment.py

# Run in PROD (development)
OSC_ENV=prod python scripts/osc/verify_dashboard.py

# Run in QA (org laptop)
OSC_ENV=qa python scripts/osc/verify_dashboard.py

# Visual debugging (any environment)
HEADLESS=false python scripts/osc/verify_dashboard.py
```

## 🔐 Credentials Reference

| Environment | Username | Password | Purpose |
|-------------|----------|----------|---------|
| PROD | contractordemo | QAContractor@123 | Development (READ-ONLY) |
| QA | ContractorQA | QAContractor!123 | Business Operations |

## 📝 Best Practices

1. **Always validate environment** before running scripts
2. **Keep development on PROD** to avoid accidental data changes
3. **Use QA only on org laptop** for actual business work
4. **Commit frequently** to maintain sync between machines
5. **Test thoroughly in PROD** before deploying to QA