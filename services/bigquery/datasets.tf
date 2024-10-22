resource "google_bigquery_dataset" "raw_data" {
  dataset_id  = "raw_data"
  description = "Raw data tables from data sources"
  location    = "EU"
  project     = var.project_id
}
resource "google_bigquery_dataset" "d_hechos" {
  dataset_id  = "d_hechos"
  description = "Tablas de hechos "
  location    = "EU"
  project     = var.project_id
}
resource "google_bigquery_dataset" "d_staging" {
  dataset_id  = "d_staging"
  description = "Tablas staging"
  location    = "EU"
  project     = var.project_id
}

resource "google_bigquery_dataset" "origen_simatic" {
  dataset_id  = "origen_simatic"
  description = "Tablas extraidas de Simatic SQL Server"
  location    = "EU"
  project     = var.project_id
}
resource "google_bigquery_dataset" "origen_circutor" {
  dataset_id  = "origen_circutor"
  description = "Tablas extraidas de Circutor SQL Server"
  location    = "EU"
  project     = var.project_id
}
resource "google_bigquery_dataset" "origen_drive" {
  dataset_id  = "origen_drive"
  description = "Tablas extraidas de Google Drive"
  location    = "EU"
  project     = var.project_id
}
resource "google_bigquery_dataset" "origen_sap" {
  dataset_id  = "origen_sap"
  description = "Tablas extraidas de SAP"
  location    = "EU"
  project     = var.project_id
}
resource "google_bigquery_dataset" "origen_neolectra" {
  dataset_id  = "origen_neolectra"
  description = "Tablas extraidas del sharepoint de neolectra"
  location    = "EU"
  project     = var.project_id
}
