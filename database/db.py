import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Create a database connection to the SQLite database specified by db_file.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn


def create_table(conn):
    """
    Create the jobs table if it doesn't exist.
    """
    sql_create_jobs_table = """
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT,  -- Unique job ID (jk value for Indeed)
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        link TEXT NOT NULL,
        date_listed TEXT NOT NULL,
        source TEXT NOT NULL,  -- Website source (e.g., "indeed")
        UNIQUE(job_id, source)  -- Composite unique key
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_jobs_table)
        print("Jobs table created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_job(conn, job, source):
    """
    Insert a job listing into the jobs table if it doesn't already exist.
    """
    job_id = job[4]  # Use the extracted job ID (data-jk)
    if job_id == "N/A":
        print(f"Failed to extract job_id from job: {job[2]}")  # Debugging print

    sql_insert_job = """
    INSERT OR IGNORE INTO jobs (job_id, title, company, link, date_listed, source)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_insert_job, (job_id, job[0], job[1], job[2], job[3], source))
        conn.commit()
        print(f"Job inserted or ignored (if duplicate): {job[0]}")  # Print the job title
    except Error as e:
        print(f"Error inserting job: {e}")


def get_all_jobs(conn):
    """
    Retrieve all job listings from the jobs table.
    """
    sql_get_jobs = "SELECT * FROM jobs;"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_get_jobs)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error retrieving jobs: {e}")
        return []