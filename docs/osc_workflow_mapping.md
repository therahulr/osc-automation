# OSC Application Workflow Mapping

## Overview
This document maps the OSC (One Source Center) application workflows discovered through live browser inspection using Chrome DevTools MCP.

## New Application Workflow

### Step 1: Sales Representative Selection
- **URL Pattern**: Accessed via Applications → New Application
- **Purpose**: Select sales representative who will be assigned to the new application
- **Form Elements**:
  - Alphabetical filter links (All, A-Z)
  - List of sales representatives with:
    - Name
    - Template (e.g., "Demo Sales Office Template", "Flat Rate", "Zero Fees")
    - Permission Level (e.g., "ISO Admin", "Contractor Level")
    - Checkbox for selection
  - Pagination (page 1 of 2, etc.)
  - "Next" button to proceed

### Step 2: Existing Merchant Choice
- **Purpose**: Determine if this is a new corporation or tied to existing merchant
- **Form Elements**:
  - Radio button: "Yes, this application will be tied to a existing corporation or merchant."
  - Radio button: "No, this is a new corporation."
  - "Previous" button (to go back to Step 1)
  - "Next" button (to proceed to application form)

### Application Form Steps (Not Fully Mapped)
- After Step 2, the system proceeds to the actual application form
- This would contain merchant information, business details, processing requirements, etc.
- **Note**: Full form mapping requires additional inspection

## Work In Progress Management

### Work In Progress List
- **URL Pattern**: Accessed via Applications → Work In Progress
- **Purpose**: View and manage existing applications in progress
- **Table Columns**:
  - App ID (e.g., "312643", "312477")
  - Contractor (e.g., "DEMONET1", "DEMONET2")
  - DBA (Doing Business As name)
  - Owner / Officer 1 (Primary contact)
  - Modified Date (Last modification timestamp)
  - Action (Dropdown menu with options)

### Application Actions
Each application in the Work In Progress list has an "Action" dropdown with:
- **Edit**: Modify application details
- **Print Credit**: Generate credit application document
- **Print EFT**: Generate EFT document
- **Email**: Send application via email
- **Copy**: Duplicate application for new submission
- **Delete**: Remove application
- **Reassign**: Change assigned sales representative

## Navigation Structure

### Main Menu
- **Home**: Dashboard with application statistics
- **Applications**: 
  - Work In Progress
  - New Application
- **Library**: Document templates and resources
- **Reporting**: Various reporting functions
- **Accounting**: Financial management
- **Links**: External links
- **Configuration**: System settings

### Sidebar Menu (Always Present)
Contains the same menu structure for easy navigation between sections.

## Key Locators and Elements

### Sales Representative Selection
- Sales rep checkboxes: Individual checkboxes for each representative
- Next button: Advances to Step 2
- Alphabetical filters: A-Z links for filtering representatives

### Existing Merchant Choice
- Radio buttons: Two options for new vs. existing corporation
- Navigation buttons: Previous/Next for step control

### Work In Progress
- Action links: Expandable dropdown menus for each application
- Table headers: Sortable columns for organization
- Pagination: Multiple pages of applications

## Workflow Patterns

### New Application Flow
1. Navigate to Applications → New Application
2. Select sales representative from list
3. Choose new vs. existing corporation
4. Complete application form (steps TBD)
5. Submit for processing

### Work In Progress Management
1. Navigate to Applications → Work In Progress
2. Locate target application by App ID, Contractor, or other criteria
3. Click Action dropdown for desired application
4. Select appropriate action (Edit, Print, Email, etc.)
5. Complete action-specific workflow

## Data Requirements

### Sales Representative Data
- Representative name
- Template type
- Permission level
- Selection criteria (alphabetical, template-based, etc.)

### Application Data
- Corporation/merchant information
- Business details
- Processing requirements
- Contact information

### Work In Progress Filters
- Application ID patterns
- Contractor names
- Date ranges
- Status criteria

## Implementation Notes

### Configuration-Driven Approach
- Sales representative selection should be configurable
- Application data should come from external data files
- No hardcoded values in automation functions
- Support for multiple test scenarios and environments

### Error Handling
- Handle pagination in sales representative lists
- Validate form submissions before proceeding
- Implement retry logic for network delays
- Graceful handling of missing or changed elements

### Modularity Requirements
- Separate function for each workflow step
- Independent functions that can be combined
- Data-driven parameter passing
- Reusable components for common actions