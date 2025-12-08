# Release Management

Comprehensive release management strategy with validation, sign-offs, and production deployment governance.

## Release Philosophy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Release Management                                   │
│                                                                             │
│   "Deploy often to staging, release deliberately to production"             │
│                                                                             │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│   │  Code   │───▶│  Build  │───▶│ Staging │───▶│ Release │───▶│  Prod   │  │
│   │  Merge  │    │  & Test │    │  Deploy │    │  Train  │    │ Deploy  │  │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│                                                     │                       │
│                                              ┌──────┴──────┐                │
│                                              │  Sign-offs  │                │
│                                              │  Checklist  │                │
│                                              │  Approval   │                │
│                                              └─────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Key Principles

1. **Continuous Deployment to Staging** – Every merge deploys automatically
2. **Deliberate Releases to Production** – Scheduled release trains with approvals
3. **Full Visibility** – Dashboard showing all changes pending release
4. **Multi-Team Sign-off** – Each team validates their components
5. **Rollback Ready** – Every release has a tested rollback plan

---

## Release Train Model

### Release Schedule

| Release Type | Frequency             | Window  | Approval Required   |
| ------------ | --------------------- | ------- | ------------------- |
| **Regular**  | Weekly (Tuesday 10am) | 2 hours | Team leads          |
| **Hotfix**   | As needed             | 30 min  | On-call + Tech lead |
| **Major**    | Monthly               | 4 hours | All stakeholders    |

### Release Calendar

```
Week 1: Feature development
Week 2: Feature freeze (Tuesday) → Staging validation
Week 3: Release train (Tuesday 10am) → Production
Week 4: Monitoring & bug fixes
```

---

## Release Dashboard

### Release Manifest

Every release has a manifest showing exactly what will be deployed:

```yaml
# releases/2024-01-15-release.yaml
release:
  id: rel-2024-01-15-001
  scheduled_at: '2024-01-15T10:00:00Z'
  release_manager: '@john.doe'
  status: pending_approval # draft, pending_approval, approved, deploying, deployed, rolled_back

components:
  - name: api
    current_version: v1.2.3
    new_version: v1.3.0
    changes:
      - 'feat: Add placement bulk upload endpoint'
      - 'fix: Rate limiting edge case'
    team: api-team
    team_lead: '@alice'
    sign_off: pending # pending, approved, rejected

  - name: placement-service
    current_version: v2.1.0
    new_version: v2.2.0
    changes:
      - 'feat: New validation rules'
      - 'perf: Optimize database queries'
    team: placement-team
    team_lead: '@bob'
    sign_off: approved
    approved_by: '@bob'
    approved_at: '2024-01-14T15:30:00Z'

  - name: portal
    current_version: v3.0.1
    new_version: v3.1.0
    changes:
      - 'feat: New campaign dashboard'
      - 'fix: Mobile responsive issues'
    team: portal-team
    team_lead: '@carol'
    sign_off: approved

  - name: workers
    current_version: v1.5.0
    new_version: v1.5.0 # No changes
    changes: []
    team: workers-team
    sign_off: not_required

validation:
  staging_deployed: true
  staging_deployed_at: '2024-01-14T09:00:00Z'
  integration_tests: passed
  performance_tests: passed
  security_scan: passed

checklist:
  - item: 'All team sign-offs received'
    status: pending
    required: true
  - item: 'Integration tests passing'
    status: completed
    completed_by: '@ci-bot'
  - item: 'Performance regression check'
    status: completed
    completed_by: '@perf-team'
  - item: 'Security scan clean'
    status: completed
    completed_by: '@security-bot'
  - item: 'Database migrations reviewed'
    status: completed
    completed_by: '@dba-team'
  - item: 'Rollback plan documented'
    status: completed
    completed_by: '@john.doe'
  - item: 'On-call team notified'
    status: pending
    required: true

approvals:
  - role: 'Release Manager'
    user: '@john.doe'
    status: approved
  - role: 'Tech Lead'
    user: '@tech-lead'
    status: pending
  - role: 'QA Lead'
    user: '@qa-lead'
    status: approved
  - role: 'Security'
    user: '@security-team'
    status: approved
```

---

## Sign-off Process

