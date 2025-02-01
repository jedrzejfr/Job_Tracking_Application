from .db import create_connection, create_table, insert_job, get_all_jobs

# Expose the database functions for easier imports
__all__ = [
    'create_connection',
    'create_table',
    'insert_job',
    'get_all_jobs'
]
