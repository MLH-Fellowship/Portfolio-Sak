import os
import re
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict
from datetime import datetime

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true" or not os.getenv("MYSQL_DATABASE"):
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
mydb.connect(reuse_if_open=True)
mydb.create_tables([TimelinePost])


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


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Sakshyam Sigdel",
        url=os.getenv("URL"),
        experiences=experiences,
        education=education,
    )


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html",
        title="Hobbies",
        url=os.getenv("URL"),
        hobbies=hobbies_list,
    )


@app.route("/map")
def map():
    return render_template(
        "map.html",
        title="Places I've Visited",
        url=os.getenv("URL"),
        places=places,
    )


@app.route("/timeline")
def timeline():
    return render_template(
        "timeline.html",
        title="Timeline",
        url=os.getenv("URL"),
    )


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    content = request.form.get("content", "").strip()

    if not name:
        return "Invalid name", 400
    if not content:
        return "Invalid content", 400
    if not EMAIL_RE.match(email):
        return "Invalid email", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    id = request.args.get("id")
    if id is not None:
        try:
            return model_to_dict(TimelinePost.get_by_id(int(id)))
        except TimelinePost.DoesNotExist:
            return {"error": "Post not found"}, 404

    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/api/timeline_post", methods=["DELETE"])
def timeline_post_delete():
    id = request.args.get("id")
    if id is not None:
        deleted = TimelinePost.delete_by_id(int(id))
        if deleted:
            return {"message": "Post Deleted", "id": int(id)}

    return {"message": "Post Not Found"}, 404