### Team Sign-off Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Sign-off Workflow                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Release Created                                                         │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              Teams Notified (Slack/Email)                            │   │
│  │  "Release rel-2024-01-15-001 includes changes to your component"    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │  API Team   │  │  Placement  │  │   Portal    │  │   Workers   │       │
│  │   Review    │  │    Team     │  │    Team     │  │    Team     │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│         │                │                │                │               │
│         ▼                ▼                ▼                ▼               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Validation Checklist                              │   │
│  │  [ ] Staging tested manually                                        │   │
│  │  [ ] No regressions found                                           │   │
│  │  [ ] Feature flags configured                                       │   │
│  │  [ ] Monitoring dashboards ready                                    │   │
│  │  [ ] Runbook updated (if needed)                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                │                │                │               │
│         ▼                ▼                ▼                ▼               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │  ✅ Approve │  │  ✅ Approve │  │  ✅ Approve │  │  ⏭️ Skip    │       │
│  │  or         │  │  or         │  │  or         │  │  (no changes)│       │
│  │  ❌ Reject  │  │  ❌ Reject  │  │  ❌ Reject  │  │             │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                        │
│                                   ▼                                        │
│                    ┌─────────────────────────────┐                         │
│                    │  All Sign-offs Received?    │                         │
│                    └──────────────┬──────────────┘                         │
│                                   │                                        │
│                    ┌──────────────┴──────────────┐                         │
│                    │                             │                         │
│                    ▼                             ▼                         │
│             ┌─────────────┐              ┌─────────────┐                   │
│             │   Release   │              │   Release   │                   │
│             │   Blocked   │              │   Ready     │                   │
│             └─────────────┘              └─────────────┘                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sign-off Checklist by Role

#### Team Lead Sign-off

- [ ] All PRs in release reviewed and approved
- [ ] Staging environment tested manually
- [ ] No critical bugs in component
- [ ] Feature flags configured correctly
- [ ] Team available during release window

#### QA Lead Sign-off

- [ ] All test suites passing
- [ ] Regression tests completed
- [ ] Edge cases validated
- [ ] Cross-browser/device testing done (portal)

#### Security Sign-off

- [ ] Security scan passed
- [ ] No new vulnerabilities introduced
- [ ] Secrets properly managed
- [ ] Auth/authz changes reviewed

#### DBA Sign-off (if migrations)

- [ ] Migration scripts reviewed
- [ ] Rollback scripts tested
- [ ] Performance impact assessed
- [ ] Backup verified

#### Release Manager Sign-off

- [ ] All team sign-offs received
- [ ] Release notes prepared
- [ ] Rollback plan documented
- [ ] On-call team notified
- [ ] Monitoring dashboards ready

---

## Release Checklist

### Pre-Release Checklist

```markdown
## Pre-Release Checklist: rel-2024-01-15-001

### Code Quality

- [ ] All PRs merged to main
- [ ] No failing CI checks
- [ ] Code coverage maintained
- [ ] SonarCloud quality gate passed

### Testing

- [ ] Unit tests passing (100%)
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Performance tests within SLO
- [ ] Security scan clean

### Staging Validation

- [ ] Deployed to staging successfully
- [ ] Staging smoke tests passing
- [ ] Manual testing completed by each team
- [ ] No P1/P2 bugs in staging

### Documentation

- [ ] Release notes written
- [ ] API documentation updated
- [ ] Runbooks updated (if needed)
- [ ] CHANGELOG updated

### Infrastructure

- [ ] Database migrations tested
- [ ] Feature flags configured
- [ ] Environment variables set
- [ ] Secrets rotated (if needed)

### Team Readiness

- [ ] All team sign-offs received
- [ ] On-call team notified
- [ ] Release manager assigned
- [ ] Rollback owner assigned

### Communication

- [ ] Stakeholders notified
- [ ] Status page prepared
- [ ] Support team briefed
```

### Release Day Checklist

```markdown
## Release Day Checklist

### T-60 minutes

- [ ] Final staging validation
- [ ] All sign-offs confirmed
- [ ] Release channel opened (#release-2024-01-15)
- [ ] Monitoring dashboards open

### T-30 minutes

- [ ] Team leads online
- [ ] On-call confirmed available
- [ ] Rollback scripts ready
- [ ] Database backup verified

### T-0 (Release Start)

- [ ] Announce release start in Slack
- [ ] Begin deployment (component by component)
- [ ] Monitor error rates

### During Release

- [ ] Each component: Deploy → Verify → Next
- [ ] Watch CloudWatch dashboards
- [ ] Check X-Ray for errors
- [ ] Validate critical user flows

### Post-Release

- [ ] All health checks passing
- [ ] Error rates normal
- [ ] Performance within SLO
- [ ] Announce release complete
- [ ] Update status page
```

