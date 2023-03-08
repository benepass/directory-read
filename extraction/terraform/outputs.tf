output "app_bucket_name" {
  value = module.files.app_bucket.id
}
output "app_queue_urls" {
  value = module.queue.app_sqs_queue_urls
}
output "app_queue_names" {
  value = module.queue.app_sqs_queue_names
}
output "iam_role_arn" {
  value = module.iam.app_role_arn
}
