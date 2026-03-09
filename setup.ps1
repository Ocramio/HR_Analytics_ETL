# 1. Log in (Only needed once per session)
# gcloud auth application-default login

# 2. Build the infra
Set-Location Terraform

# Check if the state bucket exists before trying to create it
$STATE_BUCKET = "gs://hr-analytics-remote-state"
$bucketCheck = gcloud storage buckets describe $STATE_BUCKET 2>$null
if (!$bucketCheck) {
    gcloud storage buckets create $STATE_BUCKET --location=southamerica-east1
    gcloud storage buckets update $STATE_BUCKET --versioning
}

# Standard Terraform Workflow
terraform init

# Remove old plan to avoid the "lineage" error
if (Test-Path "plan.out") { Remove-Item "plan.out" }

terraform plan -out="plan.out"
terraform apply "plan.out"

# 3. Upload the data (Only runs if Terraform succeeded)
if ($LASTEXITCODE -eq 0) {
    Write-Host "Infrastructure ready. Uploading data..." -ForegroundColor Green
    gcloud storage cp ../HR_Analytics_data/*.csv gs://hr-analytics-data-lake/landing/
    
    # 4. Trigger the workflow
    # Write-Host "Starting Dataproc Workflow..." -ForegroundColor Cyan
    # gcloud dataproc workflow-templates instantiate hr-analytics-dataproc-workflow_template --region=us-central1
} else {
    Write-Error "Terraform failed. Skipping data upload and workflow." -ForegroundColor Red
}

Set-Location ..
