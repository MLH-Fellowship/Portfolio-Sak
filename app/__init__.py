import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

experiences = [
    {
        "role": "Online Instructor",
        "org": "iD Tech",
        "period": "June 2026 – present",
        "detail": "Teaching Blender, Python, Arduino, and Scratch.",
    },
    {
        "role": "MLH x Meta Fellow",
        "org": "MLH",
        "period": "June 2026 – September 2026",
        "detail": "",
    },
    {
        "role": "Research Assistant",
        "org": "University of Southern Mississippi",
        "period": "January 2026 – present",
        "detail": "Research in agentic AI.",
    },
]

hobbies_list = [
    {"name": "Rubik's Cube", "image": "Rubiks_Cube.jpg"},
    {"name": "Running", "image": "running.png"},
    {"name": "Hiking", "image": "hollywood_hike1.jpg"},
]


@app.route('/')
def index():
    return render_template(
        'index.html',
        title="Sakshyam Sigdel",
        url=os.getenv("URL"),
        experiences=experiences,
    )


@app.route('/hobbies')
def hobbies():
    return render_template(
        'hobbies.html',
        title="Hobbies",
        url=os.getenv("URL"),
        hobbies=hobbies_list,
    )
