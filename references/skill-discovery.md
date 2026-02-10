# Skill Discovery and Composition Patterns

This guide addresses how to handle overlapping skills, when to merge vs. separate skills, and best practices for skill composition in Antigravity.

## The Skill Overlap Problem

### Common Scenario
You have two related skills:
- `github-manager`: Creates PRs, manages issues, handles branches
- `code-reviewer`: Analyzes code quality, suggests improvements

**User Request**: "Review the code in PR #42 and add comments"

**Question**: Which skill should handle this? Both? How do they coordinate?

---

## Decision Framework: Merge vs. Separate

### When to Keep Skills Separate

**Criteria**:
1. **Different domains**: Each skill serves a distinct purpose
2. **Independent usage**: Skills are often used alone
3. **Different trigger patterns**: Clear separation in when each activates
4. **Manageable size**: Each skill's SKILL.md stays under 500 lines

**Example**: `github-manager` + `code-reviewer`
- ✅ Different domains (GitHub API vs. code analysis)
- ✅ Independent usage (can review code without GitHub, can manage GitHub without reviewing)
- ✅ Clear triggers (GitHub operations vs. code quality checks)

**Recommendation**: Keep separate, use composition patterns (see below)

### When to Merge Skills

**Criteria**:
1. **Always used together**: Rarely used independently
2. **Shared context**: Both need the same domain knowledge
3. **Tight coupling**: One skill's output is always the other's input
4. **Small individual size**: Each would be < 100 lines alone

