import sqlite3

conn = sqlite3.connect("data/workforce.db")
cursor = conn.cursor()

cursor.execute("UPDATE employees SET category='Skilled' WHERE category='SKILLED'")
cursor.execute("UPDATE employees SET category='Semi-Skilled' WHERE category='SEMI-SKILLED'")
cursor.execute("UPDATE employees SET category='High-Skilled' WHERE category='HIGH-SKILLED'")
cursor.execute("UPDATE employees SET category='Unskilled' WHERE category='UNSKILLED'")

conn.commit()
conn.close()

print("Done")