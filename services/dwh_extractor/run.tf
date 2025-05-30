locals {
  tables             = flatten([for origin, tbls in var.tables : [for tbl in tbls : { origin = origin, table = tbl, extractor = var.origins[origin] }]])
  high_memory_tables = ["LIPS", "VEKP", "MSEG", "QAMV", "EKBE", "EKPO", "KONV", "VBRP", "EKKO", "LIKP", "VBAP", "NSDM_V_MSEG", "PRCD_Elements"]
  incremental_tables = ["MSEG", "NSDM_V_MSEG"]
  incremental_timestamp_source = {
    MSEG        = "${var.project_id}.d_staging.MSEG_CLEAN",
    NSDM_V_MSEG = "${var.project_id}.d_staging.MSEG_CLEAN"
  }
  incremental_field = {
    MSEG        = "CONCAT(CPUDT_MKPF, CPUTM_MKPF)",
    NSDM_V_MSEG = "CONCAT(CPUDT_MKPF, CPUTM_MKPF)"
  }
}

resource "google_project_iam_member" "vpc_access_perm" {
  for_each = toset([
    "serviceAccount:service-${data.google_project.project.number}@gcp-sa-vpcaccess.iam.gserviceaccount.com",
    "serviceAccount:${data.google_project.project.number}@cloudservices.gserviceaccount.com",
    "serviceAccount:service-${data.google_project.project.number}@serverless-robot-prod.iam.gserviceaccount.com"
  ])
  project = data.google_compute_network.vpc.project
  role    = var.run_role
  member  = each.key
}

resource "google_cloud_run_v2_job" "job" {
  for_each            = { for tbl in local.tables : "${tbl.extractor}_${tbl.origin}_${tbl.table}" => tbl }
  name                = replace(lower("crj-data-extractor-${each.value.origin}-${each.value.table}"), "_", "-")
  location            = data.google_client_config.current.region
  deletion_protection = false

  template {
    template {
      containers {
        image = "europe-southwest1-docker.pkg.dev/${data.google_client_config.current.project}/${google_artifact_registry_repository.ar_repo.name}/data_extractor:latest"
        resources {
          limits = {
            cpu    = contains(local.high_memory_tables, each.value.table) ? "4000m" : "2000m"
            memory = contains(local.high_memory_tables, each.value.table) ? "16Gi" : "4Gi"
          }
        }
        env {
          name  = "ORIGIN"
          value = each.value.origin
        }
        env {
          name  = "EXTRACTOR"
          value = each.value.extractor
        }
        env {
          name  = "TARGET"
          value = each.value.table
        }
        env {
          name  = "ROWS_PER_BATCH"
          value = "25000"
        }
        env {
          name  = "CHUNK_SIZE"
          value = contains(local.high_memory_tables, each.value.table) ? "10" : "20"
        }
        env {
          name  = "LOAD_MODE"
          value = contains(local.incremental_tables, each.value.table) ? "INCREMENTAL" : "FULL"
        }
        env {
          name  = "INCREMENTAL_TIMESTAMP_SOURCE"
          value = lookup(local.incremental_timestamp_source, each.value.table, null)
        }
        env {
          name  = "INCREMENTAL_FIELD"
          value = lookup(local.incremental_field, each.value.table, null)
        }
        env {
          name  = "ENVIROMENT"
          value = "pro" ## en desarrollo es "des"
        }
      }
      vpc_access {
        network_interfaces {
          network    = data.google_compute_network.vpc.id
          subnetwork = data.google_compute_subnetwork.subnet.id
        }
      }
      timeout = "43200s" # 12h
    }
  }
}