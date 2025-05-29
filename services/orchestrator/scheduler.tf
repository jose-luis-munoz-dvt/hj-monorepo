

resource "google_cloud_scheduler_job" "scheduler" {
  paused    = var.project_id == "pj-data-prod" ? false : true
  name      = "workflow_scheduler"
  schedule  = "0 2 * * *" # 2am todos los dias
  region    = "europe-west1"
  time_zone = "Europe/Madrid"

  http_target {
    http_method = "POST"
    uri         = "https://workflowexecutions.googleapis.com/v1/${data.google_project.project.id}/locations/${google_workflows_workflow.wf_orchestrator.region}/workflows/${google_workflows_workflow.wf_orchestrator.name}/executions"

    oauth_token {
      service_account_email = google_service_account.scheduler.email
    }
  }
}