resource "google_bigquery_dataset" "raw_data" {
  dataset_id  = "raw_data"
  description = "Raw data tables from data sources"
  location    = "EU"
  project     = var.project_id
}

resource "google_bigquery_dataset" "energia" {
  dataset_id  = "energia"
  description = "Energy tables"
  location    = "EU"
  project     = var.project_id
}
