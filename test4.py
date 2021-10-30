import sqlite3

from app import get_cars

db = sqlite3.connect("cmd.db", check_same_thread=False)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#By doing this, when executing a SELECT statement, cursor will return a list of dictionaries
#With key is the column's title, value is the value
db.row_factory = dict_factory
cursor = db.cursor()

#all_info is a dictionary with key is car name, value is another dictionary with key is column's name, value is its value
all_info = {}
#all_cars is a dictionary with key is car_id, value is car's name
all_cars = get_cars("tkthien")
for car in all_cars:
    #car_info is a dictionary is a dictionary with key is the column's name, value is its value
    car_info = cursor.execute("SELECT * FROM history WHERE user_id=? AND car_id=?", ("tkthien", car)).fetchall()
    all_info[all_cars[car]] = car_info

for key, value in all_info.items():
    print("This is key: ", key)
    print("This is value: ", value)
    print("-----------------")
