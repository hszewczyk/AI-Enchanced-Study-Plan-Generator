# AI-Enchanced-Study-Plan-Generator

A web application that helps students generate personalized study plans using Google's **Gemini API**.  
The app analyzes the user’s study habits, subjects, and goals to create structured, time-based study schedules — which can then be **exported to Google Calendar**.


## Features

- **AI-Powered Personalization:** Uses Gemini API (Gemini 2.5 Flash) to generate study plans based on your study habits and goals.  
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
- **AI Integration:** Google Gemini API (Gemini 2.5 Flash)  
- **Calendar Export:** Python `ics` generation  
- **Parsing Tools:** Regex, BeautifulSoup  


## Project Structure

```
AI-Enchanced-Study-Planner/
│
├── templates/            # HTML templates for Flask
│   ├── form.html
│   └── result.html
├── app.py                # Main Flask application
├── README.md             # Project README and instructions
└── requirements.txt      # Python dependencies
```


## Running the AI-Powered Study Planner Locally

### 1. **Clone the Repository**
```bash
git clone https://github.com/hszewczyk/AI-Enchanced-Study-Plan-Generator.git
cd AI-Enchanced-Study-Plan-Generator
```


### 2. **Create a Virtual Environment**
It’s recommended to use a virtual environment to isolate dependencies.

```bash
python -m venv venv
```

Activate it:

- **Windows:**
```bash
venv\Scripts\activate
```
- **macOS/Linux:**
```bash
source venv/bin/activate
```


### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```


### 4. **Add Your Gemini API Key**
Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_real_api_key_here
```


### 5. **Run the Flask App**
```bash
python app.py
```


## License

This project is open-source and available under the MIT License.


## Acknowledgments

- [Google Gemini API](https://ai.google/)  
- [Flask](https://flask.palletsprojects.com/)  
- [Tailwind CSS](https://tailwindcss.com/)
