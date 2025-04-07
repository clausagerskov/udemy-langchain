from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from icebreaker import ice_break_with

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary = ice_break_with(name=name)
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "photoUrl": "",
        },
    )

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)