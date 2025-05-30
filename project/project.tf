resource "google_project" "pj_data" {
  name                = var.project_name
  project_id          = var.project_id
  folder_id           = var.folder_id
  billing_account     = var.billing_account
  auto_create_network = var.auto_create_network
}

# module "projects" {
#   source   = "terraform-google-modules/project-factory/google"
#   for_each = var.projects

#   name                    = each.value.name
#   org_id                  = each.value.org_id
#   folder_id               = each.value.folder_id
#   billing_account         = each.value.default_service_account
#   default_service_account = "delete"
#   create_project_sa       = true
#   project_sa_name         = each.value.project_sa_name
#   activate_apis           = each.value.activate_apis
# }