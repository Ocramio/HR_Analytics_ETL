# This gives the default service account the power to run Dataproc nodes
resource "google_project_iam_member" "default_compute_dataproc_worker" {
  project = local.project_id
  role    = "roles/dataproc.worker"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}