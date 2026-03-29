from flask import Flask, send_from_directory, Response, abort
import os
from scraper import Scraper
from calendar_gen import CalendarGenerator

app = Flask(__name__)

# Serve the landing page
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# Dynamic calendar API
@app.route('/<std_id>')
def get_calendar(std_id):
    # Only allow numeric IDs (safety first)
    if not std_id.isdigit():
        # If it's not a digit, it might be a request for a static asset or just a 404
        # But for now, we only care about numeric student IDs
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
