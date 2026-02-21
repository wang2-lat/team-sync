from database import get_connection
from rich.table import Table

def add_task(title, assignee, priority):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, assignee, priority) VALUES (?, ?, ?)",
        (title, assignee, priority)
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def update_task_status(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )
    conn.commit()
    conn.close()

def show_board(console):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT assignee FROM tasks ORDER BY assignee")
    assignees = [row[0] for row in cursor.fetchall()]
    
    if not assignees:
        console.print("[yellow]No tasks found[/yellow]")
        conn.close()
        return
    
    for assignee in assignees:
        table = Table(title=f"{assignee}'s Tasks")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Status", style="green")
        table.add_column("Priority", style="yellow")
        
        cursor.execute(
            "SELECT id, title, status, priority FROM tasks WHERE assignee = ? ORDER BY priority DESC, created_at",
            (assignee,)
        )
        tasks = cursor.fetchall()
        
        for task in tasks:
            status_color = {
                "todo": "[red]TODO[/red]",
                "in_progress": "[yellow]IN PROGRESS[/yellow]",
                "done": "[green]DONE[/green]"
            }.get(task[2], task[2])
            
            table.add_row(str(task[0]), task[1], status_color, task[3])
        
        console.print(table)
        console.print()
    
    conn.close()