**Example**: `pdf-reader` + `pdf-writer`
- ❌ Often used together (read → modify → write)
- ❌ Shared context (PDF structure knowledge)
- ✅ Tight coupling (write needs read's output)

**Recommendation**: Merge into `pdf-manager`

---

## Composition Patterns

### Pattern 1: Sequential Composition

**Use Case**: Skills execute in a defined sequence

**Example**: GitHub PR Review Workflow

```markdown
## Workflow: PR Review and Comment

1. **Fetch PR** (github-manager skill)
   - Get PR details and changed files
   - Download code to local workspace

2. **Analyze Code** (code-reviewer skill)
   - Run static analysis
   - Identify code smells
   - Generate review comments

3. **Post Comments** (github-manager skill)
   - Format comments for GitHub API
   - Post to PR via GitHub API
```

**Implementation in SKILL.md**:
```markdown
---
name: github-pr-reviewer
description: Automated PR review workflow combining code analysis and GitHub commenting. Use when users want to review a GitHub PR and post feedback.
---

# GitHub PR Reviewer

This skill orchestrates the github-manager and code-reviewer skills.

## Workflow

1. Activate github-manager to fetch PR #X
2. Activate code-reviewer to analyze changes
3. Activate github-manager to post review comments

See [github-manager](../github-manager/SKILL.md) and [code-reviewer](../code-reviewer/SKILL.md).
```

### Pattern 2: Conditional Composition

**Use Case**: Skill selection depends on context

**Example**: Deployment Workflow

```markdown
## Workflow: Deploy Application

1. **Determine Platform** (user specifies or detect from config)
   - AWS? → Activate aws-deployer skill
   - GCP? → Activate gcp-deployer skill
   - Azure? → Activate azure-deployer skill

2. **Execute Deployment** (platform-specific skill)
   - Follow platform-specific workflow
```

**Implementation**:
```markdown
---
name: cloud-deployer
description: Multi-cloud deployment orchestrator. Use when users want to deploy applications to AWS, GCP, or Azure.
---

# Cloud Deployer

## Platform Selection

Ask user or detect from configuration:

**AWS Deployment**: See [aws-deployer](../aws-deployer/SKILL.md)
**GCP Deployment**: See [gcp-deployer](../gcp-deployer/SKILL.md)
**Azure Deployment**: See [azure-deployer](../azure-deployer/SKILL.md)
```

### Pattern 3: Parallel Composition

**Use Case**: Multiple skills execute simultaneously

**Example**: Comprehensive Code Audit

```markdown
## Workflow: Full Codebase Audit

Execute in parallel:
- **security-scanner**: Check for vulnerabilities
- **code-reviewer**: Analyze code quality
- **dependency-checker**: Verify package versions
- **test-coverage**: Calculate coverage metrics

Aggregate results into unified report.
```

---

## Naming Conventions for Related Skills

### Convention 1: Domain Prefix

**Pattern**: `{domain}-{function}`

**Examples**:
- `github-manager`, `github-actions`, `github-security`
- `aws-deployer`, `aws-monitor`, `aws-cost-optimizer`
- `pdf-reader`, `pdf-editor`, `pdf-merger`

**Benefit**: Clear grouping, easy discovery

### Convention 2: Hierarchical Naming

**Pattern**: `{parent}-{child}`

**Examples**:
- `cloud-deployer` (orchestrator)
  - `cloud-deployer-aws` (implementation)
  - `cloud-deployer-gcp` (implementation)
  - `cloud-deployer-azure` (implementation)

**Benefit**: Shows relationship, enables progressive disclosure

### Convention 3: Action-Based Naming

**Pattern**: `{action}-{object}`

**Examples**:
- `analyze-code`, `review-code`, `refactor-code`
- `create-pr`, `review-pr`, `merge-pr`

**Benefit**: Clear purpose, verb-first discovery

---

## Skill Discovery Strategies

### Strategy 1: Skill Registry (SKILL.md Reference)

Create a central registry skill:

```markdown
---
name: skill-registry
description: Directory of all available skills. Use when users ask "what can you do?" or need to discover available capabilities.
---

# Skill Registry

## Development Skills
- [code-reviewer](../code-reviewer/SKILL.md): Code quality analysis
- [refactoring-assistant](../refactoring-assistant/SKILL.md): Code refactoring
- [test-generator](../test-generator/SKILL.md): Unit test creation

## GitHub Skills
- [github-manager](../github-manager/SKILL.md): Repository management
- [github-pr-reviewer](../github-pr-reviewer/SKILL.md): PR review automation

## Cloud Skills
- [aws-deployer](../aws-deployer/SKILL.md): AWS deployment
- [gcp-deployer](../gcp-deployer/SKILL.md): GCP deployment
```

### Strategy 2: Skill Families (Shared References)

Group related skills with shared references:

```
skills/
├── github-family/
│   ├── github-manager/
│   ├── github-pr-reviewer/
│   └── shared-references/
│       ├── github-api.md
│       └── authentication.md
```

Each skill references shared docs:
```markdown
## GitHub API Reference

See [shared-references/github-api.md](../shared-references/github-api.md)
```

### Strategy 3: Capability Tagging (Metadata)

Use metadata to tag capabilities:

```yaml
---
name: github-manager
description: GitHub repository management...
metadata:
  capabilities: [pr-creation, issue-tracking, branch-management]
  integrates-with: [code-reviewer, ci-cd-manager]
---
```

---

## Handling Skill Conflicts

### Conflict Type 1: Overlapping Descriptions

**Problem**: Two skills have similar descriptions

**Example**:
- `code-analyzer`: "Analyzes code quality and suggests improvements"
- `code-reviewer`: "Reviews code and provides feedback"

**Solution**: Make descriptions more specific

```yaml
# code-analyzer
description: Static code analysis using linters and complexity metrics. Use for automated quality checks, not manual review.

# code-reviewer
description: Manual code review with contextual feedback. Use when users want human-like review comments, not just automated checks.
```

### Conflict Type 2: Duplicate Functionality

**Problem**: Two skills implement the same feature

**Solution**: Consolidate or specialize

**Option A - Consolidate**:
Merge into single skill with both capabilities

**Option B - Specialize**:
- `pdf-simple-editor`: Basic operations (rotate, merge)
- `pdf-advanced-editor`: Complex operations (forms, annotations)

### Conflict Type 3: Competing Workflows

**Problem**: Two skills suggest different approaches

**Solution**: Create orchestrator skill

```markdown
---
name: deployment-orchestrator
description: Chooses optimal deployment workflow based on project type and user preferences.
---

# Deployment Orchestrator

## Workflow Selection

- **Simple apps**: Use quick-deploy skill
- **Enterprise apps**: Use comprehensive-deploy skill
- **User preference**: Ask which workflow to follow
```

---

## Best Practices

### 1. Clear Skill Boundaries

**Good**:
```yaml
name: github-pr-creator
description: Creates GitHub pull requests. Use when users want to create a PR from a branch.
```

**Bad**:
```yaml
name: github-helper
description: Helps with GitHub stuff.
```

### 2. Document Skill Relationships

In each skill's SKILL.md:
```markdown
## Related Skills

- **github-manager**: For broader GitHub operations
- **code-reviewer**: Often used before creating PRs
- **ci-cd-manager**: Integrates with PR workflows
```

### 3. Avoid Deep Nesting

**Good** (flat structure):
```
skills/
├── github-manager/
├── code-reviewer/
└── github-pr-reviewer/  # Orchestrates the above two
```

**Bad** (nested structure):
```
skills/
└── github/
    └── manager/
        └── pr/
            └── reviewer/  # Too deep!
```

### 4. Use Progressive Disclosure

For complex skill families:

```markdown
# GitHub Manager

## Quick Start
[Basic operations]

## Advanced Features
- **PR Management**: See [pr-management.md](references/pr-management.md)
- **Issue Tracking**: See [issue-tracking.md](references/issue-tracking.md)
- **Branch Operations**: See [branch-ops.md](references/branch-ops.md)
```

---

## Real-World Examples

### Example 1: Data Science Workflow

**Skills**:
- `data-loader`: Ingests data from various sources
- `data-cleaner`: Cleans and validates data
- `data-analyzer`: Performs statistical analysis
- `data-visualizer`: Creates charts and graphs

**Orchestrator**: `data-science-workflow`

```markdown
## Workflow

1. Load data (data-loader)
2. Clean data (data-cleaner)
3. Analyze data (data-analyzer)
4. Visualize results (data-visualizer)
5. Generate report
```

### Example 2: Web Development Stack

**Skills**:
- `frontend-builder`: React/Vue/Angular apps
- `backend-builder`: API development
- `database-designer`: Schema design
- `deployment-manager`: Hosting and deployment

**Composition**: User requests trigger individual skills or combinations

---

## Summary

**When to Separate Skills**:
- Different domains
- Independent usage patterns
- Clear trigger boundaries

**When to Merge Skills**:
- Always used together
- Shared context
- Tight coupling

**Composition Patterns**:
- Sequential (one after another)
- Conditional (choose based on context)
- Parallel (multiple simultaneously)

**Naming Best Practices**:
- Use domain prefixes
- Action-based naming
- Clear, descriptive names

**Discovery Strategies**:
- Skill registry
- Skill families with shared references
- Capability tagging in metadata
