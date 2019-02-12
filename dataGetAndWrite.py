#!/usr/bin/env python
# coding: utf-8
#https://realpython.com/python-csv/


import json
import csv
import time
from requests import get
# valuesTakenOut = []
reqdFields = ['UserID','Title','Year','Rating','Poster']
with open('data/links.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	line_count = 0
	for row in csv_reader:
		# print(row['imdbId'])
		
		url = 'http://www.omdbapi.com/?i=tt'+row['imdbId']+'&apikey=3442999c';
		# print(url)
		time.sleep(0.01)
		response = get(url)
		data  = json.loads(response.text)
		# data  = response
		# print(data)
		scrape = [row['movieId'],data['Title'],data['Year'],data['Poster']]
		# if line_count>52:
		# 	print(data)
		# 	print(scrape)
		# valuesTakenOut += scrape
		print(line_count)
		
		with open('data/movie_data.csv','a') as csvfile:
			csvwriter = csv.writer(csvfile)
			if line_count == 0:
				csvwriter.writerow(reqdFields)
			csvwriter.writerow(scrape)
		line_count+=1;
		if line_count == 210:
			break;
				



