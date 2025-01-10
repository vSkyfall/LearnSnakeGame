import pygame, sys, random

# Ekran boyutları
screen_width = 600
screen_height = 600

# Arka plan grid genişliği ve hücre boyutları
gridsize = 20
gridwith = screen_width / gridsize  # Grid sütun sayısı
grid_height = screen_height / gridsize  # Grid satır sayısı

# Renk tanımlamaları
light_green = (0, 170, 140)  # Gridin açık yeşil rengi
dark_green = (0, 140, 120)   # Gridin koyu yeşil rengi
food_color = (250, 200, 0)   # Yem rengi
snake_color = (128, 0, 128)  # Yılan rengi (mor)

# Yılanın yön tanımları
up = (0, -1)    # Yukarı
down = (0, 1)   # Aşağı
right = (1, 0)  # Sağ
left = (-1, 0)  # Sol

# Yüksek skor değişkeni
high_score = 0  # Oyun boyunca tutulan yüksek skor

# Yılan sınıfı
class SNAKE:
    def __init__(self):
        self.positions = [((screen_width / 2), (screen_height / 2))]  # Yılanın başlangıç pozisyonu (ortada)
        self.lenght = 1  # Yılanın başlangıç uzunluğu
        self.direction = random.choice([up, down, right, left])  # Yılanın rastgele başlangıç yönü
        self.color = snake_color  # Yılanın rengi
        self.score = 0  # Oyuncunun skoru

    def draw(self, surface):
        # Yılanın pozisyonlarına göre çizilmesi
        for p in self.positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))  # Yılanın her parçası bir dikdörtgen
            pygame.draw.rect(surface, self.color, rect)

    def move(self):
        # Yılanın hareket etmesi
        cur = self.positions[0]  # Yılanın başı
        x, y = self.direction  # Mevcut yön
        # Yeni baş pozisyonu
        new = (((cur[0] + (x * gridsize)) % screen_width), (cur[1] + (y * gridsize)) % screen_height)
        # Eğer yılan kendi gövdesine çarparsa
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()  # Yılanı sıfırla
            return True  # Çarpışma bildirimi
        else:
            # Yılanın yeni pozisyonları
            self.positions = [new] + self.positions
            if len(self.positions) > self.lenght:  # Eğer yılan uzamadıysa kuyruğunu sil
                self.positions.pop()
            return False

    def handle_keys(self):
        # Yön değiştirmek için klavye kontrolleri
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.direction != down:  # Yukarı giderken aşağıya dönemez
            self.direction = up
        elif keys[pygame.K_DOWN] and self.direction != up:  # Aşağı giderken yukarıya dönemez
            self.direction = down
        elif keys[pygame.K_RIGHT] and self.direction != left:  # Sağa giderken sola dönemez
            self.direction = right
        elif keys[pygame.K_LEFT] and self.direction != right:  # Sola giderken sağa dönemez
            self.direction = left

    def reset(self):
        # Yılan sıfırlandığında yapılacaklar
        global high_score
        high_score = max(high_score, self.score)  # Yüksek skoru güncelle
        self.positions = [((screen_width / 2), (screen_height / 2))]  # Başlangıç pozisyonuna dön
        self.lenght = 1  # Yılan uzunluğunu sıfırla
        self.direction = random.choice([up, down, right, left])  # Yılan yönünü rastgele seç
        self.score = 0  # Skoru sıfırla

# Yem sınıfı
class FOOD:
    def __init__(self):
        self.position = (0, 0)  # Başlangıç pozisyonu
        self.color = food_color  # Yem rengi
        self.randomize_position()  # Rastgele pozisyon belirle

    def randomize_position(self):
        # Yemin rastgele bir pozisyona taşınması
        self.position = (random.randint(0, gridwith - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        # Yemin çizilmesi
        rect = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)

# Grid çizimi
def drawGrid(surface):
    # Arka plan gridinin çizilmesi
    for y in range(0, int(grid_height)):
        for x in range(0, int(gridwith)):
            if (x + y) % 2 == 0:
                light = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, light_green, light)  # Açık renk kareler
            else:
                dark = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, dark_green, dark)  # Koyu renk kareler
def main_menu():
    # Ana menünün oluşturulması
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont("arial", 40)  # Menü yazı tipi
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))  # Arka planı siyah yap
        title_text = font.render("Snake Game", True, (255, 255, 255))  # Başlık
        start_text = font.render("1. Start Game", True, (0, 255, 0))  # Başlat seçeneği
        exit_text = font.render("2. Exit", True, (255, 0, 0))  # Çıkış seçeneği
        # Yazıların ekrana çizilmesi
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 200))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 300))
        pygame.display.update()
        # Olayları kontrol et
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # "1" tuşuna basıldığında oyuna başla
                    return
                elif event.key == pygame.K_2:  # "2" tuşuna basıldığında çık
                    pygame.quit()
                    sys.exit()
        clock.tick(15)  # FPS'yi sabitle


def main():
    # Oyunun ana döngüsü
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont("arial", 20)  # Yazı tipi
    clock = pygame.time.Clock()
    surface = pygame.Surface(screen.get_size())  # Ana yüzey
    surface = surface.convert()
    snake = SNAKE()  # Yılan sınıfı oluştur
    food = FOOD()  # Yem sınıfı oluştur

    global high_score  # Yüksek skor değişkenini global yap
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Oyun işlemleri
        clock.tick(15)  # FPS
        snake.handle_keys()  # Kullanıcı girişini al
        collision = snake.move()  # Yılanı hareket ettir ve çarpışma durumunu kontrol et
        if collision:
            # Yılan öldüğünde ölüm ekranı
            death_menu(screen, snake.score)  
            return

        if snake.positions[0] == food.position:
            # Yılan yemek yediğinde skor artışı ve uzama
            snake.lenght += 1
            snake.score += 1
            food.randomize_position()

        # Skor metni
        score_text = font.render("Score: " + str(snake.score), True, (255, 255, 255))
        high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
        
        # Yüzey temizleme ve çizim
        surface.fill((0, 0, 0))
        drawGrid(surface)  # Grid çizimi
        food.draw(surface)  # Yem çizimi
        snake.draw(surface)  # Yılan çizimi
        surface.blit(score_text, (10, 10))  # Skoru ekrana yazdır
        surface.blit(high_score_text, (10, 40))  # Yüksek skoru ekrana yazdır
        screen.blit(surface, (0, 0))
        pygame.display.update()


def death_menu(screen, score):
    # Ölüm ekranı
    font = pygame.font.SysFont("arial", 40)  # Yazı tipi
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))  # Arka plan siyah
        death_text = font.render("Game Over", True, (255, 0, 0))  # Ölüm mesajı
        score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))  # Skor gösterimi
        restart_text = font.render("1. Restart", True, (0, 255, 0))  # Tekrar başlat seçeneği
        exit_text = font.render("2. Exit", True, (255, 0, 0))  # Çıkış seçeneği
        # Yazıların ekrana çizilmesi
        screen.blit(death_text, (screen_width // 2 - death_text.get_width() // 2, 100))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 200))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 300))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 400))
        pygame.display.update()
        # Olayları kontrol et
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # "1" tuşuna basıldığında tekrar başlat
                    return
                elif event.key == pygame.K_2:  # "2" tuşuna basıldığında çık
                    pygame.quit()
                    sys.exit()
        clock.tick(15)  # FPS

# Oyunu çalıştır
main_menu()  # Ana menüye git
main()  # Oyun başlasın
