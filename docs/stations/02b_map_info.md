Dataset ini diperoleh dari [Kaggle](https://www.kaggle.com/datasets/greegtitan/indonesia-climate), dengan kontribusi dari pengguna [Greegtitan](https://www.kaggle.com/datasets/greegtitan/indonesia-climate). Dataset telah [diolah menjadi HDF5](https://www.kaggle.com/code/tarumainfo/compile-rainfall-dataset-to-hdf5) dan disimpan informasi metadatanya menggunakan script yang tersedia di [taruma/demo-stations](https://github.com/taruma/demo-stations).

Dataset terdiri berbagai stasiun meteorologi dan geofisika di Indonesia, dengan fokus pada data curah hujan. Berikut adalah penjelasan rinci tentang informasi yang tersedia:

**Kolom:**

* **id**: Identifikasi unik untuk setiap stasiun, menggunakan format "kg_" diikuti oleh kode numerik.
* **station_name**: Nama lengkap stasiun meteorologi atau geofisika.
* **latitude**:  Koordinat lintang dari lokasi stasiun.
* **longitude**: Koordinat bujur dari lokasi stasiun.
* **key**: Kunci atau identifier unik yang digunakan untuk mengakses data stasiun dalam sistem atau platform tertentu.
* **filename**: Nama file (dalam format .h5) yang berisi data curah hujan untuk stasiun tersebut.
* **title**: Judul atau deskripsi singkat dari sumber data, dalam hal ini "Kaggle".
* **source**: Sumber data curah hujan, yaitu "Kaggle - Greegtitan".
* **rel_folder**: Lokasi relatif dari folder yang menyimpan file data curah hujan.
* **date_start**: Tanggal mulai data curah hujan yang tersedia untuk stasiun tersebut. 
* **date_end**: Tanggal akhir data curah hujan yang tersedia untuk stasiun tersebut.

**Konteks Data:**

* Data curah hujan bersumber dari Kaggle, khususnya dataset yang dibagikan oleh pengguna "Greegtitan".
* Data disimpan dalam format file HDF5 (.h5), yang umum digunakan untuk menyimpan data ilmiah dalam jumlah besar.
* Terdapat informasi tentang periode ketersediaan data curah hujan untuk setiap stasiun, yang bervariasi dari tahun 2010 hingga 2020. 
* Beberapa stasiun memiliki data yang tidak lengkap atau periode data yang lebih pendek dibandingkan dengan yang lain.

