# Antigravity Integration Patterns

This guide explains how skills integrate with the Antigravity environment, including directory structures, discovery mechanisms, and best practices.

## Directory Structure

### Standard Antigravity Project Layout

```
my-project/
├── .agent/
│   ├── skills/           # Project-specific skills
│   │   ├── skill-creator/
│   │   ├── github-manager/
│   │   └── data-analyst/
│   └── workflows/        # Workflow definitions
├── src/                  # Project source code
└── README.md
```

### Skill Discovery

Antigravity discovers skills in two locations:

1. **Project Skills**: `.agent/skills/` (project-specific)
2. **Global Skills**: `~/.gemini/antigravity/skills/` (available across all projects)

**Recommendation**: Use project skills for domain-specific capabilities, global skills for general utilities.

---

## Skill Activation Flow

### 1. Metadata Loading (Always in Context)

All skill `name` and `description` fields are loaded into context:

```yaml
---
name: github-manager
description: GitHub repository management including PR creation, issue tracking, and branch operations. Use when users need to interact with GitHub repositories.
---
```

**Key Insight**: The `description` field is your skill's "advertisement" - make it comprehensive and trigger-specific.

### 2. Skill Triggering

When a user request matches a skill's description, Antigravity:
1. Loads the full `SKILL.md` body
2. Makes bundled resources available
3. Follows the skill's instructions

### 3. Resource Loading (Progressive)

Resources are loaded on-demand:
- **Scripts**: May be executed without reading into context
- **References**: Loaded when the agent determines they're needed
- **Assets**: Used in output without loading into context

---

## Integration Best Practices

### Practice 1: Skill Metadata Optimization

**Good Description** (Trigger-rich):
```yaml
description: |
  Python code analysis and refactoring. Use when:
  - User requests code review or quality checks
  - Refactoring is needed (extract function, rename variable)
  - Type hints or docstrings should be added
  - Code smells need identification
```

**Poor Description** (Vague):
```yaml
description: Helps with Python code
```

### Practice 2: Reference Organization

For skills with multiple domains, organize references by domain:

```
bigquery-skill/
├── SKILL.md (navigation guide)
└── references/
    ├── finance-schema.md
    ├── sales-schema.md
    └── product-schema.md
```

In `SKILL.md`:
```markdown
## Schema References

- **Finance queries**: See [finance-schema.md](references/finance-schema.md)
- **Sales queries**: See [sales-schema.md](references/sales-schema.md)
- **Product queries**: See [product-schema.md](references/product-schema.md)
```

### Practice 3: Script Execution Patterns

**Pattern A: Deterministic Operations**
```markdown
## Rotating PDFs

Use the bundled script for reliable rotation:

```bash
python3 scripts/rotate_pdf.py input.pdf --degrees 90 --output rotated.pdf
```
```

**Pattern B: Configurable Operations**
```markdown
## Data Cleaning

The cleaning script accepts configuration:

```bash
python3 scripts/clean_data.py data.csv \
  --remove-nulls \
  --normalize-dates \
  --output clean_data.csv
```

See [scripts/clean_data.py](scripts/clean_data.py) for all options.
```

---

## Antigravity-Specific Features

### Feature 1: Artifact Directory Integration

Skills can reference the conversation's artifact directory:

```python
artifact_dir = "/Users/user/.gemini/antigravity/brain/{conversation-id}/"

# Save skill output
output_path = f"{artifact_dir}/analysis_report.md"
```

**Use Case**: Storing intermediate results, generated images, or reports.

### Feature 2: Task Boundary Integration

Skills can use `task_boundary` to communicate progress:

```markdown
## Long-Running Analysis

For multi-step analysis:

1. Set initial task boundary:
   ```python
   task_boundary(
       TaskName="Analyzing Codebase",
       Mode="EXECUTION",
       TaskSummary="Starting analysis of 150 files",
       TaskStatus="Scanning directory structure"
   )
   ```

2. Update as you progress:
   ```python
   task_boundary(
       TaskName="%SAME%",
       TaskSummary="Analyzed 75/150 files. Found 12 code smells.",
       TaskStatus="Processing remaining files"
   )
   ```
```

### Feature 3: User Interaction Patterns

Skills can request user input at decision points:

```markdown
## Deployment Workflow

When deploying:

1. Generate deployment plan
2. Request approval:
   ```python
   notify_user(
       PathsToReview=["/path/to/deployment_plan.md"],
       BlockedOnUser=True,
       Message="Review the deployment plan. Proceed?",
       ShouldAutoProceed=False
   )
   ```
3. Execute deployment after approval
```

---

## Multi-Skill Coordination

### Scenario: Using Multiple Skills Together

When a task requires multiple skills:

**Example**: "Create a GitHub PR with code review feedback"

1. **github-manager** skill: Creates the PR
2. **code-reviewer** skill: Analyzes the code
3. **github-manager** skill: Adds review comments

**Pattern**:
```markdown
## Workflow

1. Activate code-reviewer skill to analyze changes
2. Collect findings
3. Activate github-manager skill to post review
```

### Skill Composition Guidelines

- **Keep skills focused**: One skill = one domain
- **Use clear handoffs**: Document when to switch skills
- **Avoid duplication**: Don't replicate functionality across skills

---

## Environment-Specific Considerations

### Local Development
- Skills in `.agent/skills/` are immediately available
- Changes to `SKILL.md` take effect on next skill trigger
- Test with `quick_validate.py` before use

### Sharing Skills
- Package with `package_skill.py`
- Distribute `.skill` files
- Users extract to their `.agent/skills/` directory

### Version Control
- Commit skills to project repository
- Include in `.agent/skills/` for team access
- Document skill dependencies in project README

---

## Common Integration Patterns

### Pattern 1: Skill Initialization

When a user first uses a skill:

```markdown
## First-Time Setup

On first use, this skill will:
1. Check for required dependencies
2. Create necessary directories
3. Initialize configuration files

Run: `python3 scripts/setup.py`
```

### Pattern 2: Skill Configuration

For configurable skills:

```
skill-name/
├── SKILL.md
├── config.example.json  # Template
└── scripts/
    └── configure.py
```

In `SKILL.md`:
```markdown
## Configuration

Copy `config.example.json` to `config.json` and customize:

```json
{
  "api_endpoint": "https://api.example.com",
  "timeout": 30
}
```
```

### Pattern 3: Skill Dependencies

Document external dependencies clearly:

```markdown
## Requirements

This skill requires:
- Python 3.8+
- `requests` library: `pip install requests`
- API key in environment: `export API_KEY=your_key`

Run `scripts/check_dependencies.py` to verify setup.
```

---

## Troubleshooting

### Skill Not Triggering
- Check `description` field includes relevant keywords
- Ensure skill is in `.agent/skills/` or global skills directory
- Verify `SKILL.md` has valid YAML frontmatter

### Resources Not Loading
- Confirm file paths are relative to skill directory
- Check file names match references in `SKILL.md`
- Verify files exist with `ls -R skill-name/`

### Script Execution Failures
- Test scripts independently before bundling
- Include error handling in scripts
- Document required environment variables
