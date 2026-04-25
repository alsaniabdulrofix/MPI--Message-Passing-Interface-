from mpi4py import MPI
import time

# 1. Inisialisasi Environment MPI
comm = MPI.COMM_WORLD

# 2. Dapatkan ID Node (rank) dan Total Node (size)
my_rank = comm.Get_rank()
total_nodes = comm.Get_size()

def calculate_shortest_path(area_data):
    """Fungsi tiruan untuk komputasi algoritma routing (misal: OSPF/Dijkstra)"""
    time.sleep(2) # Simulasi waktu komputasi berat (2 detik)
    return f"Tabel_Routing_Selesai_Untuk_{area_data}"

# 3. Logika Master vs Worker
if my_rank == 0:
    # ==========================================
    # TUGAS NODE 0 (MASTER)
    # ==========================================
    print("[Master] Memulai simulasi perhitungan routing...")
    
    # Menyiapkan data topologi (jumlah area disesuaikan dengan jumlah worker)
    list_area = [f"Area_Jaringan_{i}" for i in range(1, total_nodes)]
    
    # --- FASE DISTRIBUSI ---
    for worker_id in range(1, total_nodes):
        # Ambil jatah data untuk worker ini (indeks array mulai dari 0)
        data_area = list_area[worker_id - 1] 
        
        # Mengirim data ke worker dengan tag 1
        comm.send(data_area, dest=worker_id, tag=1)
        print(f"[Master] Mengirim data '{data_area}' ke Worker {worker_id}")
        
    # --- FASE PENGUMPULAN ---
    tabel_routing_global = []
    
    for worker_id in range(1, total_nodes):
        # Menerima hasil dari worker dengan tag 2
        hasil_lokal = comm.recv(source=worker_id, tag=2)
        tabel_routing_global.append(hasil_lokal)
        print(f"[Master] Menerima hasil dari Worker {worker_id}: {hasil_lokal}")
        
    print("\n[Master] Simulasi Selesai! Hasil Gabungan Tabel Routing:")
    for hasil in tabel_routing_global:
        print(f" -> {hasil}")

else:
    # ==========================================
    # TUGAS NODE WORKER (Rank > 0)
    # ==========================================
    # Menerima jatah data topologi dari Master
    data_area_saya = comm.recv(source=0, tag=1)
    print(f"[Worker {my_rank}] Menerima tugas menghitung {data_area_saya}...")
    
    # Melakukan komputasi algoritma secara independen
    hasil_komputasi = calculate_shortest_path(data_area_saya)
    print(f"[Worker {my_rank}] Perhitungan selesai, mengirim kembali ke Master.")
    
    # Mengirim hasil kembali ke Master
    comm.send(hasil_komputasi, dest=0, tag=2)