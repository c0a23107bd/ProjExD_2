import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def game_over_screen(screen: pg.Surface, kk_img: pg.Surface):
    """
    ゲームオーバー画面を表示する関数。
    Args:
        screen (pg.Surface): ゲーム画面
        kk_img (pg.Surface): 泣いているこうかとんの画像
    """
    # 画面をブラックアウト
    screen.fill((0, 0, 0))
    
    # 半透明の黒いオーバーレイを描画
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)  # 半透明度の設定
    screen.blit(overlay, (0, 0))
    
    # "Game Over" テキストを表示
    font = pg.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))  # 赤色のテキスト
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    # 泣いているこうかとんの画像を表示
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(kk_img, (WIDTH // 2 - kk_img.get_width() // 2, HEIGHT // 2 + 50))
    # 画面を更新して5秒間停止
    pg.display.update()
    time.sleep(5)

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:

    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bomb_radius = 10
    bomb_color = (225, 0, 0)
    bb_img = pg.Surface((bomb_radius * 2, bomb_radius * 2),pg.SRCALPHA)
    pg.draw.circle(bb_img, bomb_color, (bomb_radius, bomb_radius), bomb_radius)

    bb_rct = bb_img.get_rect()
    bb_rct.x = random.randint(0, WIDTH - bb_rct.width)
    bb_rct.y = random.randint(0, HEIGHT - bb_rct.height)
    
    vx, vy = +5, -5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            # こうかとんと爆弾が重なっていたら
            print("GameOver")
            game_over_screen(screen, kk_img)
            return

    
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        # kk_rct.move_ip(sum_mv)
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        

        bb_rct.move_ip((vx,vy))
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
