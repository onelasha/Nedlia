variable "domain_name" {
  type        = string
  description = "Primary domain name (e.g., nedlia.com)"
}

variable "hosted_zone_id" {
  type        = string
  description = "Route 53 hosted zone ID"
}

variable "environment" {
  type        = string
  description = "Environment name"
  default     = "production"
}

variable "price_class" {
  type        = string
  description = "CloudFront price class"
  default     = "PriceClass_All"
}
