from flask import Flask, render_template, request, redirect,flash
from pprint import pprint
import json
import os
from pymongo import MongoClient

import user_user
import item_item
import matrix_factorisation

# from requests import request
# store_movie_data.solve()
app = Flask(__name__)
# path to csv files
pathr = 'data/smaller_data/small_ratings.csv'
pathw = 'data/smaller_data/small_ratings_copy.csv'
# pprint(mongo.db.usergit s)
title = "Movie Recommendation"
heading = "Rate alteast 10 movies"
MONGO_URL = os.environ.get('MONGOHQ_URL')
print(MONGO_URL)
# MONGO_URL = 'mongodb://heroku:t0jAu_Zkkvj0iSCRIMZe07kRboi-t0DQYIrnzY-1bxlHDNXBYp6AjvJXJiwe9w9D-WjrOhhoUzVdOMtyoO8FPQ' \
# 			'@candidate.66.mongolayer.com:10351,candidate.61.mongolayer.com:11313/app124683125'
client = MongoClient(MONGO_URL)
db = client.app124683125
movies_togive = db.movie_data
# for x in movies_togive.find():
# 	print(x)
show_rating_ = True


@app.route("/")
def home_page():
    # movie_to_find = movies.find_one({'Year': 1995})
    return render_template("index.html",
                           headingh=heading,
                           movies=movies_togive.find(),
                           show_rating=show_rating_)


@app.route("/action", methods=['POST'])
def action():
    rating_list = request.form.getlist('rating')
    id_list = request.form.getlist("movie_id")
    data_to_send = []
    # for i in range(len(id_list)):
    # 	if rating_list[i] !='':
    # 		data_to_send+=[[id_list[i],rating_list[i]]]

    count=0;proceed =True
    for i in range(len(id_list)):
        if rating_list[i] != '':
            # data_to_send+=[[id_list[i],rating_list[i]]]
            data_to_send.append(int(rating_list[i]))
            if(int(rating_list[i]) >5 ):
                proceed=False
            count += 1
        else:
            data_to_send.append(0)
        if i == 177:
            break
    if count>=10 and proceed:

        recommendations = []
        recommendations = user_user.solve(data_to_send)
        # print(type(recommendations))
        reclist_user = conv_to_dict(recommendations)

        recommendations = item_item.solve(data_to_send)
        # print(recommendations)
        reclist_item = conv_to_dict(recommendations)
        # print(reclist_item)
        print(data_to_send)
        recommendations = matrix_factorisation.adduserandsolve(data_to_send)
        reclist_matrix = conv_to_dict(recommendations)

        # print(recommendations)
        heading = "Recommendations for you"
        return render_template("recommendations.html",
                               headingh=heading,
                               movies_user=reclist_user,
                               movies_item=reclist_item,
                               movies_matrix_factor=reclist_matrix)
    else:
        flash('Please rate atleast 10 movies and all ratings should be less than 5')
        return redirect("/")


def conv_to_dict(recommendations):
    reclist = []
    for mov_id in recommendations:
        temp = movies_togive.find(movies_togive.find_one({'MovieID': (mov_id[0])}))
        reclist += temp
    # pprint(temp)
    return reclist


if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.run(debug=True)

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=False)
