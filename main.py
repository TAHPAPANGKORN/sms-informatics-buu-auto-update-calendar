import sys
from scraper import Scraper
from calendar_gen import CalendarGenerator

def main():
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
    else:
        student_id = input("Enter Student ID: ")

    print(f"[*] Scraping exam schedule for {student_id}...")
    scraper = Scraper(student_id)
    exams = scraper.get_exam_schedule()

    if not exams:
        print("[!] No exams found or error occurred.")
        return

    print(f"[*] Found {len(exams)} exams.")
    for i, exam in enumerate(exams, 1):
        print(f"  {i}. {exam['subject']} - {exam['date']} ({exam['time']})")

    print("[*] Generating .ics file...")
    gen = CalendarGenerator(exams)
    output_file = f"exam_schedule_{student_id}.ics"
    gen.generate(output_file)

    print(f"[+] Success! Calendar saved to: {output_file}")
    print("[+] You can now import this file into Apple Calendar or Google Calendar.")

if __name__ == "__main__":
    main()