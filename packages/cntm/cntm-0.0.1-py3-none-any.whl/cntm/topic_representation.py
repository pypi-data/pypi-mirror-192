import numpy as np
from scipy.spatial.distance import cosine
from rank_bm25 import BM25Okapi

def get_wv_ctfidf(df,dictionary):
    wv_d=[]
    for i in range(len(dictionary)):
        wv=[]
        tf=[]
        word=dictionary[i]
        a=0
        for i,row in df.iterrows():
            if word in row["content"]:
                a+=1
                wv.append(row["embedding"])
                tf.append((row["content"].count(word))/len(row["content"]))
        idf=np.log(1+a/len(df))
        tfidf = [x*idf for x in tf]
        weighted_sum = np.zeros(wv[0].shape)
        total_frequency = 0
        for v, f in zip(wv, tfidf):
            weighted_sum += v * f
            total_frequency += f
        weighted_average = weighted_sum / total_frequency
        wv_d.append(weighted_average)
    wv=dict(zip(dictionary.token2id.keys(), wv_d))
    return wv

def get_wv_bm25(df,dictionary):
    bm25 = BM25Okapi(df.content.to_list())
    doc_embeddings=df.embedding.to_list()
    wv_d=[]
    for i in range(len(dictionary)):
        doc_scores = bm25.get_scores([dictionary[i]])
        weighted_sum_array = sum([score * array for score, array in zip(doc_scores, doc_embeddings)])
        weighted_avg_array = weighted_sum_array / sum(doc_scores)
        wv_d.append(weighted_avg_array)
    wv=dict(zip(dictionary.token2id.keys(), wv_d))
    return wv

def get_closest_terms(wv, target_vector, top_n):
    distances = {}
    for word, vector in wv.items():
        distances[word] = cosine(target_vector, vector)
    closest_words = sorted(distances, key=distances.get)[:top_n]
    return closest_words

def topic_rep(wv,c,top_n=10):
    sum_vector = [sum(x) for x in zip(*c)]
    average_vector = [x / len(c) for x in sum_vector]
    return get_closest_terms(wv,average_vector,top_n)
