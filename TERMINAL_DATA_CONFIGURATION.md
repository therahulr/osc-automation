# Terminal/Equipment Data - Environment-Based Configuration

## Overview

Implemented environment-specific terminal/equipment data loading to ensure appropriate configurations and quantities are used for PROD and QA environments.

---

## What Changed

### Before
- Single `add_terminal_data.py` file used for all environments
- Same terminal quantities regardless of environment
- Generic serial number prefixes (`TEST`)

### After
- **Two separate files**:
  - `add_terminal_data_prod.py` - Production environment
  - `add_terminal_data_qa.py` - QA environment
- **Dynamic loading** based on `ENV` variable
- **Environment-specific serial prefixes**:
  - PROD: `PROD` prefix (e.g., `PROD0B12XYGMK`)
  - QA: `QA` prefix (e.g., `QA0B12XYGMK`)
- **Appropriate quantities** for each environment

---

## File Structure

```
data/osc/
├── add_terminal_data.py          # Original (can be kept as reference)
├── add_terminal_data_prod.py     # Production terminal data (NEW)
└── add_terminal_data_qa.py       # QA terminal data (NEW)
```

---

## Terminal Configurations

### Production Environment (`ENV=prod`)

**File**: `data/osc/add_terminal_data_prod.py`

**Characteristics**:
- **Serial Prefix**: `PROD` (e.g., `PROD6XO4WBT0`)
- **Quantities**: Smaller, conservative quantities
  - Sage 50: 2 terminals
  - Sage Virtual Terminal: 1 terminal
  - Paya Connect Integrated: 2 terminals
  - Paya Gateway Level 3 / VT3: 2 terminals
  - **Total**: 7 terminals

**Purpose**: Minimal terminal configuration for production validation without creating excessive test data.

---

### QA Environment (`ENV=qa`)

**File**: `data/osc/add_terminal_data_qa.py`

**Characteristics**:
- **Serial Prefix**: `QA` (e.g., `QACCENOZNF6J`)
- **Quantities**: Larger quantities for comprehensive testing
  - Sage 50: 5 terminals
  - Sage Virtual Terminal: 3 terminals
  - Paya Connect Integrated: 4 terminals
  - Paya Gateway Level 3 / VT3: 5 terminals
  - **Total**: 17 terminals

**Purpose**: Comprehensive terminal testing with realistic volumes for QA validation.

---

## Dynamic Loading Implementation

### Location
`pages/osc/new_application_page.py`

### Implementation

```python
# Dynamic terminal data loading based on environment
def _load_terminal_data():
    """Load terminal data based on current environment."""
    from config.osc.config import osc_settings
    import importlib
    
    env = osc_settings.environment
    module_name = f"data.osc.add_terminal_data_{env}"
    
    try:
        terminal_module = importlib.import_module(module_name)
        return terminal_module
    except ImportError as e:
        # Fallback to prod data if env-specific doesn't exist
        print(f"Warning: Terminal data module '{module_name}' not found. "
              f"Falling back to 'data.osc.add_terminal_data_prod'. Error: {e}")
        return importlib.import_module("data.osc.add_terminal_data_prod")

_terminal_data = _load_terminal_data()
TERMINALS_TO_ADD = _terminal_data.TERMINALS_TO_ADD
```

### Features
- **Automatic Selection**: Loads correct file based on `ENV` variable
- **Fallback Safety**: Falls back to prod data if environment-specific file not found
- **No Code Changes Needed**: Existing code using `TERMINALS_TO_ADD` works unchanged

---

## Usage

### In Scripts

No changes needed! The terminal data is automatically loaded based on environment:

```python
from pages.osc.new_application_page import NewApplicationPage

# TERMINALS_TO_ADD is automatically loaded based on ENV
# ENV=prod → uses add_terminal_data_prod.py (7 terminals)
# ENV=qa   → uses add_terminal_data_qa.py (17 terminals)
```

### Running with Different Environments

```bash
# Use PROD terminal data (7 terminals)
ENV=prod python scripts/osc/create_credit_card_merchant.py

# Use QA terminal data (17 terminals)
ENV=qa python scripts/osc/create_credit_card_merchant.py

# Or via runner.py
python runner.py --prod create_credit_card_merchant  # 7 terminals
python runner.py --qa create_credit_card_merchant    # 17 terminals
```

---

## Serial Number Generation

### Production (`add_terminal_data_prod.py`)

