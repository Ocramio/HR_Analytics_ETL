locals {
  project_id = "project-fc238dfc-cbad-45d0-bcb"
  region = "southamerica-east1"
  zone = "southamerica-east1-a"
  scripts_url = "gs://${google_storage_bucket.dataproc_staging.name}/scripts/"

  dataproc-args = [
    "--landing_path",  "gs://${google_storage_bucket.data-lake.name}/landing",
    "--bronze_path", "gs://${google_storage_bucket.data-lake.name}/bronze",
    "--silver_path", "gs://${google_storage_bucket.data-lake.name}/silver"
  ]

}