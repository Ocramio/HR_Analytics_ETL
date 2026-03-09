# Bucket to store the landing, bronze and silver layers
resource "google_storage_bucket" "data-lake" {
  name          = "hr-analytics-data-lake"
  location      = local.region
  force_destroy = true
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "dataproc_staging" {
  name     = "hr-analytics-dataproc-staging"
  location = local.region
  force_destroy = true
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "dataproc_temp" {
  name     = "hr-analytics-dataproc-temp"
  location = local.region
  force_destroy = true
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type = "Delete"
    }
  }
}


resource "google_storage_bucket" "dataproc_test_staging" {
  name     = "hr-analytics-dataproc-test-staging"
  location = local.region
  force_destroy = true
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "dataproc_test_temp" {
  name     = "hr-analytics-dataproc-test-temp"
  location = local.region
  force_destroy = true
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket_object" "upload_scripts" {
  for_each = fileset("${path.module}/../Pyspark_jobs/", "*.py")

  name   = "scripts/${each.value}"
  source = "${path.module}/../Pyspark_jobs/${each.value}"
  bucket = google_storage_bucket.dataproc_staging.name
}