import math
import random
import sys
import pygame

pygame.init()

# ============================================================
# FLAPPY BIRD - MERDAN EDITION
# Tek dosya / Pygame / Telefon için optimize
# ============================================================

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Flappy Bird - Merdan Edition")

clock = pygame.time.Clock()
FPS = 60

# ------------------------------------------------------------
# RENKLER
# ------------------------------------------------------------
SKY_DAY = (105, 190, 235)
SKY_NIGHT = (22, 32, 65)
SUN = (255, 225, 95)
MOON = (245, 245, 220)

GROUND = (222, 210, 145)
GROUND_TOP = (85, 180, 55)
GROUND_DARK = (165, 135, 80)

PIPE = (85, 190, 55)
PIPE_LIGHT = (120, 215, 70)
PIPE_DARK = (45, 125, 40)
BLACK = (25, 25, 25)
WHITE = (255, 255, 255)

# ------------------------------------------------------------
# ZEMİN
# ------------------------------------------------------------
ground_height = int(HEIGHT * 0.15)
ground_y = HEIGHT - ground_height
ground_offset = 0.0

# ------------------------------------------------------------
# KUŞ
# ------------------------------------------------------------
bird_size = max(52, int(HEIGHT * 0.070))
bird_x = int(WIDTH * 0.23)
bird_y = HEIGHT * 0.48

bird_velocity = 0.0

# Daha kontrollü fizik
GRAVITY = HEIGHT * 0.00062
FLAP_POWER = -HEIGHT * 0.010
MAX_FALL_SPEED = HEIGHT * 0.020

bird_angle = 0.0

# Çarpışma yarıçapı görselden küçük
collision_radius = bird_size * 0.27

# ------------------------------------------------------------
# BORULAR
# ------------------------------------------------------------
pipe_width = max(65, int(WIDTH * 0.095))
pipe_gap = int(HEIGHT * 0.34)

PIPE_SPEED = WIDTH * 0.0047
pipe_timer = 0.0
PIPE_INTERVAL = 1.65

pipes = []

# ------------------------------------------------------------
# OYUN DURUMU
# ------------------------------------------------------------
score = 0
high_score = 0

started = False
game_over = False
paused = False
night_mode = False

# ------------------------------------------------------------
# FONTLAR
# ------------------------------------------------------------
font_score = pygame.font.Font(
    None, max(36, int(HEIGHT * 0.055))
)

font_big = pygame.font.Font(
    None, max(50, int(HEIGHT * 0.075))
)

font_small = pygame.font.Font(
    None, max(24, int(HEIGHT * 0.035))
)

# ------------------------------------------------------------
# KUŞ GÖRSELİ
# Burada senin önceki kodundaki çizilmiş karakteri koruyorum.
# Harici PNG gerektirmez.
# ------------------------------------------------------------
bird_surface = pygame.Surface(
    (bird_size, bird_size),
    pygame.SRCALPHA
)

s = bird_size

SKIN = (235, 204, 180)
HAIR = (30, 30, 30)
SHIRT = (15, 15, 15)
SHIRT_WHITE = (245, 245, 245)
EYE = (80, 80, 80)

pygame.draw.rect(
    bird_surface,
    SHIRT_WHITE,
    (
        int(s * 0.10),
        int(s * 0.65),
        int(s * 0.80),
        int(s * 0.35)
    )
)

pygame.draw.rect(
    bird_surface,
    SHIRT,
    (
        int(s * 0.25),
        int(s * 0.55),
        int(s * 0.50),
        int(s * 0.45)
    )
)

pygame.draw.rect(
    bird_surface,
    SKIN,
    (
        int(s * 0.30),
        int(s * 0.30),
        int(s * 0.40),
        int(s * 0.35)
    )
)

pygame.draw.rect(
    bird_surface,
    EYE,
    (
        int(s * 0.38),
        int(s * 0.42),
        int(s * 0.08),
        int(s * 0.12)
    )
)

