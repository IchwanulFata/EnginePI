import os
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Tentukan direktori tempat file-file berada
directory = "C:/Users/LENOVO/Documents/Semester 5/PI/Projek/New folder/"

# Buat daftar file-file di direktori
file_list = os.listdir(directory)

# Looping semua file di direktori
for file_name in file_list:
    # Jika file adalah file teks, lanjutkan
    if file_name.endswith('.txt'):
        # Baca teks dari file
        with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as f:
            text = f.read()

        # Bersihkan teks
        text = re.sub(r'[!()-[]{};:"\, <>./?@#$%^&*_~0-9]','',text)
        text = text.lower()

        # Tokenisasi teks yang sudah dibersihkan
        tokens = text.split()

        # Stemming teks
        stemmer = StemmerFactory().create_stemmer()
        stemmed_tokens = [stemmer.stem(token) for token in tokens]

        # Hapus duplikat token
        stemmed_tokens = list(set(stemmed_tokens))

        # Hapus stopwords
        stopwords = ["dan", "yang", "atau", "juga"]
        filtered_stemmed_tokens = [token for token in stemmed_tokens if token not in stopwords]
        
        directory = "C:/Users/LENOVO/Documents/Semester 5/PI/Projek/New folder/Document"
        # Menyimpan hasil teks yang sudah dibersihkan, di-tokenisasi, di-stem, dan dihilangkan stopwords ke dalam berkas
        with open(os.path.join(directory, file_name), 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(filtered_stemmed_tokens))
