# OSC Automation Framework

Production-grade, modular Playwright (Python) automation framework for multi-app workflow orchestration.

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
├── apps/osc/               # OSC application implementation
│   ├── config.py           # OSC-specific settings
│   ├── locators/           # Selectors organized by screen
│   ├── pages/              # Page Objects (clean, composable)
│   ├── data/               # Test data (JSON)
│   ├── scripts/            # Automation scripts
│   ├── logs/               # Application logs
│   └── reports/            # Screenshots, reports
│
└── pyproject.toml          # Dependencies + tooling config
```

**Future apps** (e.g., `apps/c2a/`) follow the same structure—no changes needed in `core/`.

## Quick Start

### 1. Install dependencies
```bash
make install
```

This installs Python packages and Playwright browsers (Chromium).

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your OSC credentials and settings
```

### 3. Run example script
```bash
make run-osc-login
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

1. Create `apps/your_app/` with: `config.py`, `locators/`, `pages/`, `data/`, `scripts/`
2. Extend `OSCBasePage` pattern for common navigation
3. Import from `core/` only—never cross-import between apps
4. Add run target in `Makefile`

---

Built with Playwright • Strong typing • DRY architecture • Extensible for multi-app flows
