#!/usr/bin/env python3
"""
Interactive Skill Generator for Antigravity

A guided, interactive tool that creates customized skills based on user input.
Automatically includes relevant Antigravity tool examples and best practices.
"""

import os
import sys
import re
from pathlib import Path

# ANSI color codes for better UX
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def validate_skill_name(name):
    """Validate skill name is in kebab-case"""
    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        return False, "Skill name must be lowercase with hyphens (kebab-case)"
    if name.endswith('-'):
        return False, "Skill name cannot end with a hyphen"
    return True, ""

def get_input(prompt, default=None, validator=None):
    """Get user input with optional default and validation"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        value = input(prompt).strip()
        if not value and default:
            value = default
        
        if validator:
            valid, error = validator(value)
            if not valid:
                print_error(error)
                continue
        
        return value

def get_multiline_input(prompt):
    """Get multiline input (ends with empty line)"""
    print(f"{prompt} (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    return '\n'.join(lines)

def get_choice(prompt, options):
    """Get user choice from a list of options"""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            choice = int(input(f"Choose [1-{len(options)}]: "))
            if 1 <= choice <= len(options):
                return choice - 1
        except ValueError:
            pass
        print_error(f"Please enter a number between 1 and {len(options)}")

def get_multichoice(prompt, options):
    """Get multiple choices from a list of options"""
    print(f"\n{prompt}")
    print(f"{Colors.YELLOW}(Enter numbers separated by commas, e.g., 1,3,4){Colors.END}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            input_str = input("Select: ").strip()
            if not input_str:
                return []
            
            choices = [int(x.strip()) - 1 for x in input_str.split(',')]
            if all(0 <= c < len(options) for c in choices):
                return choices
        except ValueError:
            pass
        print_error("Please enter valid numbers separated by commas")

# Template generators for each Antigravity tool
def generate_browser_subagent_example(skill_name):
    return f"""
## Using browser_subagent

For web automation and data extraction:

```python
browser_subagent(
    TaskName="Extracting Data from Website",
    Task=\"\"\"Navigate to [target URL], 
    capture [specific data elements],
    return the results as [format - JSON/text/etc.]
    
    Return when: [completion condition - data extracted, page loaded, etc.]\"\"\",
    RecordingName="{skill_name.replace('-', '_')}_extraction"
)
```

**Best Practices**:
- Specify clear return conditions in the Task description
- Use descriptive RecordingNames for debugging
- Handle timeouts gracefully
- Be specific about what data to extract and in what format
"""

def generate_generate_image_example(skill_name):
    return f"""
## Generating Visual Assets

For creating mockups, diagrams, or visual assets:

```python
generate_image(
    Prompt=\"\"\"[Detailed description]
    - Style: [modern, minimalist, professional, etc.]
    - Colors: [specific color scheme]
    - Layout: [structure and composition]
    - Elements: [key components to include]\"\"\",
    ImageName="{skill_name.replace('-', '_')}_asset"
)
```

**Tips for Better Results**:
- Be specific about style, colors, and layout
- Include context and purpose in the prompt
- Describe layout structure clearly
- Mention any text or labels to include
"""

def generate_notify_user_example():
    return """
## User Interaction Points

For requesting user approval or feedback:

```python
notify_user(
    PathsToReview=["/path/to/file.md", "/path/to/output"],
    BlockedOnUser=True,  # Set to True if you need approval to continue
    Message="[Clear explanation of what you need from the user]",
    ShouldAutoProceed=False  # False for explicit approval
)
```

**When to Use**:
- Before making destructive changes
- When user input affects next steps
- For reviewing generated content
- At decision points in workflows
"""

def generate_task_boundary_example(skill_name):
    return f"""
## Progress Tracking

For long-running operations and progress updates:

```python
# Initialize task
task_boundary(
    TaskName="Processing {skill_name.replace('-', ' ').title()}",
    Mode="EXECUTION",
    TaskSummary="Starting [operation description]",
    TaskStatus="Loading and validating input",
    PredictedTaskSize=5  # Estimated number of steps
)

# Update progress
task_boundary(
    TaskName="%SAME%",  # Keep same name to update existing task
    TaskSummary="Processed 50/100 items. [Current status description]",
    TaskStatus="Processing remaining items"
)

# Complete
task_boundary(
    TaskName="%SAME%",
    Mode="VERIFICATION",
    TaskSummary="Completed processing. [Summary of results]",
    TaskStatus="Finalizing outputs"
)
```

**Best Practices**:
- Use PLANNING for research/design phases
- Use EXECUTION for implementation
- Use VERIFICATION for testing/validation
- Update TaskSummary with cumulative progress
"""

def generate_run_command_example():
    return """
## Running Scripts and Commands

For executing deterministic operations:

```python
run_command(
    CommandLine="python3 scripts/process.py input.txt --output results.json",
    Cwd="/path/to/working/directory",
    SafeToAutoRun=False,  # True only if completely safe
    WaitMsBeforeAsync=1000  # Wait time before sending to background
)
```

