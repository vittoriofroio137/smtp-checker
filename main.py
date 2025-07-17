from flask import Flask, request, jsonify
import smtplib
import dns.resolver
import socket

app = Flask(__name__)

def verify_email(email):
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = sorted(mx_records, key=lambda r: r.preference)[0].exchange.to_text()

        server = smtplib.SMTP(timeout=10)
        server.connect(mx_host)
        server.helo("example.com")
        server.mail("check@example.com")
        code, message = server.rcpt(email)
        server.quit()

        return code == 250
    except Exception as e:
        return False

@app.route("/check")
def check():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Missing email"}), 400
    valid = verify_email(email)
    return jsonify({"email": email, "smtp_valid": valid})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
