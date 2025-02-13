from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Define the path to the database
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'jobs.db')

# Route to fetch jobs from the database
@app.route('/jobs', methods=['GET'])
def get_jobs():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs ORDER BY id DESC')  # Sort by date_listed in descending order
    jobs = cursor.fetchall()
    conn.close()

    # Convert rows to a list of dictionaries
    job_list = []
    for job in jobs:
        job_list.append({
            'id': job[0],
            'job_id': job[1],
            'title': job[2],
            'company': job[3],
            'location': job[4],
            'salary': job[5],
            'link': job[6],
            'date_listed': job[7],
            'source': job[8]
        })

    return jsonify(job_list)

if __name__ == '__main__':
    app.run(debug=True)