# Performance Analyzer Documentation

## Overview

The Performance Analyzer provides comprehensive automation performance tracking and analysis capabilities. It automatically captures timing data, success rates, browser metrics, and step-by-step execution details for all automation scripts.

## Quick Start

### 1. Enable Performance Tracking in Scripts

```python
from core.performance_decorators import PerformanceSession

def my_automation_script():
    # Wrap your entire automation workflow
    with PerformanceSession(
        script_name="my_automation",
        environment="production",  # Optional
        browser_type="chromium",   # Optional
        tags=["regression", "api"] # Optional
    ) as session:
        # Your existing automation code - no changes needed!
        with BrowserManager() as browser:
            page = browser.get_page()
            # All actions automatically tracked
```

### 2. View Performance Reports

```python
from core.performance_analysis import print_summary_report

# Quick console report for last 7 days
print_summary_report(days=7)
```

## Core Functions

### Summary Reports

#### `print_summary_report(days=7)`
Prints a formatted performance summary to console.

```python
from core.performance_analysis import print_summary_report

print_summary_report(days=30)  # Last 30 days
```

**Output:**
```
============================================================
AUTOMATION PERFORMANCE SUMMARY (30 days)
============================================================
Total Runs: 45
Success Rate: 97.8%
Average Duration: 23.45s
Total Steps Executed: 1,234
Unique Scripts: 8

Script Performance:
Name                           Runs     Avg Duration Success Rate
--------------------------------------------------------------
create_credit_card_merchant    12       27.23        100.0%
user_registration              8        15.67        95.0%
```

#### `quick_summary(days=7)` → Dict
Returns summary data as a dictionary for programmatic use.

```python
from core.performance_analysis import quick_summary

summary = quick_summary(days=14)
print(f"Success rate: {summary['overall_statistics']['success_rate']}%")
```

### Script Analysis

#### `analyze_script(script_name, days=30)` → Dict
Detailed performance trends for a specific script.

```python
from core.performance_analysis import analyze_script

trends = analyze_script("create_credit_card_merchant", days=30)
print(f"Average duration: {trends['step_analysis'][0]['avg_duration']}s")
```

**Returns:**
- Daily performance trends
- Step-by-step analysis 
- Success rate trends
- Duration patterns

### Bottleneck Detection

#### `find_bottlenecks(min_duration=5.0)` → List[Dict]
Identifies performance bottlenecks across all scripts.

```python
from core.performance_analysis import find_bottlenecks

# Find steps taking longer than 10 seconds
bottlenecks = find_bottlenecks(min_duration=10.0)

for bottleneck in bottlenecks:
    print(f"⚠️  {bottleneck['step_name']}: {bottleneck['avg_duration']}s")
```

## Advanced Usage

### PerformanceAnalyzer Class

For advanced analysis, use the `PerformanceAnalyzer` class directly:

```python
from core.performance_analysis import PerformanceAnalyzer

analyzer = PerformanceAnalyzer()

# Get recent runs
runs = analyzer.get_recent_runs(days=7, script_name="my_script")

# Get detailed run information
latest_run = runs[0]
details = analyzer.get_run_details(latest_run['id'])

print(f"Steps: {len(details['steps'])}")
print(f"Browser metrics: {len(details['browser_metrics'])}")
```

### Key Methods

#### `get_recent_runs(days=7, script_name=None)` → List[Dict]
Retrieve recent automation runs with basic metrics.

```python
# All runs in last 7 days
all_runs = analyzer.get_recent_runs(days=7)

# Specific script runs
script_runs = analyzer.get_recent_runs(days=30, script_name="login_test")
```

#### `get_run_details(run_id)` → Dict
Get comprehensive details for a specific run.

```python
details = analyzer.get_run_details(run_id)

# Access different metrics
run_info = details['run_info']          # Overall run data
steps = details['steps']                # Step-by-step breakdown  
browser_metrics = details['browser_metrics']  # Page load times, etc.
```

#### `get_performance_trends(script_name, days=30)` → Dict
Analyze performance trends over time.

```python
trends = analyzer.get_performance_trends("my_script", days=60)

# Daily trends
for day in trends['daily_trends']:
    print(f"{day['date']}: {day['avg_duration']}s ({day['success_rate']}%)")

# Step analysis
for step in trends['step_analysis']:
    print(f"{step['step_name']}: avg {step['avg_duration']}s")
```

