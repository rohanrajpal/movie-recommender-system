# movie-recommender-system
Rohan Rajpal -2017089  
This is my submission for the Intern/Member Programming Task - Summer 2019  
**I have been given an extension (till 18th February) to do the deadline.**
## Data Acquisition 

* I've collected the data using the omdb api. 200 Imdb movie Ids were taken from the MovieLens database. The script is `dataGetAndWrite.py`
* After collecting the data I stored all the data in a mongodb database using `store_in_mogodb.py`
## Movie Recommendation System
* I used *flask* for the dynamic handling of data for the webapp
* `pymongo_flask.py` is used to do the server based work
* I've used heroku to deploy this webapp.  
It can be accessed using https://movie-recommender-precog.herokuapp.com/
* I've implemented user-user collaborative filtering in `user-user.py`
* Item-item filtering can be found in `item-item.py`
* Matrix factorisation collaborative filtering is in `matrix_factorisation.py`
* The dummy user ratings were taken from the MovieLens database.
## Docker
* Run the following command to build the docker image
`docker build -t movie-recommender:latest .`
* Now you can run the container via the following command
`docker run -d -p 5000:5000 movie-recommender`
## Value of K
There are two parameters to decide K
* Convinience of the user
* By calculating the error(RMSE) of our predictions against what the user actually rated.
## A few things to note
* The previous user ratings data is currently static, say a previous user now watches a movie and rates it. The change has to be reflected and models have to be retrained but I havent done that in my code. My solution to this problem is to do the training bi-daily or at the end of the day.
* The implementations of all collaborative filtering methods are not optimal and there are better implementations out there. However given the time contraints, I tried my best to keep the error and complexity at a minimum.
* The user ratings data collected from Movielens can be biased, to solve this problem one can ensure every type of user (liberal, strong rating wise) is there.
## Citations
* I've implemented user and item based filtering using this link.  
https://www.youtube.com/watch?v=h9gpufJFF-0  
* I've reffered to the code for collaborative filtering in this link  
http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/  
* Rest of the below links helped me understand a few things and complete this project.  
https://realpython.com/python-csv/  
https://dzone.com/articles/getting-started-with-python-and-mongodb  
https://lazyprogrammer.me/tutorial-on-collaborative-filtering-and-matrix-factorization-in-python/  
https://towardsdatascience.com/various-implementations-of-collaborative-filtering-100385c6dfe0  
https://towardsdatascience.com/building-and-testing-recommender-systems-with-surprise-step-by-step-d4ba702ef80b  
https://medium.com/@m_n_malaeb/the-easy-guide-for-building-python-collaborative-filtering-recommendation-system-in-2017-d2736d2e92a8  
https://www.analyticsvidhya.com/blog/2018/06/comprehensive-guide-recommendation-engine-python/  
https://www.stratio.com/blog/creating-a-recommender-system-part-i/  
https://surprise.readthedocs.io/en/stable/FAQ.html  
https://github.com/NicolasHug/Surprise/issues/22  
https://kerpanic.wordpress.com/2018/03/26/a-gentle-guide-to-recommender-systems-with-surprise/  
https://github.com/alexeyza/startup-programming/blob/master/past%20semesters/fall%202014/resources/tutorials/heroku%20python%20with%20flask%20mongodb%20shoutout.md  
https://blog.cambridgespark.com/tutorial-practical-introduction-to-recommender-systems-dbe22848392b
https://github.com/csaluja/JupyterNotebooks-Medium/blob/master/CF%20Recommendation%20System-Examples.ipynb
https://www.tutorialspoint.com/flask/flask_message_flashing.htm  
https://runnable.com/docker/python/dockerize-your-flask-application  
