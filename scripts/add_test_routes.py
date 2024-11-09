from app import app
from app.routes.helpers import privileged_route, provide_new_login_token, revoke_login_token

@app.route("/login")
def login():
    provide_new_login_token("1", "1")
    return ""

@app.route("/logout")
def logout():
    revoke_login_token()
    return ""

@app.route("/admin")
@privileged_route("1")
def admin():
    return ""
