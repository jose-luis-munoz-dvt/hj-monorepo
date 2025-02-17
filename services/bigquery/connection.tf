resource "google_bigquery_connection" "connection" {
   connection_id = "biglake-gcs"
   location      = "EU"
   cloud_resource {}
}

resource "google_project_iam_member" "object_user" {
  project = var.project_id
  role    = "roles/storage.objectUser"
  member  = "serviceAccount:${google_bigquery_connection.connection.cloud_resource[0].service_account_id}"
}

