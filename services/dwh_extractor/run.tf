locals {
  tables = flatten([for origin, tbls in var.tables : [for tbl in tbls : { origin = origin, table = tbl, extractor = var.origins[origin] }]])
}

resource "google_project_iam_member" "vpc_access_perm" {
  for_each = toset([
    "serviceAccount:service-${data.google_project.project.number}@gcp-sa-vpcaccess.iam.gserviceaccount.com",
    "serviceAccount:${data.google_project.project.number}@cloudservices.gserviceaccount.com",
    "serviceAccount:service-${data.google_project.project.number}@serverless-robot-prod.iam.gserviceaccount.com"
  ])
  project = data.google_compute_network.vpc.project
  role    = "roles/compute.networkUser"
  member  = each.key
}

resource "google_cloud_run_v2_job" "job" {
  for_each = { for tbl in local.tables : "${tbl.extractor}_${tbl.origin}_${tbl.table}" => tbl }
  name     = replace(lower("crj-data-extractor-${each.value.origin}-${each.value.table}"), "_", "-")
  location = data.google_client_config.current.region

  template {
    template {
      containers {
        image = "europe-southwest1-docker.pkg.dev/${data.google_client_config.current.project}/${google_artifact_registry_repository.ar_repo.name}/data_extractor:latest"
        resources {
          limits = {
            cpu    = "2000m"
            memory = "${each.value.table}" == "LIPS" ? "8Gi" : "4Gi"
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
