import sqlite3
from sqlite3 import Error
import sqlitecloud

def create_connection():
    """
    Create a connection to the SQLite Cloud database.
    """
    try:
        # SQLite Cloud connection string
        conn = sqlitecloud.connect(
            "sqlitecloud://czwglqw5hk.g5.sqlite.cloud:8860/jobsdatabase?apikey=vQVqgZyRhqQ6r09X1PiM2bKF0ga6biBIoNbVcfT8SI4"
        )
        print("Connected to SQLite Cloud database.")
        return conn
    except Exception as e:
        print(f"Error connecting to SQLite Cloud: {e}")
        return None


def create_table(conn):
    """
    Create the jobs table if it doesn't already exist.
    """
    sql_create_jobs_table = """
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT UNIQUE,  -- Unique job ID (jk value for Indeed)
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT NOT NULL,  -- Job location
        salary TEXT,  -- Salary range
        link TEXT NOT NULL,
        date_listed TEXT NOT NULL,
        source TEXT NOT NULL  -- Website source (e.g., "indeed")
    );
    """
    try:
        conn.execute(sql_create_jobs_table)
        print("Jobs table created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")


def insert_job(conn, job, source, insert_count, ignore_count):
    """
    Insert a job listing into the jobs table if it doesn't already exist.
    """
    job_id = job[6]  # Use the extracted job ID (data-jk)
    if job_id == "N/A":
        print(f"Failed to extract job_id from job: {job[2]}")  # Debugging print
        return insert_count, ignore_count

    # Check if the job listing already exists
    try:
        cursor = conn.execute("SELECT id FROM jobs WHERE job_id = ? AND source = ?", (job_id, source))
        existing_job = cursor.fetchone()

        if existing_job:
            print(f"Listing ignored (duplicate): {job[0]}, {job_id}")  # Print if the job is a duplicate
            ignore_count += 1
        else:
            # Insert the job listing
            sql_insert_job = """
            INSERT INTO jobs (job_id, title, company, location, salary, link, date_listed, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
            conn.execute(sql_insert_job, (job_id, job[0], job[1], job[2], job[3], job[4], job[5], source))
            print(f"Listing inserted: {job[0]}")  # Print if the job was inserted
            insert_count += 1

    except Exception as e:
        print(f"Error inserting job: {e}")

    return insert_count, ignore_count


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