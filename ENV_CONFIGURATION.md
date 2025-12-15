# Environment Configuration Simplification

## Summary

The environment configuration has been simplified from three separate variables to a single `ENV` variable.

## What Changed

### Before (Old Configuration)
```bash
# Had to change in 3 places
ENV=dev
OSC_ENV=prod
OSC_DATA_ENV=prod
```

### After (New Configuration)
```bash
# Change in only 1 place!
ENV=prod  # or ENV=qa
```

## How It Works

The single `ENV` variable now controls:

1. **OSC Credentials** - Automatically selects the right credentials:
   - `ENV=prod` → Uses `OSC_USER` and `OSC_PASS` (read-only production credentials)
   - `ENV=qa` → Uses `OSC_QA_USER` and `OSC_QA_PASS` (full operations)

2. **Test Data Files** - Automatically loads the correct data file:
   - `ENV=prod` → Loads `data/osc/osc_data_prod.py`
   - `ENV=qa` → Loads `data/osc/osc_data_qa.py`

3. **Logging Level** - Sets appropriate log verbosity:
   - `ENV=prod` → INFO level logging
   - `ENV=qa` or `ENV=dev` → DEBUG level logging

4. **Submit Action Control** - Controls whether applications can be submitted:
   - `ENV=prod` → Submit is **DISABLED** (read-only mode, safe for production)
   - `ENV=qa` → Submit is **ENABLED** (full operations allowed)
   
   When submit is called in PROD environment, you'll see:
   ```
   ⚠️  SUBMIT DISABLED: Cannot submit application in PROD environment.
      Current environment: PROD
      Reason: Submit action is disabled via environment configuration.
      To enable submit: Set ENV=qa in your .env file
   ```

5. **Terminal/Equipment Data** - Loads environment-specific terminal configurations:
   - `ENV=prod` → Loads `data/osc/add_terminal_prod.py`
     - Serial numbers prefixed with `PROD` (e.g., `PROD0B12XYGMK`)
     - Smaller quantities (configurable per type)
   - `ENV=qa` → Loads `data/osc/add_terminal_qa.py`
     - Serial numbers prefixed with `QA` (e.g., `QA0B12XYGMK`)
     - Larger quantities (configurable per type for testing)

## Configuration Files

Both `.env` and `.env.example` now include credentials for both environments:

```bash
# OSC PROD credentials (READ ONLY, NO SUBMISSIONS)
OSC_USER=contractordemo
OSC_PASS=QAContractor@123

# OSC QA credentials (Full Operations)
OSC_QA_USER=ContractorQA
OSC_QA_PASS=QAContractor!123
```

## Usage

### To use Production environment (read-only):
```bash
# In .env file
ENV=prod
```

### To use QA environment (full operations):
```bash
# In .env file
ENV=qa
```

### Case Insensitive
The `ENV` variable is case-insensitive, so these all work:
- `ENV=prod`, `ENV=PROD`, `ENV=Prod`
- `ENV=qa`, `ENV=QA`, `ENV=Qa`

### Command-Line Environment Selection

You can override the `.env` file setting using command-line arguments when running `runner.py`:

```bash
# Run in PROD environment (read-only, submit disabled)
python runner.py --prod

# Run in QA environment (full operations, submit enabled)
python runner.py --qa

# Run specific script in PROD environment
python runner.py --prod create_credit_card_merchant

# Run specific script in QA environment
python runner.py --qa create_credit_card_merchant

# No flag - uses .env file setting (or defaults to QA)
python runner.py
```

**Priority Order:**
1. Command-line flag (`--prod` or `--qa`) - highest priority
2. `.env` file setting - used if no command-line flag
3. Default to `qa` - if neither is set

**Environment Display:**
The runner will display the selected environment in a prominent banner:
```
╔═══════════════════════════════════════════════════════════════╗
║                     OSC AUTOMATION RUNNER                     ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────┐
│   Environment Selected: PROD        │
└─────────────────────────────────────┘
```

### Backward Compatibility
For backward compatibility, `ENV=dev` is mapped to use production credentials (read-only mode).

## Migration Guide

If you have an existing `.env` file:

1. Open your `.env` file
2. Remove the lines:
   ```bash
   OSC_ENV=...
   OSC_DATA_ENV=...
   ```
3. Set `ENV` to either `prod` or `qa`:
   ```bash
   ENV=prod  # for production/read-only
   # OR
   ENV=qa    # for QA/full operations
   ```
4. Ensure both sets of credentials are present in your `.env` file (see `.env.example` for reference)

## Files Modified

- `.env` - Updated to use single ENV variable
- `.env.example` - Updated template
- `config/osc/config.py` - Updated to read from ENV variable
- `core/logger.py` - Updated to handle qa environment for DEBUG logging
- `pages/osc/new_application_page.py` - Added submit action control and dynamic terminal data loading
- `runner.py` - Added command-line environment selection and environment display in banner
- `data/osc/add_terminal_prod.py` - Production terminal configurations (NEW)
- `data/osc/add_terminal_qa.py` - QA terminal configurations (NEW)

## Benefits

✅ **Simpler** - Change environment in one place instead of three  
✅ **Less Error-Prone** - No risk of mismatched environment settings  
✅ **Clearer** - Single source of truth for environment configuration  
✅ **Case-Insensitive** - More forgiving configuration
