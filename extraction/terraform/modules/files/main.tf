resource "aws_s3_bucket" "app_bucket" {
  bucket = "${var.project_name}-${terraform.workspace}"

  tags = {
    "environment" = terraform.workspace
    "project"     = var.project_name
    "alias"       = var.project_name
  }
}

resource "aws_s3_bucket_acl" "app_bucket_acl" {
  bucket = aws_s3_bucket.app_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "app_bucket_public_access" {
  bucket = aws_s3_bucket.app_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "app_bucket_versioning" {
  bucket = aws_s3_bucket.app_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_logging" "app_bucket_logging" {
  bucket = aws_s3_bucket.app_bucket.id

  target_bucket = var.access_log_bucket_name
  target_prefix = "${aws_s3_bucket.app_bucket.bucket}/"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "app_bucket_server_side_encryption" {
  bucket = aws_s3_bucket.app_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
