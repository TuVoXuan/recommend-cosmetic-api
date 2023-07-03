# Data preprocessing
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class ItemBased(object):
    def __init__(self, raw_data: pd.DataFrame) -> None:
        self.raw_data = raw_data

    def createUtiltiMatrix(self):
        # create matrix
        matrix = self.raw_data.pivot_table(
            index='itemId', columns='userId', values='rating')
        # print('matrix: \n', matrix)

        # normalize user-item matrix
        matrix_norm = matrix.subtract(matrix.mean(axis=1), axis=0)
        self.matrix_norm = matrix_norm

        # print('matrix_norm: \n', matrix_norm)

    def createSimilarityMatrix(self):
        # Item similarity matrix using Pearson correlation
        similarities = cosine_similarity(self.matrix_norm.fillna(0))

        item_similarity = pd.DataFrame(
            similarities, index=self.matrix_norm.index, columns=self.matrix_norm.index)
        # print('item_similarity: ', item_similarity)
        self.item_similarity = item_similarity

    def predict(self, picked_userid: str, number_of_similar_items: int, number_of_recommendations: int):
        import operator

        # print('picked_userid', picked_userid)

        self.createUtiltiMatrix()
        self.createSimilarityMatrix()

        # items that the target user has not rated
        picked_userid_not_rated = pd.DataFrame(
            self.matrix_norm[picked_userid].isna()).reset_index()
        picked_userid_not_rated = picked_userid_not_rated[picked_userid_not_rated[picked_userid]
                                                          == True]['itemId'].values.tolist()

        # items the target user has rated
        picked_userid_rated = pd.DataFrame(self.matrix_norm[picked_userid].dropna(axis=0, how='all')
                                           .sort_values(ascending=False))\
            .reset_index()\
            .rename(columns={picked_userid: 'rating'})

        # dictionary to save the unwatched movie and predited rating
        rating_prediction = {}

        # print('picked_userid_not_rated: ', picked_userid_not_rated)
        # loop through the unwatched items
        for picked_item in picked_userid_not_rated:
            # calculate the similarity score of picked item with other items
            picked_item_similarity_score = self.item_similarity[[
                picked_item]].reset_index().rename(columns={picked_item: 'similarity_score'})

            # rank the similarity between the picked user rated item and the picked not rated item
            picked_userid_rated_similarity = pd.merge(left=picked_userid_rated,
                                                      right=picked_item_similarity_score,
                                                      on='itemId',
                                                      how='inner')\
                .sort_values('similarity_score', ascending=False)[: number_of_similar_items]

            # calculate the predicted rating using average similarity score and the rating from target user
            nor_rating = picked_userid_rated_similarity['rating'].tolist()
            sim = picked_userid_rated_similarity['similarity_score'].tolist()
            
            numerator = [nor_rating[i] * sim[i] for i in range(len(nor_rating))]
            denomirator = np.abs(sim).sum()
            
            predicted_rating = round(sum(numerator)/denomirator, 6)
            # predicted_rating = round(np.average(picked_userid_rated_similarity['rating'],
            #                                     weights=picked_userid_rated_similarity['similarity_score']), 6)

            # saving the predicted rating in the dictionary
            rating_prediction[picked_item] = predicted_rating

        # print('rating_prediction: ', rating_prediction)
        # return the top recommeded movies
        return sorted(rating_prediction.items(), key=operator.itemgetter(1), reverse=True)[:number_of_recommendations]
