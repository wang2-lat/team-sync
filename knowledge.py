from database import get_connection

def add_document(title, content, tags):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (title, content, tags) VALUES (?, ?, ?)",
        (title, content, tags)
    )
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def search_knowledge(query):
    conn = get_connection()
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute(
        "SELECT id, title, content, tags FROM documents WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?",
        (search_term, search_term, search_term)
    )
    results = cursor.fetchall()
    conn.close()
    return results
