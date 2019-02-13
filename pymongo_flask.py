from flask import Flask,render_template,request,redirect
from pprint import pprint
import json
import os
from pymongo import MongoClient
import store_in_mogodb as store_movie_data
# import .Recommendation_system.matrix_factorisation
from easy_factor_surprise import remove_user_data,add_user_data
import easy_factor_surprise as recsys
# from requests import request
# store_movie_data.solve()
app = Flask(__name__)
#path to csv files
pathr = 'data/smaller_data/small_ratings.csv'
pathw = 'data/smaller_data/small_ratings_copy.csv'
# pprint(mongo.db.usergit s)
title = "Movie Recommendation"
heading = "Rate alteast 10 movies"
# MONGO_URL = os.environ.get('MONGOHQ_URL')
MONGO_URL = 'mongodb://heroku:t0jAu_Zkkvj0iSCRIMZe07kRboi-t0DQYIrnzY-1bxlHDNXBYp6AjvJXJiwe9w9D-WjrOhhoUzVdOMtyoO8FPQ' \
			'@candidate.66.mongolayer.com:10351,candidate.61.mongolayer.com:11313/app124683125'
client = MongoClient(MONGO_URL)
db=client.app124683125
movies_togive = db.movie_data
for x in movies_togive.find():
	print(x)
show_rating_ = True

@app.route("/")
def home_page():
    # movie_to_find = movies.find_one({'Year': 1995})
    return render_template("index.html",
						   headingh = heading,
						   movies = movies_togive.find(),
						   show_rating = show_rating_)


@app.route("/action", methods=['POST'])
def action ():
	rating_list = request.form.getlist('rating')
	id_list = request.form.getlist("movie_id")
	data_to_send = []
	for i in range(len(id_list)):
		if rating_list[i] !='':
			data_to_send+=[[id_list[i],rating_list[i]]]

	add_user_data(data_to_send, pathr, pathw)
	recommendations = []
	recommendations = recsys.solve_user_user(pathw)
	reclist_user = conv_to_dict(recommendations)

	recommendations = recsys.solve_item_item(pathw)
	reclist_item = conv_to_dict(recommendations)

	recommendations = recsys.solve_matrix_factorisation(pathw)
	reclist_matrix = conv_to_dict(recommendations)

	# print(recommendations)
	heading = "Recommendations for you"
	return render_template("recommendations.html",
						   headingh=heading,
						   movies_user=reclist_user,
						   movies_item = reclist_item,
						   movies_matrix_factor = reclist_matrix)


def conv_to_dict(recommendations):
	reclist = []
	for mov_id in recommendations:
		temp = movies_togive.find(movies_togive.find_one({'MovieID': int(mov_id)}))
		reclist += temp
	# pprint(temp)
	return reclist


# @app.route("/recommendations")
# def action ():
# 	# rating_list = request.form.getlist('rating')
# 	# id_list = request.form.getlist("movie_id")
# 	# data_to_send = []
# 	# for i in range(len(id_list)):
# 	# 	if rating_list[i] !='':
# 	# data_to_send+=[[id_list[i],rating_list[i]]]
# 	# print(len(rating_list))
# 	# pprint(rating_list)
# 	# pprint(data_to_send)
# 	return render_template("index.html",
# 						   headingh=heading,
# 						   movies=1)


if __name__ == '__main__':

	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
	# app.jinja_env.auto_reload = True
	# app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug = False)
