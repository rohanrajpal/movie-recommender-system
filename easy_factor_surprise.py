import zipfile
from collections import defaultdict
import csv
from pprint import pprint
import time
import os
from surprise import Reader, Dataset, SVD, evaluate, model_selection, KNNWithMeans
from surprise.model_selection import cross_validate,GridSearchCV

# Unzip ml-100k.zip
# zipfile = zipfile.ZipFile('ml-100k.zip', 'r')
# zipfile.extractall()
# zipfile.close()

# Read data into an array of strings
# with open('../../../Data_extraction/data/ratings.csv') as f:
#     all_lines = f.readlines()
def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def add_user_data(ratings_list,pathr,pathw):
    with open(pathr, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            with open(pathw, 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([row['userId'], row['movieId'], row['rating'], row['timestamp']])
                # csvwriter.writerow([row.items()])

    for elem in ratings_list:
        with open(pathw, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['615',elem[0],elem[1],int(time.time())])


def remove_user_data(path):
    # mode = 'w'
    # with open('../../../Data_extraction/data/smaller_data/small_ratings_(copy).csv', mode='r') as csv_file:
    #     csv_reader = csv.DictReader(csv_file)
    #     for row in csv_reader:
    #         with open('data/smaller_data/small_ratings.csv', mode) as csvfile:
    #             csvwriter = csv.writer(csvfile)
    #             # csvwriter.writerow([row['userId'], row['movieId'], row['rating'], row['timestamp']])
    #             if mode == 'w':
    #                 mode = 'a'
    # os.remove('../../../Data_extraction/data/smaller_data/small_ratings_(copy).csv')
    filename = path
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    f.close()

def solve_user_user(pathw):
    reader = Reader(line_format='user item rating timestamp', sep=',')

    data = Dataset.load_from_file(pathw, reader=reader)
    data.split(n_folds=5)
    # algo = SVD()
    algo = KNNWithMeans(k=50, sim_options={'name': 'pearson_baseline', 'user_based': True})
    # algo = KNNWithMeans(k=50, sim_options={'name': 'pearson_baseline', 'user_based': False})
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    # trainset.
    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)
    top_n = get_top_n(predictions, n=10)
    # Print the recommended items for each user
    for uid, user_ratings in top_n.items():
        if uid == '615':
            # print(uid, [iid for (iid, _) in user_ratings])
            return [iid for (iid, _) in user_ratings]
def solve_item_item(pathw):
    reader = Reader(line_format='user item rating timestamp', sep=',')
    data = Dataset.load_from_file(pathw, reader=reader)
    data.split(n_folds=5)
    algo = KNNWithMeans(k=50, sim_options={'name': 'pearson_baseline', 'user_based': False})
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)
    top_n = get_top_n(predictions, n=10)
    # Print the recommended items for each user
    for uid, user_ratings in top_n.items():
        if uid == '615':
            # print(uid, [iid for (iid, _) in user_ratings])
            return [iid for (iid, _) in user_ratings]

def solve_matrix_factorisation(pathw):
    reader = Reader(line_format='user item rating timestamp', sep=',')
    data = Dataset.load_from_file(pathw, reader=reader)
    data.split(n_folds=5)

    # param_grid = {'n_factors': [110, 120, 140, 160], 'n_epochs': [90, 100, 110], 'lr_all': [0.001, 0.003, 0.005, 0.008],
    #               'reg_all': [0.08, 0.1, 0.15]}
    # gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
    # gs.fit(data)
    # algo = gs.best_estimator['rmse']
    # print(gs.best_score['rmse'])
    # print(gs.best_params['rmse'])
    # cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    # print("reached")
    # Use the new parameters with the train data
    algo = SVD(n_factors=160, n_epochs=100, lr_all=0.005, reg_all=0.1)

    trainset = data.build_full_trainset()
    algo.fit(trainset)
    print("fitting crossed")
    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)
    top_n = get_top_n(predictions, n=10)
    # Print the recommended items for each user
    for uid, user_ratings in top_n.items():
        if uid == '615':
            # print(uid, [iid for (iid, _) in user_ratings])
            return [iid for (iid, _) in user_ratings]
if __name__ == '__main__':
    pathr = '../../../Data_extraction/data/smaller_data/small_ratings.csv'
    pathw = '../../../Data_extraction/data/smaller_data/small_ratings_copy.csv'
    remove_user_data(pathw)
    to_send = [['1', '5'], ['2', '2'], ['3', '3'], ['4', '4']]
    add_user_data(to_send,pathr,pathw)
    # solve(pathw)

