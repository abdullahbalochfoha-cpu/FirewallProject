from flask import Flask, render_template, request, redirect, url_for
import ipaddress

app = Flask(__name__)

# Temporary firewall rules
firewall_rules = [
    {"ip": "192.168.1.100", "action": "ALLOW"},
    {"ip": "8.8.8.8", "action": "BLOCK"}
]

# Security Headers
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


@app.route("/")
def index():
    return render_template("index.html", rules=firewall_rules)


@app.route("/add", methods=["GET", "POST"])
def add_rule():
    if request.method == "POST":
        ip = request.form["ip"].strip()
        action = request.form["action"]

        # Validate IP
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            return "<h2>Invalid IP Address</h2><a href='/add'>Go Back</a>"

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
    app.run(host="127.0.0.1", port=5000, debug=False)
    