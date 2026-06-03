import os
import uuid
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
import msal

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]


def build_msal_app():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())

    auth_url = build_msal_app().get_authorization_request_url(
        scopes=SCOPE,
        state=session["state"],
        redirect_uri=REDIRECT_URI,
    )

    return redirect(auth_url)


@app.route("/getAToken")
def authorized():
    if request.args.get("state") != session.get("state"):
        return "State mismatch. Possible CSRF issue.", 400

    if "error" in request.args:
        return f"Login error: {request.args.get('error_description')}", 400

    result = build_msal_app().acquire_token_by_authorization_code(
        request.args["code"],
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI,
    )

    if "error" in result:
        return f"Token error: {result.get('error_description')}", 400

    claims = result.get("id_token_claims", {})
    session["user"] = claims

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=session["user"])


@app.route("/admin")
@login_required
def admin():
    user = session["user"]
    groups = user.get("groups", [])

    # For now this displays group IDs from Entra.
    # We will map IAM-Admins group ID after testing the token.
    admin_group_id = os.getenv("IAM_ADMINS_GROUP_ID", "")

    if admin_group_id not in groups:
        return render_template("access_denied.html", user=user), 403

    return render_template("admin.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"{AUTHORITY}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri=http://localhost:5000/"
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)