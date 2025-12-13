# SQS Module - Placeholder
# TODO: Implement SQS queue resources when ready

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, production)"
}

variable "queue_name" {
  type        = string
  description = "Name of the SQS queue"
}

variable "visibility_timeout_seconds" {
  type        = number
  default     = 60
  description = "Visibility timeout in seconds"
}

variable "message_retention_seconds" {
  type        = number
  default     = 1209600
  description = "Message retention period in seconds (default 14 days)"
}

# Placeholder: SQS resources will be created here
# output "queue_url" {
#   value       = aws_sqs_queue.main.url
#   description = "SQS queue URL"
# }
#
# output "queue_arn" {
#   value       = aws_sqs_queue.main.arn
#   description = "SQS queue ARN"
# }
#
# output "dlq_url" {
#   value       = aws_sqs_queue.dlq.url
#   description = "Dead letter queue URL"
# }
#
# output "dlq_arn" {
#   value       = aws_sqs_queue.dlq.arn
#   description = "Dead letter queue ARN"
# }
