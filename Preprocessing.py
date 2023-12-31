import os
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Tentukan direktori tempat file-file berada
input_directory = "D:/Skill/EnginePI/Numbered Document"

# Buat direktori baru untuk menyimpan file hasil di folder "HASIL"
output_directory = "D:/Skill/EnginePI/HASIL"

# Buat daftar file-file di direktori input
file_list = os.listdir(input_directory)

# Membuat direktori output jika belum ada
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Inisialisasi Stemmer Sastrawi sekali di luar loop untuk meningkatkan kinerja
stemmer = StemmerFactory().create_stemmer()

# Inisialisasi Stopword Remover Sastrawi
stopword_factory = StopWordRemoverFactory()
stopword = stopword_factory.create_stop_word_remover()

# Looping semua file di direktori input
for file_name in file_list:
    # Jika file adalah file teks, lanjutkan
    if file_name.endswith('.txt'):
        # Baca teks dari file
        with open(os.path.join(input_directory, file_name), 'r', encoding='utf-8') as f:
            text = f.read()

        # Bersihkan teks dari angka dan nomor-nomor
        text = re.sub(r'\d+', '', text)

        # Bersihkan teks dari stopwords
        text = stopword.remove(text)

        # Bersihkan teks dari karakter khusus
        text = re.sub(r'[!()-[]{};:"\, <>./?@#$%^&*_~]', '', text)

        # Ubah teks menjadi huruf kecil
        text = text.lower()

        # Tokenisasi teks yang sudah dibersihkan
        tokens = text.split()

        # Stemming teks tanpa menghapus duplikat token
        stemmed_tokens = [stemmer.stem(token) for token in tokens]

        # Hapus stopwords sekali lagi, jika ada yang tersisa
        stopwords = ["yang", "untuk", "pada", "ke", "para", "namun", "antara", "dia", "dua", "ia", "seperti", "jika", "sehingga", "kembali", "dan", "ini", "kepada", "saat", "harus", "sementara", "belum", "kami", "sekitar", "bagi", "serta", "di", "dari", "telah", "sebagai", "masih", "hal", "adalah", "itu", "dalam", "bisa", "bahwa", "atau", "hanya", "kita", "dengan", "akan", "juga", "ada", "mereka", "sudah", "saya", "terhadap", "agar", "lain", "anda", "begitu", "mengapa", "kenapa", "yaitu", "yakni", "daripada", "itulah", "lagi", "maka", "tentang", "demi", "dimana", "kemana", "pula", "sambil", "supaya", "guna", "kah", "pun", "sedangkan", "selagi", "sementara", "tetapi", "apakah", "kecuali", "selain", "seolah", "seraya", "seterusnya", "tanpa", "agak", "boleh", "dapat", "dsb", "dst", "dll", "dahulu", "dulunya", "anu", "demikian", "tapi", "ingin", "juga", "nggak", "mari", "nanti", "melainkan", "oh", "ok", "seharusnya", "sebetulnya", "setidaknya", "sesuatu", "pasti", "saja", "toh", "ya", "walau", "tolong", "tentu", "amat", "apalagi","bagaimanapun"]
        filtered_stemmed_tokens = [token for token in stemmed_tokens if token not in stopwords]
        
        # Menyimpan hasil teks yang sudah dibersihkan, di-tokenisasi, di-stem, dan dihilangkan stopwords ke dalam berkas
        output_file_name = file_name
        output_file_path = os.path.join(output_directory, output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(filtered_stemmed_tokens))