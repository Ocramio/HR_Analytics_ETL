
resource "google_dataproc_workflow_template" "workflow_template" {
  name = "hr-analytics-dataproc-workflow_template"
  location = local.region
  placement {
    managed_cluster {
      cluster_name = "hr-analytics-dataproc-cluster"
      config {
        gce_cluster_config {
          internal_ip_only = false

          # Explicitly use the default account
          service_account = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"
        }
        master_config {
          num_instances = 1
          machine_type = "n2-standard-2"
          disk_config {
            boot_disk_type = "pd-ssd"
            boot_disk_size_gb = 50
          }
        }
        worker_config {
          num_instances = 2
          machine_type = "n2-standard-2"
          disk_config {
            boot_disk_size_gb = 50
          }
        }
        software_config {
          image_version = "2.0.35-debian10"
        }
        staging_bucket = google_storage_bucket.dataproc_staging.name
        temp_bucket = google_storage_bucket.dataproc_temp.name
      }
    }
  }
  jobs {
    step_id = "bronze_layer"
    pyspark_job {
      main_python_file_uri = "${local.scripts_url}/bronze_layer_load.py"
      args = local.dataproc-args
    }
  }
}