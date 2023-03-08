provider "aws" {
  region = var.region
}

terraform {
  backend "s3" {
    bucket         = "directory-read/extraction-terraform-state"
    dynamodb_table = "directory-read/extraction-terraform-locks"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}

module "files" {
  source                 = "./modules/files"
  project_name           = var.project_name
  access_log_bucket_name = var.access_log_bucket_name
}

module "iam" {
  source       = "./modules/iam"
  region       = var.region
  project_name = var.project_name
}
