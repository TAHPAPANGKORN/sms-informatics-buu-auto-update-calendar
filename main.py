import sys
import os
from scraper import Scraper
from calendar_gen import CalendarGenerator

def process_student(student_id):
    print(f"[*] Scraping exam schedule for {student_id}...")
    scraper = Scraper(student_id)
    try:
        exams = scraper.get_exam_schedule()
        if not exams:
            print(f"[!] No exams found for {student_id}.")
            return False

        print(f"[*] Found {len(exams)} exams for {student_id}.")
        
        # Create public directory if it doesn't exist
        os.makedirs("public", exist_ok=True)
        
        print("[*] Generating .ics file...")
        gen = CalendarGenerator(exams)
        output_file = f"public/{student_id}.ics"
        gen.generate(output_file)
        print(f"[+] Success! Saved to: {output_file}")
        return True
    except Exception as e:
        print(f"[!] Error processing {student_id}: {e}")
        return False

def main():
    # Priority 1: Environment Variable (Single ID, usually for testing/secrets)
    env_id = os.environ.get("STUDENT_ID")
    if env_id:
        process_student(env_id)
        return

    # Priority 2: Command Line Argument
    if len(sys.argv) > 1:
        process_student(sys.argv[1])
        return

    # Priority 3: students.txt (List of IDs for Automation)
    if os.path.exists("students.txt"):
        with open("students.txt", "r") as f:
            student_ids = [line.strip() for line in f if line.strip()]
        
        if student_ids:
            print(f"[*] Processing {len(student_ids)} students from students.txt")
            for sid in student_ids:
                process_student(sid)
            return

    # Priority 4: Manual Input
    student_id = input("Enter Student ID: ")
    process_student(student_id)

if __name__ == "__main__":
    main()