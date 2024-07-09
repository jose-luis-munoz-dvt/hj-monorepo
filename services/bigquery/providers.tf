terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = "pj-data-des"
  region  = "europe-southwest1"
  zone    = "europe-southwest1-a"
}
