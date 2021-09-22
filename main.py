from pytube import YouTube
from flask import Flask, render_template, request, send_file, url_for, redirect
import urllib.request
import re
from youtubesearchpython import VideosSearch
import urllib.parse
import os

search_keyword = "arcade"
search_keyword = search_keyword.replace(" ", "+")
html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" +
                              search_keyword)
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())\

app = Flask(__name__)

@app.route("/delete/<string:s>")
def delete(s):
	with open("./static/songs.txt", "r") as txt_file:
		data = []
		for i in txt_file:
			data.append(i.replace("\n", ""))
	data.remove(s)
	with open("./static/songs.txt", "w") as txt_file:
		for line in data:
			txt_file.write(line + "\n")
	os.remove(f"./static/songs/{s}")
	return render_template("index.html", songs=data)

def downloader(link):
    title = YouTube(link).title
    title = title.replace(" ", "_")
    arr = os.listdir('/home/runner/MusicPlayer/static/songs')
    if title+".mp3" in arr:
        return title+".mp3"
    else:
        file_object = open('./static/songs.txt', 'a')
        file_object.write(title + ".mp3" + "\n")
        file_object.close()
        tmp = YouTube(link).streams.filter(type="audio", abr="128kbps")
        tmp[0].download("/home/runner/MusicPlayer/static/songs/",
                        filename=title + ".mp3")
        return title + ".mp3"


#print(downloader("https://www.youtube.com/watch?v=oFrvRiixXcA"))
@app.route("/search", methods=["GET", "POST"])
def search():
	#query = request.args.get('query')
	if request.method == "POST":
		result = request.form['keyword']
		videosSearch = VideosSearch(result, limit=20)
		searchResults = videosSearch.result()
		searchResults = searchResults["result"]
		#print(searchResults)
		return render_template("search.html",
		                       len=len(searchResults),
		                       searchResult=searchResults)
	else:
		return render_template("searchResults.html")


@app.route("/download", methods=["GET", "POST"])
def download():
	link = request.args.get("query")
	title = downloader(link)
	#print(title)
	if request.method == "POST":
		path = f"/home/runner/MusicPlayer/static/songs/{title}"
		return send_file(path, as_attachment=True)
	return render_template("download.html", title=title)


@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		result = request.form['keyword']
		videosSearch = VideosSearch(result, limit=20)
		searchResults = videosSearch.result()
		searchResults = searchResults["result"]
		#print(searchResults)
		return render_template("search.html",len=len(searchResults),searchResult=searchResults)
	#arr = os.listdir('/home/runner/MusicPlayer/static/songs')
	with open("./static/songs.txt", "r") as txt_file:
		data = []
		for i in txt_file:
			data.append(i.replace("\n", ""))
	return render_template("index.html", songs=data)


@app.route("/songs/<string:s>", methods=["GET", "POST"])
def songs(s):
    if request.method == "POST":
        result = request.form['keyword']
        videosSearch = VideosSearch(result, limit=20)
        searchResults = videosSearch.result()
        searchResults = searchResults["result"]
        return render_template("search.html",len=len(searchResults),searchResult=searchResults)
    with open("./static/songs.txt", "r") as txt_file:
        data = []
        for i in txt_file:
            data.append(i.replace("\n", ""))
    curr = data.pop(0)
    data.append(curr)
    data.remove(s)
    data.insert(0, s)
    with open("./static/songs.txt", "w") as txt_file:
        for line in data:
            txt_file.write(line + "\n")
    #print(data)
    return render_template("index.html", songs=data)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=143, debug=True)
