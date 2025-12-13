# Aurora Serverless v2 Module - Placeholder
# TODO: Implement Aurora RDS cluster when ready

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, production)"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID for database subnet group"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs for database"
}

variable "min_capacity" {
  type        = number
  default     = 0.5
  description = "Minimum Aurora Serverless v2 capacity"
}

variable "max_capacity" {
  type        = number
  default     = 2
  description = "Maximum Aurora Serverless v2 capacity"
}
  engine_version     = aws_rds_cluster.main.engine_version
}

output "cluster_endpoint" {
  value = aws_rds_cluster.main.endpoint
}

output "cluster_reader_endpoint" {
  value = aws_rds_cluster.main.reader_endpoint
}
