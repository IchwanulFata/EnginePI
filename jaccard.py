from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import math
from collections import Counter

# Inisialisasi stemmer dari Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Fungsi untuk membaca inverted index dari file
def read_inverted_index(file_path):
    inverted_index = {}
    with open(file_path, 'r') as file:
        for line in file:
            term, postings = line.strip().split(': ')
            postings = eval(postings)
            inverted_index[term] = postings
    return inverted_index

# Fungsi untuk menghitung skor Jaccard Similarity
def calculate_jaccard_similarity(query_terms, doc_id, inverted_index):
    doc_terms = set()
    query_terms = set(query_terms)
    for term in query_terms:
        if term in inverted_index:
            for doc_freq, freq in inverted_index[term]:
                if doc_freq == doc_id:
                    doc_terms.add(term)
    
    if len(query_terms) == 0 or len(doc_terms) == 0:
        return 0.0
    
    intersection = len(query_terms.intersection(doc_terms))
    union = len(query_terms) + len(doc_terms) - intersection
    similarity = intersection / union
    return similarity

def search(query, inverted_index):
    # Melakukan stemming pada kata-kata dalam query dengan Sastrawi
    stemmed_query = stemmer.stem(query)
    query_terms = set(stemmed_query.split())
    
    scores = {}
    
    # Mengubah iterasi menjadi 100 dokumen (doc_id dari 0 hingga 99)
    for doc_id in range(102):
        score = calculate_jaccard_similarity(query_terms, doc_id, inverted_index)
        if score != 0:
            scores[doc_id] = score
    
    # Sort dokumen berdasarkan skor
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    if not ranked_docs:
        return "Tidak ada dokumen yang cocok"
    
    results = []
    for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
        results.append(f"Ranking: {rank}, Nama Dokumen: Doc{doc_id}, Similarity: {score}")
    
    return results

# Membaca inverted index dari file
inverted_index = read_inverted_index('./Hasil_index/inverted_index.txt')

# Mencari query
query = input("Masukkan query: ")
results = search(query, inverted_index)

for result in results:
    print(result)
