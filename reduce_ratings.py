import json
import csv
with open('data/ratings.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:
		if int(row['movieId'])<210:
			with open('data/smaller_data/small_ratings.csv','a') as csvfile:
				csvwriter = csv.writer(csvfile)
				# if line_count == 0:
				# 	csvwriter.writerow(reqdFields)
				csvwriter.writerow([row['userId'],row['movieId'],row['rating'],row['timestamp']])