# Cognito Module - Placeholder
# TODO: Implement Cognito User Pool resources when ready

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, production)"
}

# Placeholder: Cognito resources will be created here
# output "user_pool_id" {
#   value       = aws_cognito_user_pool.main.id
#   description = "Cognito User Pool ID"
# }
#
# output "user_pool_client_id" {
#   value       = aws_cognito_user_pool_client.main.client_id
#   description = "Cognito User Pool Client ID"
# }
}

output "user_pool_id" {
  value = aws_cognito_user_pool.main.id
}

output "user_pool_arn" {
  value = aws_cognito_user_pool.main.arn
}

output "client_id" {
  value = aws_cognito_user_pool_client.main.id
}
