project_name    = "pj-data-pro" #
project_id      = "pj-data-pro" #
folder_id       = "250601392705"
billing_account = "010B71-8B4F43-739548"
##

gcp_api_services = toset([
  "compute.googleapis.com",
  "iap.googleapis.com",
  "servicenetworking.googleapis.com",
  "dataform.googleapis.com",
  "cloudfunctions.googleapis.com",
  "bigquery.googleapis.com",
  "workflows.googleapis.com",
  "run.googleapis.com",
  "cloudscheduler.googleapis.com",
  "vpcaccess.googleapis.com",
  "secretmanager.googleapis.com"
])



# projects = [{
#   name            = string
#   org_id          = string
#   folder_id       = string
#   billing_account = string
#   project_sa_name = optional(string, "")
# activate_apis = optional(list(string), []) }]
