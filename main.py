import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from database import init_db
from knowledge import add_document, search_knowledge
from meeting import create_meeting, list_meetings, add_action_item, list_pending_actions
from tasks import add_task, update_task_status, show_board

app = typer.Typer(help="CLI tool for remote teams to manage knowledge, meetings, and action items")
console = Console()

@app.callback()
def callback():
    init_db()

kb_app = typer.Typer(help="Knowledge base commands")
app.add_typer(kb_app, name="kb")

@kb_app.command("add")
def kb_add(
    title: str = typer.Argument(..., help="Document title"),
    content: str = typer.Argument(..., help="Document content"),
    tags: str = typer.Option("", help="Comma-separated tags")
):
    """Add a document to knowledge base"""
    doc_id = add_document(title, content, tags)
    console.print(f"[green]Document added with ID: {doc_id}[/green]")

@kb_app.command("search")
def kb_search(query: str = typer.Argument(..., help="Search query")):
    """Search knowledge base"""
    results = search_knowledge(query)
    if not results:
        console.print("[yellow]No results found[/yellow]")
        return
    
    table = Table(title="Search Results")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Content Preview", style="white")
    table.add_column("Tags", style="magenta")
    
    for doc in results:
        preview = doc[2][:80] + "..." if len(doc[2]) > 80 else doc[2]
        table.add_row(str(doc[0]), doc[1], preview, doc[3] or "")
    
    console.print(table)

meeting_app = typer.Typer(help="Meeting management commands")
app.add_typer(meeting_app, name="meeting")

@meeting_app.command("create")
def meeting_create(
    title: str = typer.Argument(..., help="Meeting title"),
    attendees: str = typer.Argument(..., help="Comma-separated attendees"),
    notes: str = typer.Option("", help="Meeting notes")
):
    """Create a new meeting record"""
    meeting_id = create_meeting(title, attendees, notes)
    console.print(f"[green]Meeting created with ID: {meeting_id}[/green]")

@meeting_app.command("list")
def meeting_list():
    """List all meetings"""
    meetings = list_meetings()
    if not meetings:
        console.print("[yellow]No meetings found[/yellow]")
        return
    
    table = Table(title="Meetings")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Date", style="yellow")
    table.add_column("Attendees", style="white")
    
    for m in meetings:
        table.add_row(str(m[0]), m[1], m[2], m[3])
    
    console.print(table)

@meeting_app.command("action")
def meeting_action(
    meeting_id: int = typer.Argument(..., help="Meeting ID"),
    description: str = typer.Argument(..., help="Action item description"),
    assignee: str = typer.Argument(..., help="Person assigned")
):
    """Add action item to a meeting"""
    action_id = add_action_item(meeting_id, description, assignee)
    console.print(f"[green]Action item added with ID: {action_id}[/green]")

@meeting_app.command("pending")
def meeting_pending():
    """List pending action items"""
    actions = list_pending_actions()
    if not actions:
        console.print("[green]No pending action items[/green]")
        return
    
    table = Table(title="Pending Action Items")
    table.add_column("ID", style="cyan")
    table.add_column("Meeting", style="green")
    table.add_column("Description", style="white")
    table.add_column("Assignee", style="yellow")
    table.add_column("Created", style="magenta")
    
    for a in actions:
        table.add_row(str(a[0]), a[1], a[2], a[3], a[4])
    
    console.print(table)

task_app = typer.Typer(help="Task board commands")
app.add_typer(task_app, name="task")

@task_app.command("add")
def task_add(
    title: str = typer.Argument(..., help="Task title"),
    assignee: str = typer.Argument(..., help="Person assigned"),
    priority: str = typer.Option("medium", help="Priority: low, medium, high")
):
    """Add a new task"""
    task_id = add_task(title, assignee, priority)
    console.print(f"[green]Task added with ID: {task_id}[/green]")

@task_app.command("update")
def task_update(
    task_id: int = typer.Argument(..., help="Task ID"),
    status: str = typer.Argument(..., help="Status: todo, in_progress, done")
):
    """Update task status"""
    update_task_status(task_id, status)
    console.print(f"[green]Task {task_id} updated to {status}[/green]")

@task_app.command("board")
def task_board():
    """Show team task board"""
    show_board(console)

if __name__ == "__main__":
    app()
