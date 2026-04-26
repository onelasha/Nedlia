output "bucket_name" {
  value       = aws_s3_bucket.website.id
  description = "S3 bucket name"
}

output "bucket_arn" {
  value       = aws_s3_bucket.website.arn
  description = "S3 bucket ARN"
}

output "cloudfront_distribution_id" {
  value       = aws_cloudfront_distribution.website.id
  description = "CloudFront distribution ID"
}

output "cloudfront_domain_name" {
  value       = aws_cloudfront_distribution.website.domain_name
  description = "CloudFront distribution domain name"
}

output "website_url" {
  value       = "https://${var.domain_name}"
  description = "Website URL"
}
