# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "carbon_mrv_ghg"
app_title = "Frappe Carbon Credit Mrv Ghg Protocol Engine"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Carbon Credit Mrv Ghg Protocol Engine - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/carbon_mrv_ghg/css/carbon_mrv_ghg.bundle.css"
app_include_js = "/assets/carbon_mrv_ghg/js/carbon_mrv_ghg.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Carbon Credit Mrv Ghg Protocol Engine Entry": {
        "validate": "carbon_mrv_ghg.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "carbon_mrv_ghg.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "carbon_mrv_ghg.tasks.hourly_sync"
    ],
    "daily": [
        "carbon_mrv_ghg.tasks.daily_reconciliation"
    ],
    "weekly": [
        "carbon_mrv_ghg.tasks.weekly_digest"
    ]
}
