from flask import Flask, send_from_directory, Response, abort
import os

# Robust imports for both local development and Vercel deployment
try:
    from .scraper import Scraper
    from .calendar_gen import CalendarGenerator
except ImportError:
    # This happens when running locally with 'python3 api/index.py'
    try:
        from scraper import Scraper
        from calendar_gen import CalendarGenerator
    except ImportError:
        # Fallback for other environments
        import sys
        sys.path.append(os.path.dirname(__file__))
        from scraper import Scraper
        from calendar_gen import CalendarGenerator

app = Flask(__name__)

# Create absolute path to public folder
# On Vercel, the current working directory is usually the root.
# On local, we determine it relative to this file.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')

# Serve the landing page
@app.route('/')
def index():
    # Attempt to serve from the absolute path
    if os.path.exists(os.path.join(PUBLIC_DIR, 'index.html')):
        return send_from_directory(PUBLIC_DIR, 'index.html')
    # Fallback to local 'public' folder if relative path works
    return send_from_directory('../public', 'index.html')

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
        return Response(f"No exam schedule found for student ID: {std_id}.", status=404, mimetype='text/plain')
        
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
