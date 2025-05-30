data "google_project" "project" {}
data "google_client_config" "current" {}

data "google_compute_subnetwork" "subnet" {
  project = var.project
  name    = var.subnet_name # nwr-data-des
  region  = var.region
}

data "google_compute_network" "vpc" {
  project = var.project
  name    = var.vpc_name # nw-data-des-vpc
}
