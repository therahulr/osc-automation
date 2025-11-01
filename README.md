# OSC Automation Framework

Production-grade Playwright automation framework for OSC (Online Sales Center) with environment-aware configuration and safety controls.

## 🏗️ Project Structure

```
automation/
├── core/                    # Framework utilities
│   ├── browser.py          # Browser lifecycle management
│   ├── config.py           # Global settings
│   ├── logger.py           # Logging with file + console
│   ├── ui.py               # High-level UI interaction API
│   ├── utils.py            # Common helpers
│   └── types.py            # Type definitions
│
├── config/osc/             # OSC-specific configuration
│   └── config.py           # Environment-aware settings
│
├── locators/osc/           # Element selectors
│   └── osc_locators.py     # Organized by page classes
│
├── pages/osc/              # Page objects
│   ├── base_page.py        # Base page with common functionality
│   ├── login_page.py       # Login workflow
│   └── dashboard_page.py   # Dashboard operations
│
├── scripts/osc/            # Automation scripts
│   ├── check_environment.py    # Environment validation
│   ├── verify_dashboard.py     # Login + dashboard verification
│   └── main.py                 # Complete automation workflow
│
├── data/osc/               # Test data and configurations
├── logs/                   # Application logs
├── traces/                 # Screenshots and artifacts
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone https://github.com/therahulr/osc-automation.git
cd osc-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Settings
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Key settings:
# - OSC_ENV=prod (for development) or qa (for production)
# - HEADLESS=false (to see browser during development)
```

### 3. Validate Environment
```bash
# Check configuration and credentials
python scripts/osc/check_environment.py
```

### 4. Run Automation
```bash
# Basic dashboard verification
python scripts/osc/verify_dashboard.py

# Run with visible browser (for debugging)
HEADLESS=false python scripts/osc/verify_dashboard.py
```

## 🛡️ Environment Safety

### PROD Environment (Development Only)
- **Credentials**: `contractordemo / QAContractor@123`
- **Purpose**: Automation development and testing
- **Safety**: **READ-ONLY** - No data submission allowed
- **Config**: `OSC_ENV=prod` in `.env` file

### QA Environment (Production Use)
- **Credentials**: `ContractorQA / QAContractor!123`  
- **Purpose**: Actual business operations
- **Safety**: Full operations allowed
- **Config**: `OSC_ENV=qa` in `.env` file

⚠️ **Important**: Always run `python scripts/osc/check_environment.py` to verify you're in the correct environment before automation.

## 🔄 Development Workflow

### Development Machine Workflow
```bash
# 1. Ensure PROD environment (safe for development)
echo "OSC_ENV=prod" >> .env

# 2. Validate environment
python scripts/osc/check_environment.py

# 3. Develop and test (READ-ONLY operations)
HEADLESS=false python scripts/osc/verify_dashboard.py

# 4. Commit and push changes
git add .
git commit -m "feat: add new automation feature"
git push origin main
```

### Production Machine Workflow
```bash
# 1. Pull latest changes
git pull origin main

# 2. Switch to QA environment
echo "OSC_ENV=qa" >> .env

# 3. Validate environment
python scripts/osc/check_environment.py

# 4. Run automation with full capabilities
python scripts/osc/verify_dashboard.py
```

## 🧪 Available Scripts

| Script | Purpose | Environment |
|--------|---------|-------------|
| `scripts/osc/check_environment.py` | Validate configuration and show safety status | Any |
| `scripts/osc/verify_dashboard.py` | Complete login + dashboard verification | Any |
| `scripts/osc/main.py` | Main automation workflow | Any |

## 🔧 Configuration Reference

### Environment Variables (.env)
```bash
# Browser settings
HEADLESS=false
INCOGNITO=true
SLOW_MO_MS=100
DEFAULT_TIMEOUT_MS=30000

# Environment configuration
OSC_ENV=prod                    # 'prod' or 'qa'

# OSC application settings
OSC_BASE_URL=https://uno.eftsecure.net/SalesCenter
OSC_LOGIN_PATH=/frmHome.aspx

# PROD credentials (Development - READ ONLY)
OSC_USER=contractordemo
OSC_PASS=QAContractor@123

# QA credentials (Production - Full Operations)
OSC_QA_USER=ContractorQA
OSC_QA_PASS=QAContractor!123
```

### Command Line Options
```bash
# Run with visible browser
HEADLESS=false python scripts/osc/verify_dashboard.py

# Enable debug logging
ENV=dev python scripts/osc/verify_dashboard.py

# Combine options
HEADLESS=false ENV=dev python scripts/osc/verify_dashboard.py
```

## 🏗️ Extending the Framework

### Adding New Pages
1. Create page object in `pages/osc/new_page.py`
2. Extend `OSCBasePage` for common functionality
3. Add locators to `locators/osc/osc_locators.py`
4. Create automation scripts in `scripts/osc/`

### Adding New Applications
1. Create `config/new_app/`, `pages/new_app/`, `locators/new_app/`
2. Follow the same pattern as OSC implementation
3. Import only from `core/` - no cross-app dependencies

## 🛠️ Development Commands

```bash
# Environment validation
python scripts/osc/check_environment.py

# Format code
black .
isort .

# Type checking
mypy core/ config/ pages/ scripts/

# Linting
flake8 core/ config/ pages/ scripts/
```

## 📚 Key Features

- **Environment Safety**: Automatic credential management with read-only development mode
- **Production Ready**: Comprehensive logging, error handling, and screenshot capture
- **Modular Design**: Clean separation of concerns with reusable components
- **Type Safety**: Full type hints and mypy compatibility
- **Browser Management**: Automated browser lifecycle with context isolation
- **Visual Debugging**: Configurable headless/visible modes for development

## 🤝 Contributing

1. Use PROD environment for development (read-only operations)
2. Test thoroughly before committing
3. Follow existing code patterns and type hints
4. Validate environment before running scripts
5. Keep development and production environments separate

---

**Built with Playwright • Python • Type Safety • Production Grade**
