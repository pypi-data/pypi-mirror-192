import pandas as pd
import numpy as np
from sklearn.cluster import Birch
from gensim.corpora import Dictionary
from nltk import word_tokenize
import swifter
import umap
import hdbscan
from cntm.linkbert import LinkBert
from cntm.text_processing import preprocess_docs, get_bigrammer, token_frequency_filter
from cntm.topic_representation import get_wv_bm25, topic_rep, get_wv_ctfidf


class CNTM:
    def __init__(self, dt,num_topics=None,num_words=10,umap_dimension=2,umap_neighbor_size=15,clustering_mode="birch",branching_factor=50 ,min_hdbscan_cluster_size=10 , hdbsacn_soft_clustering=False,
                 tokenizing_method="unigram",bigram_threshold=10,filter_threshold=5, wv_method="bm25"):

        self.min_hdbscan_cluster_size = min_hdbscan_cluster_size
        self.clustering_mode = clustering_mode
        self.umap_dimension = umap_dimension
        self.umap_neighbor_size = umap_neighbor_size
        self.tokenizing_method = tokenizing_method
        self.filter_threshold = filter_threshold
        self.num_words = num_words
        self.wv_method = wv_method
        self.bigram_threshold = bigram_threshold
        self.hdbsacn_soft_clustering = hdbsacn_soft_clustering
        self.branching_factor= branching_factor
        self.dt = dt
        self.num_topics=num_topics

        self.cluster_model = None
        self.dictionary = None
        self.wv = None

        self.tokens=None
        self.dictionary = None

        self.doc_embedding=None
        self.umap_model=None

    def fit(self):
        print("Embedding is initializing...")
        self.dt["embedding"] = self.dt["content"].swifter.apply(lambda x: LinkBert(x))
        print("Embedding is done!")

        # Dimension Reduction
        print("Dimension Reduction for clustering is happening...")
        self.doc_embedding = pd.DataFrame(self.dt.embedding.to_list())
        umap_args = {'n_neighbors': self.umap_neighbor_size,
                     'n_components': self.umap_dimension,
                     'metric': 'cosine'}
        self.umap_model = umap.UMAP(**umap_args).fit(self.doc_embedding)
        print("Dimension is Reduced to: ", self.umap_dimension)

        # Clustering
        print("Clustering is proceeding...")
        if self.clustering_mode == "birch":
            self.cluster_model = Birch(threshold=0.5, branching_factor=self.branching_factor, n_clusters=self.num_topics,
                                       compute_labels=True, copy=True).fit(self.umap_model.embedding_)
            self.dt = self.dt.assign(C=self.cluster_model.labels_)
        else:
            hdbscan_args = {'min_cluster_size': self.min_cluster_size,
                            'metric': 'euclidean',
                            'cluster_selection_method': 'eom'}
            self.cluster_model = hdbscan.HDBSCAN(**hdbscan_args, prediction_data=True).fit(self.umap_model.embedding_)
            hard_labels = self.cluster_model.labels_
            soft_clusters = hdbscan.all_points_membership_vectors(self.cluster_model)
            soft_labels = np.argmax(soft_clusters, axis=1)
            if self.soft_clustering:
                self.dt = self.dt.assign(C=soft_labels)
            else:
                self.dt = self.dt.assign(C=hard_labels)
        print("Clustering is done!")

        # Topic Representation
        print("Topics are getting represented.....")
        all_docs = self.dt.content.to_list()
        cleaned_docs = preprocess_docs(all_docs)
        if self.tokenizing_method == "bigram":
            self.tokens = get_bigrammer(cleaned_docs, threshold=self.bigram_threshold)
        else:
            self.tokens = [word_tokenize(text) for text in cleaned_docs]
        self.tokens = token_frequency_filter(self.tokens, threshold=self.filter_threshold)
        self.dictionary = Dictionary(self.tokens)
        self.dt["content"] = self.tokens
        if self.wv_method == "bm25":
            self.wv = get_wv_bm25(self.dt, self.dictionary)
        else:
            self.wv = get_wv_ctfidf(self.dt, self.dictionary)

        self.output = self.dt.groupby("C")["embedding"].apply(list).reset_index()
        self.output = self.output[self.output["C"] > -1]
        self.output["topic_representation"] = self.output["embedding"].apply(lambda x: topic_rep(self.wv, x, top_n=self.num_words))
        print("Topic modeling is done")
        #if self.save:
            #output.to_pickle("ctm")
        return self.output
