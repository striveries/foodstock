# FoodStock
FoodStock merupakan suatu aplikasi berbasis _website_ yang berfungsi sebagai platform untuk membantu pengelolaan inventori stok bahan makanan suatu bisnis FnB. Melalui aplikasi ini, pengguna dapat mengetahui stok bahan makanan dasar terkini, bahan makanan yang sudah perlu untuk dilakukan _restock_, hingga melakukan pendataan harga bahan makanan tersebut.

### Penyusun Proyek
Nama : Calista Sekar    
NPM : 2206082064    
Kelas : C   

## Langkah-Langkah Development FoodStock
### Membuat sebuah proyek Django baru.
1.  Saya membuat direktori terlebih dahulu dengan nama `foodstock` kemudian membuka terminal shell dari direktori tersebut. 
2. Saya membuat virtual environment dengan perintah `python -m venv env` 
3. Virtual environment diaktifkan dengan perintah `source env/bin/activate` sehingga terdapat tanda (env) pada terminal.
4. Saya membuat berkas requirements.txt dan menambahkan beberapa depedencies di bawah ini :
```
    django
    gunicorn
    whitenoise
    psycopg2-binary
    requests
    urllib3
```
5. Saya memasang dependencies dengan perintah `pip install -r requirements.txt`
6. Setelah semua persiapan selesai, saya membuat proyek Django baru bernama `foodstock` dengan perintah `django-admin startproject foodstock .` Setelah perintah ini dijalankan, Django otomatis menginisiasi proyeknya di direktori yang sama.
7. Setelah proyek dibuat, saya menambahkan `*` pada `ALLOWED_HOST` di file `setting.py` untuk mengizinkan semua host untuk mengakses aplikasi web.

### Membuat aplikasi dengan nama main pada proyek tersebut.
1. Pada terminal direktori utama `foodstock`, saya mengaktifkan _virtual environment_ untuk mengisolasi _package_ dan _dependencies_ sehingga tidak bertabrakan dengan versi lainnya pada laptop saya.
2. Untuk membuat aplikasi baru dengan nama `main`, saya menjalankan perintah `python manage.py startapp main`. Aplikasi baru ini
berisi struktur awal yang akan menjadi pondasi aplikasi foodstock kedepannya.
3. Sebelum mengimplementasikan _template_, saya mendaftarkan terlebih dahulu aplikasi main ke dalam proyek dengan menambahkan `main` pada `INSTALLED_APPS` di dalam berkas `setting.py`
4. Selanjutnya, saya membuat direktori baru `templates` di dalam direktori aplikasi main serta membuat berkas baru bernama `main.html` yang akan berisikan _landing page_ aplikasi FoodStock.

### Melakukan routing pada proyek agar dapat menjalankan aplikasi main.

### Membuat model pada aplikasi main dengan nama Item dan memiliki atribut wajib sebagai berikut.
* `name` sebagai nama item dengan tipe CharField.
* `amount` sebagai jumlah item dengan tipe IntegerField.
* `description` sebagai deskripsi item dengan tipe TextField.

Setelah memeriksa bahwa tampilan HTML aplikasi telah sesuai, saya membuat berkas baru `models.py` pada direktori aplikasi main. Berkas tersebut akan berisikan model yang akan digunakan pada aplikasi ini.
```
    from django.db import models

    class Items(models.Model):
        item_name = models.CharField(max_length=255)
        amount = models.IntegerField()
        description = models.TextField()
```

**Penjelasan kode**
- `Item` : nama model yang akan digunakan
- `nama` : nama item stok makanan
- `amount` : jumlah stok makanan tersebut saat ini
- `description` : deskripsi singkat mengenai item stok makanan

Model yang telah dibuat tersebut perlu untuk dimigrasikan  ke basis data lokal. Pada direktori yang sama, saya menjalankan perintah `python manage.py makemigrations` untuk membuat berkas migrasi yang berisi perubahan yang telah dilakukan pada model. Namun, pada makemigrations, perubahan belum diaplikasikan pada basis data.
Untuk menerapkan migrasi ke basis data lokal, saya menjalankan perintah `python manage.py migrate`. Dengan demikian, perubahan pada model pun telah berhasil disimpan.

### Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu
1. Dalam direktori aplikasi `main`, saya membuat berkas `views.py`. Berkas ini berfungsi sebagai tempat dimana kode mengenai 'tampilan' website akan disimpan.
2.  Pada berkas `views.py`, saya menambahkan `from django.shortcuts import render` untuk me-render tampilan HTML dengan menggunakan data yang telah diberikan sebelumnya.
3. Selain import render, saya juga menambahkan fungsi `show_main`
```
    from django.shortcuts import render
    def show_main(request):
        context = {
            'name': 'Calista Sekar',
            'class': 'PBP C',
            'item_name' : 'wortel',
            'amount' : '2',
        }
    return render(request, "main.html", context)
```

**Penjelasan kode**
- Fungsi `show_main` berfungsi untuk mengatur permintaan HTTP dan mengembalikan tampilan yang sesuai dengan request yang diterima
- Pada dictionary `context`, saya menambahkan empat data, yaitu :
    - `name` : data nama pengguna
    - `class` : data kelas pengguna
    - `item_name` : nama dari item yang didaftarkan
    - `amount` : jumlah stok saat ini dari item yang didaftarkan
