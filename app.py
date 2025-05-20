from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
import os
from etl import check_website
from db import get_db_connection, fetch_recent_checks

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            flash('Please enter a URL', 'error')
            return redirect(url_for('index'))
        
        # Run ETL process
        try:
            result = check_website(url)
            flash('Website checked successfully!', 'success')
        except Exception as e:
            flash(f'Error checking website: {str(e)}', 'error')
        
        return redirect(url_for('index'))
    
    return render_template('index.html', checks=fetch_recent_checks())

if __name__ == '__main__':
    app.run(debug=True)