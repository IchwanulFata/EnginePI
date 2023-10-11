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
    query_terms = query.split()
    scores = {}
    
    # Mengubah iterasi menjadi 100 dokumen (doc_id dari 0 hingga 99)
    for doc_id in range(102):
        scores[doc_id] = calculate_jaccard_similarity(query_terms, doc_id, inverted_index)
    
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    if ranked_docs[0][1] == 0:
        return "Tidak ada dokumen yang cocok"
    
    results = []
    for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
        results.append(f"Ranking: {rank}, Nama Dokumen: Doc{doc_id}, Similarity: {score}")
    
    return results

# Membaca inverted index dari file
inverted_index = read_inverted_index('inverted_index.txt')

# Mencari query
query = input("Masukkan query: ")
results = search(query, inverted_index)

for result in results:
    print(result)
