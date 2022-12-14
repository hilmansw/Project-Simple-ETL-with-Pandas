# -*- coding: utf-8 -*-
"""Project Simple ETL with Pandas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TC9VtazweCPVl4vMX9edbFRtJWDuxnsL

# Project Simple ETL with Pandas
Created by: Hilman Singgih Wicaksana, S.Kom<br>
Masters Student of Information Systems at Diponegoro University

# Import Library
"""

import pandas as pd

"""# Load the Data"""

df_participant = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/dqthon-participants.csv')
df_participant

"""# Transform Bagian I - Kode Pos
Ada permintaan datang dari tim logistik bahwa mereka membutuhkan kode pos dari peserta agar pengiriman piala lebih mudah dan cepat sampai. Maka dari itu buatlah kolom baru bernama postal_code yang memuat informasi mengenai kode pos yang diambil dari alamat peserta (kolom address).

Diketahui bahwa kode pos berada di paling akhir dari alamat tersebut.

Note:
Jika regex yang dimasukkan tidak bisa menangkap pattern dari value kolom address maka akan menghasilkan NaN.
"""

df_participant['postal_code'] = df_participant['address'].str.extract(r'(\d+)$') #Masukkan regex Anda didalam fungsi extract
df_participant['postal_code']

"""# Transform Bagian II - Kota
Selain kode pos, mereka juga membutuhkan kota dari peserta.

Untuk menyediakan informasi tersebut, buatlah kolom baru bernama city yang didapat dari kolom address. Diasumsikan bahwa kota merupakan sekumpulan karakter yang terdapat setelah nomor jalan diikuti dengan \n (newline character) atau dalam bahasa lainnya yaitu enter.
"""

#Masukkan regex Anda didalam fungsi extract
df_participant['city'] = df_participant['address'].str.extract(r'(?<=\n)(\w.+)(?=,)') 
df_participant['city']

"""# Transform Bagian III - Github
Salah satu parameter untuk mengetahui proyek apa saja yang pernah dikerjakan oleh peserta yaitu dari git repository mereka.

Pada kasus ini kita menggunakan profil github sebagai parameternya. Tugas Anda yaitu membuat kolom baru bernama github_profile yang merupakan link profil github dari peserta.

Diketahui bahwa profil github mereka merupakan gabungan dari first_name dan last_name yang sudah di-lowercase. 
"""

df_participant['github_profile'] = 'https://github.com/' + df_participant['first_name'].str.lower() + df_participant['last_name'].str.lower()
df_participant['github_profile']

"""# Transform Bagian IV - Nomor Handphone
Jika kita lihat kembali, ternyata nomor handphone yang ada pada data csv kita memiliki format yang berbeda-beda. Maka dari itu, kita perlu untuk melakukan cleansing pada data nomor handphone agar memiliki format yang sama. Anda sebagai Data Engineer diberi privilege untuk menentukan format nomor handphone yang benar. Pada kasus ini mari kita samakan formatnya dengan aturan:
1. Jika awalan nomor HP berupa angka 62 atau +62 yang merupakan kode telepon Indonesia, maka diterjemahkan ke 0. 
2. Tidak ada tanda baca seperti kurung buka, kurung tutup, strip??? ()-
3. Tidak ada spasi pada nomor HP nama kolom untuk menyimpan hasil cleansing pada nomor HP yaitu cleaned_phone_number




"""

#Masukkan regex anda pada parameter pertama dari fungsi replace
df_participant['cleaned_phone_number'] = df_participant['phone_number'].str.replace(r'^(\+62|62)', '0')
df_participant['cleaned_phone_number']

df_participant['cleaned_phone_number'] = df_participant['cleaned_phone_number'].str.replace(r'[()-]', '')
df_participant['cleaned_phone_number']

df_participant['cleaned_phone_number'] = df_participant['cleaned_phone_number'].str.replace(r'\s+', '')
df_participant['cleaned_phone_number']

"""# Transform Bagian V - Nama Tim
Dataset saat ini belum memuat nama tim, dan rupanya dari tim Data Analyst membutuhkan informasi terkait nama tim dari masing-masing peserta.

Diketahui bahwa nama tim merupakan gabungan nilai dari kolom first_name, last_name, country dan institute.

Tugas Anda yakni buatlah kolom baru dengan nama team_name yang memuat informasi nama tim dari peserta.
"""

