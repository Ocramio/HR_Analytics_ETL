data "google_project" "project" {}

terraform {
  required_version = ">= 1.3.0"
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.21.0"
    }
  }
  backend "gcs" {
    bucket = "hr-analytics-remote-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = local.project_id
  region  = local.region
  zone    = local.zone
}

data "terraform_remote_state" "vpc" {
  backend = "gcs"
  config = {
    bucket = "hr-analytics-remote-state"
    prefix = "terraform/state"
  }
}