**Safety Guidelines**:
- Set SafeToAutoRun=False for any destructive operations
- Always use absolute paths for Cwd
- Check command outputs for errors
- Use WaitMsBeforeAsync appropriately for operation duration
"""

# Skill type templates
SKILL_TEMPLATES = {
    'workflow': """
## Workflow

This skill implements a multi-step workflow:

1. **[Step 1 Name]**: [Brief description]
2. **[Step 2 Name]**: [Brief description]
3. **[Step 3 Name]**: [Brief description]
4. **[Step 4 Name]**: [Brief description]

### Execution Flow

[Describe the overall flow, decision points, and error handling]
""",
    'tool': """
## Tool Integration

This skill provides integration with [tool/format/API name].

### Key Operations

- **[Operation 1]**: [Description]
- **[Operation 2]**: [Description]
- **[Operation 3]**: [Description]

### Usage Patterns

[Describe common usage patterns and examples]
""",
    'knowledge': """
## Domain Knowledge

This skill provides specialized knowledge for [domain/area].

### Key Concepts

[List and explain key domain concepts]

### Reference Materials

See the `references/` directory for detailed documentation:
- [reference-file-1.md](references/reference-file-1.md): [Description]
- [reference-file-2.md](references/reference-file-2.md): [Description]
""",
    'interactive': """
## Interactive Workflow

This skill guides users through an interactive process.

### Workflow Steps

1. **Initialize**: Set up the environment and gather initial requirements
2. **Interactive Loop**: 
   - Present options or request input
   - Process user responses
   - Provide feedback
3. **Complete**: Finalize and deliver results

### User Interaction Points

[Describe when and how to interact with users]
"""
}

def generate_skill_md(skill_info):
    """Generate complete SKILL.md content based on user selections"""
    
    skill_name = skill_info['name']
    description = skill_info['description']
    triggers = skill_info['triggers']
    skill_type = skill_info['skill_type']
    tools = skill_info['tools']
    
    # Start with frontmatter
    content = f"""---
name: {skill_name}
description: {description} Use when {triggers}
---

# {skill_name.replace('-', ' ').title()}

## Overview

{description}

This skill is triggered when: {triggers}

"""
    
    # Add skill type template
    type_names = ['workflow', 'tool', 'knowledge', 'interactive']
    content += SKILL_TEMPLATES[type_names[skill_type]]
    
    # Add Antigravity tool examples
    if tools:
        content += "\n## Antigravity Tools\n"
        content += "\nThis skill uses the following Antigravity capabilities:\n"
        
        tool_options = [
            ('browser_subagent', 'Web automation and data extraction'),
            ('generate_image', 'Visual asset generation'),
            ('notify_user', 'User interaction and approval'),
            ('task_boundary', 'Progress tracking'),
            ('run_command', 'Script execution')
        ]
        
        for tool_idx in tools:
            tool_name, tool_desc = tool_options[tool_idx]
            content += f"- **{tool_name}**: {tool_desc}\n"
        
        # Add detailed examples for each selected tool
        for tool_idx in tools:
            tool_name = tool_options[tool_idx][0]
            if tool_name == 'browser_subagent':
                content += generate_browser_subagent_example(skill_name)
            elif tool_name == 'generate_image':
                content += generate_generate_image_example(skill_name)
            elif tool_name == 'notify_user':
                content += generate_notify_user_example()
            elif tool_name == 'task_boundary':
                content += generate_task_boundary_example(skill_name)
            elif tool_name == 'run_command':
                content += generate_run_command_example()
    
    # Add resources section if applicable
    if skill_info.get('needs_scripts') or skill_info.get('needs_references') or skill_info.get('needs_assets'):
        content += "\n## Bundled Resources\n\n"
        
        if skill_info.get('needs_scripts'):
            content += "### Scripts\n\n"
            content += "This skill includes executable scripts for deterministic operations:\n\n"
            content += "- `scripts/[script-name].py`: [Description]\n\n"
        
        if skill_info.get('needs_references'):
            content += "### References\n\n"
            content += "Additional documentation and reference materials:\n\n"
            content += "- `references/[reference-name].md`: [Description]\n\n"
        
        if skill_info.get('needs_assets'):
            content += "### Assets\n\n"
            content += "Templates and resources used in output:\n\n"
            content += "- `assets/[asset-name]`: [Description]\n\n"
    
    # Add best practices section
    content += """
## Best Practices

- [Add skill-specific best practices]
- [Common pitfalls to avoid]
- [Optimization tips]

## Examples

### Example 1: [Use Case]

```
[Example usage with expected input/output]
```

### Example 2: [Use Case]

```
[Example usage with expected input/output]
```
"""
    
    return content

def create_skill_structure(skill_info, output_path):
    """Create the skill directory structure and files"""
    skill_name = skill_info['name']
    skill_dir = Path(output_path) / skill_name
    
    # Create main directory
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Create SKILL.md
    skill_md_content = generate_skill_md(skill_info)
    (skill_dir / "SKILL.md").write_text(skill_md_content)
    print_success(f"Created {skill_name}/SKILL.md")
    
    # Create directories and stub files based on selections
    if skill_info.get('needs_scripts'):
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        # Create example script stub
        example_script = scripts_dir / "example_script.py"
        example_script.write_text(f"""#!/usr/bin/env python3
