resource "google_dataproc_cluster" "test-cluster" {
  name     = "test-cluster"
  region   = "us-central1"

  cluster_config {
    staging_bucket = "${google_storage_bucket.dataproc_test_staging.name}"
    temp_bucket = "${google_storage_bucket.dataproc_test_temp.name}"
    cluster_tier = "CLUSTER_TIER_STANDARD"

    endpoint_config {
      enable_http_port_access = true
    }

    master_config {
      num_instances = 1
      machine_type = "n2-standard-4"
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
      image_version = "2.1-debian11"
      override_properties = {
        "dataproc:dataproc.allow.zero.workers" = "true"
      }
      optional_components = ["JUPYTER"]
    }
    

    gce_cluster_config {
      service_account = local.service_account
    }
  }
}
