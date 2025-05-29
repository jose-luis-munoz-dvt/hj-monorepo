terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  region  = "europe-southwest1"
  zone    = "europe-southwest1-a"
}
