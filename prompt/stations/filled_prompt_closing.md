Sebagai ahli hidrologi, buat 4 paragraf penutup yang menyimpulkan narasi berikut (tanpa mengulangi informasi yang sama):

---

## Stasiun Terdekat

Berdasarkan koordinat yang Anda masukkan, telah ditemukan sebanyak :orange-background[**5 stasiun hujan terdekat**] dalam radius :orange-background[25 kilometer] dari titik :orange-background[**Queensdale**] _(:orange-background[-6.2631, 106.8095])_. Peta dan tabel di bawah ini menunjukkan lokasi dan informasi detail dari stasiun-stasiun tersebut.

| ID       | DATASET   |   DISTANCE | STATION NAME                              |
|:---------|:----------|-----------:|:------------------------------------------|
| kg_96733 | Kaggle    |      6.494 | Stasiun Klimatologi Banten                |
| kg_96747 | Kaggle    |      8.863 | Halim Perdana Kusuma Jakarta              |
| kg_96745 | Kaggle    |     12.359 | Stasiun Meteorologi Kemayoran             |
| kg_96741 | Kaggle    |     18.887 | Stasiun Meteorologi Maritim Tanjung Priok |
| kg_96749 | Kaggle    |     23.707 | Stasiun Meteorologi Soekarno Hatta        |

Dari peta diatas terlihat :orange-background[5 stasiun hujan terdekat]. Stasiun tersebut antara lain: :orange-background[***Stasiun Klimatologi Banten, Halim Perdana Kusuma Jakarta, Stasiun Meteorologi Kemayoran, Stasiun Meteorologi Maritim Tanjung Priok, Stasiun Meteorologi Soekarno Hatta***]. Dengan stasiun terdekat yaitu :orange-background[**Stasiun Klimatologi Banten**] yang berjarak :orange-background[_6 km_] dari titik koordinat :orange-background[Queensdale] dan stasiun terjauh yaitu :orange-background[**Stasiun Meteorologi Soekarno Hatta**] yang berjarak :orange-background[_24 km_] dari titik koordinat :orange-background[Queensdale]. 

## Kelengkapan Data

Untuk memudahkan memeriksa kelengkapan data, kita dapat menggunakan grafik heatmap. Grafik ini akan menunjukkan keberadaan data yang hilang dalam bentuk warna. Semakin gelap warna yang dihasilkan, maka data yang hilang semakin banyak. Grafik akan menampilkan :orange-background[5 stasiun pengamatan yang terdekat] terhadap titik tinjauan :orange-background[Queensdale].

Berdasarkan aplikasi didapatkan hasil analisis sebagai berikut:

Berdasarkan tabel kelengkapan data hujan, kita dapat melihat bahwa stasiun yang sering menghasilkan data terlengkap adalah **kg_96733 - Stasiun Klimatologi Banten** dengan rata-rata kelengkapan data yang tinggi di sebagian besar bulan dalam beberapa tahun. Terutama dari tahun 2010 hingga 2013, persentase kelengkapan data sering berada di atas :blue-background[90%] dan beberapa kali mencapai :blue-background[100%]. Selama periode 2015-2016, kelengkapan data menurun secara signifikan, terkadang hanya mencapai :blue-background[10%] hingga :blue-background[50%], tetapi kembali meningkat setelah tahun 2017.

Sementara itu, **kg_96747 - Halim Perdana Kusuma Jakarta** menunjukkan penurunan dramatis dalam kelengkapan data mulai dari sekitar pertengahan tahun 2013, di mana persentase kelengkapannya sering di bawah :blue-background[30%] atau bahkan :blue-background[10%]. Meski sempat menunjukkan kelengkapan di kisaran :blue-background[50%] hingga :blue-background[70%] di beberapa bulan tahun 2014, kinerja stasiun ini menjadi jauh lebih buruk hingga tahun 2015 dan setelah itu data tidak tersedia lagi sehingga tidak dapat dianalisis lebih lanjut.

**kg_96745 - Stasiun Meteorologi Kemayoran** secara umum memiliki rata-rata kelengkapan data yang cukup baik, lebih sering berada di atas :blue-background[90%] dari tahun 2010 hingga awal 2014. Namun, seperti stasiun lain, terjadi penurunan mulai pertengahan 2014 dengan nilai kelengkapan yang kadang jatuh di bawah :blue-background[50%]. Pada periode berikutnya, kelengkapan data kembali naik dan tetap stabil di atas :blue-background[60%] hingga tahun 2020.

Kesimpulan dari analisis ini adalah bahwa **kg_96733 - Stasiun Klimatologi Banten** secara konsisten memiliki kelengkapan data tertinggi, diikuti dengan **kg_96745 - Stasiun Meteorologi Kemayoran** yang menunjukkan keandalan yang hampir sebanding. Sebaliknya, **kg_96747 - Halim Perdana Kusuma Jakarta** menunjukkan kelemahan signifikan dengan penurunan dramatis dalam kelengkapan data pada pertengahan hingga akhir periode yang diukur. Ini dapat memberi informasi penting dalam memilih stasiun yang relevan dan andal untuk analisis lebih lanjut dan penelitian hidrologi di wilayah terkait.

