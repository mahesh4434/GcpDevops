terraform {
  backend "gcs" {
    bucket = "gkestandardbackup"
    prefix = "terraform.tfstate"
  }
}
