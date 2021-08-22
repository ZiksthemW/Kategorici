import sqlite3

bglnt = sqlite3.connect('database.db', check_same_thread=False)
cursor = bglnt.cursor()

def tabloolustur():
	bglnt = sqlite3.connect('database.db')
	cursor = bglnt.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS paylasimlar (yid INT, baslik TEXT, icerik TEXT, kategori TEXT, ip TEXT)")
	bglnt.commit()
	bglnt.close()
	return '--\nSuccessfully created the table(s)'

def dbsorgu():
	cursor.execute("SELECT * FROM paylasimlar")
	return cursor.fetchall()

def dbwhere(a, b):
	cursor.execute(f"SELECT * FROM paylasimlar WHERE {a} = '{b}'")
	return cursor.fetchall()

def ekle(a, b, c, d, e):
	try:
		bglnt = sqlite3.connect('database.db')
		cursor = bglnt.cursor()
		cursor.execute('INSERT INTO paylasimlar VALUES (?, ?, ?, ?, ?)', (a, b, c, d, e))
		bglnt.commit()
		bglnt.close()
	except Exception as e:
		return '---\nError:', e