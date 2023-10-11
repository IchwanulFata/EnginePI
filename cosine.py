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

# Fungsi untuk menghitung skor Cosine Similarity dengan memperhitungkan frekuensi muncul token
def calculate_cosine_similarity(query_terms, doc_id, inverted_index):
    doc_vector = Counter()
    query_vector = Counter(query_terms)
    
    # Melakukan stemming pada kata-kata dalam query dengan Sastrawi
    stemmed_query = stemmer.stem(' '.join(query_terms))
    query_terms = stemmed_query.split()
    
    for term in query_terms:
        if term in inverted_index:
            for posting in inverted_index[term]:
                if posting[0] == doc_id:
                    doc_vector[term] = posting[1]  # Menggunakan frekuensi sebagai bobot dalam dokumen
    
    dot_product = sum(doc_vector[term] * query_vector[term] for term in query_terms)
    doc_length = math.sqrt(sum(doc_vector[term] ** 2 for term in doc_vector))
    query_length = math.sqrt(sum(query_vector[term] ** 2 for term in query_vector))
    
    if doc_length == 0 or query_length == 0:
        return 0
    
    similarity_score = dot_product / (doc_length * query_length)
    return similarity_score

def search(query, inverted_index, doc_lengths):
    query_terms = query.split()
    scores = {}
    
    # Melakukan stemming pada kata-kata dalam query dengan Sastrawi
    stemmed_query = stemmer.stem(' '.join(query_terms))
    query_terms = stemmed_query.split()
    
    # Mengubah iterasi menjadi 100 dokumen (doc_id dari 0 hingga 99)
    for doc_id in range(102):
        if doc_id in doc_lengths:
            score = calculate_cosine_similarity(query_terms, doc_id, inverted_index)
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
