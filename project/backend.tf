terraform {
  backend "gcs" {
    bucket = "gcs-terraform-state-eu-pro"
    prefix = "pj-data-pro/project"
  }
}
