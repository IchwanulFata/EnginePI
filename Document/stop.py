import os
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re

# Inisialisasi StopWordRemover
stopword_factory = StopWordRemoverFactory()
stopword = stopword_factory.create_stop_word_remover()

# Daftar kata stop tambahan
more_stopwords = ['dengan', 'ia', 'bahwa', 'oleh']

# Direktori dengan file-file teks
directory_path = 'C:/Users/LENOVO/Documents/Semester 5/PI/Projek/New folder'  # Ganti dengan path ke direktori yang berisi file-file teks

# Loop melalui semua file dalam direktori
for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):  # Hanya proses file dengan ekstensi .txt
        file_path = os.path.join(directory_path, filename)
        
        # Baca teks dari file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Menghapus stop words
        text_without_stopwords = ' '.join([word for word in text.split() if word not in more_stopwords])

        # Menghapus angka dengan menggunakan regular expression
        text_without_stopwords_and_numbers = re.sub(r'\d+', '', text_without_stopwords)

        # Simpan teks yang sudah dihapus stop words dan angka ke dalam file baru dengan ekstensi _cleaned.txt
        output_file_path = os.path.join(directory_path, filename.replace(".txt", "_cleaned.txt"))
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text_without_stopwords_and_numbers)

        print("Stop words dan angka telah dihapus, hasil disimpan di", output_file_path)
