# Personal AI Employee - Bronze Tier

This is the Bronze Tier implementation of the Personal AI Employee system as described in the hackathon document. This represents the minimum viable deliverable with basic functionality.

## Components

### 1. Obsidian Vault Structure
- **Dashboard.md** - Real-time summary of system status
- **Company_Handbook.md** - Rules of engagement and operational guidelines
- **Folders:**
  - `/Inbox` - Incoming items to be processed
  - `/Needs_Action` - Items requiring action from the AI Employee
  - `/Done` - Completed tasks
  - `/Logs` - System logs
  - `/Plans` - Planning documents
  - `/Pending_Approval` - Items awaiting human approval
  - `/Approved` - Approved items
  - `/Rejected` - Rejected items
  - `/Drop_Folder` - Where external files are placed for processing

### 2. File System Watcher
- **filesystem_watcher.py** - Monitors the Drop_Folder for new files
- Creates action items in Needs_Action when files are detected
- Logs all activities for audit trail

### 3. Configuration Files
- **requirements.txt** - Python dependencies

## Setup Instructions

1. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Start the file system watcher:
   ```
   python filesystem_watcher.py
   ```

3. Place files in the `AI_Employee_Vault/Drop_Folder` directory to trigger the system

## How It Works

1. The filesystem watcher continuously monitors the Drop_Folder
2. When a new file is detected, it:
   - Copies the file to the Inbox
   - Creates a metadata file in Needs_Action
   - The AI Employee (Claude Code) can then process these action items
3. Based on the Company Handbook, the AI Employee takes appropriate actions
4. Completed tasks are moved to the Done folder

## Next Steps (Silver/Gold Tier)

Future enhancements could include:
- Gmail watcher integration
- WhatsApp monitoring
- MCP server integration
- Automated social media posting
- Banking integration