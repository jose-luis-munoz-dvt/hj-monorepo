terraform {
  backend "gcs" {
    bucket = "gcs-terraform-state-eu-pro"
    prefix =  "pj-data-des/services/orchestrator" #"pj-data-pro/services/orchestrator" 
  }
}