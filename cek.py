# =========================================
# 1. Mount Google Drive
# =========================================
from google.colab import drive
drive.mount('/content/drive')

# =========================================
# 2. Install OpenAI API and other libraries
# =========================================
!pip install -q openai pymupdf pandas
import openai
import time # Import the time module
import re # Import the regex module for extraction

# =========================================
# 3. Konfigurasi API Key OpenAI (GANTI DENGAN MILIK KAMU YANG VALID!)
# =========================================
# Penting: JANGAN langsung menulis API key di sini untuk produksi.
# Gunakan Google Colab Secrets atau variabel lingkungan.
# Contoh ini menggunakan API key langsung hanya untuk demonstrasi cepat.
openai.api_key = "xxxxxxxxxxxxxx" # Ganti dengan API key Anda yang sebenarnya!


# =========================================
# 4. Ambil dan Ekstrak Isi dari File PDF & Lakukan Penilaian
# =========================================
import os
import fitz  # PyMuPDF
import pandas as pd # Import pandas di sini untuk DataFrame

# Path ke folder utama yang berisi sub-folder laporan mahasiswa
base_path = '/content/drive/MyDrive/file path'

all_student_assessments = [] # List untuk menyimpan semua hasil penilaian

# Prompt penilaian (disimpan di luar loop agar tidak dibuat berulang)
assessment_prompt_template = """
Saya ingin Anda bertindak sebagai dosen penilai laporan akademik yang **objektif, konstruktif, dan inspiratif**. Fokus utama Anda adalah mengevaluasi kualitas laporan sambil memberikan **umpan balik yang membangun untuk pertumbuhan mahasiswa**, serta mengapresiasi upaya yang sudah dilakukan.

Tugas mahasiswa adalah membuat laporan analisis clustering terhadap data lulusan perguruan tinggi menggunakan metode K-Means. Data yang digunakan: nilai IPS per semester, program studi, dan lama studi mahasiswa.

Laporan harus mencakup:
1.  **Penjelasan masalah/fenomena akademik**: Apakah masalah yang ingin dipecahkan sudah dijelaskan dengan jelas, dan apakah relevansinya dengan konteks akademik disampaikan dengan baik?
2.  **Pra-pemrosesan data**: Apakah langkah-langkah pra-pemrosesan data dijelaskan dengan rinci dan tepat? Apakah keputusan yang diambil dalam pra-pemrosesan data memiliki justifikasi yang logis?
3.  **Metode penentuan jumlah cluster optimal**: Apakah metode untuk menentukan jumlah cluster (misalnya metode Elbow, Silhouette Score) dijelaskan dan diterapkan dengan benar? Seberapa baik penyajian argumen untuk pemilihan jumlah cluster optimal?
4.  **Visualisasi hasil clustering dan pola yang muncul**: Apakah hasil clustering divisualisasikan dengan cara yang membantu pemahaman? Apakah pola yang muncul dianalisis dengan baik, relevan, dan memberikan wawasan awal yang menarik?
5.  **Kesimpulan dari analisis**: Apakah kesimpulan yang ditarik relevan dengan hasil analisis? Apakah ini memberikan wawasan yang berarti atau potensi implikasi?
6.  **Menghindari plagiarisme dan menulis dengan bahasa sendiri**: Apakah laporan menunjukkan orisinalitas dalam penulisan dan menggunakan gaya bahasa akademik yang tepat?

Tolong:
-   Nilai laporan berikut ini berdasarkan kriteria di atas.
-   Berikan umpan balik akademik yang **spesifik, seimbang, dan berorientasi pada perbaikan**, menyoroti poin-poin kuat laporan sekaligus memberikan saran yang jelas untuk pengembangan di masa depan.
-   Berikan **skor keseluruhan antara 0 - 100**, yang **mencerminkan upaya mahasiswa, pemahaman dasar konsep, dan potensi laporan ini**. Angka ini harus mencerminkan pandangan seorang dosen yang mendukung.
-   Format respons Anda harus jelas, dengan sub-bagian terpisah untuk setiap kriteria penilaian.

Berikut isi laporan mahasiswa:
{report_text}
"""

