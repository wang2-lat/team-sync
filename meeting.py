from database import get_connection

def create_meeting(title, attendees, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO meetings (title, attendees, notes) VALUES (?, ?, ?)",
        (title, attendees, notes)
    )
    meeting_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return meeting_id

def list_meetings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, created_at, attendees FROM meetings ORDER BY created_at DESC"
    )
    meetings = cursor.fetchall()
    conn.close()
    return meetings

def add_action_item(meeting_id, description, assignee):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO action_items (meeting_id, description, assignee) VALUES (?, ?, ?)",
        (meeting_id, description, assignee)
    )
    action_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return action_id

def list_pending_actions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, m.title, a.description, a.assignee, a.created_at
        FROM action_items a
        JOIN meetings m ON a.meeting_id = m.id
        WHERE a.status = 'pending'
        ORDER BY a.created_at DESC
    """)
    actions = cursor.fetchall()
    conn.close()
    return actions
