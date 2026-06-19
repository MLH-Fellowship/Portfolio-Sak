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

education = [
    {
        "degree": "BSc in Computer Engineering",
        "org": "University of Southern Mississippi",
        "period": "2024 – 2028",
    },
]

# left/top are percentages on an equirectangular world map:
# left = (lon + 180) / 360, top = (90 - lat) / 180
places = [
    {"name": "Nepal", "left": 73.7, "top": 34.6},
    {"name": "New York", "left": 29.4, "top": 27.4},
    {"name": "Los Angeles", "left": 17.2, "top": 31.1},
    {"name": "Indonesia", "left": 79.7, "top": 53.5},
    {"name": "India", "left": 71.4, "top": 34.1},
]


@app.context_processor
def inject_pages():
    pages = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue
        name = "Home" if rule.endpoint == "index" else rule.endpoint.capitalize()
        pages.append({"name": name, "url": str(rule)})
    pages.sort(key=lambda page: page["url"])
    return dict(pages=pages)


@app.route('/')
def index():
    return render_template(
        'index.html',
        title="Sakshyam Sigdel",
        url=os.getenv("URL"),
        experiences=experiences,
        education=education,
    )


@app.route('/hobbies')
def hobbies():
    return render_template(
        'hobbies.html',
        title="Hobbies",
        url=os.getenv("URL"),
        hobbies=hobbies_list,
    )


@app.route('/map')
def map():
    return render_template(
        'map.html',
        title="Places I've Visited",
        url=os.getenv("URL"),
        places=places,
    )
