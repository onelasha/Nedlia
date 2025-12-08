# Deployment

This guide covers the deployment process and CI/CD pipeline for Nedlia.

## Environments

| Environment    | Purpose                   | URL | Branch                   |
| -------------- | ------------------------- | --- | ------------------------ |
| **dev**        | Individual development    | -   | feature branches         |
| **testing**    | Automated tests, CI       | -   | PR branches              |
| **staging**    | Pre-production validation | TBD | `main`                   |
| **production** | Live system               | TBD | `main` (tagged releases) |

## Deployment Flow

```text
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Feature   │────▶│   Testing   │────▶│   Staging   │────▶│ Production  │
│   Branch    │     │   (CI)      │     │   (Auto)    │     │  (Manual)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │                   │
      │                   │                   │                   │
   PR Created         CI Passes          Merge to main      Tag Release
```

## CI Pipeline

Every PR triggers the CI pipeline (`.github/workflows/ci.yml`):

1. **Lint JS/TS** – ESLint, Prettier
2. **Lint Python** – Ruff
3. **Lint Terraform** – terraform fmt
4. **Test JS/TS** – Jest/Vitest
5. **Test Python** – pytest
6. **Security Scan** – Gitleaks
7. **Build** – Compile all projects

All checks must pass before merging.

## Infrastructure Deployment

Infrastructure is managed with Terraform + Terragrunt.

### Prerequisites

```bash
# Install tools
brew install terraform terragrunt awscli

# Configure AWS credentials
aws configure --profile nedlia-dev
```

### Deploy to an Environment

```bash
cd nedlia-IaC/environments/dev

# Preview changes
terragrunt plan

# Apply changes
terragrunt apply

# Deploy all modules
terragrunt run-all apply
```

### Environment-Specific Configuration

Each environment has its own configuration in `nedlia-IaC/environments/<env>/env.hcl`:

```hcl
# environments/production/env.hcl
locals {
  environment         = "production"
  aurora_min_capacity = 2
  aurora_max_capacity = 64
  lambda_memory       = 1024
}
```

## Application Deployment

### Backend (Lambda)

Lambdas are deployed via Terraform. The deployment process:

1. Build the application
2. Package as ZIP
3. Upload to S3
4. Update Lambda function

```bash
# Build Python Lambda
cd nedlia-back-end/python
uv run python -m build

# Build NestJS Lambda
cd nedlia-back-end/nestjs
pnpm build
```

### Frontend (S3 + CloudFront)

```bash
cd nedlia-front-end/web

# Build
pnpm build

# Deploy (via Terraform or direct S3 sync)
aws s3 sync dist/ s3://nedlia-${ENV}-frontend --delete
aws cloudfront create-invalidation --distribution-id ${DIST_ID} --paths "/*"
```

## Release Process

### 1. Create Release Branch (optional)

For major releases:

```bash
git checkout -b release/v1.0.0
```

### 2. Update Version

```bash
# Update package.json versions
pnpm version minor  # or major, patch

# Update CHANGELOG.md
# Add release notes under ## [1.0.0] - YYYY-MM-DD
```

### 3. Create Tag

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 4. Deploy to Production

Production deployments are triggered by:

- Manual approval in GitHub Actions
- Or manual `terragrunt apply` in production environment

```bash
cd nedlia-IaC/environments/production
terragrunt run-all apply
```

## Rollback

### Application Rollback

```bash
# Revert to previous Lambda version
aws lambda update-function-code \
  --function-name nedlia-production-api \
  --s3-bucket nedlia-deployments \
  --s3-key previous-version.zip
```

### Infrastructure Rollback

```bash
# Revert to previous state
cd nedlia-IaC/environments/production
git checkout HEAD~1 -- .
terragrunt run-all apply
```

## Monitoring Deployments

### CloudWatch

- **Logs**: `/aws/lambda/nedlia-*`
- **Metrics**: Lambda invocations, errors, duration
- **Alarms**: Error rate > 1%, latency > 5s

### X-Ray

Distributed tracing is enabled for all Lambda functions:

```bash
# View traces
aws xray get-trace-summaries --start-time $(date -d '1 hour ago' +%s) --end-time $(date +%s)
```

## Secrets Management

Secrets are stored in AWS Secrets Manager and SSM Parameter Store:

```bash
# Store a secret
aws secretsmanager create-secret \
  --name nedlia/production/api-key \
  --secret-string "your-secret-value"

# Reference in Terraform
data "aws_secretsmanager_secret_version" "api_key" {
  secret_id = "nedlia/production/api-key"
}
```

## Deployment Checklist

Before deploying to production:

- [ ] All CI checks pass
- [ ] Code reviewed and approved
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Staging tested
- [ ] Rollback plan ready
- [ ] Team notified

## Troubleshooting

### Deployment Failed

1. Check GitHub Actions logs
2. Check Terraform output for errors
3. Verify AWS credentials are valid
4. Check CloudWatch logs for Lambda errors

### Lambda Not Updating

```bash
# Force update by changing description
aws lambda update-function-configuration \
  --function-name nedlia-production-api \
  --description "Deployed at $(date)"
```

### Database Migration Failed

```bash
# Check migration status
# Run migrations manually if needed
cd nedlia-back-end/nestjs
pnpm migrate:status
pnpm migrate:up
```

## Next Steps

- [Architecture](../ARCHITECTURE.md) – System design
- [Testing](testing.md) – Test strategy
- [Local Development](local-development.md) – Running locally
