import requests
from datetime import datetime
import pytz
from urllib.parse import urlparse, urljoin
from db import get_db_connection
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def normalize_url(url):
    """Normalize URL by adding scheme if missing."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def generate_fix(url, status_code, status_message):
    """Generate a fix suggestion using Gemini API (4-5 words max)."""
    if status_code and 200 <= status_code <= 299:
        return "Working"
    
    prompt = f"""
    A website ({url}) has HTTP status {status_code or 'none'} ({status_message}).
    Suggest a fix in 4-5 words maximum.
    Examples: "Check DNS configuration", "Verify server status", "Fix URL syntax"
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        response = model.generate_content(prompt)
        fix = response.text.strip()
        # Ensure 4-5 words max
        words = fix.split()
        if len(words) > 5:
            fix = ' '.join(words[:5])
        return fix
    except Exception as e:
        return "Check connection"

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

    # Generate fix suggestion
    fix = generate_fix(url, status_code, status_message)

    # Get current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    checked_at = datetime.now(ist)

    result = {
        'url': url,
        'status_code': status_code,
        'status_message': status_message,
        'response_time_ms': response_time,
        'checked_at': checked_at,
        'fix': fix
    }

    # LOAD
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO website_checks_log (
            url, status_code, status_message, response_time_ms, checked_at, fix
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        result['url'],
        result['status_code'],
        result['status_message'],
        result['response_time_ms'],
        result['checked_at'],
        result['fix']
    ))
    conn.commit()
    cur.close()
    conn.close()

    return result