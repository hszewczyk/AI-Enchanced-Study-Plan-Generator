# AI-Enchanced-Study-Plan-Generator

A web application that helps students generate personalized study plans using Google's **Gemini API**.  
The app analyzes the user’s study habits, subjects, and goals to create structured, time-based study schedules — which can then be **exported to Google Calendar**.


## Features

- **AI-Powered Personalization:** Uses Gemini API to generate study plans based on your study habits and goals.  
- **Time-Structured Sessions:** Creates detailed plans with specific start times, durations, and subjects.  
- **Google Calendar Export:** Automatically generates a downloadable `.ics` file to import into Google Calendar.  
- **Responsive Design:** Clean and mobile-friendly interface built with Tailwind CSS.  
- **Fast and Lightweight:** Powered by Flask for simplicity and speed.


## How It Works

1. The user fills out a short form with details like:
   - Average study hours per day  
   - Preferred study times  
   - Subjects to focus on  
   - Study goal or upcoming deadline  

2. The data is sent to the **Gemini API**, which generates a detailed HTML-formatted study plan.  

3. The Flask backend parses this plan, displays it neatly in the browser, and allows the user to download an `.ics` calendar file.

4. The file can then be **imported directly into Google Calendar**, maintaining all event titles, durations, and descriptions.


## Tech Stack

- **Frontend:** HTML, Tailwind CSS  
- **Backend:** Flask (Python)  
- **AI Integration:** Google Gemini API  
- **Calendar Export:** Python `ics` generation  
- **Parsing Tools:** Regex, BeautifulSoup  


## Project Structure

```
.
├── templates/             # HTML templates for Flask
│   ├── form.html         # Input form for study habits
│   └── result.html        # Displays generated study plan
├── app.py                 # Main Flask application
└── README.md              # Project documentation
```


## License

This project is open-source and available under the MIT License.

---

## Acknowledgments

- [Google Gemini API](https://ai.google/)  
- [Flask](https://flask.palletsprojects.com/)  
- [Tailwind CSS](https://tailwindcss.com/)
