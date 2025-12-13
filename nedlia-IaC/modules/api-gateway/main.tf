# API Gateway Module - Placeholder
# TODO: Implement API Gateway resources when ready

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, production)"
}

variable "name" {
  type        = string
  default     = "nedlia-api"
  description = "Name of the API Gateway"
}

# Placeholder: API Gateway resources will be created here
# output "api_id" {
#   value       = aws_api_gateway_rest_api.main.id
#   description = "API Gateway ID"
# }
#
# output "api_endpoint" {
#   value       = aws_api_gateway_stage.main.invoke_url
#   description = "API Gateway endpoint URL"
# }
