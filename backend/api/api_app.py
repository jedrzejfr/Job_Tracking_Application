from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import sqlitecloud

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# SQLite Cloud connection string
SQLITE_CLOUD_CONN_STRING = "sqlitecloud://czwglqw5hk.g5.sqlite.cloud:8860/jobsdatabase?apikey=vQVqgZyRhqQ6r09X1PiM2bKF0ga6biBIoNbVcfT8SI4"

@app.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        # Connect to SQLite Cloud
        conn = sqlitecloud.connect(SQLITE_CLOUD_CONN_STRING)
        cursor = conn.execute("SELECT * FROM jobs")  # Fetch all jobs
        jobs = cursor.fetchall()

        # Convert the result to a list of dictionaries
        jobs_list = []
        for job in jobs:
            jobs_list.append({
                "id": job[0],
                "job_id": job[1],
                "title": job[2],
                "company": job[3],
                "location": job[4],
                "salary": job[5],
                "link": job[6],
                "date_listed": job[7],
                "source": job[8]
            })

        # Close the connection
        conn.close()

        # Return the jobs as JSON
        return jsonify(jobs_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)