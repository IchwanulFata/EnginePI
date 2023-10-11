import os

# Fungsi untuk membaca inverted index dari file
def read_inverted_index(file_path):
    inverted_index = {}
    freq = {}
    with open(file_path, 'r') as file:
        for line in file:
            term, postings = line.strip().split(': ')
            freqs = postings.strip().split('()')
            frequens = freqs.strip().split(',')
            
            # inverted_index[term] = postings
            freq[term] = frequens
    return freq


# Contoh penggunaan
inverted_index = read_inverted_index("inverted_index.txt")
print(inverted_index)