4. Untuk menampilkan data yang telah diambil dari model, saya mengubah data yang telah ada di dalam berkas `main.html` pada direktori `main/template` sehingga nilainya dapat berubah bergantung pada apa yang telah didefinisikan dalam `context`
```
    <h1>Developer Page</h1>

    <h5>Name: </h5>
    <p>{{ name }}</p> 
    <h5>Class: </h5>
    <p>{{ class }}</p> 

    <h1>FoodStock</h1>

    <h5>Item Name: </h5>
    <p>{{ item_name }}</p>
    <h5>Amount: </h5>
    <p>{{ amount }}</p> 
```

### Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py
1. Dalam direktori `main`, saya membuat berkas `urls.py` yang berfungsi untuk mengatur URL spesifik aplikasi ini, yaitu ke fungsi `show_main` pada berkas `views.py`. Pada berkas `urls.py`, saya menambahkan kode sebagai berikut :
```
from django.urls import path
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
```

2. Selain pada direktori main, saya juga memodifikasi kode pada berkas `urls.py` dalam direktori proyek `foodstock` dengan mengimpor fungsi include dan menambahkan rute URL. Berkas `urls.py` pada direktori ini berfungsi untuk mengarahkan rute URL di tingkat proyek sehingga memungkinkan aplikasi dalam proyek Django bersifat modular dan terpisah. 
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
]
```


### Melakukan deployment ke Adaptable terhadap aplikasi yang sudah dibuat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.
Aplikasi FoodStock sudah di-_deploy_ ke platform Adaptable dan dapat diakses secara bebas pada [FoodStock](https://foodstock.adaptable.app/main/)

###  Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html

![Bagan Request Client ke Web Aplikasi berbasis Django](diagram-request.png)

Ketika user mengirimkan _request_ kepada web, HTTP _request_ tersebut diproses oleh urls.py dan diarahkan ke View (views.py) yang sesuai. Setelah itu, View menghubungi Model (models.py) sehingga Model mengambil data yang dibutuhkan ke database. Data yang diterima dari Database kemudian diolah oleh Model dengan mengubah dan mengklasifikasikan tiap objek di Database menjadi kelas-kelas. Hasilnya kemudian dikirimkan ke View. Oleh View, data tersebut ditambahkan ke Template. Hasil dari penggabungan tersebut berbentuk berkas HTML. Hasil ini kemudian dikirimkan kembali ke Client sebagai HTTP Response.

###  Jelaskan mengapa kita menggunakan virtual environment? Apakah kita tetap dapat membuat aplikasi web berbasis Django tanpa menggunakan virtual environment?
_Virtual environment_ berfungsi untuk mengisolasi _package_ serta _dependencies_ dari aplikasi sehingga tidak bertabrakan dengan versi lain yang ada pada komputer yang sama. Dengan _virtual environment_, kita dapat mengerjakan beberapa aplikasi/proyek dengan versi berbeda meski dengan modul yang sama. Selain itu, kita dapat mengontrol lingkungan pengembangan aplikasi dengan lebih baik sehingga proses pengembangan dan pemeliharaan aplikasi pun menjadi lebih mudah.

Kita tetap dapat membuat aplikasi web berbasis Django tanpa menggunakan _virtual environment._ Akan tetapi, tanpa penggunaan _virtual environment_, kemungkinan munculnya masalah terkait konflik versi atau manajemen dependensi proyek lebih besar. Oleh karena itu, penggunaan virtual environment dalam pengembangkan web berbasis Django sangat disarankan.

###  Jelaskan apakah itu MVC, MVT, MVVM dan perbedaan dari ketiganya
- MVC (Model-View-Controller) adalah sebuah pola arsitektur dalam membuat sebuah aplikasi dengan cara memisahkan kode menjadi tiga bagian, yaitu Model, View, dan Controller. Karena dibagi menjadi tiga komponen atau unit, pemeliharaan dan pengoptimalan sistem jadi lebih mudah.
- MVT adalah singkatan dari Model-View-Template. MVT adalah sebuah konsep arsitektur yang digunakan dalam pengembangan web untuk memisahkan komponen-komponen utama dari sebuah aplikasi. Konsep ini memungkinkan pengembang web untuk mengorganisasi dan mengelola kode dengan lebih terstruktur.
- MVVM (Model-View-ViewModel) adalah salah satu arsitektur pembuatan aplikasi berbasis GUI yang berfokus pada pemisahan antara kode untuk logika bisnis dan tampilan aplikasi. Dalam penerapannya, MVVM terbagi atas beberapa layer, yaitu Model, View, dan ViewModel.

Perbedaan utama dari ketiganya adalah pola pembagian komponen-komponennya
- 'Template' pada MTV setara dengan 'View' pada MVC yang mana berfungsi untuk merancang tampilan yang akhirnya akan diisi dengan data dari model melalui View (MTV) atau Controller (MVC).
- 'View' pada MTV setara dengan 'Controller' pada MVC yang mana berfungsi sebagai pengatur tampilan dan mengambil data dari model untuk disajikan kepada pengguna.
- 'View' pada MVVM mirip dengan 'View' pada MVC yang mana berfungsi sebagai antarmuka grafis antara pengguna dan pola desain, serta menampilkan output dari data yang telah diproses.
- 'ViewModel' pada MVVM merupakan abstraksi dari 'View' yang berfungsi sebagai pembungkus data model. 'ViewModel' berisi perintah yang dapat digunakan oleh 'View' untuk memengaruhi 'Model'

