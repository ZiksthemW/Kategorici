from flask import Flask, render_template, request, redirect, abort
import database, random

app = Flask(__name__)
kategoriler = []

@app.route('/')
def index():
	global kategoriler
	for a, b, c, d, e in database.dbsorgu():
		if d not in kategoriler:
			kategoriler.append(d)
	return render_template('index.html', kategoriler=kategoriler)

@app.route('/paylas', methods = ["POST", "GET"])
def paylas():
	if request.method == "GET":
		return render_template('paylas.html')
	else:
		baslik = request.form.get("baslik")
		icerik = request.form.get("icerik")
		kategori = request.form.get("kategori")
		sayi = random.randint(1000, 9999)
		tuttu = 0
		if len(baslik) or len(icerik) or len(kategori) != 0:
			for a, b, c, d, e in database.dbsorgu():
				if sayi == a:
					tuttu += 1
			if tuttu == 0:
				database.ekle(sayi, baslik, icerik, kategori.lower(), request.remote_addr)
				return redirect(f"m/{sayi}")

@app.route("/kategori/<string:kategori>")
def kategoriara(kategori):
	global kategoriler
	if kategori in kategoriler:
		konular = database.dbwhere("kategori", kategori)
		print(konular)
		print(database.dbwhere("kategori", kategori))
		return render_template("kategoriara.html", kategori=kategori, konular=konular)
	else:
		abort(404)

@app.route("/m/<int:mid>")
def makale(mid):
	for a, b, c, d, e in database.dbsorgu():
		if a == mid:
			return render_template("makale.html", a=a, b=b, c=c, d=d, e=e)
	abort(404)


if __name__ == '__main__':
	database.tabloolustur()
	app.run(debug=True)