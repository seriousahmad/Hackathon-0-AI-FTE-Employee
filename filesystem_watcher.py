"""
File System Watcher for AI Employee

This script monitors the file system for new files and creates action items
in the Needs_Action folder when new files are detected.
"""

import time
import logging
from pathlib import Path
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('watcher.log'),
        logging.StreamHandler()
    ]
)

class DropFolderHandler(FileSystemEventHandler):
    """Handles file system events and creates action items"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        self.drop_folder = self.vault_path / 'Drop_Folder'  # Where external files are placed

        # Create directories if they don't exist
        self.needs_action.mkdir(exist_ok=True)
        self.inbox.mkdir(exist_ok=True)
        self.drop_folder.mkdir(exist_ok=True)

        logging.info(f"Initialized DropFolderHandler with vault: {vault_path}")

    def on_created(self, event):
        """Called when a file is created in the watched directory"""
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Only process files from the drop folder
        if self.drop_folder in source.parents:
            logging.info(f"New file detected: {source.name}")

            # Copy file to Inbox
            inbox_dest = self.inbox / source.name
            shutil.copy2(source, inbox_dest)

            # Create metadata file in Needs_Action
            self.create_metadata(inbox_dest)

    def on_modified(self, event):
        """Called when a file is modified"""
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Only process files from the drop folder
        if self.drop_folder in source.parents:
            logging.info(f"File modified: {source.name}")

            # Create metadata file in Needs_Action if not already processed
            inbox_dest = self.inbox / source.name
            if inbox_dest.exists():
                self.create_metadata(inbox_dest, action_type="modified")

    def create_metadata(self, source: Path, action_type: str = "created"):
        """Create metadata file in Needs_Action folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        meta_filename = f"FILE_ACTION_{timestamp}_{source.name}.md"
        meta_path = self.needs_action / meta_filename

        metadata_content = f"""---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size}
action_type: {action_type}
timestamp: {datetime.now().isoformat()}
status: pending
---

# New file dropped for processing

## File Information
- **Name:** {source.name}
- **Size:** {source.stat().st_size} bytes
- **Location:** {source}
- **Detected at:** {datetime.now().isoformat()}

## Processing Instructions
1. Review the file content in [[Inbox]]
2. Determine appropriate action based on [[Company_Handbook]]
3. Create a plan in [[Plans]] if needed
4. Move to [[Done]] when completed

## File Content Preview
```
{self._get_file_preview(source)}
```

## Suggested Actions
- [ ] Review file content
- [ ] Determine priority level
- [ ] Assign to appropriate task queue
- [ ] Process according to company policies
"""

        meta_path.write_text(metadata_content)
        logging.info(f"Created action file: {meta_path.name}")

    def _get_file_preview(self, source: Path, max_lines: int = 10):
        """Get a preview of the file content"""
        try:
            with open(source, 'r', encoding='utf-8') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        if i == max_lines:  # Only add ellipsis once
                            lines.append("... (truncated)")
                        break
                    lines.append(line.rstrip())
            return '\n'.join(lines)
        except UnicodeDecodeError:
            return "[Binary file - content not previewable]"
        except Exception as e:
            return f"[Error reading file: {str(e)}]"

def main():
    """Main function to run the file system watcher"""
    vault_path = Path(__file__).parent / "AI_Employee_Vault"

    if not vault_path.exists():
        print(f"Vault directory not found: {vault_path}")
        print("Creating vault directory...")
        vault_path.mkdir(exist_ok=True)

    event_handler = DropFolderHandler(str(vault_path))
    observer = Observer()

    # Watch the drop folder for new files
    drop_folder_path = vault_path / 'Drop_Folder'
    observer.schedule(event_handler, str(drop_folder_path), recursive=False)

    observer.start()
    logging.info(f"File watcher started. Monitoring: {drop_folder_path}")
    logging.info("Press Ctrl+C to stop the watcher")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("File watcher stopped by user")

    observer.join()

if __name__ == "__main__":
    main()