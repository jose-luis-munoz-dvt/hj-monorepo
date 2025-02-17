locals {
  sap_datasets = { for bq_object in var.bq_sap: bq_object.dataset => bq_object }
  non_sap_datasets = { for bq_object in var.bq_datasets: bq_object.dataset => bq_object }
  sap_tables = flatten([for dataset_name, dataset in local.sap_datasets: [for table in dataset.tables: { table_name = table, dataset_id = dataset_name, path = dataset.storage_path }]])
}