---

## GitHub Workflow for Release Management

````yaml
# .github/workflows/release-train.yml
name: Release Train

on:
  workflow_dispatch:
    inputs:
      release_id:
        description: 'Release ID (e.g., rel-2024-01-15-001)'
        required: true
      action:
        description: 'Action to perform'
        required: true
        type: choice
        options:
          - create_release
          - request_signoffs
          - check_signoffs
          - deploy_production
          - rollback
      dry_run:
        description: 'Dry run (no actual deployment)'
        type: boolean
        default: true

jobs:
  # ===========================================================================
  # Create Release Manifest
  # ===========================================================================
  create-release:
    if: inputs.action == 'create_release'
    runs-on: ubuntu-latest
    outputs:
      manifest: ${{ steps.manifest.outputs.content }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changes since last release
        id: changes
        run: |
          LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
          if [ -z "$LAST_TAG" ]; then
            COMMITS=$(git log --oneline)
          else
            COMMITS=$(git log --oneline $LAST_TAG..HEAD)
          fi
          echo "commits<<EOF" >> $GITHUB_OUTPUT
          echo "$COMMITS" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Detect component changes
        id: components
        run: |
          # Detect which components have changes
          COMPONENTS=""

          if git diff --name-only $LAST_TAG..HEAD | grep -q "nedlia-back-end/api/"; then
            COMPONENTS="$COMPONENTS api"
          fi
          if git diff --name-only $LAST_TAG..HEAD | grep -q "nedlia-back-end/workers/"; then
            COMPONENTS="$COMPONENTS workers"
          fi
          if git diff --name-only $LAST_TAG..HEAD | grep -q "nedlia-back-end/services/placement-service/"; then
            COMPONENTS="$COMPONENTS placement-service"
          fi
          if git diff --name-only $LAST_TAG..HEAD | grep -q "nedlia-back-end/services/validation-service/"; then
            COMPONENTS="$COMPONENTS validation-service"
          fi
          if git diff --name-only $LAST_TAG..HEAD | grep -q "nedlia-back-end/services/notification-service/"; then
            COMPONENTS="$COMPONENTS notification-service"
          fi
          if git diff --name-only $LAST_TAG..HEAD | grep -q "nedlia-front-end/portal/"; then
            COMPONENTS="$COMPONENTS portal"
          fi

          echo "components=$COMPONENTS" >> $GITHUB_OUTPUT

      - name: Generate release manifest
        id: manifest
        run: |
          cat > releases/${{ inputs.release_id }}.yaml << EOF
          release:
            id: ${{ inputs.release_id }}
            created_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
            created_by: ${{ github.actor }}
            status: draft

          components:
          $(for comp in ${{ steps.components.outputs.components }}; do
            echo "  - name: $comp"
            echo "    sign_off: pending"
          done)

          checklist:
            - item: "All team sign-offs received"
              status: pending
              required: true
            - item: "Integration tests passing"
              status: pending
              required: true
            - item: "Security scan clean"
              status: pending
              required: true
            - item: "Rollback plan documented"
              status: pending
              required: true
          EOF

          echo "content=$(cat releases/${{ inputs.release_id }}.yaml | base64 -w 0)" >> $GITHUB_OUTPUT

      - name: Commit release manifest
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add releases/
          git commit -m "chore(release): create manifest for ${{ inputs.release_id }}"
          git push

      - name: Notify teams
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "🚀 New release created: ${{ inputs.release_id }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*New Release Created*\n\nRelease ID: `${{ inputs.release_id }}`\nComponents: ${{ steps.components.outputs.components }}\n\nPlease review and sign off: <${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Release>"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

  # ===========================================================================
  # Request Sign-offs
  # ===========================================================================
  request-signoffs:
    if: inputs.action == 'request_signoffs'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Read release manifest
        id: manifest
        run: |
          if [ ! -f "releases/${{ inputs.release_id }}.yaml" ]; then
            echo "Release manifest not found"
            exit 1
          fi
          cat releases/${{ inputs.release_id }}.yaml

      - name: Create sign-off issues
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const yaml = require('js-yaml');

            const manifest = yaml.load(fs.readFileSync(`releases/${{ inputs.release_id }}.yaml`, 'utf8'));

            for (const component of manifest.components) {
              await github.rest.issues.create({
                owner: context.repo.owner,
                repo: context.repo.repo,
                title: `[Sign-off Required] ${component.name} - ${{ inputs.release_id }}`,
                body: `## Sign-off Request\n\nRelease: \`${{ inputs.release_id }}\`\nComponent: \`${component.name}\`\n\n### Checklist\n- [ ] Staging tested\n- [ ] No regressions\n- [ ] Ready for production\n\n### To Approve\nComment \`/approve\` on this issue.\n\n### To Reject\nComment \`/reject [reason]\` on this issue.`,
                labels: ['release', 'sign-off-required', component.name]
              });
            }

      - name: Notify via Slack
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "📋 Sign-offs requested for ${{ inputs.release_id }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Sign-off Required*\n\nRelease `${{ inputs.release_id }}` is ready for team sign-offs.\n\nPlease review your components and approve in GitHub Issues."
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

  # ===========================================================================
  # Check Sign-offs Status
  # ===========================================================================
  check-signoffs:
    if: inputs.action == 'check_signoffs'
    runs-on: ubuntu-latest
    outputs:
      all_approved: ${{ steps.check.outputs.all_approved }}
      status: ${{ steps.check.outputs.status }}

    steps:
      - uses: actions/checkout@v4

      - name: Check sign-off status
        id: check
        uses: actions/github-script@v7
        with:
          script: |
            const issues = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              labels: 'release,sign-off-required',
              state: 'open'
            });

            const releaseIssues = issues.data.filter(i =>
              i.title.includes('${{ inputs.release_id }}')
            );

            let status = [];
            let allApproved = true;

            for (const issue of releaseIssues) {
              const comments = await github.rest.issues.listComments({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number
              });

              const approved = comments.data.some(c => c.body.includes('/approve'));
              const rejected = comments.data.some(c => c.body.includes('/reject'));

              status.push({
                component: issue.title.split(' - ')[0].replace('[Sign-off Required] ', ''),
                approved,
                rejected
              });

              if (!approved || rejected) {
                allApproved = false;
              }
            }

            core.setOutput('all_approved', allApproved);
            core.setOutput('status', JSON.stringify(status));

            console.log('Sign-off Status:', status);
            console.log('All Approved:', allApproved);

      - name: Update release manifest
        run: |
          # Update manifest with sign-off status
          echo "Sign-off status: ${{ steps.check.outputs.status }}"

      - name: Report status
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Sign-off Status: ${{ inputs.release_id }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Sign-off Status*\n\nRelease: `${{ inputs.release_id }}`\nAll Approved: ${{ steps.check.outputs.all_approved }}\n\nDetails:\n```${{ steps.check.outputs.status }}```"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

  # ===========================================================================
  # Deploy to Production
  # ===========================================================================
  deploy-production:
    if: inputs.action == 'deploy_production'
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Verify all sign-offs
        id: verify
        run: |
          # In real implementation, check the manifest
          echo "Verifying sign-offs for ${{ inputs.release_id }}..."
          # This would check the actual sign-off status

      - name: Pre-deployment checklist
        run: |
          echo "## Pre-Deployment Checklist"
          echo "- [ ] All sign-offs received"
          echo "- [ ] Staging validation complete"
          echo "- [ ] Rollback plan ready"
          echo "- [ ] On-call notified"

      - name: Deploy (Dry Run)
        if: inputs.dry_run == true
        run: |
          echo "🔍 DRY RUN - No actual deployment"
          echo "Would deploy the following components:"
          cat releases/${{ inputs.release_id }}.yaml

      - name: Deploy (Production)
        if: inputs.dry_run == false
        run: |
          echo "🚀 Deploying to production..."
          # Actual deployment logic here

      - name: Post-deployment verification
        run: |
          echo "Verifying deployment..."
          # Health checks, smoke tests, etc.

      - name: Update release status
        run: |
          echo "Updating release status to 'deployed'"

      - name: Notify completion
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "✅ Release ${{ inputs.release_id }} deployed to production",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Release Complete*\n\nRelease `${{ inputs.release_id }}` has been deployed to production.\n\nDry Run: ${{ inputs.dry_run }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

  # ===========================================================================
  # Rollback
  # ===========================================================================
  rollback:
    if: inputs.action == 'rollback'
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Confirm rollback
        run: |
          echo "⚠️ ROLLBACK INITIATED for ${{ inputs.release_id }}"

      - name: Execute rollback
        if: inputs.dry_run == false
        run: |
          echo "Rolling back..."
          # Rollback logic here

      - name: Notify rollback
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "⚠️ ROLLBACK: ${{ inputs.release_id }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*ROLLBACK EXECUTED*\n\nRelease `${{ inputs.release_id }}` has been rolled back.\n\nInitiated by: ${{ github.actor }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
````

---

## Release Dashboard UI

For visibility, create a simple dashboard (can be a GitHub Pages site or integrate with existing tools):

```markdown
# Release Dashboard

## Current Release: rel-2024-01-15-001

| Status              | Scheduled        | Release Manager |
| ------------------- | ---------------- | --------------- |
| 🟡 Pending Approval | Jan 15, 10:00 AM | @john.doe       |

### Components

| Component         | Version         | Team            | Sign-off      | Status  |
| ----------------- | --------------- | --------------- | ------------- | ------- |
| api               | v1.2.3 → v1.3.0 | @api-team       | ✅ Approved   | Ready   |
| placement-service | v2.1.0 → v2.2.0 | @placement-team | ✅ Approved   | Ready   |
| portal            | v3.0.1 → v3.1.0 | @portal-team    | 🟡 Pending    | Waiting |
| workers           | v1.5.0          | @workers-team   | ⏭️ No changes | Skip    |

### Checklist

| Item               | Status    | Owner     |
| ------------------ | --------- | --------- |
| All team sign-offs | 🟡 2/3    | Teams     |
| Integration tests  | ✅ Passed | CI        |
| Performance tests  | ✅ Passed | CI        |
| Security scan      | ✅ Clean  | Security  |
| Rollback plan      | ✅ Ready  | @john.doe |

### Approvals

| Role            | Approver   | Status      |
| --------------- | ---------- | ----------- |
| Release Manager | @john.doe  | ✅ Approved |
| Tech Lead       | @tech-lead | 🟡 Pending  |
| QA Lead         | @qa-lead   | ✅ Approved |

### Actions

- [Request Missing Sign-offs]
- [View Full Manifest]
- [Start Deployment] (disabled until all approved)
- [Cancel Release]
```

---

## Slack Integration

### Release Bot Commands

```
/release create           - Create new release from staging
/release status           - Show current release status
/release signoff [component] - Sign off on a component
/release approve          - Final approval (release manager only)
/release deploy           - Start production deployment
/release rollback         - Initiate rollback
```

### Automated Notifications

```yaml
# Notification triggers
notifications:
  - event: release_created
    channel: '#releases'
    message: '🚀 New release {release_id} created with {component_count} components'

  - event: signoff_pending
    channel: '#team-{team}'
    message: '📋 Sign-off required for {component} in release {release_id}'

  - event: signoff_received
    channel: '#releases'
    message: '✅ {team} approved {component} for {release_id}'

  - event: all_signoffs_received
    channel: '#releases'
    message: '🎉 All sign-offs received for {release_id}. Ready for deployment!'

  - event: deployment_started
    channel: '#releases'
    message: '🚀 Deployment started for {release_id}'

  - event: deployment_completed
    channel: '#releases'
    message: '✅ {release_id} successfully deployed to production'

  - event: rollback_initiated
    channel: '#releases'
    priority: urgent
    message: '⚠️ ROLLBACK initiated for {release_id} by {user}'
```

---

## Hotfix Process

For urgent production fixes:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Hotfix Process                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Create hotfix branch from production tag                                │
│     git checkout -b hotfix/critical-bug v1.3.0                             │
│                                                                             │
│  2. Fix and test locally                                                    │
│                                                                             │
│  3. Create PR with [HOTFIX] prefix                                         │
│     - Requires: Tech Lead + On-call approval                               │
│     - Skip: Full team sign-off                                             │
│                                                                             │
│  4. Deploy to staging → Quick validation (15 min)                          │
│                                                                             │
│  5. Deploy to production                                                    │
│     - Single component only                                                │
│     - Immediate monitoring                                                 │
│                                                                             │
│  6. Merge hotfix back to main                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Related Documentation

- [Deployment Orchestration](deployment-orchestration.md) – CI/CD pipelines
- [Branching Strategy](branching-strategy.md) – Git workflow
- [Observability](observability.md) – Monitoring during releases
- [Resilience Patterns](resilience-patterns.md) – Rollback procedures
