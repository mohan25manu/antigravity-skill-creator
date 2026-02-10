# Antigravity-Specific Skill Examples

This guide provides concrete examples of skills designed for Antigravity environments, showcasing how to leverage Antigravity's unique tools and capabilities.

## Example 1: Web Research Skill (using browser_subagent)

### Skill Structure
```
web-research/
├── SKILL.md
└── scripts/
    └── extract_data.py
```

### SKILL.md (excerpt)
```markdown
---
name: web-research
description: Automated web research and data extraction. Use when users need to gather information from websites, scrape data, or perform multi-step web interactions.
---

# Web Research

## Workflow

1. **Navigate**: Use browser_subagent to open target URLs
2. **Extract**: Capture relevant data from page DOM
3. **Iterate**: Follow links or pagination as needed
4. **Report**: Format findings in structured markdown

## Using browser_subagent

```python
# Example: Research competitor pricing
browser_subagent(
    TaskName="Extracting Pricing Data",
    Task="Navigate to example.com/pricing, capture all plan names and prices, return as JSON",
    RecordingName="pricing_research"
)
```

**Key Pattern**: Always specify clear return conditions in the Task description.
```

### When to Use This Pattern
- Multi-step web navigation
- Data extraction from dynamic sites
- Automated form filling
- Visual verification tasks

---

## Example 2: UI Design Skill (using generate_image)

### Skill Structure
```
ui-designer/
├── SKILL.md
├── references/
│   └── design-system.md
└── assets/
    └── color-palettes.json
```

### SKILL.md (excerpt)
```markdown
---
name: ui-designer
description: Generate UI mockups and design assets. Use when users request interface designs, mockups, landing pages, or visual prototypes.
---

# UI Designer

## Workflow

1. **Understand**: Clarify design requirements and target audience
2. **Design**: Use generate_image to create mockups
3. **Iterate**: Refine based on feedback
4. **Export**: Save final assets

## Using generate_image

```python
# Example: Create a login page mockup
generate_image(
    Prompt="Modern login page UI with email/password fields, 'Remember me' checkbox, and gradient blue background. Clean, minimalist design with rounded corners.",
    ImageName="login_page_mockup"
)
```

**Best Practice**: Be specific about style, colors, and layout in prompts.
```

### When to Use This Pattern
- UI/UX mockups
- Marketing materials
- Icon generation
- Visual prototyping

---

## Example 3: Interactive Tutorial Skill (using notify_user + task_boundary)

### Skill Structure
```
interactive-tutorial/
├── SKILL.md
└── references/
    └── lesson-plans.md
```

### SKILL.md (excerpt)
```markdown
---
name: interactive-tutorial
description: Step-by-step interactive coding tutorials. Use when users want to learn a new technology through guided, hands-on exercises.
---

# Interactive Tutorial

## Workflow

1. **Initialize**: Set task_boundary for the tutorial session
2. **Teach**: Present concept with examples
3. **Practice**: User attempts exercise
4. **Review**: Use notify_user to request code review
5. **Iterate**: Continue to next lesson

## Using task_boundary

```python
task_boundary(
    TaskName="Teaching Python Basics - Lesson 1",
    Mode="EXECUTION",
    TaskSummary="Introduced variables and data types. User completed first exercise.",
    TaskStatus="Waiting for user to attempt loop exercise"
)
```

## Using notify_user

```python
notify_user(
    PathsToReview=["/path/to/user_exercise.py"],
    BlockedOnUser=True,
    Message="Please complete the loop exercise and let me know when ready for review.",
    ShouldAutoProceed=False
)
```

**Key Pattern**: Use task boundaries to track progress across multi-step tutorials.
```

### When to Use This Pattern
- Interactive learning experiences
- Code review workflows
- Multi-session projects
- User-paced tutorials

---

## Example 4: Data Analysis Skill (combining multiple tools)

### Skill Structure
```
data-analyst/
├── SKILL.md
├── scripts/
│   ├── clean_data.py
│   └── visualize.py
└── references/
    └── statistical-methods.md
```

### SKILL.md (excerpt)
```markdown
---
name: data-analyst
description: Automated data analysis and visualization. Use for CSV/Excel analysis, statistical computations, or generating charts and insights.
---

# Data Analyst

## Workflow

1. **Ingest**: Load and validate data
2. **Clean**: Run scripts/clean_data.py
3. **Analyze**: Perform statistical analysis
4. **Visualize**: Generate charts with generate_image
5. **Report**: Create markdown summary with findings

## Tool Combination Example

```python
# Step 1: Clean data
run_command(
    CommandLine="python3 scripts/clean_data.py data.csv",
    Cwd="/path/to/skill"
)

# Step 2: Generate visualization
generate_image(
    Prompt="Bar chart showing sales by region: North $45K, South $38K, East $52K, West $41K. Professional style with grid lines.",
    ImageName="sales_by_region"
)

# Step 3: Present findings
notify_user(
    PathsToReview=["/path/to/analysis_report.md"],
    Message="Analysis complete. Key finding: East region outperforms by 15%."
)
```

**Key Pattern**: Combine deterministic scripts with AI-generated visualizations.
```

### When to Use This Pattern
- Data pipelines
- Automated reporting
- Visual analytics
- Business intelligence

---

## Common Antigravity Patterns

### Pattern 1: Progressive Task Tracking
Use `task_boundary` to communicate progress in long-running operations:

```python
# Start
task_boundary(TaskName="Processing Dataset", Mode="EXECUTION", ...)

# Update
task_boundary(TaskName="%SAME%", TaskSummary="Processed 50/100 files", ...)

# Complete
task_boundary(TaskName="%SAME%", Mode="VERIFICATION", ...)
```

### Pattern 2: User Approval Gates
Use `notify_user` with `BlockedOnUser=True` for critical decisions:

```python
notify_user(
    PathsToReview=["/path/to/implementation_plan.md"],
    BlockedOnUser=True,
    Message="Review the proposed database schema changes before I proceed.",
    ShouldAutoProceed=False  # Requires explicit approval
)
```

### Pattern 3: Artifact Management
Store intermediate results in the artifacts directory:

```python
# Generate and save
generate_image(Prompt="...", ImageName="prototype_v1")
# Artifact saved to: /Users/user/.gemini/antigravity/brain/{conversation-id}/prototype_v1.webp

# Reference in markdown
![Prototype V1](/Users/user/.gemini/antigravity/brain/{conversation-id}/prototype_v1.webp)
```

---

## Best Practices

1. **Tool Selection**: Choose the right tool for the job
   - `browser_subagent`: Web interactions requiring visual context
   - `read_url_content`: Fast text extraction from static pages
   - `generate_image`: UI mockups, diagrams, visual assets
   - `run_command`: Deterministic operations, existing scripts

2. **Error Handling**: Always check command outputs and handle failures gracefully

3. **Context Management**: Use progressive disclosure to avoid loading unnecessary content into context

4. **User Experience**: Provide clear status updates via `task_boundary` for long operations
