import numpy as np
import pandas as pd
import csv


def get_prediction(P, Q, userId, movieId):
    pvector = P[userId, :]
    qvector = Q[:, movieId]

    return np.dot(np.array(pvector), np.array(qvector))


def error_rating(M, P, Q, userId, movieId):
    actualrating = M[userId][movieId]
    predictedrating = get_prediction(P, Q, userId, movieId)

    sqddiff = (actualrating - predictedrating)

    return sqddiff


def calc_error(R, P, Q, beta, K):
    e = 0
    for i in range(len(R)):
        for j in range(len(R[i])):
            if R[i][j] > 0:
                e += error_rating(R, P, Q, i, j) + calc_magnitude(P, Q, beta, i, j, K)

    return e


def calc_magnitude(P, Q, beta, i, j, K):
    e = 0
    for k in range(K):
        e += (beta / 2) * (P[i][k] ** 2 + Q[k][j] ** 2)
    return e


def update_factors(R, P, Q, alpha, iterations, beta, K):
    Q = Q.transpose()
    # print(P[0,:])
    # print(Q[:,0])
    for c in range(iterations):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = error_rating(R, P, Q, i, j)
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        e = calc_error(R, P, Q, beta, K)
        if e < 0.001:
            break

    return P, Q.T


def get_and_conv_data():
    df = pd.read_csv('data/smaller_data/small_ratings_copy.csv', low_memory=False)
    df.columns = ['User', 'Item', 'ItemRating', 'timestamp']
    # print(df)
    ans = df.pivot_table(values='ItemRating', index='User', columns='Item')
    # print(ans.fillna(0))
    # print(len(ans))
    return ans.fillna(0).values


def gen_topnmovies(movieRecs):
    movieId = 1
    # print(movieRecs)
    movie_list = {}
    for elem in movieRecs:
        # print("going")
        movie_list[movieId] = elem
        movieId+=1

    # print(movie_list)
    return (sorted(movie_list.items(), reverse=True, key=lambda kv: (kv[1], kv[0])))[0:10]
    # print(ans)
    # return ans

def solve(data_to_add):
    # define constants
    alpha = 0.0002
    beta = 0.02
    iterations = 500
    similarities = 2

    R = (get_and_conv_data())
    # R = np.vstack([R, data_to_add])
    Q = np.random.rand(len(R[0]), similarities)
    P = np.random.rand(len(R), similarities)
    fP, fQ = update_factors(R, P, Q, alpha, iterations, beta, similarities)
    save_traineddata(fP, fQ)
    finalRatings = np.dot(fP, fQ.T)

    # movieRecs = finalRatings[len(finalRatings)-1]

    # return gen_topnmovies(movieRecs)
    return finalRatings


def solvefortraineddata(R, alpha, beta, K, iterations, P, Q):
    Q = Q.transpose()
    # print(P[0,:])
    # print(Q[:,0])
    for c in range(iterations):
        i = len(R) - 1
        # for i in range(len(R)):
        for j in range(len(R[i])):
            if R[i][j] > 0:
                eij = error_rating(R, P, Q, i, j)
                for k in range(K):
                    P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                    Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        e = calc_error(R, P, Q, beta, K)
        if e < 0.001:
            break

    return np.dot(P, Q)


def adduserandsolve(data_toadd):
    alpha = 0.0002
    beta = 0.02
    iterations = 5
    similarities = 2

    getP, getQ = (get_traineddata())
    # tempR = np.dot(getP,getQ)
    # R = np.vstack([R, data_toadd])
    # Q = np.random.rand(tempR[0], similarities)
    randdata = np.random.rand(1, similarities)
    getP = np.vstack([getP, randdata])
    getQ = np.array(getQ)
    calcR = np.dot(getP, getQ.T)
    print(len(calcR),len(calcR[len(calcR)-1]))
    # print(calcR)
    finalRatings = solvefortraineddata(calcR, alpha, beta, similarities, iterations, getP, getQ)
    movieRecs = finalRatings[len(finalRatings) - 1]
    # print(movieRecs)
    return gen_topnmovies(movieRecs)


def save_traineddata(tosaveP, tosaveQ):
    with open("data/matrix_trainedP.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(tosaveP)
    with open("data/matrix_trainedQ.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(tosaveQ)


def get_traineddata():
    datafile = open('data/matrix_trainedP.csv', 'r')
    datareader = csv.reader(datafile, delimiter=',')
    P = []
    for row in datareader:
        P.append(row)

    datafile = open('data/matrix_trainedQ.csv', 'r')
    datareader = csv.reader(datafile, delimiter=',')
    Q = []
    for row in datareader:
        Q.append(row)

    # [[float(y) for y in x] for x in P]
    # [[float(y) for y in x] for x in Q]
    P = np.array(P, dtype=float)
    Q = np.array(Q, dtype=float)
    return P, Q


if __name__ == '__main__':
    R = np.array([
        [5, 3, 0, 1],
        [4, 0, 0, 1],
        [1, 1, 0, 5],
        [1, 0, 0, 4],
        [0, 1, 5, 4],
    ])

    # get_prediction(R, userId, MovieId);

    data_toadd = np.array(
        [0, 2, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # print(data_toadd)
    # print(adduserandsolve(data_toadd))
    # solve(data_toadd)
    print(adduserandsolve(data_toadd))
    # M = get_traineddata()
    # print(len(M))
    # save_traineddata(solve(data_toadd))
    # Q = np.random.rand(len(R[0]), similarities)
    # P = np.random.rand(len(R),similarities)
    # finalRatings = update_factors(R,P,Q,alpha,iterations,beta,similarities)
    # print(finalRatings)
    # print(R.transpose())
