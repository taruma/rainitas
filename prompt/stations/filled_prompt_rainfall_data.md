Setelah kamu memeriksa kelengkapan data hujan, Kamu melanjutkan ke tahap mengeksplorasi curah hujan harian pada setiap stasiun. 

Berikut tabel stasiun hujan terdekat:

| ID       | DATASET   |   DISTANCE | STATION NAME                              |
|:---------|:----------|-----------:|:------------------------------------------|
| kg_96733 | Kaggle    |      6.494 | Stasiun Klimatologi Banten                |
| kg_96747 | Kaggle    |      8.863 | Halim Perdana Kusuma Jakarta              |
| kg_96745 | Kaggle    |     12.359 | Stasiun Meteorologi Kemayoran             |
| kg_96741 | Kaggle    |     18.887 | Stasiun Meteorologi Maritim Tanjung Priok |
| kg_96749 | Kaggle    |     23.707 | Stasiun Meteorologi Soekarno Hatta        |

Berikut tabel statisitik data hujan di setiap stasiun yang diperoleh menggunakan fungsi .describe(), dengan kolom menunjukkan setiap stasiun (menggunakan kode stasiun):

|       |   kg_96733 |   kg_96747 |   kg_96745 |   kg_96741 |   kg_96749 |
|:------|-----------:|-----------:|-----------:|-----------:|-----------:|
| count | 2750       |  1973      | 3662       | 2894       |  3514      |
| mean  |    8.49676 |    10.6368 |    6.36043 |    7.49879 |     5.3403 |
| std   |   15.7246  |    19.5013 |   17.0089  |   18.5653  |    15.3933 |
| min   |    0       |     0      |    0       |    0       |     0      |
| 25%   |    0       |     0      |    0       |    0       |     0      |
| 50%   |    1.2     |     2.3    |    0       |    0       |     0      |
| 75%   |    9.7     |    13      |    4.5     |    5.6     |     3.2    |
| max   |  208.9     |   305      |  277.5     |  284       |   397.4    |

Buat setidaknya 3 paragraf yang berisikan informasi apa saja yang dapat diperoleh dari tabel tersebut.

---

Ikuti panduan berikut:
- saat menuliskan nama stasiun, tuliskan dengan format: {id_stasiun} - {nama stasiun}
- nama stasiun harus ditebalkan/bold.
- untuk setiap angka gunakan format sebagai berikut: :blue-background[{angka}]
- awali hasil analisis dengan "Berdasarkan ...."
- pada akhir paragraf berikan kesimpulan untuk seluruh stasiun.