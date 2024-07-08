resource "google_artifact_registry_repository" "ar_repo" {
  location      = "europe-southwest1"
  repository_id = "ar-${data.google_client_config.current.project}"
  description   = "Repositorio para imágenes de Docker de ${data.google_client_config.current.project}"
  format        = "DOCKER"
}
