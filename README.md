# movie-recommender-system
Rohan Rajpal -2017089  
This is my submission for the Intern/Member Programming Task - Summer 2019

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
## A few things to note
* Though logically the matrix factorization algorithm has been correctly implemented but my top recommendations was taking a lot of time, hence I had to reduce the iterations(and hence increase the error) to give the values.
* The previous user ratings data is currently static, say a previous user now watches a movie and rates it. The change has to be reflected and models have to be retrained but I havent done that in my code. My solution to the problem though is to do the training bi-daily or at the end of the day.
* The implementations of all collaborative filtering methods are not efficient and there are better implementations out there. However given the time contraints, I tried my best to keep the error at a minimum.
* The user ratings data collected from Movielens can be biased, to solve this problem one can ensure every type of user (liberal, strong rating wise) is there.
## Citations
* I've implemented user and item based filtering using this link.  
https://www.youtube.com/watch?v=h9gpufJFF-0  
* I've reffered to the code for collaborative filtering in this link  
http://www.quuxlabs.com/wp-content/uploads/2010/09/mf.py_.txt  
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