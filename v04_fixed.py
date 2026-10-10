import re

from argon2 import PasswordHasher
from argon2.low_level import Type
from flask import abort, make_response, request
from markupsafe import escape


password_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=19456,
    parallelism=1,
    type=Type.ID,
)


def booking_fragment(db, password):
    code = request.args.get("code", "")
    if re.fullmatch(r"[A-Z0-9]{8}", code) is None:
        abort(400, description="Код брони: ровно 8 символов A-Z0-9.")

    nights_text = request.form.get("nights", "")
    if re.fullmatch(r"[0-9]{1,2}", nights_text) is None:
        abort(400, description="Количество ночей: целое число от 1 до 30.")
    nights = int(nights_text)
    if not 1 <= nights <= 30:
        abort(400, description="Количество ночей: целое число от 1 до 30.")

    pw = password_hasher.hash(password)
    sql = "SELECT room FROM bookings WHERE code = ?"
    row = db.execute(sql, (code,)).fetchone()
    wish = request.form.get("wish", "")
    return make_response(f"<p>Ваше пожелание: {escape(wish)}</p>")
