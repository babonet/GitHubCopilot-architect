# GitHub Copilot Architect - Implementation Instructions

This document contains instructions for GitHub Copilot to ensure consistent maintenance of the progress tracking file as development continues.

## Automatic Progress Tracking

When working on this project, GitHub Copilot should:

1. **Track Implementation Progress**: Update the `IMPLEMENTATION_PROGRESS.md` file after completing any task from the adaptation plan.

2. **Maintain Last Updated Date**: Always update the "Last Updated" date at the top of the `IMPLEMENTATION_PROGRESS.md` file.

3. **Task Completion Marking**: When tasks are completed, mark them with [x] in the progress tracking file.

4. **Task Status Updates**: Provide accurate status updates using these indicators:
   - ✅ Complete section
   - ⏳ In progress section 
   - 🔄 Needs review
   - ⚠️ Issues or blockers

5. **Issues Section**: Add any encountered issues to the "Issues and Blockers" section, including:
   - Description of the issue
   - Files affected
   - Potential solutions

## Progress Update Structure

Ensure that the `IMPLEMENTATION_PROGRESS.md` file maintains the following sections:

1. Core Changes Progress
2. Detailed Implementation Progress (follow steps from adaptation plan)
3. Security and Dependency Implementation
4. Azure OpenAI Client Implementation
5. Next Steps
6. Testing Progress
7. Issues and Blockers

## Output Files Maintenance

As part of development:

1. Generate phase outputs as Markdown files in the `phases_output/` directory
2. Document each phase clearly with timestamps and completion status
3. Reference any implementation challenges in the blockers section

## PEP 8 Compliance

All Python code should follow PEP 8 standards with appropriate type hints and docstrings as specified in the user instructions.

## Testing Requirements

Maintain test coverage of 90%+ and ensure all unit tests using `pytest` pass before considering a task complete.
