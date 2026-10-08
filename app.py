from flask import Flask, render_template, jsonify, request
from network_monitor import ping_host, dns_lookup, tcp_check

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/ping")
def api_ping():
    host = request.args.get("host", "google.com").strip()
    return jsonify(ping_host(host))


@app.route("/api/dns")
def api_dns():
    host = request.args.get("host", "google.com").strip()
    return jsonify(dns_lookup(host))


@app.route("/api/tcp")
def api_tcp():
    host = request.args.get("host", "google.com").strip()
    try:
        port = int(request.args.get("port", "443"))
    except ValueError:
        port = 443

    return jsonify(tcp_check(host, port))


if __name__ == "__main__":
    app.run(debug=True)