pygame.draw.rect(
    bird_surface,
    EYE,
    (
        int(s * 0.54),
        int(s * 0.42),
        int(s * 0.08),
        int(s * 0.12)
    )
)

pygame.draw.rect(
    bird_surface,
    HAIR,
    (
        int(s * 0.25),
        int(s * 0.15),
        int(s * 0.50),
        int(s * 0.22)
    )
)

pygame.draw.rect(
    bird_surface,
    HAIR,
    (
        int(s * 0.20),
        int(s * 0.25),
        int(s * 0.12),
        int(s * 0.25)
    )
)

pygame.draw.rect(
    bird_surface,
    HAIR,
    (
        int(s * 0.68),
        int(s * 0.25),
        int(s * 0.12),
        int(s * 0.25)
    )
)

pygame.draw.rect(
    bird_surface,
    HAIR,
    (
        int(s * 0.35),
        int(s * 0.08),
        int(s * 0.30),
        int(s * 0.10)
    )
)

# Yuvarlak maske
bird_mask = pygame.Surface(
    (bird_size, bird_size),
    pygame.SRCALPHA
)

pygame.draw.circle(
    bird_mask,
    (255, 255, 255, 255),
    (bird_size // 2, bird_size // 2),
    bird_size // 2
)

# Alfa kanalını maskeyle çarp
for y in range(bird_size):
    for x in range(bird_size):
        pixel = bird_surface.get_at((x, y))
        mask = bird_mask.get_at((x, y))

        bird_surface.set_at(
            (x, y),
            (
                pixel.r,
                pixel.g,
                pixel.b,
                pixel.a * mask.a // 255
            )
        )

pygame.draw.circle(
    bird_surface,
    WHITE,
    (bird_size // 2, bird_size // 2),
    bird_size // 2 - 1,
    2
)

# Önceden hazırlanmış dönüş kareleri
bird_frames = {}

for angle in range(-30, 31, 5):
    bird_frames[angle] = pygame.transform.rotate(
        bird_surface,
        angle
    )

# ------------------------------------------------------------
# BULUTLAR
# ------------------------------------------------------------
clouds = []

for _ in range(5):
    clouds.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(
            int(HEIGHT * 0.06),
            int(HEIGHT * 0.35)
        ),
        "size": random.randint(
            int(HEIGHT * 0.035),
            int(HEIGHT * 0.075)
        )
    })

# ------------------------------------------------------------
# BİNALAR
# ------------------------------------------------------------
buildings = []

x = 0

while x < WIDTH + 300:

    w = random.randint(
        int(WIDTH * 0.06),
        int(WIDTH * 0.13)
    )

    h = random.randint(
        int(HEIGHT * 0.12),
        int(HEIGHT * 0.35)
    )

    buildings.append({
        "x": x,
        "width": w,
        "height": h
    })

    x += w + random.randint(8, 25)

# ------------------------------------------------------------
# SKOR ÖNBELLEĞİ
# ------------------------------------------------------------
last_score = -1
score_surface = None
score_shadow = None


def update_score_text():

    global last_score
    global score_surface
    global score_shadow

    if score != last_score:

        last_score = score

        text = str(score)

        score_surface = font_score.render(
            text,
            True,
            WHITE
        )

        score_shadow = font_score.render(
            text,
            True,
            BLACK
        )


# ------------------------------------------------------------
# BORU OLUŞTUR
# ------------------------------------------------------------
def create_pipe():

    # Boru merkezinin güvenli aralığı
    min_center = int(HEIGHT * 0.25)
    max_center = int(HEIGHT * 0.62)

    center = random.randint(
        min_center,
        max_center
    )

    top_height = center - pipe_gap // 2
    bottom_y = center + pipe_gap // 2

    top = pygame.Rect(
        WIDTH,
        0,
        pipe_width,
        top_height
    )

    bottom = pygame.Rect(
        WIDTH,
        bottom_y,
        pipe_width,
        ground_y - bottom_y
    )

    return {
        "top": top,
        "bottom": bottom,
        "scored": False
    }


