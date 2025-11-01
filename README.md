# OSC Automation Framework

OSC (Online Sales Center) automation framework using Playwright for login, navigation, and dashboard verification.

## Architecture

```
automation/
├── core/                    # App-agnostic utilities
│   ├── config.py           # Global settings
│   ├── logger.py           # Logging with console + file handlers
│   ├── browser.py          # Browser lifecycle management
│   ├── ui.py               # High-level UI interaction API
│   ├── utils.py            # Common helpers
│   └── types.py            # Type aliases
│
├── locators/osc/           # OSC-specific selectors organized by screen
├── pages/osc/              # OSC Page Objects (clean, composable)
├── config/osc/             # OSC configuration
├── scripts/osc/            # OSC automation scripts
├── data/osc/               # OSC test data (JSON)
├── logs/                   # Application logs
└── reports/                # Screenshots, reports
```

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your OSC credentials and settings
```

### 3. Run example script
```bash
python scripts/osc/verify_dashboard.py
```

Executes: Login → Dashboard → Quote navigation (with full logging & error handling).

## Development

**Format code:**
```bash
make fmt
```

**Lint & type check:**
```bash
make lint
make typecheck
```

## Adding a New App

1. Create `locators/your_app/`, `pages/your_app/`, `config/your_app/`, `scripts/your_app/`
2. Extend base page patterns for common navigation
3. Import from `core/` only—never cross-import between apps
4. Add run target in `Makefile`

---

Built with Playwright • Strong typing • DRY architecture • Extensible for multi-app flows
