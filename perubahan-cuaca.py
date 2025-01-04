import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("KELOMPOK MAYORA JAYANTI")

# Warna
SKY_COLOR = (135, 206, 235)  # Warna langit (biru cerah)
RAINY_SKY_COLOR = (192, 192, 192)  # Warna langit saat hujan (abu-abu)
GRASS_COLOR = (34, 139, 34)  # Warna rumput (hijau)
SUN_COLOR = (255, 255, 0)    # Warna matahari (kuning)
MOUNTAIN_COLOR = (105, 105, 105)  # Warna gunung (abu-abu)
CLOUD_COLOR = (255, 255, 255)  # Warna awan cerah (putih)
CLOUD_DARK_COLOR = (169, 169, 169)  # Warna awan mendung (abu-abu gelap)
RAIN_COLOR = (255, 255, 255)    # Warna hujan (biru muda)
HOUSE_WALL_COLOR = (139, 69, 19)  # Warna dinding rumah (coklat)
HOUSE_ROOF_COLOR = (178, 34, 34)  # Warna atap rumah (merah)
HOUSE_DOOR_COLOR = (205, 133, 63)  # Warna pintu rumah (coklat muda)
HOUSE_WINDOW_COLOR = (0, 191, 255)  # Warna jendela rumah (biru muda)

# Posisi matahari
sun_x = screen_width - 420
sun_y = 190
sun_speed = 1  # Kecepatan pergerakan matahari

# Properti hujan
raindrops = []  # List untuk menyimpan tetesan hujan
is_raining = False  # Flag untuk mendeteksi apakah sedang hujan

# Fungsi untuk menggambar pemandangan
def draw_scene():
    global is_raining
    
    # Mengatur warna latar belakang berdasarkan kondisi hujan
    current_sky_color = RAINY_SKY_COLOR if is_raining else SKY_COLOR

    # Menggambar latar belakang
    screen.fill(current_sky_color)

    # Menggambar gunung pertama
    pygame.draw.polygon(screen, MOUNTAIN_COLOR, [(0, screen_height - 100), (300, 200), (600, screen_height - 100)])
    
    # Menggambar gunung kedua
    pygame.draw.polygon(screen, MOUNTAIN_COLOR, [(200, screen_height - 100), (500, 150), (800, screen_height - 100)])
    
    # Menggambar awan
    cloud_color = CLOUD_COLOR if not is_raining else CLOUD_DARK_COLOR
    pygame.draw.circle(screen, cloud_color, (150, 100), 40)
    pygame.draw.circle(screen, cloud_color, (200, 120), 50)
    pygame.draw.circle(screen, cloud_color, (250, 100), 40)
    pygame.draw.circle(screen, cloud_color, (400, 90), 50)
    pygame.draw.circle(screen, cloud_color, (450, 110), 40)
    pygame.draw.circle(screen, cloud_color, (500, 90), 50)
    pygame.draw.circle(screen, cloud_color, (600, 130), 40)
    pygame.draw.circle(screen, cloud_color, (650, 110), 50)
    
    # Menggambar rumput
    pygame.draw.rect(screen, GRASS_COLOR, (0, screen_height - 100, screen_width, 100))
    
    # Menggambar rumah
    house_x = 400
    house_y = 350
    house_width = 200
    house_height = 150
    roof_height = 80

    # Dinding rumah (rectangle)
    pygame.draw.rect(screen, HOUSE_WALL_COLOR, (house_x, house_y, house_width, house_height))

    # Atap rumah (segitiga)
    pygame.draw.polygon(screen, HOUSE_ROOF_COLOR, [(house_x - 20, house_y), (house_x + house_width + 20, house_y), (house_x + house_width // 2, house_y - roof_height)])

    # Pintu rumah
    door_width = 60
    door_height = 100
    pygame.draw.rect(screen, HOUSE_DOOR_COLOR, (house_x + house_width // 2 - door_width // 2, house_y + house_height - door_height, door_width, door_height))

    # Jendela rumah (2 jendela)
    window_size = 40
    pygame.draw.rect(screen, HOUSE_WINDOW_COLOR, (house_x + 30, house_y + 40, window_size, window_size))  # Jendela kiri
    pygame.draw.rect(screen, HOUSE_WINDOW_COLOR, (house_x + house_width - 70, house_y + 40, window_size, window_size))  # Jendela kanan
    
    # Menggambar matahari
    if not is_raining:
        pygame.draw.circle(screen, SUN_COLOR, (sun_x, sun_y), 50)
    
    # Menggambar pohon
    pygame.draw.rect(screen, (139, 69, 19), (150, 400, 40, 100))  # batang pohon
    pygame.draw.circle(screen, (0, 128, 0), (170, 350), 50)        # daun pohon
    
    # Menggambar hujan jika matahari keluar layar
    if is_raining:
        # Menambahkan tetesan hujan baru
        if random.random() < 0.1:  # Frekuensi hujan
            raindrop_x = random.randint(0, screen_width)
            raindrop_y = 0
            raindrops.append([raindrop_x, raindrop_y])
        
        # Menggambar dan memindahkan hujan
        for raindrop in raindrops:
            pygame.draw.circle(screen, RAIN_COLOR, (raindrop[0], raindrop[1]), 3)
            raindrop[1] += 5  # Kecepatan tetesan hujan
            
            # Menghapus tetesan hujan yang sudah keluar layar
            if raindrop[1] > screen_height:
                raindrops.remove(raindrop)

# Properti petir
lightning_active = False  # Status petir aktif atau tidak
lightning_timer = 0  # Timer untuk mengatur durasi petir
lightning_duration = 20  # Durasi petir dalam frame

# Fungsi untuk menggambar petir
def draw_lightning():
    if lightning_active:
        # Posisi petir acak di sekitar awan
        start_x = random.randint(100, 700)
        start_y = random.randint(50, 150)
        for _ in range(3):  # Buat beberapa segmen petir
            end_x = start_x + random.randint(-50, 50)
            end_y = start_y + random.randint(20, 50)
            pygame.draw.line(screen, (255, 255, 255), (start_x, start_y), (end_x, end_y), 2)
            start_x, start_y = end_x, end_y

# Loop utama permainan
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Mengambil input keyboard
    keys = pygame.key.get_pressed()
    
    # Menggerakkan matahari dengan tombol W, A, S, D
    if keys[pygame.K_a]:  # Gerak kiri
        sun_x -= sun_speed
    if keys[pygame.K_d]:  # Gerak kanan
        sun_x += sun_speed
    if keys[pygame.K_w]:  # Gerak atas
        sun_y -= sun_speed
    if keys[pygame.K_s]:  # Gerak bawah
        sun_y += sun_speed
    
    # Cek apakah matahari keluar dari layar
    if sun_x < 0 or sun_x > screen_width or sun_y < 0 or sun_y > screen_height:
        is_raining = True  # Aktifkan hujan
    else:
        is_raining = False  # Matikan hujan jika matahari di layar
    
    # Logika petir
    if is_raining:
        if not lightning_active and random.random() < 0.02:  # Peluang petir muncul
            lightning_active = True
            lightning_timer = lightning_duration
        if lightning_active:
            lightning_timer -= 15
            if lightning_timer <= 0:  # Petir selesai
                lightning_active = False

    # Menggambar pemandangan
    draw_scene()

    # Menggambar petir (jika aktif)
    if lightning_active:
        draw_lightning()

    # Update layar
    pygame.display.flip()

# Keluar dari Pygame
pygame.quit()
sys.exit()
