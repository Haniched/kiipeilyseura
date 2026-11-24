from urllib import request
import db

def get_threads():
    sql = """SELECT t.id, t.title, t.climbing_type,
                    COUNT(m.id) AS total,
                    COALESCE(MAX(m.sent_at), t.sent_at) AS last
             FROM threads t LEFT JOIN messages m ON t.id = m.thread_id
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def get_thread(thread_id):
    sql = """SELECT t.id, t.title, t.content, t.sent_at, t.climbing_type,
                    t.user_id, u.username
             FROM threads t, users u
             WHERE t.user_id = u.id AND t.id = ?"""
    result = db.query(sql, [thread_id])
    return result[0] if result else None

def get_messages(thread_id):
    sql = """SELECT m.id, m.content, m.sent_at, m.user_id, u.username
             FROM messages m, users u
             WHERE m.user_id = u.id AND m.thread_id = ?
             ORDER BY m.id"""
    return db.query(sql, [thread_id])

def get_message(message_id):
    sql = """SELECT m.id, m.content, m.user_id, m.thread_id, t.climbing_type
             FROM messages m, threads t
             WHERE m.thread_id = t.id AND m.id = ?"""
    result = db.query(sql, [message_id])
    return result[0] if result else None

def add_thread(title, content, user_id, climbing_type):
    sql = "INSERT INTO threads (title, content, sent_at, user_id, climbing_type) VALUES (?, ?, datetime('now'), ?, ?)"
    db.execute(sql, [title, content, user_id, climbing_type])
    thread_id = db.last_insert_id()
    return thread_id

def add_message(content, user_id, thread_id):
    sql = """INSERT INTO messages (content, sent_at, user_id, thread_id)
             VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, thread_id])

def new_message():
    content = request.form["content"]
    user_id = session["user_id"]
    thread_id = request.form["thread_id"]

    forum.add_message(content, user_id, thread_id)
    return redirect("/thread/" + str(thread_id))

def update_thread(thread_id, content):
    sql = "UPDATE threads SET content = ? WHERE id = ?"
    db.execute(sql, [content, thread_id])

def update_message(message_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ?"
    db.execute(sql, [content, message_id])

def update_thread_type(thread_id, climbing_type):
    sql = "UPDATE threads SET climbing_type = ? WHERE id = ?"
    db.execute(sql, [climbing_type, thread_id])

def remove_thread(thread_id):
    db.execute("DELETE FROM messages WHERE thread_id = ?", [thread_id])
    db.execute("DELETE FROM threads WHERE id = ?", [thread_id])

def remove_message(message_id):
    db.execute("DELETE FROM messages WHERE id = ?", [message_id])

def search(query):
    sql = """SELECT t.id as thread_id,
                    t.title as thread_title, 
                    t.climbing_type,
                    t.sent_at,
                    u.username
             FROM threads t, users u
             WHERE t.user_id = u.id AND (t.title LIKE ? OR t.content LIKE ? OR EXISTS (SELECT 1 FROM messages m
                               WHERE m.thread_id = t.id AND m.content LIKE ?))
             ORDER BY t.sent_at DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like])