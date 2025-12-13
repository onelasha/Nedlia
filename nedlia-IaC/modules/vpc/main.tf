# VPC Module - Placeholder
# TODO: Implement VPC, subnets, NAT gateway, and security groups when ready

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, production)"
}

variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "CIDR block for VPC"
}
