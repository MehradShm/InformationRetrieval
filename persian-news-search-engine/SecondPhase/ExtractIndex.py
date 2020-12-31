import time
import numpy as np
import heapq
import random

collection_size = 55109
def make_term_frequencies():
    term_frequencies, count = {}, 0
    with open("tf.txt",'r') as tf:
        line = tf.readline().split(" ")
        while count <113181:
            count+=1
            term, frequencies = line[0],line[1:-1]
            term_frequencies[term] = {}
            for doc in frequencies:
                doc_id, frequency = doc.split(':')
                term_frequencies[term][int(doc_id)] = int(frequency)
            line = tf.readline().split(" ")
    return term_frequencies

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

def make_tf_idf():
    count = 0 
    tf_idf, term_frequencies, document_frequencies, champions_lists = {}, make_term_frequencies(), make_document_frequencies(), {}
    for term in term_frequencies:
        count +=1
        tf_idf[term] = {}
        score_list = []
        for doc_id in term_frequencies[term]:
            tf_idf[term][doc_id] = (1+np.log10(term_frequencies[term][doc_id]) * np.log10(collection_size/document_frequencies[term]))
            heapq.heappush(score_list,(((-1)*tf_idf[term][doc_id],doc_id)))
        champions_lists[term] = [tmp[1] for tmp in heapq.nsmallest(10,score_list)]
    
    with open("ChampionsList.txt",'w') as champion:
        for term in champions_lists.keys():
            champion.write(term+" ")
            for doc_id in champions_lists[term]:
                champion.write(str(doc_id)+" ")
            champion.write("\n")


    with open("tf_idf.txt",'w') as scores:
        for term in tf_idf.keys():
            scores.write(term+" ")
            for doc_id in tf_idf[term].keys():
                scores.write(str(doc_id)+":"+str(tf_idf[term][doc_id])+" ")
            scores.write("\n")

    return tf_idf

def random_sample_champion_list():
    x = random.randint(1, 55119)
    print("Document ID: {}".format(x))
    champions_lists, count = {}, 0
    with open("ChampionsList.txt",'r') as champion:
        line = champion.readline().split(" ")
        while count < 113181:
            count += 1
            term, champions = line[0], map(int,line[1:-1])
            champions_lists[term] = champions
            line = champion.readline().split(" ")
    scores = []
    for term in champions_lists.keys():
        for doc_index in range(len(list(champions_lists[term]))):
            if champions_lists[term][doc_index] == x:
                heapq.heappush(scores,(champions_lists[term][doc_index], term))
    best, worst = [tmp[1] for tmp in heapq.nlargest(scores)], [tmp[1] for tmp in heapq.nsmallest(scores)]
    print(best)
    print("=======")
    print(worst)



def make_document_vectors():
    document_vectors, count = {}, 0
    with open("tf_idf.txt",'r') as index:
        line = index.readline().split(" ")
        while count < 113181:
            count+=1
            term, scores = line[0], line[1:-1]
            for tmp in scores:
                doc_id, score = tmp.split(":")
                if int(doc_id) not in document_vectors.keys():
                    document_vectors[int(doc_id)] = {}
                document_vectors[int(doc_id)][term] = score
            line = index.readline().split(" ")
    
    with open("documentvector.txt","w") as vectors:
        for doc_id in document_vectors:
            vectors.write(str(doc_id)+" ")
            for term in document_vectors[doc_id]:
                vectors.write(term + ":" + document_vectors[doc_id][term]+ " ")
            vectors.write("\n")


#make_tf_idf()
#make_document_vectors()
random_sample_champion_list()