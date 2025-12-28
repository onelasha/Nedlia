# IaC Naming Conventions

Consistency is key for maintainable infrastructure. All Infrastructure as Code (IaC) in the Nedlia project must follow these naming conventions.

## General Rules

- **Case**: Always use `snake_case` for resource names, variables, and outputs.
- **Hyphens**: Avoid hyphens in resource names unless the resource type or a specific provider requirement mandates it.
- **Uniqueness**: Ensure names are unique within their scope (e.g., within a module or environment).

## Terraform Resources

Resource names should be descriptive of their function, not just their type.

**Format**: `<provider>_<type>.<functional_name>`

- ✅ `aws_s3_bucket.main_storage`
- ✅ `aws_instance.api_server`
- ❌ `aws_s3_bucket.bucket1`

## Variables and Outputs

- **Variables**: Use `snake_case`. Include a clear `description` and `type`.
- **Outputs**: Use `snake_case`. Provide a `description` for clarity when consumed by other modules.

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
