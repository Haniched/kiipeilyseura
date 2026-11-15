import sqlite3
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def ensure_schema():
    con = get_connection()
    columns = {row[1] for row in con.execute("PRAGMA table_info(threads)")}
    if "climbing_type" not in columns:
        con.execute("ALTER TABLE threads ADD COLUMN climbing_type TEXT NOT NULL DEFAULT 'Bouldering'")
        con.commit()
    con.close()

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    return g.last_insert_id
    
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