# ------------------------------------------------------------
# BORU ÇİZ
# ------------------------------------------------------------
def draw_pipe(rect, is_top):

    pygame.draw.rect(
        screen,
        PIPE,
        rect
    )

    # Işık şeridi
    pygame.draw.rect(
        screen,
        PIPE_LIGHT,
        (
            rect.x + int(pipe_width * 0.10),
            rect.y,
            int(pipe_width * 0.18),
            rect.height
        )
    )

    # Koyu kenar
    pygame.draw.rect(
        screen,
        PIPE_DARK,
        (
            rect.right - int(pipe_width * 0.18),
            rect.y,
            int(pipe_width * 0.18),
            rect.height
        )
    )

    cap_height = max(
        20,
        int(HEIGHT * 0.032)
    )

    cap = pygame.Rect(
        rect.x - int(pipe_width * 0.07),
        rect.bottom - cap_height
        if is_top
        else rect.top,
        int(pipe_width * 1.14),
        cap_height
    )

    pygame.draw.rect(
        screen,
        PIPE_LIGHT,
        cap
    )

    pygame.draw.rect(
        screen,
        PIPE_DARK,
        cap,
        2
    )


# ------------------------------------------------------------
# DAİRE - DİKDÖRTGEN ÇARPIŞMASI
# ------------------------------------------------------------
def circle_hits_rect(cx, cy, radius, rect):

    closest_x = max(
        rect.left,
        min(cx, rect.right)
    )

    closest_y = max(
        rect.top,
        min(cy, rect.bottom)
    )

    dx = cx - closest_x
    dy = cy - closest_y

    return (
        dx * dx +
        dy * dy
    ) < radius * radius


# ------------------------------------------------------------
# ÇARPIŞMA
# ------------------------------------------------------------
def check_collision():

    cx = bird_x
    cy = bird_y

    for pipe in pipes:

        if circle_hits_rect(
            cx,
            cy,
            collision_radius,
            pipe["top"]
        ):
            return True

        if circle_hits_rect(
            cx,
            cy,
            collision_radius,
            pipe["bottom"]
        ):
            return True

    if (
        cy - collision_radius <= 0
        or
        cy + collision_radius >= ground_y
    ):
        return True

    return False


# ------------------------------------------------------------
# RESET
# ------------------------------------------------------------
def reset_game():

    global bird_y
    global bird_velocity
    global score
    global started
    global game_over
    global paused
    global pipe_timer
    global bird_angle
    global last_score

    bird_y = HEIGHT * 0.48
    bird_velocity = 0.0

    score = 0
    last_score = -1

    started = False
    game_over = False
    paused = False

    pipe_timer = 0.0
    bird_angle = 0.0

    pipes.clear()


# ------------------------------------------------------------
# FLAP
# ------------------------------------------------------------
def flap():

    global bird_velocity
    global started

    if game_over:

        reset_game()
        started = True

    elif not paused:

        started = True
        bird_velocity = FLAP_POWER


# ------------------------------------------------------------
# OYUN DÖNGÜSÜ
# ------------------------------------------------------------
running = True

