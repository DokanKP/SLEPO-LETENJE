import pygame as pg
import random
pg.init()
SIRINA = 1280
VISINA = 720
prozor = pg.display.set_mode([SIRINA, VISINA])
tekst = pg.font.Font('04B_30__.TTF', 30)
restart = pg.font.Font('04B_30__.TTF', 70)

FPS = 60
vreme = pg.time.Clock()
run = True

poeni = 0
mapa = True
mapskiprav = []
prav_sirina = 5
uprav = SIRINA//prav_sirina
razmak = 10

naj = 0
status = True
letenje = False
vbrzina = 0
gravitacija = 0.3
brzmape = 3
mis = pg.transform.scale(pg.image.load('mis.png'), (60, 60))

while run:
    prozor.fill('gray5')
    vreme.tick(FPS)

    if mapa:
        najvis = random.randint(0, VISINA//3*2)
        igracx = 150
        igracy = (najvis+VISINA)//2
        for i in range(uprav):
            najvis = random.randint(najvis - razmak, najvis + razmak)
            if najvis < 0:
                najvis = 0
            elif najvis > VISINA//3*2:
                najvis = VISINA//3*2
            gorprav = pg.draw.rect(prozor, 'white', [i * prav_sirina, 0, prav_sirina, najvis])
            donjprav = pg.draw.rect(prozor, 'white', [i * prav_sirina, najvis + VISINA//3*2, prav_sirina, VISINA-najvis-VISINA//3*2])
            mapskiprav.append(gorprav)
            mapskiprav.append(donjprav)
        mapa = False
    
    for i in range(len(mapskiprav)):
        pg.draw.rect(prozor, 'chocolate4', mapskiprav[i])
    
    igrac = pg.draw.circle(prozor, 'gray5', (igracx, igracy), 15)
    prozor.blit(mis, (igracx-30, igracy-35))
    okvir = pg.draw.rect(prozor, 'darkgoldenrod1', [0, 0, SIRINA, VISINA], 5)
    gornjihit = pg.draw.rect(prozor, 'darkgoldenrod1', [0, 0, SIRINA, 1])
    donjihit = pg.draw.rect(prozor, 'darkgoldenrod1', [0, VISINA-1, SIRINA, 1])

    if status:
        if letenje:
            vbrzina += gravitacija
        else:
            vbrzina -= gravitacija
        igracy -= vbrzina

        for i in range(len(mapskiprav)):
            mapskiprav[i] = (mapskiprav[i][0] - brzmape, mapskiprav[i][1], prav_sirina, mapskiprav[i][3])
            if mapskiprav[i][0] + prav_sirina < 0:
                mapskiprav.pop(1)
                mapskiprav.pop(0)
                najvis = random.randint(mapskiprav[-2][3] - razmak, mapskiprav[-2][3] + razmak)
                if najvis < 0:
                    najvis = 0
                elif najvis > VISINA//3*2:
                    najvis = VISINA//3*2
                mapskiprav.append((mapskiprav[-2][0] + prav_sirina, 0, prav_sirina, najvis))
                mapskiprav.append((mapskiprav[-2][0] + prav_sirina, najvis + VISINA//3*2, prav_sirina, VISINA))
                poeni += 1

    for i in range(len(mapskiprav)):
        if igrac.colliderect(mapskiprav[i]):
            status = False
        if igrac.colliderect(gornjihit):
            status = False
        if igrac.colliderect(donjihit):
            status = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                letenje = True
            if event.key == pg.K_RETURN:
                if not status:
                    mapa = True
                    mapskiprav = []
                    status = True
                    vbrzina = 0
                    brzmape = 5
                    if poeni > naj:
                        naj = poeni
                    poeni = 0
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                letenje = False
    
    brzmape = 7 + poeni//300
    razmak = 10 + poeni // 500

    prozor.blit(tekst.render(f'Poeni: {poeni}', True, 'white'), (20, 15))
    prozor.blit(tekst.render(f'Najbolje: {naj}', True, 'darkgoldenrod1'), (20, 675))
    if not status:
        prozor.blit(restart.render('Enter za Restart', True, 'white'), (165, 330))
    pg.display.flip()

pg.quit()