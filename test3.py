import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sqlite3.connect("cmd.db", check_same_thread=False)

db.row_factory = dict_factory
cursor = db.cursor()

#Now, all_data is a list containing dictionaries
all_data = cursor.execute("SELECT * FROM history WHERE user_id=?", ("tkthien",)).fetchall()

for x in all_data:
    print(type(x["cost"]))
    print(x["cost"])

