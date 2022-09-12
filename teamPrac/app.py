from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.0lc3ei6.mongodb.net/?Cluster0=true&w=majority')
db = client.dbsparta


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/running/current.naver',headers=headers)


# 이미지 주소
#content > div.article > div > div.lst_wrap > ul > li:nth-child(1)
# 평점 주소
#content > div.article > div > div.lst_wrap > ul > li > dl > dd.star > dl > dd > div > a > span.num





@app.route('/')
def home():
    #
    # soup = BeautifulSoup(data.text, 'html.parser')
    #
    # trs = soup.select('#content > div.article > div > div.lst_wrap > ul > li')
    #
    # i = 0
    # for tr in trs:
    #     i = i + 1
    #     title = tr.select_one('dl > dt > a').text.strip()
    #     star = tr.select_one('dl > dd.star > dl > dd > div > a > span.num').text[0:1].strip()
    #     image = tr.select_one('div > a > img')['src']
    #     print(i, title, star, image)
    #
    #     doc = {
    #         'movie_num': i,
    #         'title': title,
    #         'star': star,
    #         'image': image
    #     }
    #
    #     db.pracMovie.insert_one(doc)

    return render_template('index.html')


@app.route("/movieReview", methods=["POST"])
def movie_post():
    title_give = request.form['title_give']
    movie_num_give = int(request.form['movie_num_give'])
    review_give = request.form['review_give']
    star_give = request.form['star_give']
    sample_receive = request.form['sample_give']
    print(title_give, movie_num_give, review_give, star_give)
    doc = {
        'title' :title_give,
        'movie_num' : movie_num_give,
        'review' : review_give,
        'star' : star_give
    }
    db.review.insert_one(doc)
    return jsonify({'msg': 'POST 연결 완료!'})


@app.route("/movie", methods=["GET"])
def movie_get():

    movie_list = list(db.pracMovie.find({},{'_id':False}))
    #print(movie_list)
    return jsonify({'movies': movie_list})

@app.route("/movieDetail", methods=["GET"])
def movieDetail_get():
    movie_num = int(request.args['movie_num'])
    #movie_num = int(request.form.get['movie_num', False])

    #print("Location : movieDetail.html?movie_num="movie_num)
    movie_list = list(db.pracMovie.find({"movie_num" : movie_num},{'_id':False}))
    review_list = list(db.review.find({"movie_num" : movie_num},{'_id':False}))
    #print(movie_list)
    print(review_list)
    #return render_template('movieDetail.html', movie_num)
    return jsonify({'movie_list': movie_list, 'review_list':review_list})

@app.route("/reviewUpdate", methods=["POST"])
def updateReview():
    movie_num = int(request.args['movie_num'])


    reviewList = list(db.review.update({'movie_num':movie_num},{'$set':{'':}}))
    #print(movie_list)
    return jsonify({'revies': reviewList})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
