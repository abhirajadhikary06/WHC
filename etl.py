import requests
from datetime import datetime
import pytz
from urllib.parse import urlparse, urljoin
from db import get_db_connection

def normalize_url(url):
    """Normalize URL by adding scheme if missing."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def check_website(url):
    """ETL process: Extract, Transform, Load for website health check."""
    # EXTRACT
    url = normalize_url(url)
    try:
        response = requests.get(url, timeout=5)
        status_code = response.status_code
        response_time = response.elapsed.total_seconds() * 1000  # Convert to ms
    except requests.RequestException as e:
        status_code = None
        response_time = None

    # TRANSFORM
    if status_code:
        if 200 <= status_code <= 299:
            status_message = 'Up'
        elif 400 <= status_code <= 499:
            status_message = 'Client Error'
        elif 500 <= status_code <= 599:
            status_message = 'Server Error'
        else:
            status_message = 'Unknown'
    else:
        status_message = 'Down (Connection Error)'

    # Get current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    checked_at = datetime.now(ist)

    result = {
        'url': url,
        'status_code': status_code,
        'status_message': status_message,
        'response_time_ms': response_time,
        'checked_at': checked_at,
    }

    # LOAD
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO website_checks_log (
            url, status_code, status_message, response_time_ms, checked_at, error_message
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        result['url'],
        result['status_code'],
        result['status_message'],
        result['response_time_ms'],
        result['checked_at'],
        result['error_message']
    ))
    conn.commit()
    cur.close()
    conn.close()

    return result