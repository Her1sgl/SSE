import hashlib

from flask import make_response, request


def booking_fragment(db, password):
    pw = hashlib.sha256(password.encode()).hexdigest()
    code = request.args.get("code", "")              # 8 символов A-Z0-9
    sql = f"SELECT room FROM bookings WHERE code = '{code}'"
    row = db.execute(sql).fetchone()
    nights = request.form["nights"]                  # ожидается 1..30
    wish = request.form.get("wish", "")
    return make_response("<p>Ваше пожелание: " + wish + "</p>")
