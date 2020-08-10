import pygame
import lzma, base64
import time, math

BREAKOUT_SPRITES = b'/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj4APdAjRdAAKAjkKoM08lH2uEOo/rcuUOhxiX0ZkQV0GNZp2\
c0laZz/AQYennOMPOt3ciHQEI/1DsSnXBO4tnu5kDdIIMRG7iK4j5kCzxz6/G6r2+4Fuum8hJM/Yeljt2fE/ULrCvXQ734Qijj6m\
bu88jRCGH7tcVrgQMl3GPX8W7fi4RbwhruQSfYKR/bvCAYNKkEv7vRxn5toCsvXAAg19ezKtqLEhFK810/fCKZd2JCmMLrrx1o/N\
UI//+fZaeppOJ5uDZcOHw4qIoz75bxMxSIZUvehGvtNF3qfc1610Er2aCHTgjDcVW1HWxse47+Xf8B+37qbPFwCdJfzuO8Y5qFHD\
QUp6QPJNOHzm3Rx9fZ0CCHm/auvZgup+nVL1bU0vAQ42S0uScdzEyyB5GbnKL4n8Y0tBjCiu7JFo4elvWA9B60zBvlo4FOT/YFZ3\
0/FrUeMOdLUoomUWDZ4cI5shVvOKGmE1qKzFuxo/zTDJSDkyRwuwA1LyRCET8JneWILCGe/vrSpZ4tTPFRoQk6u4vwSl2l4Oc6Re\
Q5se78SG3UzqhjD7El/HH6s1B5MEk4HPp2CS+E8Ax4dCfzPg/cwrkHFcTHFOAjjs59ha7RjAq2wqXBJi2ckizfbalZlxYtzXyYzO\
my85ngyD0b+0Z4YGEIw+xNJ4Up4md6wYUFt/yBWnZiEGImsqxrFp1FF0hdS5uou5c82NXSODYwbEdGXRqW1WAhhZEf/ucMsGRbr3\
qoMwOVNIFxI4aNgD/d5614KloKgAB0ATeBwAAHbYv57HEZ/sCAAAAAARZWg=='

MAP = b'/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj4AFfADddAADuGE1r3b4H/A7syKBXW69az164Q4tMGeDoPiBScQvgano899RG\
ZHePlTQvu2GfNLBsFotLCgAAANaAZ217PTDeAAFT4AIAAADQoZLLscRn+wIAAAAABFla'


class maps:
    class brick:
        def __init__(s, id, index):
            global ZX_WIDTH, ZX_TILE_SIZE

            s.x = index % ZX_WIDTH * ZX_TILE_SIZE
            s.y = int(index / ZX_WIDTH) * ZX_TILE_SIZE
            s.id = id
            s.dead = False

    def __init__(s, lz64_data):
        data = lzma.decompress(base64.b64decode(lz64_data))

        s.bricks = []
        for index in range(11 * ZX_WIDTH):
            id = data[index]
            s.bricks.append(s.brick(id, index))

    def draw(s):
        global SPRITES
        global ZX_SURFACE

        for b in s.bricks:
            if b.dead: continue
            ZX_SURFACE.blit(SPRITES.sprites['b' + str(b.id)], (b.x, b.y))


