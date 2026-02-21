# team-sync

CLI tool for remote teams to manage knowledge, meetings, and action items.

## Features

- **Knowledge Base**: Index and search documents, chat logs, and team knowledge
- **Meeting Management**: Create meeting records and track action items with automatic reminders
- **Task Board**: Visual board showing each team member's work status and progress

## Installation


## Usage

### Knowledge Base

Add a document:

Search knowledge base:

### Meeting Management

Create a meeting:

List all meetings:

Add action item:

List pending action items:

### Task Board

Add a task:

Update task status:

Show team task board:

## Status Values

- Tasks: `todo`, `in_progress`, `done`
- Priority: `low`, `medium`, `high`

## Data Storage

All data is stored in SQLite database at `~/.team_sync.db`
pip install -r requirements.txt
python main.py --help