def func(col):
    abbrev_name = "%s%s"%(col['first_name'][0],col['last_name'][0]) #Singkatan dari Nama Depan dan Nama Belakang dengan mengambil huruf pertama
    country = col['country']
    abbrev_institute = '%s'%(''.join(list(map(lambda word: word[0], col['institute'].split())))) #Singkatan dari value di kolom institute
    return "%s-%s-%s"%(abbrev_name,country,abbrev_institute)

df_participant['team_name'] = df_participant.apply(func, axis=1)
df_participant['team_name']

"""# Transform Bagian VI - Email
Setelah dilihat kembali dari data peserta yang dimiliki, ternyata ada satu informasi yang penting namun belum tersedia, yaitu email.

Anda sebagai Data Engineer diminta untuk menyediakan informasi email dari peserta dengan aturan bahwa format email sebagai berikut:

> Format email:<br>
xxyy@aa.bb.[ac/com].[cc]

> Keterangan:<br>
xx -> nama depan (first_name) dalam lowercase<br>
yy -> nama belakang (last_name) dalam lowercase<br>
aa -> nama institusi<br>

>  Nama depan: Citra<br>
  Nama belakang: Nurdiyanti<br>
  Institusi: UD Prakasa Mandasari<br>
  Negara: Georgia<br>
  Maka,Email nya: citranurdiyanti@upm.geo
  
>  Nama depan: Aris<br>
  Nama belakang: Setiawan<br>
  Institusi: Universitas Diponegoro<br>
  Negara: Korea Utara<br>
  Maka, Email nya: arissetiawan@ud.ac.ku
"""

def func(col):
    first_name_lower = col['first_name'].lower()
    last_name_lower = col['last_name'].lower()
    institute = ''.join(list(map(lambda word: word[0], col['institute'].lower().split()))) #Singkatan dari nama perusahaan dalam lowercase

    if 'Universitas' in col['institute']:
        if len(col['country'].split()) > 1: #Kondisi untuk mengecek apakah jumlah kata dari country lebih dari 1
            country = ''.join(list(map(lambda word: word[0], col['country'].lower().split())))
        else:
            country = col['country'][:3].lower()
        return "%s%s@%s.ac.%s"%(first_name_lower,last_name_lower,institute,country)

    return "%s%s@%s.com"%(first_name_lower,last_name_lower,institute)

df_participant['email'] = df_participant.apply(func, axis=1)
df_participant['email']

"""# Transform Bagian VII - Tanggal Lahir
MySQL merupakan salah satu database yang sangat populer dan digunakan untuk menyimpan data berupa tabel, termasuk data hasil pengolahan yang sudah kita lakukan ini nantinya bisa dimasukkan ke MySQL.

Meskipun begitu, ada suatu aturan dari MySQL terkait format tanggal yang bisa mereka terima yaitu YYYY-MM-DD dengan keterangan:
* YYYY: 4 digit yang menandakan tahun
* MM: 2 digit yang menandakan bulan
* DD: 2 digit yang menandakan tanggal
Contohnya yaitu: 2021-04-07

Jika kita lihat kembali pada kolom tanggal lahir terlihat bahwa nilainya belum sesuai dengan format DATE dari MySQL.

Oleh karena itu, lakukanlah formatting terhadap kolom birth_date menjadi YYYY-MM-DD dan simpan di kolom yang sama.
"""

df_participant['birth_date'] = pd.to_datetime(df_participant['birth_date'], format='%d %b %Y')
df_participant['birth_date']

"""# Transform Bagian VII - Tanggal Daftar Kompetisi
Selain punya aturan mengenai format DATE, MySQL juga memberi aturan pada data yang bertipe DATETIME yaitu YYYY-MM-DD HH:mm:ss dengan keterangan:

* YYYY: 4 digit yang menandakan tahun
* MM: 2 digit yang menandakan bulan
* DD: 2 digit yang menandakan tanggal
* HH: 2 digit yang menandakan jam
* mm: 2 digit yang menandakan menit
* ss: 2 digit yang menandakan detik

Contohnya yaitu: 2021-04-07 15:10:55

Karena data kita mengenai waktu registrasi peserta (register_time) belum sesuai format yang seharusnya.

Maka dari itu, tugas Anda yaitu untuk merubah register_time ke format DATETIME sesuai dengan aturan dari MySQL.

Simpanlah hasil tersebut ke kolom register_at.
"""

df_participant['register_at'] = pd.to_datetime(df_participant['register_time'], unit='s')
df_participant['register_at']