from datetime import datetime, timedelta
from flask import Flask, render_template, request, send_file, Response
from io import BytesIO
from bs4 import BeautifulSoup
from google import genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable.")

client = genai.Client(api_key=API_KEY)

app = Flask(__name__)

today_date = datetime.today()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    shours = request.form['study_hours']
    stime = request.form['study_time']
    subj = request.form['subjects']
    date = request.form['date']
    goal = request.form['goal']

    if shours:
        study_hours = f"The preferred amount of hours daily studying is: {shours}. The plan itself does not have to have that exact amount of study hours per day, but an average. You can think about some days having less hours of studying like weekend."
    else:
        study_hours = ""

    if stime:
        study_time = f"Preferred time of the day to study is: {stime}. Make the plan to have study blocks in this time. If not enough information is provided regarding time of the day, make it up yourself."
    else:
        study_time = ""
    
    if subj:
        subjects = f"Here are the subjects to learn: {subj}. If there is more than subject, make the plan diverse, to not learn the same subject all the time. "
    else:
        subjects = ""

    if date:
        due_date = f"The date for which I should know everything by is: {date}. If it does not make sense, or you can't understand what it means, ignore the whole chunk about the date."
    else:
        due_date = ""
    
    if goal:
        study_goal = f"This is the study goal: {goal}. Try to tailor the study plan to suit this goal. If you can't, don't know how, or the goal is not suitable, does not make sense, ignore it."
    else:
        study_goal = ""

    prompt = f'''
        Today's date is {today_date}. Remember the date when calculating due dates. 
        Create a study plan using the following information: 
        - Average study hours per day: {study_hours} 
        - Preferred study time: {study_time} 
        - Subjects: {subjects} 
        - Due date: {due_date} 
        - Study goal: {study_goal}

        Remember to include short breaks but do not make them too long or too frequent. 
        Do not invent new topics unless explicitly stated. In the study session details, only state the subject.

        Format the response **in clean HTML** so it can be displayed correctly in a browser. 
        Use `<ul>` and `<li>` for the study sessions. Each <li> must include:
        - The exact date (e.g., March 1)
        - The start time (e.g., 10:00 AM)
        - The end time (e.g., 12:00 PM)
        - The subject as description

        Example of a single session line inside <li>:
        "March 1, 10:00 AM - 12:00 PM: Math"

        Do not just provide duration; always provide the **explicit start and end times** for each study session. 
        This will prevent overlapping events when creating the calendar file.


        The HTML headings and other content should be displayed properly in the browser. 
        Make sure the study sessions are **structured so they can be parsed into a calendar file**.
    '''

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    study_plan_html = response.text.strip()
    if study_plan_html.lower().startswith("'''html"):
        study_plan_html = study_plan_html[7:]
    if study_plan_html.endswith("'''"):
        study_plan_html = study_plan_html[:-3]
    study_plan_html = study_plan_html.strip()

    del response

    return render_template('result.html', plan=study_plan_html)

@app.route('/download_ics', methods=['POST'])
def download_ics():
    study_plan_html = request.form['plan']
    soup = BeautifulSoup(study_plan_html, "html.parser")

    del study_plan_html

    full_text = soup.get_text(separator="\n")
    lines = [line.strip() for line in full_text.split("\n") if line.strip()]

    events = []

    for line in lines:
        date_match = re.search(r"(\w+\s\d{1,2})", line)
        time_match = re.search(r"(\d{1,2}:\d{2}\s?[APMapm]{2}|\d{1,2}\s?[APMapm]{2})\s*-\s*(\d{1,2}:\d{2}\s?[APMapm]{2}|\d{1,2}\s?[APMapm]{2})", line)

        if not date_match or not time_match:
            continue

        today = datetime.now()
        date_str = date_match.group(1) + f" {today.year}"

        start_str = time_match.group(1)
        end_str = time_match.group(2)

        if ":" in line:
            subject = line.split(":")[-1].strip()
        else:
            subject = "Study Session"

        if ":" not in start_str:
            start_str = start_str.replace(" ", ":00 ")
        if ":" not in end_str:
            end_str = end_str.replace(" ", ":00 ")

        start_dt = datetime.strptime(date_str + " " + start_str, "%B %d %Y %I:%M %p")
        end_dt = datetime.strptime(date_str + " " + end_str, "%B %d %Y %I:%M %p")

        events.append({
            "summary": f"Study Session: {subject}",
            "description": line.strip(),
            "start": start_dt,
            "end": end_dt
        })

    if not events:
        events.append({
            "summary": "Study Session",
            "description": "AI-generated plan (no specific times found)",
            "start": datetime.now(),
            "end": datetime.now() + timedelta(hours=1)
        })

    return generate_calendar_response(events)
'''
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//StudyPlan//EN\n"
    for e in events:
        ics_content += "BEGIN:VEVENT\n"
        ics_content += f"SUMMARY:{e['summary']}\n"
        ics_content += f"DESCRIPTION:{e['description']}\n"
        ics_content += f"DTSTART:{e['start'].strftime('%Y%m%dT%H%M%S')}\n"
        ics_content += f"DTEND:{e['end'].strftime('%Y%m%dT%H%M%S')}\n"
        ics_content += "END:VEVENT\n"
    ics_content += "END:VCALENDAR"

    return send_file(
        BytesIO(ics_content.encode("utf-8")),
        as_attachment=True,
        download_name="study_plan.ics",
        mimetype="text/calendar"
    )
'''

def generate_calendar_response(events):
    def generate():
        yield "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//StudyPlan//EN\n"
        for e in events:
            yield "BEGIN:VEVENT\n"
            yield f"SUMMARY:{e['summary']}\n"
            yield f"DESCRIPTION:{e['description']}\n"
            yield f"DTSTART:{e['start'].strftime('%Y%m%dT%H%M%S')}\n"
            yield f"DTEND:{e['end'].strftime('%Y%m%dT%H%M%S')}\n"
            yield "END:VEVENT\n"
        yield "END:VCALENDAR"

    return Response(
        generate(),
        mimetype="text/calendar",
        headers={
            "Content-Disposition": "attachment; filename=study_plan.ics"
        }
    )


if __name__ == '__main__':
    app.run(debug=True)