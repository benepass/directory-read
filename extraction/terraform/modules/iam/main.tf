resource "aws_iam_role" "app_role" {
  name = "${var.project_name}-${terraform.workspace}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    "environment" = terraform.workspace
    "project"     = var.project_name
    "alias"       = var.project_name
  }
}

resource "aws_iam_role_policy" "app_policy" {
  name = "${var.project_name}-${terraform.workspace}"
  role = aws_iam_role.app_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:*:logs:*:*:*"
      },
      {
        Action = [
          "secretsmanager:GetSecretValue",
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:ObjectExists"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}
