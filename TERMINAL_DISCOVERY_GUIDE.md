# Terminal Discovery Script - Usage Guide

## Overview

The `discover_valid_terminals.py` script systematically tests all Part Type and Provider combinations to identify which terminals can be successfully added in the OSC application.

## Purpose

This is a **one-time discovery script** to:
- Identify all valid terminal combinations
- Document available Part IDs for each combination
- Test terminal addition through all 6 wizard steps
- Record success/failure results in JSON format

## Usage

### Running the Script

```bash
# Via runner.py (recommended)
python runner.py discover_valid_terminals

# Or directly
python scripts/osc/discover_valid_terminals.py
```

### What It Does

1. **Logs in** to OSC
2. **Navigates** to existing application (ID: 313320)
3. **Tests 12 combinations** (4 Part Types × 3 Providers):
   - Software + Merchant
   - Software + Sage Payment Solutions
   - Software + ISO
   - V Terminal + Merchant
   - V Terminal + Sage Payment Solutions
   - V Terminal + ISO
   - Terminal/Printer + Merchant
   - Terminal/Printer + Sage Payment Solutions
   - Terminal/Printer + ISO
   - Gateway + Merchant
   - Gateway + Sage Payment Solutions
   - Gateway + ISO

4. **For each combination**:
   - Opens Terminal Wizard
   - Selects Part Type and Provider
   - Extracts all available Part IDs from Step 2 grid
   - Tests adding each Part ID through all 6 steps
   - Handles incompatible terminals (disabled Next button)
   - Verifies successful addition in equipment table
   - Records results in JSON

## Output

### JSON Results File

**Location**: `data/osc/valid_prod_parts_osc.json`

**Structure**:
```json
{
  "discovery_date": "2025-12-15T09:35:00",
  "application_id": "313320",
  "total_combinations": 12,
  "combinations_tested": 12,
  "total_parts_found": 150,
  "total_parts_tested": 150,
  "successful_parts": 120,
  "failed_parts": 30,
  "combinations": {
    "Software_Merchant": {
      "part_type": "Software",
      "provider": "Merchant",
      "available_parts": ["Part1", "Part2", "Part3"],
      "valid_parts": {
        "Part1": {
          "status": "success",
          "notes": "Terminal added successfully",
          "failed_at_step": null
        },
        "Part2": {
          "status": "failed",
          "notes": "Incompatible - Next button disabled at Step 3",
          "failed_at_step": 3
        }
      }
    }
  }
}
```

### Result Status

- **success**: Terminal added successfully and verified in equipment table
- **failed**: Terminal could not be added (see notes for reason)

### Failure Reasons

- "Incompatible - Next button disabled at Step 3" - Terminal not compatible
- "Failed at Step X" - Error during wizard step
- "Part ID not found or not selectable" - Part not available in grid
- "Terminal not found in equipment table after addition" - Addition failed

## Execution Time

- **Estimated**: 2-4 hours (depends on number of terminals)
- **Per combination**: ~10-20 minutes
- **Per terminal**: ~30-60 seconds

## Progress Tracking

- Results saved after each terminal test
- Can resume if interrupted (checks existing results)
- Real-time logging to console and log file

## After Discovery

1. **Review results** in `valid_prod_parts_osc.json`
2. **Update terminal data files** (`add_terminal_prod.py`, `add_terminal_qa.py`)
3. **Use valid terminals** in automation scripts

## Notes

- Script uses existing `AddTerminalPage` methods (no modifications needed)
- Handles wizard timeouts and retries
- Automatically closes wizard on incompatible terminals
- Safe to run multiple times (updates existing results)
