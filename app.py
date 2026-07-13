from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary firewall rules (stored in memory)
firewall_rules = [
    {"ip": "192.168.1.100", "action": "ALLOW"},
    {"ip": "8.8.8.8", "action": "BLOCK"}
]


@app.route("/")
def index():
    return render_template("index.html", rules=firewall_rules)


@app.route("/add", methods=["GET", "POST"])
def add_rule():
    if request.method == "POST":
        ip = request.form["ip"]
        action = request.form["action"]

        firewall_rules.append({
            "ip": ip,
            "action": action
        })

        return redirect(url_for("index"))

    return render_template("add_rule.html")


@app.route("/delete/<int:index>")
def delete_rule(index):
    if 0 <= index < len(firewall_rules):
        firewall_rules.pop(index)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)