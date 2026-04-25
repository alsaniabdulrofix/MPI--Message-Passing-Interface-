import os
# Baris di bawah ini opsional, gunakan jika muncul error DLL pada Windows
# os.add_dll_directory(r"C:\Program Files\Microsoft MPI\Bin")

from mpi4py import MPI

# 1. Inisialisasi komunikator
comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()

# 2. Menyiapkan variabel di semua node
shared_data = None

if my_rank == 0:
    # Master mengisi data ke dalam memorinya
    shared_data = {
        'informasi_jaringan': 'Config_OSPF_V1',
        'threshold_latency': 50,
        'status': 'Aktif'
    }
    print(f"[Node {my_rank}] Master menyiapkan data di memori: {shared_data}")
else:
    print(f"[Node {my_rank}] Worker menunggu kiriman data dari Master...")

# 3. Proses 'Sharing' menggunakan Broadcast (bcast)
# Fungsi ini mengirimkan data dari root (0) ke semua node lainnya
shared_data = comm.bcast(shared_data, root=0)

# 4. Verifikasi: Semua node sekarang memiliki data yang sama di memori lokalnya
print(f"[Node {my_rank}] Sekarang memiliki data di memori lokal: {shared_data}")

MPI.Finalize()