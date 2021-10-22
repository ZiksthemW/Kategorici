import sqlite3

def tabloolustur():
	bglnt = sqlite3.connect('database.db')
	cursor = bglnt.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS paylasimlar (yid INT, baslik TEXT, icerik TEXT, kategori TEXT, ip TEXT)")
	cursor.execute("CREATE TABLE IF NOT EXISTS adminler (kullaniciadi TEXT, parola TEXT, mail TEXT)")
	cursor.execute("CREATE TABLE IF NOT EXISTS ihbarlar (iid INT, postid INT, ihbar TEXT, ip TEXT)")
	bglnt.commit()
	bglnt.close()
	return '--\nSuccessfully created the table(s)'

def adminekle(user, _pass, mail):
	bglnt = sqlite3.connect('database.db')
	cursor = bglnt.cursor()
	cursor.execute("INSERT INTO adminler VALUES (?, ?, ?)", (user, _pass, mail))
	bglnt.commit()
	bglnt.close()

def ihbarekle(iid, pid, icerik, ip):
	bglnt = sqlite3.connect('database.db')
	cursor = bglnt.cursor()
	cursor.execute("INSERT INTO ihbarlar VALUES (?, ?, ?, ?)", (iid, pid, icerik, ip))
	bglnt.commit()
	bglnt.close()

def dbsorgu(db):
	bglnt = sqlite3.connect('database.db')
	cursor = bglnt.cursor()
	cursor.execute(f"SELECT * FROM {db}")
	return cursor.fetchall()

def dbwhere(a, b, c):
	bglnt = sqlite3.connect('database.db')
	cursor = bglnt.cursor()
	cursor.execute(f"SELECT * FROM {a} WHERE {b} = '{c}'")
	return cursor.fetchall()

def yazionay(yaziid):
	bglnt = sqlite3.connect('database.db')
	cursor = bglnt.cursor()
	cursor.execute(f"UPDATE paylasimlar SET durum = 1 WHERE yid = '{yaziid}'")
	bglnt.commit()
	bglnt.close()

def sil(a, b, c):
	bglnt = sqlite3.connect('database.db')
	cursor = bglnt.cursor()
	cursor.execute(f"DELETE FROM {a} WHERE {b} = '{c}'")
	bglnt.commit()
	bglnt.close()

def ekle(a, b, c, d, e):
	try:
		bglnt = sqlite3.connect('database.db')
		cursor = bglnt.cursor()
		cursor.execute('INSERT INTO paylasimlar VALUES (?, ?, ?, ?, ?)', (a, b, c, d, e))
		bglnt.commit()
		bglnt.close()
	except Exception as e:
		return '---\nError:', e
