from flask import (
    Flask,
    request,
    make_response,
    render_template,
    jsonify,
    Response,
)
from distutils.util import strtobool
import os.path
import datetime
import dateutil.parser


app = Flask(__name__)

cat_love_cookie_name = "ilovecats"
hints_filename = "hints_timestamp"

hints = {
    "1": (
        """<img src="https://i.guim.co.uk/img/media/"""
        """bfdc32b715106735fa1b93696d555ca5005861ce/0_0_1500_1500/master/"""
        """1500.jpg?width=700&quality=85&auto=format&fit=max"""
        """&s=821bba7a63d9407fc729545846752346">"""
    ),
    "2": (
        """<iframe width="560" height="315" src="https://"""
        """www.youtube-nocookie.com/embed/E-j-vlDuYtA" title="YouTube"""
        """ video player" frameborder="0" allow="accelerometer; autoplay; """
        """clipboard-write; encrypted-media; gyroscope; picture-in-picture" """
        """ allowfullscreen></iframe>"""
    ),
}


@app.route("/")
def main():
    got_cookie = request.cookies.get(cat_love_cookie_name, "false")
    if got_cookie.lower() == "true":
        response = make_response(render_template("reallylovescats.html"), 200)
    elif got_cookie == "undefined":
        # https://github.com/PwnFunction/Blank-Rick-Roll/blob/main/main.py
        response = Response()
        response.headers["link"] = "</static/css/style.css>; rel=stylesheet;"
        response.headers["Refresh"] = "5; url=https://www.hackthebox.eu/"
        response.headers["X-Koniec"] = "Zerknij w zrodlo strony - CTRL + U"
    else:
        response = make_response(render_template("423.html"), 423)
        response.set_cookie(cat_love_cookie_name, "false")

    return response


@app.route("/instruction")
def instruction():
    return render_template("instruction.html")


@app.route("/hints/<number>")
def hints_handle(number):
    if os.path.isfile(hints_filename):
        with open(hints_filename, "r") as f:
            timestamp_str = f.readline().strip()
            timestamp = dateutil.parser.parse(timestamp_str)
        now = datetime.datetime.now(datetime.timezone.utc)
        difference = now - timestamp

        if difference.days >= int(number) - 1:
            content = hints.get(str(number))
            return jsonify({"status": "OK", "content": content})
        else:
            resp = {
                "status": "BAD",
                "reason": (
                    f"Too fast! - You requested a hint at {timestamp.ctime()}"
                    f" - wait at least a day."
                ),
            }
            return jsonify(resp)
    else:
        with open(hints_filename, "w") as f:
            now = datetime.datetime.now(datetime.timezone.utc)
            f.write(str(now))
        content = hints.get(str(number))
        return jsonify({"status": "OK", "content": content})
