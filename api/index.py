from flask import Flask, send_from_directory, Response, abort
import os
import sys

# Add root directory to sys.path so we can import scraper and calendar_gen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import Scraper
from calendar_gen import CalendarGenerator

app = Flask(__name__)

# Create absolute path to public folder (Vercel's root is the working directory)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')

# Serve the landing page
@app.route('/')
def index():
    return send_from_directory(PUBLIC_DIR, 'index.html')

# Dynamic calendar API
@app.route('/<std_id>')
def get_calendar(std_id):
    # Only allow numeric IDs
    if not std_id.isdigit():
        abort(404)
    
    scraper = Scraper(std_id)
    exams = scraper.get_exam_schedule()
    
    if exams is None:
        return Response("Error fetching data from university website. Please check Student ID.", status=500, mimetype='text/plain')
    
    if not exams:
        return Response(f"No exam schedule found for student ID: {std_id}. Please verify the ID on the university website.", status=404, mimetype='text/plain')
        
    generator = CalendarGenerator(exams)
    ical_data = generator.generate()
    
    return Response(
        ical_data,
        mimetype='text/calendar',
        headers={
            "Content-Disposition": f"attachment; filename=exam_schedule_{std_id}.ics",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

if __name__ == "__main__":
    # Local development support (Using 8080 to avoid macOS AirPlay conflict on 5000)
    app.run(host='0.0.0.0', port=8080, debug=True)
