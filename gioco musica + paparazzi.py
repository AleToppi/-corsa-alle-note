# Importazione dei moduli necessari di Pygame Zero
from pgzero.actor import Actor
from pgzero.clock import clock
from pgzero.keyboard import keyboard
import pgzrun
from random import randint

# ===== VARIABILI STATO =====
punteggio = 0
game_over = False
tempo_rimasto = 0
mostra_flash = False
messaggio_paparazzi = ""

# ===== FUNZIONI DI GIOCO =====

def draw():
    screen.blit("sfondo_bn", (0, 0))
    
    nota.draw()
    tony.draw()
    paparazzi.draw()

    screen.draw.text(
        "Note imparate: " + str(punteggio),
        color="black",
        topleft=(10, 10),
        shadow=(1, 1),
        scolor="#FFFFFF",
        fontsize=40,
    )

    # Mostra immagine flash nel punto di impatto
    if mostra_flash:
        flash_img.draw()

    if game_over:
        if punteggio > VITTORIA_PUNTEGGIO:
            screen.blit("vittoria", (0, 0))
            screen.draw.text(
                "Daje Tony, questo pezzo spacca!\nNote messe insieme: " + str(punteggio),
                center=(WIDTH / 2, HEIGHT / 2),
                fontsize=60,
                color="white",
            )
            tony.image = "tony2"
            tony.pos = 400, 200
            tony.draw()
        else:
            screen.draw.text(
                "Peccato!\nDevi esercitarti di più.\nNote messe insieme: " + str(punteggio),
                midtop=(WIDTH / 2, 10),
                fontsize=40,
                color="red",
            )

        screen.draw.text(
            "Premi SPAZIO per ricominciare",
            center=(WIDTH / 2, HEIGHT - 100),
            fontsize=40,
            color="white",
        )


def piazza_nota():
    nota.x = randint(70, WIDTH - 70)
    nota.y = randint(70, HEIGHT - 70)


def piazza_paparazzi():
    paparazzi.x = randint(100, WIDTH - 100)
    paparazzi.y = randint(100, HEIGHT - 100)


def tempo_scaduto():
    global game_over
    game_over = True


def mostra_collisione_paparazzi():
    global mostra_flash

    # Calcolo posizione dell'impatto tra Tony e paparazzi
    flash_x = (tony.x + paparazzi.x) / 2
    flash_y = (tony.y + paparazzi.y) / 2
    flash_img.pos = (flash_x, flash_y)

    mostra_flash = True

    # Nascondi flash dopo 0.5 secondi
    clock.schedule_unique(nascondi_flash, 0.5)


def nascondi_flash():
    global mostra_flash
    mostra_flash = False

    # sposta il flash fuori dallo schermo
    flash_img.pos = (-100, -100)


def reset_gioco():
    global punteggio, game_over, tempo_rimasto
    punteggio = 0
    game_over = False
    tempo_rimasto = DURATA_GIOCO

    tony.pos = (100, 100)
    tony.image = "tony"

    piazza_nota()
    piazza_paparazzi()

    paparazzi.vx = 8
    paparazzi.vy = 7

    clock.unschedule(tempo_scaduto)
    clock.schedule(tempo_scaduto, tempo_rimasto)


def on_key_down(key):
    if game_over and key == keys.SPACE:
        reset_gioco()


def penalita_paparazzi():
    global tempo_rimasto
    tempo_rimasto -= 4
    if tempo_rimasto < 0:
        tempo_rimasto = 0

    clock.unschedule(tempo_scaduto)
    clock.schedule(tempo_scaduto, tempo_rimasto)


def update():
    global punteggio

    if not game_over:

        # Movimento Tony
        if keyboard.left:
            tony.x -= 6
        if keyboard.right:
            tony.x += 6
        if keyboard.up:
            tony.y -= 6
        if keyboard.down:
            tony.y += 6

        # Movimento Paparazzi
        paparazzi.x += paparazzi.vx
        paparazzi.y += paparazzi.vy

        # Rimbalzo sui bordi
        if paparazzi.left < 0 or paparazzi.right > WIDTH:
            paparazzi.vx = -paparazzi.vx
        if paparazzi.top < 0 or paparazzi.bottom > HEIGHT:
            paparazzi.vy = -paparazzi.vy

        # Collisione con nota
        if tony.colliderect(nota):
            punteggio += 1
            piazza_nota()

        # Collisione con paparazzi
        if tony.colliderect(paparazzi):
            penalita_paparazzi()
            piazza_paparazzi()
            mostra_collisione_paparazzi()


# ===== CONFIGURAZIONE INIZIALE =====

TITLE = "Tony alla ricerca... della musica"
WIDTH = 800
HEIGHT = 600

DURATA_GIOCO = 44
VITTORIA_PUNTEGGIO = 25

# Tony
tony = Actor("tony")
tony.pos = (100, 100)

# Nota
nota = Actor("nota musicale")
piazza_nota()

# Paparazzi
paparazzi = Actor("paparazzi")
piazza_paparazzi()
paparazzi.vx = 8
paparazzi.vy = 7

# Immagine flash da mostrare all'impatto
flash_img = Actor("flash")
flash_img.pos = (-100, -100)   # nascosto all'inizio

clock.schedule(tempo_scaduto, DURATA_GIOCO)

pgzrun.go()
