'''
 @Date: 2022-05-17 16:08:41
 @LastEditors: Wu Han
 @LastEditTime: 2022-05-17 18:15:28
 @FilePath: \test\app.py
'''
from flask import Flask,render_template,send_from_directory
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/hiyori/<path:pth>")
def hiyori(pth):
    try:
        return send_from_directory("static/hiyori", pth, as_attachment=True)
    except Exception as e:
        return str(e),404

@app.route("/gongzi/<path:pth>")
def gongzi(pth):
    try:
        return send_from_directory("static/gongzi", pth, as_attachment=True)
    except Exception as e:
        return str(e),404
        
if __name__ == "__main__":
    app.run("0.0.0.0",port=8086)
