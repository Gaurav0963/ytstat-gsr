from flask import Flask, render_template, request
from flask_cors import cross_origin
from pytube import YouTube
from youtubesearchpython import *
from pytube import Channel
import pafy

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])  
@cross_origin()
def homePage():
    return render_template("new.html")

@app.route('/review',methods=['POST','GET']) 
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content']
            channel_url = searchString
            video_tab = channel_url + "/videos"

            channel = Channel(video_tab)

            video_url_list = []

            for url in channel.video_urls[:5]:
                video_url_list.append(url)

            reviews = []

            for video_url in video_url_list:
                video = pafy.new(video_url)
                yt1 = YouTube(video_url)
                id = yt1.video_id
                name = video.author
                Title = video.title
                Likes = video.likes
                Views = video.viewcount
                Thumbnail = video.bigthumbhd

                mydict = {"video_URL": video_url, "Title":Title , 'Likes':Likes, "Views": Views, "Thumbnail_link":Thumbnail, "id":id, "author":name}
                
                reviews.append(mydict)
            
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        
        except Exception as e:
            print('The Exception message is: ', e)
            return render_template('error.html')

    else:
        return render_template('new.html')


@app.route('/download/<text>', methods=['GET', 'POST'])
def mylink(text):
    vdnld = pafy.new(text)
    quality = vdnld.getbest()
    q = quality.get_filesize()
    try:
        filename = quality.download('D:/')
        return '<h2 style="color: red;">Filesize={}Kb; Downloaded and saved in D drive</h2>'.format(q/1024)
    except Exception as e:
        print(e)
        return 'Error'

@app.route("/comments/<vid>", methods=['GET', 'POST'])
def comment(vid):
    comments = Comments(vid)
    reviews = []

    while comments.hasMoreComments:
        comments.getNextComments()
        for i in range(len(comments.comments['result'])):
            name = comments.comments['result'][i]['author']['name']
            comnt = comments.comments['result'][i]['content']
            mydict = {'Name':name, 'Comment':comnt}
            reviews.append(mydict)
    return render_template('comment.html', reviews=reviews[0:(len(reviews)-1)])


if __name__ == "__main__":
	app.run(debug=True)