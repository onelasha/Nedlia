# IaC Naming Conventions

Consistency is key for maintainable infrastructure. All Infrastructure as Code (IaC) in the Nedlia project must follow these naming conventions.

## General Rules

- **Case**: Always use `snake_case` for resource names, variables, and outputs.
- **Hyphens**: Avoid hyphens in resource names unless the resource type or a specific provider requirement mandates it.
- **Uniqueness**: Ensure names are unique within their scope (e.g., within a module or environment).

## The Azure CAF Resource Naming Pattern

To align with the **Official Azure Cloud Adoption Framework (CAF)**, we use a **Type-Prefix** pattern. This ensures that resources are automatically grouped by type when viewed in sorted lists.

`[type]-[org]-[app]-[env]-[region]-[instance]`

| Segment      | Code       | Examples                               |
| :----------- | :--------- | :------------------------------------- |
| **Type**     | 2-4 chars  | `s3`, `iam`, `vpc`, `st`, `kv`, `rg`   |
| **Org**      | 2-4 chars  | `ndla` (Nedlia)                        |
| **App**      | 3-6 chars  | `api`, `portal`, `worker`              |
| **Env**      | 3-4 chars  | `dev`, `test`, `stg`, `prod`           |
| **Region**   | 3-4 chars  | `use1` (us-east-1), `euw1` (eu-west-1) |
| **Instance** | 2-3 digits | `01`, `001` (Optional)                 |

### Examples (CAF Compliant)

- **S3 Bucket**: `s3-ndla-portal-prod-use1-01`
- **IAM Role**: `iam-ndla-api-dev-use1-lambda`
- **VPC**: `vpc-ndla-shared-prod-use1`
- **Azure Storage**: `stndlaprodue01` (Note: Storage accounts omit hyphens)

---

## Why Type-Prefix? (HashiCorp vs. Azure CAF)

While many Terraform users use suffixes, the **Azure CAF** standard specifically uses **Prefixes** because:

1.  **Sorting**: In the Portal/Console, resources of the same type group together.
2.  **Consistency**: It mimics the way we declare resources in code (`resource "aws_s3_bucket" "name"`).
3.  **Standardization**: It follows the Microsoft-recommended abbreviations list.

---

## Provider Constraints (AWS)

While we aim for the pattern above, some AWS resources have strict rules:

### 1. S3 Buckets

- **Constraints**: 3-63 chars, lowercase, no underscores. **Globally unique.**
- **Pattern**: `ndla-[app]-[env]-[region]-s3-[unique-id]`

### 2. IAM Resources

- **Constraints**: Uppercase/lowercase allowed, but `snake_case` or `kebab-case` is preferred for clarity. No global uniqueness required.

### 3. RDS/Aurora Clusters

- **Constraints**: Lowercase and hyphens ONLY. Must start with a letter.
- **Pattern**: `ndla-[app]-[env]-rds`

---

## The "Type-Omit" Rule (Terraform Identifiers)

In your `.tf` files, the **Local Resource Name** (internal to Terraform) should remain simple to avoid redundancy, as the type is already explicit.

- ✅ `resource "aws_vpc" "main" {}` -> Referenced as `aws_vpc.main`
- ❌ `resource "aws_vpc" "ndla_vpc" {}` -> Redundant redundancy.

The **Name Tag** (the physical cloud resource name) should use the full pattern:

```hcl
resource "aws_vpc" "main" {
  tags = {
    Name = "ndla-shared-prod-use1-vpc"
  }
}
```

## Tagging Strategy

All taggable resources must include a standard set of tags to assist with cost allocation and organization. Use `PascalCase` for keys and `snake_case` or `kebab-case` for values.

| Tag Key       | Example Value     | Description                           |
| ------------- | ----------------- | ------------------------------------- |
| `Project`     | `nedlia`          | Constant for this project             |
| `Environment` | `production`      | `dev`, `testing`, `staging`, `prod`   |
| `Component`   | `api`, `database` | The subsystem the resource belongs to |
| `ManagedBy`   | `terraform`       | Tool used to manage the resource      |

## File Organization

Standard Terraform file names should be used in every module:

- `main.tf`: Primary resource definitions.
- `variables.tf`: Input variable definitions.
- `outputs.tf`: Output value definitions.
- `data.tf`: Data source definitions.
- `versions.tf`: Provider and Terraform version constraints.
- `locals.tf`: Local value definitions.

## 🔗 References

For more details on industry-standard naming conventions, refer to the official documentation:

- **Azure Cloud Adoption Framework (CAF)**: [Define your naming convention](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
- **Azure Resource Abbreviations**: [Recommended abbreviations for Azure resources](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations)
