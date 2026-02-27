# Sample Claude Code Interaction Script

This document explains how Claude Code would interact with the AI Employee vault structure.

## Basic Commands

### 1. Check for new tasks
```
claude "Check /Needs_Action folder for new items to process"
```

### 2. Review company policies
```
claude "Review Company_Handbook.md to understand rules of engagement"
```

### 3. Process a task
```
claude "Process the highest priority item in /Needs_Action according to Company_Handbook guidelines"
```

### 4. Update dashboard
```
claude "Update Dashboard.md with current system status"
```

## Example Workflow

1. Watcher detects a new file in Drop_Folder
2. Creates action item in Needs_Action
3. Claude Code is triggered to:
   - Read the action item
   - Consult Company_Handbook for processing rules
   - Perform necessary actions
   - Update status in appropriate folders
   - Log the activity

## MCP Integration

The system is prepared for MCP (Model Context Protocol) integration:
- File system operations
- Email sending (future)
- Web automation (future)
- Banking operations (future)

## Human-in-the-Loop

For sensitive operations requiring approval:
- Create approval request in Pending_Approval folder
- Wait for human to move to Approved/Rejected
- Continue processing based on approval status