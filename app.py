from flask import render_template
from interact import app
import os

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5555))  # 5555 locally, 8080 on Cloud Run
    app.run(host="0.0.0.0", port=port, debug=True)