class spritesSheet:
    def b(s, a):
        return a[1:], int.from_bytes(a[: 1], "big")

    def w(s, a):
        return a[2:], int.from_bytes(a[: 2], "big")

    def d(s, a):
        return a[4:], int.from_bytes(a[: 4], "big")

    def rgb(s, a):
        return a[3:], int.from_bytes(a[: 3], "big")

    def name(s, a):
        sl = int.from_bytes(a[: 1], "big")
        return a[1 + sl:], a[1: sl + 1].decode("utf-8")

    def cr(s, index):
        return [index % s.c * s.cw, int(index / s.c) * s.ch, s.cw, s.ch]

    def __init__(s, lz64_data):
        # decompress data
        data = lzma.decompress(base64.b64decode(lz64_data))

        # get image dimensions
        data, s.c = s.b(data)  # cols
        data, s.r = s.b(data)  # rows
        data, s.cw = s.b(data)  # cell width
        data, s.ch = s.b(data)  # cell height
        s.iw = s.c * s.cw  # image width
        s.ih = s.r * s.ch  # image height

        # get palette length
        data, s.pl = s.b(data)  # palette length

        # get palette
        s.palette = []
        for index in range(s.pl):
            data, irgb = s.rgb(data)
            s.palette.append(irgb)

        # create pygame surface to place spritesheet
        s.surface = pygame.Surface((s.iw, s.ih))
        pa = pygame.PixelArray(s.surface)

        # get image data length in bytes
        idl = s.iw * s.ih

        # extract image data
        for index in range(idl):
            data, pi = s.b(data)  # palette index
            pa[index % s.iw][int(index / s.iw)] = s.palette[pi]
        pa.close()
        del pa

        # make the sprites using the assembly data
        s.sprites = {}
        cell = pygame.Surface((s.cw, s.ch))  # to temp store cell

        while data:
            data, sn = s.name(data)  # sprite name
            data, sw = s.w(data)  # sprite width, if width is zero then it's a copy instruction

            if sw == 0:  # copy instruction?
                data, snc = s.name(data)  # sprite name to copy
                data, at = s.b(data)  # assembly attribute

                # apply attribute 0 = none, 1 = h flip, 2 = v flip, 3 = rot 90, 4 = rot 180, 5 = rot 270
                if at == 0:
                    s.sprites[sn] = s.sprites[snc].copy()
                elif at == 1:
                    s.sprites[sn] = pygame.transform.flip(s.sprites[snc], True, False)
                elif at == 2:
                    s.sprites[sn] = pygame.transform.flip(s.sprites[snc], False, True)
                elif at == 3:
                    s.sprites[sn] = pygame.transform.rotate(s.sprites[snc], -90)
                elif at == 4:
                    s.sprites[sn] = pygame.transform.rotate(s.sprites[snc], -180)
                elif at == 5:
                    s.sprites[sn] = pygame.transform.rotate(s.sprites[snc], -270)
                continue

            data, sh = s.w(data)  # sprite height

            sc = math.ceil(sw / s.cw)  # sprite columns
            sr = math.ceil(sh / s.ch)  # sprite rows
            scc = sc * sr  # sprite cell count
            scc_index = 0

            # create a surface for the sprite
            s.sprites[sn] = pygame.Surface((sw, sh))

            # cycle through assembly instructions
            while scc_index < scc:
                # print(scc_index, scc)
                data, ci = s.w(data)  # cell index
                data, at = s.b(data)  # assembly attribute

                if at < 6:  # single cell placement?
                    # calc x, y coords of cell placement
                    x = scc_index % sc * s.cw
                    y = int(scc_index / sc) * s.ch

                    # get cell image
                    cell.blit(s.surface, (0, 0), s.cr(ci))

                    # apply attribute 0 = none, 1 = h flip, 2 = v flip, 3 = rot 90, 4 = rot 180, 5 = rot 270
                    if at == 0:
                        s.sprites[sn].blit(cell, (x, y))
                    elif at == 1:
                        s.sprites[sn].blit(pygame.transform.flip(cell, True, False), (x, y))
                    elif at == 2:
                        s.sprites[sn].blit(pygame.transform.flip(cell, False, True), (x, y))
                    elif at == 3:
                        s.sprites[sn].blit(pygame.transform.rotate(cell, -90), (x, y))
                    elif at == 4:
                        s.sprites[sn].blit(pygame.transform.rotate(cell, -180), (x, y))
                    elif at == 5:
                        s.sprites[sn].blit(pygame.transform.rotate(cell, -270), (x, y))
                    scc_index += 1
                else:
                    data, r = s.w(data)  # get range count

                    for index in range(r):
                        # get x, y coords of cell placement
                        x = (scc_index + index) % sc * s.cw
                        y = int((scc_index + index) / sc) * s.ch

                        # get cell image
                        cell.blit(s.surface, (0, 0), s.cr(ci))

                        # apply attribute 6 = none, 7 = h flip, 8 = v flip, 9 = rot 90, 10 = rot 180, 11 = rot 270
                        if at == 6 or at == 12 or at == 18:
                            s.sprites[sn].blit(cell, (x, y))
                        elif at == 7 or at == 13 or at == 19:
                            s.sprites[sn].blit(pygame.transform.flip(cell, True, False), (x, y))
                        elif at == 8 or at == 14 or at == 20:
                            s.sprites[sn].blit(pygame.transform.flip(cell, False, True), (x, y))
                        elif at == 9 or at == 15 or at == 21:
                            s.sprites[sn].blit(pygame.transform.rotate(cell, -90), (x, y))
                        elif at == 10 or at == 16 or at == 22:
                            s.sprites[sn].blit(pygame.transform.rotate(cell, -180), (x, y))
                        elif at == 11 or at == 17 or at == 23:
                            s.sprites[sn].blit(pygame.transform.rotate(cell, -270), (x, y))

                        # increment/decrement the sprite sheet cell index
                        if at > 11 and at < 18:
                            ci += 1
                        elif at > 17:
                            ci -= 1

                    scc_index += r


