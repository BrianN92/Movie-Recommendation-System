import numpy as np
import pandas as pd
#from sklearn import cross_validation as cv
from sklearn.metrics.pairwise import pairwise_distances


def recommend_movie(userid,num):
    # read in users
    df_users = pd.read_csv('u.data', sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])
    n_users = df_users.user_id.unique().shape[0]
    n_items = df_users.item_id.unique().shape[0]

# read in items
    item_dic = {}
    for line in open('u.item'):
        record = line.strip().split('|')
        movie_id, movie_name = record[0], record[1]
        item_dic[movie_id] = movie_name

    train_data_matrix = np.zeros((n_users, n_items))
    #train_data, test_data = cv.train_test_split(df_users, test_size=0.01)
    train_data = df_users

    for line in train_data.itertuples():
        train_data_matrix[line[1]-1, line[2]-1] = line[3]  

    user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
    item_similarity = pairwise_distances(train_data_matrix.T, metric='cosine')

    def predict(ratings, similarity, type='user'):
        if type == 'user':
            mean_user_rating = ratings.mean(axis=1)
        #You use np.newaxis so that mean_user_rating has same format as ratings
            ratings_diff = (ratings - mean_user_rating[:, np.newaxis]) 
            pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
        elif type == 'item':
            pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])     
        return pred

    user_prediction = predict(train_data_matrix, user_similarity, type='user')
    item_prediction = predict(train_data_matrix, item_similarity, type='item') #not used


    a = list(item_prediction[userid])
    pre = sorted(range(len(a)), key=lambda i: a[i])[-num:]
    itemnum = [x+1 for x in pre]

    premovie = []
    for i in itemnum:
        premovie.append(item_dic[str(i)])

    return premovie