\"\"\"
Example script for {skill_name}

TODO: Implement the actual functionality
\"\"\"

def main():
    \"\"\"Main entry point\"\"\"
    print("TODO: Implement {skill_name} logic")
    pass

if __name__ == "__main__":
    main()
""")
        print_success(f"Created scripts/example_script.py stub")
    
    if skill_info.get('needs_references'):
        refs_dir = skill_dir / "references"
        refs_dir.mkdir(exist_ok=True)
        
        # Create example reference stub
        example_ref = refs_dir / "example_reference.md"
        example_ref.write_text(f"""# Reference Documentation

TODO: Add detailed reference documentation, schemas, or domain knowledge here.

## Section 1

[Content]

## Section 2

[Content]
""")
        print_success(f"Created references/example_reference.md stub")
    
    if skill_info.get('needs_assets'):
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        # Create README for assets
        assets_readme = assets_dir / "README.md"
        assets_readme.write_text(f"""# Assets Directory

Place templates, images, boilerplate code, and other output resources here.

Examples:
- Templates (HTML, React, etc.)
- Images and icons
- Sample documents
- Font files
""")
        print_success(f"Created assets/ directory")
    
    return skill_dir

def main():
    """Main interactive flow"""
    print_header("🎨 Antigravity Skill Creator - Interactive Mode")
    print(f"{Colors.BOLD}Let's create an amazing skill together!{Colors.END}\n")
    
    skill_info = {}
    
    # 1. Get basic information
    print_info("Step 1: Basic Information")
    skill_info['name'] = get_input(
        "Skill name (kebab-case, e.g., 'web-scraper')",
        validator=validate_skill_name
    )
    
    skill_info['description'] = get_input(
        "Brief description (1-2 sentences)",
        validator=lambda x: (len(x) >= 10, "Description should be at least 10 characters")
    )
    
    skill_info['triggers'] = get_input(
        "When should this skill trigger? (e.g., 'users need to extract data from websites')"
    )
    
    # 2. Skill type
    print_info("\nStep 2: Skill Type")
    skill_types = [
        "Workflow - Multi-step process (e.g., deployment, testing)",
        "Tool Integration - Specific formats/APIs (e.g., PDF, GitHub)",
        "Knowledge Base - Domain expertise (e.g., schemas, policies)",
        "Interactive - User-guided workflows (e.g., tutorials, reviews)"
    ]
    skill_info['skill_type'] = get_choice("What type of skill is this?", skill_types)
    
    # 3. Antigravity tools
    print_info("\nStep 3: Antigravity Tools")
    tool_options = [
        "browser_subagent - Web automation, scraping, visual verification",
        "generate_image - UI mockups, diagrams, visual assets",
        "notify_user - User approval points, feedback requests",
        "task_boundary - Progress tracking for long operations",
        "run_command - Execute scripts, shell commands"
    ]
    skill_info['tools'] = get_multichoice(
        "Which Antigravity tools will this skill use?",
        tool_options
    )
    
    # 4. Resources needed
    print_info("\nStep 4: Resources")
    resource_options = [
        "Scripts - Deterministic operations",
        "References - Documentation, schemas, examples",
        "Assets - Templates, images, boilerplate code"
    ]
    resources = get_multichoice(
        "What resources does this skill need?",
        resource_options
    )
    
    skill_info['needs_scripts'] = 0 in resources
    skill_info['needs_references'] = 1 in resources
    skill_info['needs_assets'] = 2 in resources
    
    # 5. Output path
    print_info("\nStep 5: Output Location")
    output_path = get_input(
        "Output directory",
        default="."
    )
    
    # Generate the skill
    print_header("\n✨ Generating your skill...")
    
    try:
        skill_dir = create_skill_structure(skill_info, output_path)
        
        # Validate the generated skill
        print_info("\nValidating generated skill...")
        # We'll just check if SKILL.md exists and has content
        skill_md_path = skill_dir / "SKILL.md"
        if skill_md_path.exists() and skill_md_path.stat().st_size > 0:
            print_success("Skill structure validated")
        
        print_header(f"\n🎉 Success! Your skill is ready at: {skill_dir}")
        
        print(f"\n{Colors.BOLD}Next steps:{Colors.END}")
        print(f"  1. Review and customize {skill_dir}/SKILL.md")
        if skill_info.get('needs_scripts'):
            print(f"  2. Implement scripts/example_script.py")
        if skill_info.get('needs_references'):
            print(f"  3. Add documentation to references/")
        print(f"  4. Run: python3 scripts/quick_validate.py {skill_dir}")
        print(f"  5. Package: python3 scripts/package_skill.py {skill_dir}")
        
    except Exception as e:
        print_error(f"Error creating skill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