SCALE = 3
ZX_TILE_SIZE = 8
ZX_WIDTH = 32
ZX_HEIGHT = 24

W, H = ZX_WIDTH * ZX_TILE_SIZE, ZX_HEIGHT * ZX_TILE_SIZE
HW, HH = int(W / 2), int(H / 2)
FPS = 60

pygame.init()
DS = pygame.display.set_mode((W * SCALE, H * SCALE))
ZX_SURFACE = pygame.Surface((W, H))
CLOCK = pygame.time.Clock()

SPRITES = spritesSheet(BREAKOUT_SPRITES)
BRICKS = maps(MAP)

BAT_WIDTH = 6 * ZX_TILE_SIZE
BAT_WIDTH_HALF = int(BAT_WIDTH / 2)
BAT_HEIGHT = ZX_TILE_SIZE
batX = pygame.mouse.get_pos()[0] - BAT_WIDTH_HALF
batY = H - BAT_HEIGHT

BALL_RADIUS = int(ZX_TILE_SIZE / 2)
BALL_COLLISION_RADIUS = BALL_RADIUS - 1
ballX, ballY = HW, H - BAT_HEIGHT - BALL_RADIUS
ballVX, ballVY = 0, -1

BALL_MAX_VX = 1
BALL_VX_CHUNK = BALL_MAX_VX / BAT_WIDTH_HALF

start = False

while True:
    e = pygame.event.get()
    if pygame.key.get_pressed()[pygame.K_ESCAPE]: break
    if pygame.mouse.get_pressed()[0]: start = True

    batX = pygame.mouse.get_pos()[0] / SCALE - BAT_WIDTH_HALF
    if batX <= 0:
        batX = 0
    elif batX + BAT_WIDTH >= W:
        batX = W - BAT_WIDTH

    if not start:
        ballX = batX + BAT_WIDTH_HALF

    if ballY + BALL_RADIUS <= batY and ballY + BALL_RADIUS + ballVY >= batY:
        if ballX >= batX and ballX <= batX + BAT_WIDTH:
            ballVY = -ballVY

            ballHitX = ballX - (batX + BAT_WIDTH_HALF)
            ballVX = ballHitX * BALL_VX_CHUNK

    bx1 = ballX - BALL_COLLISION_RADIUS
    by1 = ballY - BALL_COLLISION_RADIUS
    bx2 = ballX + BALL_COLLISION_RADIUS
    by2 = ballY + BALL_COLLISION_RADIUS

    for b in BRICKS.bricks:
        if b.dead: continue
        if ((bx2 <= b.x and bx2 + ballVX >= b.x) or (
                bx1 >= b.x + ZX_TILE_SIZE and bx1 + ballVX <= b.x + ZX_TILE_SIZE)) and not (
                by2 < b.y or by1 > b.y + ZX_TILE_SIZE):
            ballVX = -ballVX
            b.dead = True
        if ((by2 <= b.y and by2 + ballVY >= b.y) or (
                by1 >= b.y + ZX_TILE_SIZE and by1 + ballVY <= b.y + ZX_TILE_SIZE)) and not (
                bx2 < b.x or bx1 > b.x + ZX_TILE_SIZE):
            ballVY = -ballVY
            b.dead = True

    if start:
        ballX += ballVX
        ballY += ballVY

    if ballY >= H - BALL_RADIUS:
        break
    elif ballY <= BALL_RADIUS:
        ballVY = -ballVY

    if ballX >= W - BALL_RADIUS or ballX <= BALL_RADIUS:
        ballVX = -ballVX

    ZX_SURFACE.fill([0, 0, 0])
    ZX_SURFACE.blit(SPRITES.sprites['bat'], (int(batX), int(batY)))
    ZX_SURFACE.blit(SPRITES.sprites['ball'], (int(ballX - BALL_RADIUS), int(ballY - BALL_RADIUS)))

    BRICKS.draw()

    DS.blit(pygame.transform.scale(ZX_SURFACE, (W * SCALE, H * SCALE)), (0, 0))

    pygame.display.update()
    CLOCK.tick(FPS)
pygame.quit()