# resource "google_service_account" "scheduler" {
#   account_id   = "sa-extraction-scheduler"
#   display_name = "Extraction jobs scheduler for ${data.google_client_config.current.project} Service Account"
# }

# resource "google_project_iam_member" "scheduler_perm" {
#   project = data.google_client_config.current.project
#   role    = "roles/run.invoker"
#   member  = google_service_account.scheduler.member
# }

# resource "google_cloud_scheduler_job" "scheduler" {
#   for_each  = google_cloud_run_v2_job.job
#   paused    = true
#   name      = each.value.name
#   schedule  = "0 2 * * *" # 2am todos los dias
#   region    = "europe-west1"
#   time_zone = "Europe/Madrid"

#   http_target {
#     http_method = "POST"
#     uri         = "https://${each.value.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${data.google_project.project.number}/jobs/${each.value.name}:run"

#     oauth_token {
#       service_account_email = google_service_account.scheduler.email
#     }
#   }
# }
