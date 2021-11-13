# Import
import datetime
import requests
import json

# From
from flask import Flask, render_template, flash, request, redirect
from pathlib import Path 

# CWD
cwd = Path(__file__).parents[0]
cwd = str(cwd)

# Secret File
secret_file = json.load(open(cwd + '/database/secret_file.json'))

# App
app = Flask(__name__)
app.secret_key = 'Secret Key'

@app.route('/')
def main():
  CurrentYear = datetime.datetime.now().year
  return render_template('index.html', CurrentYear=CurrentYear, flag="False")

@app.route('/changelog')
def changelog():
	CurrentYear = datetime.datetime.now().year
	return render_template('changelog.html', CurrentYear=CurrentYear, flag="False")
	
@app.route('/sending',methods=["POST"])
def sending():
  CurrentYear = datetime.datetime.now().year
  password = request.form.get("password")
  content = request.form.get("content")
  color = request.form.get("color")
  title = request.form.get("title")
  description = request.form.get("description")
  author = request.form.get("author")
  image_url = request.form.get("image_url")
  thumbnail_url = request.form.get("thumbnail_url")
  footer = request.form.get("footer")

  webhook_url = secret_file["webhook_url"]
  psw = secret_file["password"]

  data = {}

  if password == psw:
    
    if content != "":
      data["content"] = content

    if description != "":
      data["embeds"] = [{}]

      if title != "":
        data["embeds"][0]['title']=title
      if color != "":
        data["embeds"][0]['color']=int(color[1:],16)
      if description != "":
        data["embeds"][0]['description']=description
      if author != "":
        data["embeds"][0]['author']={'name':author}
      if image_url != "":
        data["embeds"][0]['image']={"url":image_url}
      if thumbnail_url != "":
        data["embeds"][0]['thumbnail']={"url":thumbnail_url}
      if footer != "":
        data["embeds"][0]['footer']={"text":footer}

    response = requests.post(webhook_url, json = data)
    try:
      if response.ok:
        flash('success')
        return redirect('/')
      flash('error')
      return redirect('/')
    except Exception: 
      flash('error')
      return redirect('/')
      
  else:
    flash('wrong_password')
    return redirect('/')

# Run
if __name__ == "__main__":
    app.run()
