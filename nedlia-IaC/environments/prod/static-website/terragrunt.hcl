# Standalone config for static-website module

locals {
  aws_region  = "us-east-1"
  environment = "production"
}

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "nedlia-terraform-state"
    key            = "static-website/terraform.tfstate"
    region         = local.aws_region
    encrypt        = true
    dynamodb_table = "nedlia-terraform-locks"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"

  default_tags {
    tags = {
      Project     = "Nedlia"
      ManagedBy   = "Terraform"
      Environment = "${local.environment}"
    }
  }
}
EOF
}

terraform {
  source = "../../../modules/static-website"
}

inputs = {
  domain_name    = "nedlia.com"
  hosted_zone_id = "Z05913602VDPGOTVJCV1G"
  environment    = local.environment
}
