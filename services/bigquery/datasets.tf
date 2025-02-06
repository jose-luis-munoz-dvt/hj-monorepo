resource "google_bigquery_dataset" "dataset" {
  for_each = merge(local.sap_datasets, local.non_sap_datasets)
  dataset_id  = each.value.dataset
  description = each.value.description
  location    = try(each.value.location, "EU")
  project     = var.project_id
}

# resource "google_bigquery_dataset" "non_sap_datasets" {
#   for_each = local.non_sap_datasets
#   dataset_id  = "${each.value.dataset}_T"
#   description = each.value.description
#   location    = each.value.location
#   project     = var.project_id
# }
