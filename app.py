import os, json, urllib.request
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "rousstica-secret-2026"
app.config["UPLOAD_FOLDER"] = "videos"
os.makedirs("videos", exist_ok=True)
SECRET_ROUTE = "/roussi-secret-2026"
ADMIN_PASSWORD = "rousstica123"
SOCIAL = {"facebook":"https://www.facebook.com/rousstica","instagram":"https://www.instagram.com/elroussi01","tiktok":"https://www.tiktok.com/@poulis.el.roussi","whatsapp":"https://wa.me/201552432592","phone":"01552432592"}
def load_videos():
    try:
        with open("videos.json", encoding="utf-8") as f: return json.load(f)
    except: return []
def save_videos(v):
    with open("videos.json","w",encoding="utf-8") as f: json.dump(v,f,ensure_ascii=False,indent=2)
def get_followers():
    try:
        with open("followers.json", encoding="utf-8") as f: return int(json.load(f).get("count",15))
    except: return 15
@app.route("/")
def index():
    return render_template("index.html", videos=load_videos(), followers=get_followers(), social=SOCIAL)
@app.route("/api/followers")
def api_followers():
    return jsonify({"followers": get_followers()})
@app.route("/videos/<path:filename>")
def serve_video(filename):
    # يسمح بالمشاهدة والتحميل للعميل
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=False)
@app.route(SECRET_ROUTE, methods=["GET","POST"])
def secret_upload():
    if not session.get("roussi_admin"): return redirect(url_for("secret_login"))
    videos=load_videos()
    if request.method=="POST":
        if "followers_count" in request.form:
            try:
                with open("followers.json","w") as f: json.dump({"count":int(request.form["followers_count"])},f)
            except: pass
            return redirect(url_for("secret_upload"))
        title=request.form.get("title","").strip() or "فيديو جديد"
        file=request.files.get("video")
        if file and file.filename:
            import time as _t
            fname=f"{int(_t.time())}_{secure_filename(file.filename)}"
            file.save(os.path.join("videos",fname))
            videos.insert(0,{"title":title,"file":fname}); save_videos(videos)
        return redirect(url_for("secret_upload"))
    return render_template("admin.html", videos=videos, followers=get_followers(), social=SOCIAL)
@app.route(SECRET_ROUTE+"/login", methods=["GET","POST"])
def secret_login():
    if request.method=="POST" and request.form.get("password")==ADMIN_PASSWORD:
        session["roussi_admin"]=True; return redirect(url_for("secret_upload"))
    return render_template("login.html", error="كلمة السر غلط" if request.method=="POST" else "")
@app.route(SECRET_ROUTE+"/delete/<int:idx>")
def secret_delete(idx):
    if not session.get("roussi_admin"): return redirect(url_for("secret_login"))
    videos=load_videos()
    if 0<=idx<len(videos):
        try: os.remove(os.path.join("videos",videos[idx]["file"]))
        except: pass
        videos.pop(idx); save_videos(videos)
    return redirect(url_for("secret_upload"))
@app.route(SECRET_ROUTE+"/logout")
def secret_logout():
    session.pop("roussi_admin",None); return redirect(url_for("index"))
if __name__=="__main__": app.run(host="0.0.0.0",port=5000,debug=True)
