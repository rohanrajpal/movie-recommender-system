import numpy as np
import pprint as pprint
from scipy import spatial
import pandas
import pandas as pd
from copy import copy, deepcopy
import csv

def calc_cosine_sim(vec1, vec2):
    return 1 - spatial.distance.cosine(vec1, vec2)


def normalize(M):
    # print(M)

    for row in deepcopy(M):
        sum = 0
        size = 0
        # print(row)
        for elem in row:
            if elem != 0:
                sum += elem
                size += 1
        tosub = sum / size
        # print(tosub)
        for i in range(len(row)):
            if row[i] != 0:
                row[i] = float(row[i] - tosub)

    # print(M)
    return M


def get_similarusers(M, userId, itemId):
    sim_list = {}
    user_vector = M[userId - 1]
    for row in M:
        if row[itemId - 1] != 0:
            # print(row[itemId-1])
            sim = calc_cosine_sim(row, user_vector)

            sim_list[sim] = (row)
    # sim_list = sorted(sim_list, key=sim_list.__getitem__, reverse=False)
    # print(sim_list)
    list = []
    for i in sorted(sim_list,reverse=True):
        list.append(sim_list[i])
        if(len(list) == 2):
            break
    return list


def get_ratings(M, userId, similar_users, itemId):
    user_vector = M[userId - 1]
    topsum = 0
    bottom_sum = 0
    for row in similar_users:
        sim_xy = calc_cosine_sim(row, user_vector)
        # print(sim_xy,row[itemId-1])
        topsum += sim_xy * row[itemId - 1]
        bottom_sum += sim_xy
    # print(topsum,bottom_sum)
    return (topsum / bottom_sum)

def get_top_recommendations(M,newM,userId):
    movie_list={}
    movieId=0
    # for elem in M[userId-1]:
    #     movieId+=1
    #     if elem == 0:
    #         sims = get_similarusers(newM,userId,movieId)
    #         movie_list[movieId] = get_ratings(M,userId,sims,movieId)
    for elem in M:
        movieId +=1
        if elem[userId-1] == 0:
            # print("enter")
            sims = get_similarusers(newM,movieId,userId)
            movie_list[movieId] = get_ratings(M,movieId,sims,userId)
    # movie_list = sorted(movie_list,key=movie_list.__getitem__)
    # movie_list = sorted(movie_list)
    return (sorted(movie_list.items(), reverse=True,key=lambda kv: (kv[1], kv[0])))[0:10]
    # return movie_list

def get_and_conv_data():
    df = pd.read_csv('data/smaller_data/small_ratings_copy.csv',low_memory=False)
    df.columns = ['User', 'Item', 'ItemRating', 'timestamp']
    # print(df)
    ans = df.pivot_table(values='ItemRating', index='Item', columns='User')
    # print(ans.fillna(0))
    print(len(ans))
    return ans.fillna(0).values

def solve(data_to_add,M=None):
    M = (get_and_conv_data())
    data_to_add = np.array(data_to_add)
    data_to_add = data_to_add.reshape(data_to_add.shape[0], -1)
    # print(len(M[lenlast-1]),len(M))
    # data_to_add.append(M)
    # print(data_to_add)
    altM = []
    # M = np.column_stack((M,data_to_add))
    # print(type(M),type(data_to_add))
    # print(len(M[0]))
    M = np.hstack((M,data_to_add))
    # print(len(M[0]))
    # M.append(data_to_add)
    # print(len(M),len(M[0]))
    newM = normalize(M)
    # simusers = get_similarusers(newM, 1, 5)
    # print(get_ratings(M,1,simusers,5))
    final_recs = get_top_recommendations(M, newM, len(M[0]))
    # print(final_recs)
    return final_recs
if __name__ == '__main__':
    pass
    # M = ([[4, 0, 0, 5, 1, 0, 0],
    #       [5, 5, 4, 0, 0, 0, 2],
    #       [0, 0, 0, 2, 4, 5, 1],
    #       [0, 3, 0, 0, 0, 0, 3]])
    M = np.asarray([[1,0,3,0,0,5,0,0,5,0,4],
          [0,0,5,4,0,0,4,0,0,2,1],
          [2,4,0,1,2,0,3,0,4,3,5],
          [0,2,4,0,5,0,0,4,0,0,2],
          [0,0,4,3,4,2,0,0,0,0,2],
          [1, 0, 3, 0, 3, 0, 0, 2, 0, 0, 4]]
          )
    toadd =np.array([0,3,0,0,5,0])

    # print(toadd)
    # toadd = np.array([[0], [3], [0], [0], [5], [0]])

    # M =np.vstack([M,toadd])
    # print(len(M))
    # a = np.zeros((6, 2))
    # b = np.ones((6, 1))
    # print(type(a),type(b))
    # print(np.hstack((a,b)))
    print(solve(toadd,M))
    # solve()
    # print(len(M[6]))

    # r=np.asanyarray(M)
    # print(r)
    # if newM == M:
    #     print("yes")
    # simusers = get_similarusers(newM, 1, 103)
    # print(simusers)
    # print(get_ratings(M,1,simusers,103))

    # print(type(final_recs))

    # for item in final_recs:
    #     print(item[0])
    # print(final_recs)
    # print(calc_cosine_sim(M[0], M[1]))
    # print(calc_cosine_sim(M[0], M[2]))
