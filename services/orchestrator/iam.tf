# WORKFLOWS #
resource "google_service_account" "wf_service_account" {
  account_id   = "sa-workflow"
  display_name = "Workflow Service Account"
}

resource "google_project_iam_member" "log_writer" {
  project = data.google_project.project.id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.wf_service_account.email}"
}

resource "google_project_iam_member" "cloud_run_jobs_executor" {
  project = data.google_project.project.id
  role    = "roles/run.jobsExecutor"
  member  = "serviceAccount:${google_service_account.wf_service_account.email}"
}

resource "google_project_iam_member" "cloud_run_viewer" {
  project = data.google_project.project.id
  role    = "roles/run.viewer"
  member  = "serviceAccount:${google_service_account.wf_service_account.email}"
}

resource "google_project_iam_member" "bigquery_user" {
  project = data.google_project.project.id
  role    = "roles/bigquery.user"
  member  = "serviceAccount:${google_service_account.wf_service_account.email}"
}

resource "google_project_iam_member" "bigquery_data_editor" {
  project = data.google_project.project.id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.wf_service_account.email}"
}

resource "google_project_iam_member" "dataform_editor" {
  project = data.google_project.project.id
  role    = "roles/dataform.editor"
  member  = "serviceAccount:${google_service_account.wf_service_account.email}"
}

# SCHEDULER

resource "google_service_account" "scheduler" {
  account_id   = "sa-workflows-scheduler"
  display_name = "Service Account for invoking Workflows"
}

resource "google_project_iam_member" "workflow_invoker" {
  project = data.google_project.project.id
  role    = "roles/workflows.invoker"
  member  = "serviceAccount:${google_service_account.scheduler.email}"  
}