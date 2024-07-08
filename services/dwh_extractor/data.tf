data "google_project" "project" {}
data "google_client_config" "current" {}

data "google_compute_subnetwork" "subnet" {
  project = "pj-hub-pro"
  name    = "nwr-data-des"
  region  = "europe-southwest1"
}

data "google_compute_network" "vpc" {
  project = "pj-hub-pro"
  name    = "nw-data-des-vpc"
}
