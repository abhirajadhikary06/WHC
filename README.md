# <i class="fas fa-heartbeat" style="color: #00ff00;"></i> NetPulse

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.3.3-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

The **NetPulse** is a Flask-based web application that allows users to check the health status (up/down) of websites by submitting URLs. It performs real-time HTTP requests, logs results in a Neon-hosted PostgreSQL database, and displays recent checks in a user-friendly interface. The app implements an **Extract, Transform, Load (ETL)** process to ensure robust data handling.

## Features

- **Real-Time Website Checks**: Submit a URL to check its HTTP status, response time, and availability.
- **ETL Pipeline**: Extracts data from HTTP requests, transforms it (e.g., normalizes URLs, formats timestamps in IST), and loads it into a PostgreSQL database.
- **Neon PostgreSQL Integration**: Stores check results in a scalable, serverless PostgreSQL database hosted by Neon.
- **User-Friendly Interface**: Displays the last 10 checks in a table, with flash messages for success or error feedback.
- **Timezone Support**: Timestamps are stored and displayed in Indian Standard Time (IST) in the format `YYYY-MM-DD HH:MM:SS`.
- **POST-Redirect-GET Pattern**: Prevents duplicate submissions on page refresh.

## Project Structure

```
WHC/
├── app.py              # Main Flask application
├── db.py               # Database connection and schema setup
├── etl.py              # ETL process for website checks
├── templates/
│   └── index.html      # HTML frontend for user interaction
├── static/
│   └── style.css       # CSS styling for the frontend
├── .env                # Environment variables (Neon DB URL, Flask secret key)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Prerequisites

- **Python**: 3.8 or higher
- **Neon Account**: For PostgreSQL database hosting ([neon.tech](https://neon.tech))
- **Git**: For cloning the repository
- **psql** (optional): For direct database access

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/abhirajadhikary06/WHC
   cd WHC
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Neon PostgreSQL**:
   - Sign up at [neon.tech](https://neon.tech) and create a new database (e.g., `whc`).
   - Copy the `DATABASE_URL` from the Neon Console (format: `postgresql://username:password@host/dbname?sslmode=require`).
   - Create a `.env` file in the project root:
     ```env
     DATABASE_URL=postgresql://<username>:<password>@<neon-host>/<dbname>?sslmode=require
     SECRET_KEY=9b8f4e2a1c7d3f6e0b2a8c5d4e1f7a9b3c2d8e6f
     ```
   - Replace `<username>`, `<password>`, `<neon-host>`, and `<dbname>` with your Neon credentials.

5. **Initialize the Database**:
   - Run the `db.py` script to create the `website_checks_log` table:
     ```bash
     python db.py
     ```
   - If you encounter a `permission denied for schema public` error, grant permissions using the Neon SQL Editor or `psql`:
     ```sql
     GRANT CREATE, USAGE ON SCHEMA public TO <your-username>;
     ```

6. **Run the Application**:
   ```bash
   python app.py
   ```
   - Open `http://127.0.0.1:5000` in your browser.

## Usage

1. **Access the Web Interface**:
   - Navigate to `http://127.0.0.1:5000`.
2. **Check a Website**:
   - Enter a URL (e.g., `example.com`) in the form and click **Check Website**.
   - The app will display a success or error message and update the table with the check result.
3. **View Recent Checks**:
   - The table shows the last 10 checks, including URL, status, response time (ms), timestamp (in IST), and any error messages.
4. **Error Handling**:
   - Invalid URLs or connection issues are logged with appropriate error messages.
   - Flash messages provide immediate feedback.

## ETL Process

The app implements an **Extract, Transform, Load (ETL)** pipeline in `etl.py`:
- **Extract**: Retrieves the user-submitted URL and performs an HTTP GET request using `requests`.
- **Transform**: Normalizes URLs, interprets HTTP status codes (e.g., 200 → "Up"), converts response times to milliseconds, and formats timestamps in IST (`YYYY-MM-DD HH:MM:SS`).
- **Load**: Stores results in the `website_checks_log` table in Neon PostgreSQL.


## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/) for the web framework.
- Powered by [Neon](https://neon.tech/) for serverless PostgreSQL.
- Uses [requests](https://requests.readthedocs.io/) for HTTP requests and [pytz](https://pythonhosted.org/pytz/) for timezone handling.

For questions or issues, open a ticket on the [GitHub Issues page](https://github.com/<your-username>/WHC/issues).