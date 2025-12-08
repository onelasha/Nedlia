# Release Manifests

This directory contains release manifests for production deployments.

## Structure

```
releases/
├── README.md
├── rel-2024-01-15-001.yaml    # Release manifest
├── rel-2024-01-22-001.yaml
└── ...
```

## Manifest Format

```yaml
release:
  id: rel-2024-01-15-001
  created_at: '2024-01-14T10:00:00Z'
  created_by: '@release-manager'
  status: pending_signoffs # draft, pending_signoffs, approved, deploying, deployed, rolled_back

components:
  - name: api
    sign_off:
      status: pending # pending, approved, rejected
      approved_by: null
      approved_at: null

validation:
  staging_deployed: true
  integration_tests: passed
  performance_tests: passed
  security_scan: passed

checklist:
  all_signoffs: false
  staging_validated: false
  rollback_plan: false
  oncall_notified: false

approvals:
  release_manager: pending
  tech_lead: pending
  qa_lead: pending
```

## Workflow

1. **Create Release**: `gh workflow run release-train.yml -f action=create_release`
2. **Check Status**: `gh workflow run release-train.yml -f action=check_status -f release_id=rel-xxx`
3. **Deploy**: `gh workflow run release-train.yml -f action=deploy_production -f release_id=rel-xxx`
4. **Rollback**: `gh workflow run release-train.yml -f action=rollback -f release_id=rel-xxx`

## Sign-off Process

Team leads sign off by commenting `/signoff [component]` on the GitHub Release.

Final approval requires commenting `/approve` after all sign-offs are received.
