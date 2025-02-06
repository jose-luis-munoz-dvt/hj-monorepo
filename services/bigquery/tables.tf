resource "google_bigquery_table" "gcs_external_table" {
  for_each            =  { for table in local.sap_tables: table.table_name => table }
  dataset_id          = google_bigquery_dataset.dataset[each.value.dataset_id].dataset_id
  deletion_protection = false
  project             = "pj-data-des"
  # schema              = file("schemas/${each.value.table_name}.json")
  table_id            = each.value.table_name
  external_data_configuration {
    autodetect            = true
    # compression           = "GZIP"
    connection_id         = "283405604430.eu.biglake-gcs"
    ignore_unknown_values = false
    max_bad_records       = 0
    source_format         = "PARQUET"
    source_uris           = ["gs://gcs-pj-data-des-data-extraction/${each.value.path}/${each.value.table_name}/${each.value.table_name}_chunk*.parquet"]
    # parquet_options {
    #   # allow_jagged_rows     = false
    #   # allow_quoted_newlines = false
    #   # encoding              = "UTF-8"
    #   # field_delimiter       = "^"
    #   # quote                 = "\""
    #   # skip_leading_rows     = each.value.skip_leading_rows
    # }
  }
}