```python
def generate_serial_number() -> str:
    """Generate serial number with PROD prefix."""
    random_part = ''.join(random.choices(
        string.ascii_uppercase + string.digits, 
        k=random.randint(8, 10)
    ))
    return f"PROD{random_part}"
```

**Example Output**: `PROD6XO4WBT0`, `PRODK3M9XYLZ`

### QA (`add_terminal_data_qa.py`)

```python
def generate_serial_number() -> str:
    """Generate serial number with QA prefix."""
    random_part = ''.join(random.choices(
        string.ascii_uppercase + string.digits, 
        k=random.randint(8, 10)
    ))
    return f"QA{random_part}"
```

**Example Output**: `QACCENOZNF6J`, `QA8P2MXKL9`

---

## Testing

### Test Script
`tests/test_terminal_data.py`

### What It Tests
1. ✅ Correct module is loaded for each environment
2. ✅ Serial number prefix matches environment
3. ✅ Terminal quantities are appropriate
4. ✅ Terminal configuration structure is valid

### Test Results

**PROD Environment**:
```
Environment: PROD
Module Loaded: data.osc.add_terminal_data_prod
Serial Prefix: PROD
Total Terminals: 7
Terminal Types: 4
```

**QA Environment**:
```
Environment: QA
Module Loaded: data.osc.add_terminal_data_qa
Serial Prefix: QA
Total Terminals: 17
Terminal Types: 4
```

---

## Benefits

✅ **Environment Isolation** - PROD and QA data are completely separate  
✅ **Appropriate Volumes** - Each environment has suitable quantities  
✅ **Easy Identification** - Serial prefixes clearly show environment  
✅ **Automatic Selection** - No manual configuration needed  
✅ **Backward Compatible** - Existing code works without changes  
✅ **Fallback Safety** - Graceful degradation if file missing  
✅ **Maintainable** - Easy to update quantities per environment

---

## Customization

### Adjusting Quantities

#### Production (`add_terminal_data_prod.py`)
```python
TERMINAL_QUANTITIES: List[tuple] = [
    (SAGE_50, 2),                      # Change quantity here
    (SAGE_VIRTUAL_TERMINAL, 1),
    (PAYA_CONNECT_INTEGRATED, 2),
    (PAYA_GATEWAY_LEVEL_3_VT3, 2),
]
```

#### QA (`add_terminal_data_qa.py`)
```python
TERMINAL_QUANTITIES: List[tuple] = [
    (SAGE_50, 5),                      # Change quantity here
    (SAGE_VIRTUAL_TERMINAL, 3),
    (PAYA_CONNECT_INTEGRATED, 4),
    (PAYA_GATEWAY_LEVEL_3_VT3, 5),
]
```

### Adding New Terminal Types

Add to both files:

```python
NEW_TERMINAL: Dict[str, Any] = {
    "name": "New Terminal",
    "part_type": "Gateway",
    "provider": "Sage Payment Solutions",
    "part_condition": "New",
    "part_id": "New Terminal",
    # ... other configuration
}

# Add to quantities
TERMINAL_QUANTITIES: List[tuple] = [
    # ... existing terminals
    (NEW_TERMINAL, 3),  # Add with desired quantity
]
```

---

## Migration Notes

### From Original `add_terminal_data.py`

If you were using the original file:

1. **No code changes needed** - Dynamic loading handles everything
2. **Original file can remain** - It won't be used but can serve as reference
3. **Test both environments** - Verify quantities work for your use case

### Updating Existing Scripts

No updates needed! Scripts using:
```python
from data.osc.add_terminal_data import TERMINALS_TO_ADD
```

Will automatically work with the new system because `new_application_page.py` handles the dynamic loading.

---

## Summary

| Aspect | PROD | QA |
|--------|------|-----|
| **File** | `add_terminal_data_prod.py` | `add_terminal_data_qa.py` |
| **Serial Prefix** | `PROD` | `QA` |
| **Total Terminals** | 7 | 17 |
| **Purpose** | Minimal validation | Comprehensive testing |
| **Sage 50** | 2 | 5 |
| **Sage Virtual** | 1 | 3 |
| **Paya Connect** | 2 | 4 |
| **Paya Gateway L3** | 2 | 5 |

---

## Related Documentation

- `ENV_CONFIGURATION.md` - Overall environment configuration guide
- `IMPLEMENTATION_SUMMARY.md` - Complete implementation details
- Original `add_terminal_data.py` - Reference implementation
