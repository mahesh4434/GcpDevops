provider "google" {
  credentials = data.google_secret_manager_secret_version.credentials.secret_data
  project     = "devopsgkestandardproject"
  region      = "us-central1"
}

data "google_secret_manager_secret" "credentials" {
  secret_id = "my-secret-name"  # Replace with your secret name
}

data "google_secret_manager_secret_version" "credentials" {
  secret_id = data.google_secret_manager_secret.credentials.id
}
