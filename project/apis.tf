resource "google_project_service" "services" {
  for_each                   = var.gcp_api_services
  service                    = each.key
  disable_dependent_services = true
  disable_on_destroy         = true
  project                    = google_project.pj_data.id
}
