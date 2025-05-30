resource "google_artifact_registry_repository" "ar_repo" {
  location      = var.location
  repository_id = var.repository_id
  description   = "Repositorio para imágenes de Docker de ${data.google_client_config.current.project}"
  format        = "DOCKER"

  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = var.cleanup_policies_id
    action = "KEEP"
    most_recent_versions {
      keep_count            = 5
      package_name_prefixes = []
    }
  }
}
