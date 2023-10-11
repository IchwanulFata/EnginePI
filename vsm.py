import math
from collections import Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

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

# Fungsi untuk menghitung skor VSM
def calculate_vsm_score(query_terms, doc_id, inverted_index, doc_lengths):
    score = 0
    for term in query_terms:
        if term in inverted_index:
            for doc_freq, freq in inverted_index[term]:
                if doc_freq == doc_id:
                    idf = math.log(len(doc_lengths) / len(inverted_index[term]))
                    score += (freq * idf)
    return score

def search(query, inverted_index, doc_lengths):
    # Melakukan stemming pada kata-kata dalam query dengan Sastrawi
    query_terms = [stemmer.stem(word) for word in query.split()]
    scores = {}
    
    # Mengubah iterasi menjadi 100 dokumen (doc_id dari 0 hingga 99)
    for doc_id in range(102):
        if doc_id in doc_lengths:
            score = calculate_vsm_score(query_terms, doc_id, inverted_index, doc_lengths)
            if score != 0:
                scores[doc_id] = score
    
    # Sort dokumen berdasarkan skor
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    if not ranked_docs:
        return "Tidak ada dokumen yang cocok"
    
    results = []
    for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
        results.append(f"Ranking: {rank}, Nama Dokumen: Doc{doc_id}, Score: {score}")
    
    return results

# Membaca inverted index dari file
inverted_index = read_inverted_index('./Hasil_index/inverted_index.txt')
# Anda perlu memiliki data panjang dokumen untuk perhitungan VSM
# Di sini, kita hanya mengasumsikan panjang dokumen rata-rata
avg_doc_length = 500

# Misalnya, panjang dokumen untuk setiap dokumen tersimpan dalam sebuah dictionary
doc_lengths = {i: avg_doc_length for i in range(102)}
               
# Mencari query
query = input("Masukkan query: ")
results = search(query, inverted_index, doc_lengths)

for result in results:
    print(result)
