# Terminal Discovery Script - Navigation Fix

## Issue Identified

The script was using `fill_step_1()` which only fills the form fields but doesn't click the Next button, causing it to get stuck on Step 1.

## Fix Applied

Changed from:
```python
if not add_terminal_page.fill_step_1(temp_config):
    logger.error("Failed to fill Step 1, skipping combination")
    ...
    continue

# Click Next to Step 2
try:
    page.click("#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnNext1")
    time.sleep(2)
except Exception as e:
    ...
```

To:
```python
if not add_terminal_page.complete_step_1(temp_config):
    logger.error("Failed to complete Step 1, skipping combination")
    ...
    continue

# Now on Step 2 - extract Part IDs (complete_step_1 already navigated)
part_ids = extract_part_ids(page)
```

## Why This Works

- `complete_step_1()` fills the fields **AND** clicks Next button
- It waits for Step 2 header to verify navigation succeeded
- Returns `True` only when Step 2 is confirmed visible
- No need for manual Next button click

## Verification Strategy

As per user's guidance:
- Step 1 complete = Step 2 header verified ✅
- Step 2 complete = Step 3 header verified ✅
- Step 3 complete = Step 4 header verified ✅
- etc.

Each `complete_step_X()` method already implements this verification pattern.

## Status

✅ **Fixed and ready to run**

The script will now properly navigate through all wizard steps.