## Hujan Harian

Setelah mengetahui kelengkapan data untuk stasiun terdekat, kita dapat melanjutkan ke tahap berikutnya yaitu mengeksplorasi data curah hujan harian. Pada tahap ini, kita akan memeriksa data curah hujan harian yang tersedia dalam dataset. Data curah hujan harian ini akan digunakan untuk mengevaluasi kondisi curah hujan harian untuk setiap stasiun pengamatan. Stasiun yang ditampilkan antara lain:

1. `kg_96733` - :green-background[**Stasiun Klimatologi Banten**]
1. `kg_96747` - :green-background[**Halim Perdana Kusuma Jakarta**]
1. `kg_96745` - :green-background[**Stasiun Meteorologi Kemayoran**]
1. `kg_96741` - :green-background[**Stasiun Meteorologi Maritim Tanjung Priok**]
1. `kg_96749` - :green-background[**Stasiun Meteorologi Soekarno Hatta**]

Berikut grafik yang menunjukkan data curah hujan harian untuk setiap stasiun pengamatan.

Berdasarkan aplikasi didapatkan hasil analisis sebagai berikut:

Berdasarkan tabel stasiun hujan terdekat dan statistik data hujan harian, kita dapat menarik beberapa informasi penting. Pertama, mengenai jumlah data yang ada, stasiun **kg_96733 - Stasiun Klimatologi Banten** memiliki :blue-background[2750] entri data, sedangkan **kg_96747 - Halim Perdana Kusuma Jakarta** memiliki :blue-background[1973] entri data. **kg_96745 - Stasiun Meteorologi Kemayoran** merupakan yang terbanyak dengan :blue-background[3662] entri data, diikuti oleh **kg_96741 - Stasiun Meteorologi Maritim Tanjung Priok** yang memiliki :blue-background[2894] entri data, dan **kg_96749 - Stasiun Meteorologi Soekarno Hatta** dengan :blue-background[3514] entri data. Dari segi rata-rata curah hujan harian, **kg_96747 - Halim Perdana Kusuma Jakarta** mencatat rata-rata tertinggi yakni :blue-background[10.6368] mm, sementara **kg_96749 - Stasiun Meteorologi Soekarno Hatta** mencatat rata-rata curah hujan terendah dengan :blue-background[5.3403] mm.

Kedua, di sisi penyebaran data atau deviasi standar, stasiun-stasiun menunjukkan variasi yang signifikan dalam curah hujan hariannya. **kg_96733 - Stasiun Klimatologi Banten** memiliki standar deviasi :blue-background[15.7246] mm, sementara **kg_96747 - Halim Perdana Kusuma Jakarta** memiliki standar deviasi tertinggi yaitu :blue-background[19.5013] mm. **kg_96749 - Stasiun Meteorologi Soekarno Hatta** memiliki deviasi standar :blue-background[15.3933] mm, sedikit lebih rendah dibandingkan stasiun sebelumnya. Hal ini menunjukkan bahwa variabilitas curah hujan harian di **kg_96747 - Halim Perdana Kusuma Jakarta** relatif lebih tinggi dibandingkan dengan stasiun lainnya, yang berarti hujan di area ini mungkin lebih tidak terprediksi atau berubah-ubah.

Selain itu, mengenai distribusi data, untuk semua stasiun, curah hujan minimum yang diamati adalah :blue-background[0] mm serta 25% nilai persentil juga adalah :blue-background[0] mm, menunjukkan bahwa pada banyak hari tidak ada hujan. Namun demikian, perbedaan mencolok terlihat pada nilai persentil ke-75 dan nilai maksimum. **kg_96747 - Halim Perdana Kusuma Jakarta** mengalami curah hujan maksimum tertinggi dengan :blue-background[305] mm, sedangkan **kg_96749 - Stasiun Meteorologi Soekarno Hatta** mencatat maksimum tertinggi kedua sebesar :blue-background[397.4] mm. Ini memperkuat fakta bahwa hujan harian bisa sangat tinggi pada beberapa kesempatan di wilayah-wilayah ini. 

Kesimpulannya, data ini menunjukkan bahwa ada variabilitas signifikan dalam curah hujan harian di berbagai stasiun di sekitar area yang dipertimbangkan. **kg_96747 - Halim Perdana Kusuma Jakarta** memiliki rata-rata curah hujan harian tertinggi serta variabilitas yang tinggi, sementara **kg_96749 - Stasiun Meteorologi Soekarno Hatta** menunjukkan kesamaan dalam variabilitas tetapi dengan rata-rata curah hujan harian yang lebih rendah. Secara keseluruhan, informasi ini penting untuk merencanakan manajemen air dan penanggulangan banjir di area terkait.

---

Ikuti panduan berikut:
- saat menuliskan nama stasiun, tuliskan dengan format: {id_stasiun} - {nama stasiun}
- nama stasiun harus ditebalkan/bold.
- untuk setiap angka gunakan format sebagai berikut: :blue-background[{angka}%]
- bulatkan angka ke 2 desimal terdekat.
- pada akhir paragraf berikan informasi apa yang dapat dilakukan selanjutnya.