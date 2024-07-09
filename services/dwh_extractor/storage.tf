resource "google_storage_bucket" "regional_bucket" {
  project                  = var.project_id
  name                     = "gcs-${var.project_id}-data-extraction"
  location                 = "europe-southwest1"
  storage_class            = "STANDARD"
  force_destroy            = false
  public_access_prevention = "enforced"

  lifecycle_rule {
    condition {
      age            = 1
      matches_prefix = ["backup/"]
    }
    action {
      type = "Delete"
    }
  }
}
