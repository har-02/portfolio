import pygame #ゲームを作るライブラリ
import sys #標準ライブラリ
import time

pygame.init() #pygame使用時に必須の初期化処理

#ウィンドウサイズとタイトル設定
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("友だちと待ち合わせ！カメさんのジャンプゲーム")

#文字の表示
font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 80) #（デフォルト,文字の大きさ）
midium_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 30)
small_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 25)
gameover_text = None

#ゲームの状態
state = "play" #play / gameover / clear

hello_text = None
hello_start_time = None
HELLO_DURATION = 1000 #1000ミリ秒

#スタートボタン(x,y,幅,高さ)
button_rect = pygame.Rect(300, 240, 170, 70)

#リトライボタン
retry_button = pygame.Rect(200, 250, 170, 70)

#終了ボタン
quit_button = pygame.Rect(400, 250, 170, 70)

#地面
ground = pygame.Rect(0, 350, 800, 50)

clear_text = None

#ゲームオーバーフラグ
game_over = False

clock = pygame.time.Clock() #ループの速さ調整

#画像読み込み
player_img = pygame.image.load("player.png").convert_alpha()
enemy_img = pygame.image.load("enemy.png").convert_alpha()
friend_img = pygame.image.load("friend.png").convert_alpha()
back_img = pygame.image.load("blue.png").convert_alpha()
back_img_gameover = pygame.image.load("pale_blue.png").convert_alpha()
back_img_gameclear = pygame.image.load("pink.png").convert_alpha()

#背景画像
back_img = pygame.transform.scale(back_img, (800, 400))
back_img_gameover = pygame.transform.scale(back_img_gameover, (800, 400))
back_img_gameclear = pygame.transform.scale(back_img_gameclear, (800, 400))

#プレイヤー作成
player_start = player_img.get_rect(topleft=(100,300))
player = player_img.get_rect(topleft=(100,300))
player_y_speed = 0 #プレイヤー上下速度
player_speed = 1
gravity = 1 #重力（落下速度）
jump_power = -25 #ジャンプ時の上向き速度
on_ground = True #地面にいるかどうかのフラグ

#敵の初期位置＝x=800（右端）
enemy_start = enemy_img.get_rect(topleft=(500,300))
enemy = enemy_img.get_rect(topleft=(800,300))
#enemy = pygame.Rect(800, 300, 50, 50)
enemy_speed = 4 #左に4pxずつ動く

#友達の初期位置
friend_start = friend_img.get_rect(topleft=(700,300))
friend = friend_img.get_rect(topleft=(700,300))
friend_speed = 1

#ゲーム初期化
def reset_game():
    global player, enemy, friend, player_y_speed, on_ground, state
    player.x, player.y = 100, 300
    enemy.x = 800
    friend.x = 700
    player_y_speed = 0
    on_ground = True
    state = "play"

#タイトル画面表示
def title_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #ボタンクリックでタイトル画面終了（ゲーム開始）
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return
        
        #背景
        screen.blit(back_img, (0, 0))

        title_text = midium_font.render("友だちと待ち合わせ！カメさんのジャンプゲーム", True, (0, 0, 0))
        screen.blit(title_text, (40, 30))

        screen.blit(player_img, player_start)

        title_description001 = small_font.render("★緑色カメさんを操作して、ピンク色カメさんに会いに行こう。", True, (0, 0, 0))
        screen.blit(title_description001, (80, 120))
        
        title_description002 = small_font.render("★灰色カメさんにぶつかるとゲームオーバー！", True, (0, 0, 0))
        screen.blit(title_description002, (80, 160))

        screen.blit(enemy_img, enemy_start)

        title_description003 = small_font.render("★スペースキーでジャンプできるよ！", True, (0, 0, 0))
        screen.blit(title_description003, (80, 200))

        screen.blit(friend_img, friend_start)
        
        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 3)
    
        pygame.draw.rect(screen, (0, 200, 0), button_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 3, border_radius = 10)
        start_text = small_font.render("スタート", True, (0, 0, 0))
        screen.blit(start_text, (button_rect.x + 30, button_rect.y + 20))

        pygame.draw.rect(screen, (60,200, 60), ground)

        pygame.display.update()
        clock.tick(60)

title_screen()

while True: #ゲームループ
    for event in pygame.event.get(): #キーボード操作
        if event.type == pygame.QUIT: #ウィンドウ閉じる
            pygame.quit()
            sys.exit()
    
        if state == "play":
            if event.type == pygame.KEYDOWN: #スペースキーでジャンプ
                if event.key == pygame.K_SPACE and on_ground: #地面にいるとジャンプできる
                    player_y_speed = jump_power
                    on_ground = False
    
        if state in["gameover", "clear"]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    reset_game()
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    #プレイヤーのジャンプ処理

    if state == "play":
        player_y_speed += gravity #重力を加える
        player.y += player_y_speed #速度分プレイヤーを動かす

        if player.y >= 300:
            player.y = 300
            player_y_speed = 0
            on_ground = True

        player.x += player_speed

        #敵の移動
        enemy.x -= enemy_speed #敵を左に向かって動かす

        #画面外に敵が出たら右端に戻す
        if enemy.x < -50:
           enemy.x = 800

        #あたり判定 Rect同士が重なったらゲーム終了
        if player.colliderect(enemy):
            state = "gameover"
            #背景
            #screen.blit(back_img_gameover, (0, 0))
            #game_over = True
            gameover_text = font.render("Game Over",True, (100,0,0))

    if player.colliderect(friend):
        state = "clear"
        clear_text = font.render("Game Clear!", True, (0,0,0))

    if state == "play":
        screen.blit(back_img, (0,0))
        #screen.blit(clear_text, (200,100))
        screen.blit(player_img, player)
        screen.blit(enemy_img, enemy)
        screen.blit(friend_img, friend)
        pygame.draw.rect(screen, (60, 200, 60), ground)    

    elif state == "gameover":
        screen.blit(back_img_gameover, (0,0))
        screen.blit(gameover_text, (200,100))
        screen.blit(player_img, player)
        screen.blit(enemy_img, enemy)
        pygame.draw.rect(screen, (60,200, 60), ground)
        
        pygame.draw.rect(screen, (255,255,255), retry_button, border_radius = 20)
        pygame.draw.rect(screen, (255,255,255), quit_button, border_radius = 20)
        screen.blit(small_font.render("リトライ", True, (0,0,0)), (retry_button.x+40, retry_button.y+20))
        screen.blit(small_font.render("おわり", True, (0,0,0)), (quit_button.x+50, quit_button.y+20))


    #クリア画面
    elif state == "clear":
        screen.blit(back_img_gameclear, (0, 0))
        screen.blit(clear_text, (200,100))
        #text = font.render("Game Clear!", True, (0,0,0))
        #screen.blit(text, (200, 100))
        screen.blit(player_img, player)
        screen.blit(friend_img, friend)
        pygame.draw.rect(screen, (60,200, 60), ground)

        pygame.draw.rect(screen, (255,255,255), retry_button, border_radius = 20)
        pygame.draw.rect(screen, (255,255,255), quit_button, border_radius = 20)
        screen.blit(small_font.render("リトライ", True, (0,0,0)), (retry_button.x+40, retry_button.y+20))
        screen.blit(small_font.render("おわり", True, (0,0,0)), (quit_button.x+50, quit_button.y+20))

    pygame.display.update()
    clock.tick(60)
