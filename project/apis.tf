resource "google_project_service" "services" {
  for_each = toset([
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
  service                    = each.key
  disable_dependent_services = true
  disable_on_destroy         = true
  project                    = google_project.pj_data_des.id
}
