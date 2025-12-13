# Lambda Module - Placeholder
# TODO: Implement Lambda function resources when ready

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, production)"
}

variable "function_name" {
  type        = string
  description = "Name of the Lambda function"
}

variable "handler" {
  type        = string
  description = "Lambda handler (e.g., index.handler)"
}

variable "runtime" {
  type        = string
  default     = "python3.11"
  description = "Lambda runtime"
}

variable "memory_size" {
  type        = number
  default     = 256
  description = "Memory allocation in MB"
}

variable "timeout" {
  type        = number
  default     = 30
  description = "Timeout in seconds"
}

variable "environment_variables" {
  type        = map(string)
  default     = {}
  description = "Environment variables for Lambda"
}

resource "aws_lambda_function" "main" {
  function_name = "nedlia-${var.environment}-${var.function_name}"
  role          = aws_iam_role.lambda.arn
  handler       = var.handler
  runtime       = var.runtime
  memory_size   = var.memory_size
  timeout       = var.timeout

  filename         = "${path.module}/placeholder.zip"
  source_code_hash = filebase64sha256("${path.module}/placeholder.zip")

  environment {
    variables = merge(
      {
        ENVIRONMENT = var.environment
      },
      var.environment_variables
    )
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name = "nedlia-${var.environment}-${var.function_name}"
  }
}

resource "aws_iam_role" "lambda" {
  name = "nedlia-${var.environment}-${var.function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_xray" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

output "function_arn" {
  value = aws_lambda_function.main.arn
}

output "function_name" {
  value = aws_lambda_function.main.function_name
}
