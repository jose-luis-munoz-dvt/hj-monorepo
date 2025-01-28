locals {
  flattened_origins = flatten([for origin, tables in var.table_origins : [for table in tables : { origin = origin, table = table, path = var.gcs_path[origin] }]])
}

resource "google_bigquery_table" "gcs_external_table" {
  for_each            = { for item in local.flattened_origins : "${item.origin}=>${item.path}=>${item.table}" => item }
  dataset_id               = each.value.origin
  deletion_protection      = true
  project                  = "pj-data-des"
  schema = file("schemas/A980.json")
  table_id = each.value.table
  external_data_configuration {
    autodetect                = false
    compression               = "GZIP"
    connection_id             = "283405604430.eu.biglake-gcs"
    ignore_unknown_values     = false
    max_bad_records           = 0
    source_format             = "CSV"
    source_uris               = ["gs://gcs-pj-data-des-data-extraction/${each.value.path}/${each.value.table}/${each.value.table}_chunk*.csv.gz"]
    csv_options {
      allow_jagged_rows     = false
      allow_quoted_newlines = false
      encoding              = "UTF-8"
      field_delimiter       = "^"
      quote                 = "\""
      skip_leading_rows     = 1
    }
  }
}
