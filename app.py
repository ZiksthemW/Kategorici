from flask import Flask, render_template, request, redirect, abort, session, url_for
import database, random

app = Flask(__name__)
app.secret_key = "Secret Key"

@app.route('/')
def index():
	session["User"] = None
	session["Admin"] = False
	kategoriler = []
	for kategori in database.dbsorgu("paylasimlar"):
		if kategori[3] not in kategoriler:
			kategoriler.append(kategori[3])
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
		if len(baslik) >= 3 and len(baslik) <= 15 and len(icerik) >= 5 and len(icerik) <= 500 and len(kategori) >= 1 and len(kategori) <= 7:
			if len(database.dbwhere("paylasimlar", "kategori", kategori)) >= 1:
				for a, b, c, d, e, f in database.dbwhere("paylasimlar", "kategori", kategori):
					if baslik == b:
						return f'Seçtiğiniz başlık ("{baslik.upper()}") seçtiğiniz kategoride ("{kategori.upper()}") zaten kullanılıyor! Farklı bir başlık veya kategori ile tekrar paylaşmayı deneyin. (Geri giderek yazınızı kurtarabilirsiniz.)'
			while database.dbwhere("paylasimlar", "yid", sayi) != []:
				sayi = random.randint(0000, 9999)

			database.ekle(sayi, baslik, icerik, kategori.lower(), request.remote_addr)
			return redirect(f"m/{sayi}")
		abort(404)

@app.route("/kategori/<string:kategori>")
def kategoriara(kategori):
	konular = database.dbwhere("paylasimlar", "kategori", kategori)
	return render_template("kategoriara.html", kategori=kategori, konular=konular)

@app.route("/<int:pid>/ihbar", methods=["GET", "POST"])
def ihbar(pid):
	if request.method == "GET":
		return render_template("ihbar.html")
	else:
		if database.dbwhere("paylasimlar", "yid", pid) != []:
			ihbar = request.form.get("ihbar")
			sayi = random.randint(0000, 9999)
			if len(ihbar) >= 5 and len(ihbar) <= 75:
				while database.dbwhere("ihbarlar", "iid", sayi) != []:
					sayi = random.randint(0000, 9999)
				database.ihbarekle(sayi, pid, ihbar, request.remote_addr)
				return redirect(f"/m/{pid}")
		else:
			return "Hata!"

@app.route("/admin/giris", methods=["GET", "POST"])
def admingiris():
  if request.method == "GET":
    return render_template("/admin/login.html")
  else:
    kullanici = request.form.get("kullaniciadi")
    parola = request.form.get("sifre")
    for admin in database.dbsorgu("adminler"):
    	if kullanici == admin[0] and parola == admin[1]:
	    	session["User"] = kullanici
	    	session["Admin"] = True
	    	return redirect("/admin")
    abort(401)

@app.route("/admin")
def adminindex():
	if session["Admin"] == True:
		return render_template("/admin/index.html")
	else:
		abort(404)

@app.route("/admin/yeni", methods=["GET", "POST"])
def adminekle():
	if session["Admin"] == True and session["User"] == "root":
		if request.method == "GET":
			return render_template("/admin/ekle.html")
		else:
			kullanici = request.form.get("kullaniciadi")
			parola = request.form.get("parola")
			mail = request.form.get("mail")
			if len(kullanici) > 0 and len(parola) > 0 and len(mail) > 0:
				for admin in database.dbsorgu("adminler"):
					if kullanici == admin[0] or mail == admin[2]:
						return "Bu mail adresi veya kullanıcı adı zaten kullanılmakta..!"
				database.adminekle(kullanici, parola, mail)
				return url_for("adminindex")
			return "Hata!"
	abort(404)

@app.route("/admin/ihbarlar")
def ihbarlar():
	if session["Admin"] == True:
		ihbarlar = database.dbsorgu("ihbarlar")
		print(database.dbsorgu("ihbarlar"))
		return render_template("/admin/ihbarlar.html", ihbarlar=ihbarlar)
	abort(404)

@app.route("/admin/ihbarlar/tamamla/<int:iid>")
def iid(iid):
	if session["Admin"] == True:
		for ihbarlar in database.dbsorgu("ihbarlar"):
			if iid == ihbarlar[0]:
				database.sil("ihbarlar", "iid", iid)
				return redirect("/admin/ihbarlar")
		return "Hata!"
	else:
		abort(404)

@app.route("/admin/yazilar")
def adminyazilar():
	if session["Admin"] == True:
		yazilar = database.dbsorgu("paylasimlar")
		return render_template("/admin/yazilar.html", yazilar=yazilar)
	abort(404)

@app.route("/admin/reddet/<int:yaziid>")
def adminyaziret(yaziid):
	if session["Admin"] == True:
		for yazi in database.dbsorgu("paylasimlar"):
			if yaziid == yazi[0]:
				database.sil("paylasimlar", "yid", yaziid)
				return redirect("/admin/yazilar")
		return "Yazı bulunamadı!"
	else:
		abort(404)

@app.route("/m/<int:mid>")
def makale(mid):
	yazi = database.dbwhere("paylasimlar", "yid", mid)
	if yazi[0][0] == database.dbwhere("paylasimlar", "yid", mid)[0][0]:
		return render_template("makale.html", yazi=yazi[0])
	abort(404)

if __name__ == '__main__':
	database.tabloolustur()
	app.run(debug=False, host="0.0.0.0")
