from UI import get_input
import numpy as np
import heapq
import pandas as pd
import random
import time

collection_size = 55109

def Load_Data(field):
    df1 = pd.read_csv('data/1.csv')
    df2 = pd.read_csv('data/2.csv')
    df3 = pd.read_csv('data/3.csv')
    df4 = pd.read_csv('data/4.csv')
    df5 = pd.read_csv('data/5.csv')
    df6 = pd.read_csv('data/6.csv')
    a = [df1,df2,df3,df4,df5,df6]
    b = [df1.shape[0],df2.shape[0],df3.shape[0],df4.shape[0],df5.shape[0],df6.shape[0]]
    df_sizes = [0,df1.shape[0],df1.shape[0]+df2.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0]+df4.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0]+df4.shape[0]+df5.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0]+df4.shape[0]+df5.shape[0]+df6.shape[0]]
    Gdata, file_index = [], 0
    for doc_index in range(0,55109):
        if doc_index == df_sizes[file_index+1]:
            file_index += 1
        target_data = a[file_index].loc[doc_index-df_sizes[file_index],field]
        Gdata.append(target_data)
    return (Gdata)

def Load_TFIDF():
    tf_idf, count = {},0
    with open("tf_idf.txt",'r') as index:
        line = index.readline().split(" ")
        while count < 113181:
            count+=1
            term, scores = line[0], line[1:-1]
            if term not in tf_idf.keys():
                tf_idf[term] = {}
            for tmp in scores:
                doc_id, score = tmp.split(":")
                tf_idf[term][int(doc_id)] = float(score)
            line = index.readline().split(" ")
    return tf_idf

def Load_DocumentVectors():
    document_vectors, count = {}, 0
    with open("documentvector.txt",'r') as vectors:
        line = vectors.readline().split(" ")
        while count < 54481:
            count+=1
            doc_id, terms = int(line[0]), line[1:-1]
            if doc_id not in document_vectors.keys():
                document_vectors[doc_id] = {}
            for tmp in terms:
                term, score = tmp.split(":")
                document_vectors[doc_id][term] = float(score)
            line = vectors.readline().split(" ")
    return document_vectors

def make_document_frequencies():
    document_frequencies, count = {}, 0
    with open("inverted_index.txt",'r') as index:
        line = index.readline().split(" ")
        while count < 113181:
            count+=1
            term, frequency = line[0], len(line[1:-1])
            document_frequencies[term] = frequency
            line = index.readline().split(" ")
    return document_frequencies

def Similarity(query , document, tf_idf, document_vectors, document_frequencies):
    product, norm_query, norm_document, query_score = 0, 0, 0, 0
    for term in query:
        count = query[term]
        query_score = (1+np.log10(count)) * np.log10(collection_size/document_frequencies[term])
        if document in tf_idf[term].keys():
            product += query_score * tf_idf[term][document]
        norm_query += query_score ** 2
    if document in document_vectors.keys():
        for term in document_vectors[document]:
            norm_document += document_vectors[document][term] ** 2
    if norm_document !=0:
        similarity = product / np.sqrt(norm_query * norm_document)       
        return similarity
    else:
        return 0


def ProcessQueriesWithoutChampionsList():
    print("Preparing Data For Query Processing, Please Wait...")
    tf_idf, document_vectors, document_frequencies, titles, contents = Load_TFIDF(), Load_DocumentVectors(), make_document_frequencies(), Load_Data('title'), Load_Data('content')

    while True:
        query = get_input()
        start_time = time.time()
        scores = []
        for index in range(1,collection_size+1):
            similarity = Similarity(query, index, tf_idf, document_vectors, document_frequencies)
            heapq.heappush(scores, (((-1) * similarity,index)))      
        best = heapq.nsmallest(10,scores)      
        doc_IDs = [tmp[1] for tmp in best]
        for i in range(10):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(str(i+1)+"." + titles[doc_IDs[i]]+ " --> ID:" + str(doc_IDs[i]+1), '\n')
            print(contents[doc_IDs[i]],'\n')
            
        print("\n", end = '')
        print("--- %s seconds ---" % (time.time() - start_time))
        print("\n\n")


ProcessQueriesWithoutChampionsList()