# Loop melalui setiap sub-folder (mahasiswa)
for folder_name in os.listdir(base_path):
    student_folder_path = os.path.join(base_path, folder_name)
    if os.path.isdir(student_folder_path):
        pdf_file = None
        for file in os.listdir(student_folder_path):
            if file.lower().endswith('.pdf'):
                pdf_file = os.path.join(student_folder_path, file)
                break # Ambil file PDF pertama di folder mahasiswa

        if not pdf_file:
            print(f"❌ Tidak ada file PDF ditemukan di folder: {folder_name}. Melewati...")
            continue # Lanjutkan ke folder mahasiswa berikutnya

        print(f"\nProcessing: {folder_name} - {os.path.basename(pdf_file)}")

        # Ekstrak isi PDF
        text = ""
        try:
            with fitz.open(pdf_file) as doc:
                for page in doc:
                    text += page.get_text()
            print(f"✅ Teks berhasil diekstrak. Panjang teks: {len(text)} karakter.")
        except Exception as e:
            print(f"❌ Terjadi kesalahan saat membaca PDF '{os.path.basename(pdf_file)}': {e}. Melewati...")
            continue # Lanjutkan ke folder mahasiswa berikutnya

        if not text:
            print(f"❌ Tidak ada teks yang berhasil diekstraksi dari '{os.path.basename(pdf_file)}'. Melewati...")
            continue # Lanjutkan ke folder mahasiswa berikutnya

        # Gunakan seluruh teks, tidak dipotong
        full_report_text = text

        # Siapkan prompt dengan isi laporan
        current_prompt = assessment_prompt_template.format(report_text=full_report_text)

        # Panggil OpenAI API untuk penilaian
        student_assessment = {
            "NIM_Nama_Folder": folder_name,
            "Nama File PDF": os.path.basename(pdf_file),
            "Skor Keseluruhan": None,
            "Komentar Penjelasan Masalah": None,
            "Komentar Pra-pemrosesan Data": None,
            "Komentar Metode Optimal Cluster": None,
            "Komentar Visualisasi": None,
            "Komentar Kesimpulan": None,
            "Komentar Plagiarisme": None,
            "Raw Response": None # Untuk debugging jika perlu
        }

        print("🚀 Mengirimkan prompt ke OpenAI...")
        try:
            # --- Perubahan utama untuk OpenAI API ---
            response = openai.chat.completions.create(
                model="gpt-4o",  # Atau "gpt-3.5-turbo", "gpt-4-turbo" sesuai kebutuhan
                messages=[
                    {"role": "system", "content": "You are a helpful academic report assessor."},
                    {"role": "user", "content": current_prompt}
                ],
                max_tokens=2000, # Sesuaikan jika respons terlalu pendek/panjang
                temperature=0.7 # Sesuaikan kreativitas model (0.0-1.0)
            )
            openai_response_text = response.choices[0].message.content
            student_assessment["Raw Response"] = openai_response_text
            print("✅ Penilaian dari AI diterima.")

            # --- Ekstraksi Nilai dan Komentar dari Respons OpenAI (Sama seperti Gemini) ---
            # Ekstrak Skor Keseluruhan
            score_match = re.search(r"Skor Keseluruhan:\s*(\d{1,3})", openai_response_text) # Adjusted regex for "Skor Keseluruhan"
            if score_match:
                student_assessment["Skor Keseluruhan"] = int(score_match.group(1))

            criteria_patterns = {
                "Penjelasan Masalah": r"1\.\s*\*\*Penjelasan masalah\/fenomena akademik\*\*.*?\n(.*?)(?=\n2\.\s*\*\*Pra-pemrosesan data\*\*|$)",
                "Pra-pemrosesan Data": r"2\.\s*\*\*Pra-pemrosesan data\*\*.*?\n(.*?)(?=\n3\.\s*\*\*Metode penentuan jumlah cluster optimal\*\*|$)",
                "Metode Optimal Cluster": r"3\.\s*\*\*Metode penentuan jumlah cluster optimal\*\*.*?\n(.*?)(?=\n4\.\s*\*\*Visualisasi hasil clustering dan pola yang muncul\*\*|$)",
                "Visualisasi": r"4\.\s*\*\*Visualisasi hasil clustering dan pola yang muncul\*\*.*?\n(.*?)(?=\n5\.\s*\*\*Kesimpulan dari analisis\*\*|$)",
                "Kesimpulan": r"5\.\s*\*\*Kesimpulan dari analisis\*\*.*?\n(.*?)(?=\n6\.\s*\*Menghindari plagiarisme dan menulis dengan bahasa sendiri\*\*|$)",
                "Plagiarisme": r"6\.\s*\*Menghindari plagiarisme dan menulis dengan bahasa sendiri\*\*.*?\n(.*?)(?=\n\*\*Saran Umum:\*\*|$|\n\*\*Kesimpulan Akhir:\*\*|$)" # Added more robust end markers
            }

            for key, pattern in criteria_patterns.items():
                match = re.search(pattern, openai_response_text, re.DOTALL)
                if match:
                    comment_text = match.group(1)
                    student_assessment[f"Komentar {key}"] = comment_text.strip()

            all_student_assessments.append(student_assessment)

            # --- Tambahkan delay di sini ---
            time.sleep(5) # Delay 5 detik setelah setiap panggilan API OpenAI

        except openai.APIError as e:
            print(f"❌ Terjadi kesalahan API OpenAI untuk '{folder_name}': {e}")
            student_assessment["Raw Response"] = f"OpenAI API Error: {e}"
            all_student_assessments.append(student_assessment)
        except Exception as e:
            print(f"❌ Terjadi kesalahan umum saat memanggil API OpenAI untuk '{folder_name}': {e}")
            student_assessment["Raw Response"] = f"Error: {e}"
            all_student_assessments.append(student_assessment)

# =========================================
# 5. Simpan Hasil Penilaian ke Excel
# =========================================
output_excel_path = '/content/drive/MyDrive/adi file (perkuliahan)/adi file/Dosen/MK/2024/Pembelajaran Mesin/Hasil_Penilaian_UTS_Otomatis_OpenAI.xlsx' # Changed output filename
df_assessments = pd.DataFrame(all_student_assessments)
df_assessments.to_excel(output_excel_path, index=False)

print(f"\n✅ Semua hasil penilaian mahasiswa disimpan di: {output_excel_path}")
