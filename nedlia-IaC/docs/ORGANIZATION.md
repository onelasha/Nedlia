# IaC Project Organization

Nedlia uses a **Terraform + Terragrunt** architecture to manage infrastructure across multiple environments while maintaining a DRY (Don't Repeat Yourself) codebase.

## Directory Structure

```text
nedlia-IaC/
├── environments/         # Environmental configurations (Terragrunt)
│   ├── dev/             # Development environment
│   ├── qa/              # QA/Testing environment
│   ├── stg/             # Staging environment
│   └── prod/            # Production environment
├── modules/              # Reusable Terraform modules
│   ├── vpc/             # Networking infrastructure
│   ├── aurora/          # Database infrastructure
│   └── lambda/          # Serverless compute
├── docs/                 # Documentation and guidelines
└── terragrunt.hcl        # Root configuration for remote state & global providers
```

## The "Modules vs. Environments" Split

### 1. Modules Layer (`/modules`)

This layer contains pure Terraform code. These modules are meant to be generic and reusable. They should not contain environment-specific hardcoding.

- **Inputs**: Defined in `variables.tf`.
- **Outputs**: Defined in `outputs.tf`.
- **Drafting**: Create modules for common patterns (e.g., a "Service" module that includes a Lambda, SQS, and IAM roles).

### 2. Environments Layer (`/environments`)

This layer uses **Terragrunt** to instantiate modules. Each environment directory contains a `terragrunt.hcl` file that:

- Points to a module in `/modules` (or a remote git source).
- Provides environment-specific inputs (e.g., `instance_type = "t3.medium"` for prod, but `"t3.micro"` for dev).

## Artifact Management

### Remote State

State files are stored remotely (e.g., AWS S3 with DynamoDB locking). The root `terragrunt.hcl` handles the generation of backend configuration.

### Documentation

Use `terraform-docs` to automatically generate `README.md` files for each module.

```bash
terraform-docs markdown table . > README.md
```

## Workflow

1.  **Develop** or update a module in `/modules`.
2.  **Configure** the relevant environment in `/environments`.
3.  **Validate** using Terragrunt:
    ```bash
    terragrunt plan
    ```
4.  **Apply** changes:
    ```bash
    terragrunt apply
    ```