while running:

    dt = clock.tick(FPS) / 1000.0

    # FPS bağımsız zaman
    dt = min(dt, 0.033)

    # --------------------------------------------------------
    # EVENTLER
    # --------------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            elif event.key == pygame.K_SPACE:

                flap()

            elif event.key == pygame.K_p:

                if started and not game_over:
                    paused = not paused

            elif event.key == pygame.K_n:

                night_mode = not night_mode

        elif event.type == pygame.MOUSEBUTTONDOWN:

            flap()

    # --------------------------------------------------------
    # GÜNCELLEME
    # --------------------------------------------------------
    if started and not game_over and not paused:

        # Fizik
        bird_velocity += GRAVITY * dt * 60

        bird_velocity = min(
            bird_velocity,
            MAX_FALL_SPEED
        )

        bird_y += bird_velocity * dt * 60

        # Boru zamanlayıcı
        pipe_timer += dt

        if pipe_timer >= PIPE_INTERVAL:

            pipe_timer = 0.0
            pipes.append(
                create_pipe()
            )

        # Borular
        for pipe in pipes:

            pipe["top"].x -= int(
                PIPE_SPEED * dt * 60
            )

            pipe["bottom"].x -= int(
                PIPE_SPEED * dt * 60
            )

            # Gerçek skor:
            # kuş borunun sağından geçtiğinde +1
            if (
                not pipe["scored"]
                and pipe["top"].right < bird_x
            ):

                pipe["scored"] = True
                score += 1

                if score > high_score:
                    high_score = score

        # Eski boruları temizle
        pipes[:] = [
            p for p in pipes
            if p["top"].right > -100
        ]

        # Çarpışma
        if check_collision():

            game_over = True

    # --------------------------------------------------------
    # KUŞ AÇISI
    # --------------------------------------------------------
    target_angle = -bird_velocity * 2.2

    target_angle = max(
        -30,
        min(30, target_angle)
    )

    bird_angle += (
        target_angle - bird_angle
    ) * 0.12

    frame_angle = int(
        round(bird_angle / 5) * 5
    )

    frame_angle = max(
        -30,
        min(30, frame_angle)
    )

    # --------------------------------------------------------
    # ARKA PLAN
    # --------------------------------------------------------
    if night_mode:

        screen.fill(SKY_NIGHT)

        pygame.draw.circle(
            screen,
            MOON,
            (
                int(WIDTH * 0.82),
                int(HEIGHT * 0.15)
            ),
            int(HEIGHT * 0.045)
        )

    else:

        screen.fill(SKY_DAY)

        pygame.draw.circle(
            screen,
            SUN,
            (
                int(WIDTH * 0.82),
                int(HEIGHT * 0.14)
            ),
            int(HEIGHT * 0.045)
        )

    # --------------------------------------------------------
    # BULUTLAR
    # --------------------------------------------------------
    for cloud in clouds:

        if started and not paused:

            cloud["x"] -= WIDTH * 0.00025 * dt * 60

            if cloud["x"] < -200:

                cloud["x"] = WIDTH + 100

        x = int(cloud["x"])
        y = int(cloud["y"])
        size = cloud["size"]

        pygame.draw.circle(
            screen,
            WHITE,
            (x, y),
            int(size * 0.45)
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (
                x + int(size * 0.40),
                y - int(size * 0.20)
            ),
            int(size * 0.38)
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (
                x + int(size * 0.72),
                y
            ),
            int(size * 0.40)
        )

    # --------------------------------------------------------
    # BİNALAR
    # --------------------------------------------------------
    for building in buildings:

        if started and not paused:

            building["x"] -= (
                PIPE_SPEED *
                0.32 *
                dt *
                60
            )

        rect = pygame.Rect(
            int(building["x"]),
            ground_y - building["height"],
            building["width"],
            building["height"]
        )

        pygame.draw.rect(
            screen,
            (92, 168, 198),
            rect
        )

    # Sonsuz bina döngüsü
    if buildings:

        if buildings[0]["x"] + buildings[0]["width"] < -10:

            buildings.pop(0)

            last = buildings[-1]

            new_w = random.randint(
                int(WIDTH * 0.06),
                int(WIDTH * 0.13)
            )

            new_h = random.randint(
                int(HEIGHT * 0.12),
                int(HEIGHT * 0.35)
            )

            buildings.append({
                "x": (
                    last["x"] +
                    last["width"] +
                    random.randint(8, 25)
                ),
                "width": new_w,
                "height": new_h
            })

    # --------------------------------------------------------
    # BORULAR
    # --------------------------------------------------------
    for pipe in pipes:

        draw_pipe(
            pipe["top"],
            True
        )

        draw_pipe(
            pipe["bottom"],
            False
        )

    # --------------------------------------------------------
    # ZEMİN
    # --------------------------------------------------------
    if started and not paused:

        ground_offset -= (
            PIPE_SPEED *
            0.8 *
            dt *
            60
        )

        ground_offset %= 40

    pygame.draw.rect(
        screen,
        GROUND,
        (
            0,
            ground_y,
            WIDTH,
            ground_height
        )
    )

    pygame.draw.rect(
        screen,
        GROUND_TOP,
        (
            0,
            ground_y,
            WIDTH,
            max(8, int(HEIGHT * 0.015))
        )
    )

    for x in range(
        -40,
        WIDTH + 40,
        40
    ):

        pygame.draw.line(
            screen,
            GROUND_DARK,
            (
                int(x + ground_offset),
                ground_y + int(HEIGHT * 0.025)
            ),
            (
                int(x + ground_offset - 15),
                HEIGHT
            ),
            3
        )

    # --------------------------------------------------------
    # KUŞ
    # --------------------------------------------------------
    bird_image = bird_frames[
        frame_angle
    ]

    bird_rect = bird_image.get_rect(
        center=(
            bird_x,
            int(bird_y)
        )
    )

    screen.blit(
        bird_image,
        bird_rect
    )

    # --------------------------------------------------------
    # SKOR
    # --------------------------------------------------------
    update_score_text()

    score_rect = score_surface.get_rect(
        center=(
            WIDTH // 2,
            int(HEIGHT * 0.08)
        )
    )

    screen.blit(
        score_shadow,
        (
            score_rect.x + 3,
            score_rect.y + 3
        )
    )

    screen.blit(
        score_surface,
        score_rect
    )

    # --------------------------------------------------------
    # BAŞLANGIÇ
    # --------------------------------------------------------
    if not started and not game_over:

        title = font_big.render(
            "FLAPPY BIRD",
            True,
            WHITE
        )

        title_rect = title.get_rect(
            center=(
                WIDTH // 2,
                int(HEIGHT * 0.38)
            )
        )

        screen.blit(
            title,
            title_rect
        )

        hint = font_small.render(
            "DOKUN / SPACE",
            True,
            WHITE
        )

        hint_rect = hint.get_rect(
            center=(
                WIDTH // 2,
                int(HEIGHT * 0.55)
            )
        )

        screen.blit(
            hint,
            hint_rect
        )

    # --------------------------------------------------------
    # PAUSE
    # --------------------------------------------------------
    if paused:

        pause = font_big.render(
            "DURAKLATILDI",
            True,
            WHITE
        )

        pause_rect = pause.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2
            )
        )

        screen.blit(
            pause,
            pause_rect
        )

    # --------------------------------------------------------
    # GAME OVER
    # --------------------------------------------------------
    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 120)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        over = font_big.render(
            "OYUN BITTI",
            True,
            WHITE
        )

        over_rect = over.get_rect(
            center=(
                WIDTH // 2,
                int(HEIGHT * 0.38)
            )
        )

        screen.blit(
            over,
            over_rect
        )

        final = font_small.render(
            "Skor: " + str(score),
            True,
            WHITE
        )

        final_rect = final.get_rect(
            center=(
                WIDTH // 2,
                int(HEIGHT * 0.49)
            )
        )

        screen.blit(
            final,
            final_rect
        )

        best = font_small.render(
            "Rekor: " + str(high_score),
            True,
            WHITE
        )

        best_rect = best.get_rect(
            center=(
                WIDTH // 2,
                int(HEIGHT * 0.55)
            )
        )

        screen.blit(
            best,
            best_rect
        )

        restart = font_small.render(
            "Tekrar oynamak icin dokun",
            True,
            WHITE
        )

        restart_rect = restart.get_rect(
            center=(
                WIDTH // 2,
                int(HEIGHT * 0.65)
            )
        )

        screen.blit(
            restart,
            restart_rect
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
