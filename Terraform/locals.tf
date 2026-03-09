locals {
  project_id = "project-fc238dfc-cbad-45d0-bcb"
  region = "us-central1"
  zone = "us-central1-a"
  scripts_url = "gs://${google_storage_bucket.dataproc_staging.name}/scripts/"
  service_account = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"

  dataproc-args = [
    "--landing_path",  "gs://${google_storage_bucket.data-lake.name}/landing",
    "--bronze_path", "gs://${google_storage_bucket.data-lake.name}/bronze",
    "--silver_path", "gs://${google_storage_bucket.data-lake.name}/silver",
  ]
}