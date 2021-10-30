import sqlite3

db = sqlite3.connect("cmd.db", check_same_thread=False)

cursor = db.cursor()

#all_data is stored as list of sets. [(user_id, car_id, part, service, place, cost, note, date, mileague)]
all_data = cursor.execute("SELECT * FROM history WHERE user_id=?", ("tkthien",))

rows = [dict(row) for row in all_data.fetchall()]

print(rows)