#### `identify_bottlenecks(script_name=None, min_duration=5.0)` → List[Dict]
Find performance bottlenecks.

```python
# All bottlenecks across scripts
all_bottlenecks = analyzer.identify_bottlenecks(min_duration=8.0)

# Script-specific bottlenecks  
script_bottlenecks = analyzer.identify_bottlenecks(
    script_name="checkout_flow", 
    min_duration=3.0
)
```

### Data Export

#### `export_data(output_file, format='json', days=30)`
Export performance data to file.

```python
analyzer.export_data(
    output_file="reports/performance_report.json",
    format="json",
    days=30
)
```

## Integration Examples

### Browser-Level Tracking

Performance tracking is automatically enabled in `BrowserManager`:

```python
# Automatic browser metrics collection
with BrowserManager(enable_performance_tracking=True) as browser:
    page = browser.get_page()
    # Page loads, navigation, clicks automatically tracked
```

### Step-Level Tracking

Use decorators for granular step tracking:

```python
from core.performance_decorators import performance_step

@performance_step("User Login", "action") 
def login_user(username, password):
    # Function automatically tracked with custom name
    pass

# Or use context manager
from core.performance_decorators import track_step

with track_step("Data Validation", "verification"):
    # Code block automatically tracked
    validate_user_data()
```

### Enhanced Existing Decorators

Existing decorators automatically integrate when performance session is active:

```python
@timeit  # Now includes performance tracking
@log_step  # Now includes step metrics
def process_application():
    # Existing code unchanged, but now tracked
    pass
```

## Database Schema

Performance data is stored in SQLite at `data/performance.db`:

- **`automation_runs`** - Complete workflow sessions
- **`step_metrics`** - Individual step performance
- **`browser_metrics`** - Page load and navigation timing  
- **`action_metrics`** - Micro-level action tracking

## Best Practices

### 1. Use Descriptive Names
```python
with PerformanceSession("user_registration_e2e_test"):
    # Clear, descriptive script names for better reporting
```

### 2. Add Meaningful Tags
```python
with PerformanceSession(
    script_name="checkout_flow",
    tags=["payment", "critical", "e2e"],
    environment="staging"
):
    # Tags help filter and organize performance data
```

### 3. Regular Analysis
```python
# Set up regular performance monitoring
def weekly_performance_check():
    bottlenecks = find_bottlenecks(min_duration=5.0)
    if bottlenecks:
        send_alert(f"Found {len(bottlenecks)} performance bottlenecks")
```

### 4. Track Environment Impact
```python
# Compare performance across environments
prod_trends = analyze_script("critical_flow", days=30)
# Deploy to staging, then compare
staging_trends = analyze_script("critical_flow", days=7)
```

## Troubleshooting

### No Data Captured
- Ensure `PerformanceSession` wraps your automation code
- Check that `BrowserManager` has `enable_performance_tracking=True`
- Verify database exists at `data/performance.db`

### Missing Step Details
- Add `@performance_step` decorators to functions you want to track
- Use `track_step` context manager for code blocks
- Existing `@timeit` and `@log_step` automatically integrate

### Export Issues
```python
# Check database path
analyzer = PerformanceAnalyzer()
print(f"Database: {analyzer.db_path}")
print(f"Exists: {analyzer.db_path.exists()}")
```

## Example: Complete Performance Monitoring Setup

```python
from core.performance_decorators import PerformanceSession, performance_step
from core.performance_analysis import print_summary_report, find_bottlenecks

@performance_step("Environment Setup", "setup")
def setup_test_data():
    # Setup code automatically tracked
    pass

def run_automation_with_monitoring():
    with PerformanceSession(
        script_name="complete_user_flow",
        environment="production",
        tags=["regression", "critical"],
        notes="Full user registration and verification flow"
    ) as session:
        
        setup_test_data()
        
        with BrowserManager(enable_performance_tracking=True) as browser:
            page = browser.get_page()
            # All browser actions automatically tracked
            
    # Generate report after run
    print_summary_report(days=1)
    
    # Check for new bottlenecks
    bottlenecks = find_bottlenecks(min_duration=10.0)
    if bottlenecks:
        print(f"⚠️  Found {len(bottlenecks)} bottlenecks to investigate")
```

This setup provides comprehensive performance monitoring with minimal code changes and maximum insight into your automation performance.