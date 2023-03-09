resource "aws_lambda_function_event_invoke_config" "app_lambda_custom_configuration" {
  for_each = toset(var.lambda_functions_name)

  function_name          = "${var.project_name}-${terraform.workspace}-${each.value}"
  maximum_retry_attempts = 0
}
