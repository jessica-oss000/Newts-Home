#NEWT's HOME
# 作者 313 09 翁苡瑄   313 12 范珈熏
#遊戲規則:透過方向鍵的左右控制蠑螈的橫向移動，上鍵或空白鍵控制跳躍，目標是跳躍過更多的泡泡，避免被泡泡碰到，挑戰自己的極限，若碰到泡泡則遊戲結束，必須重新開始。
#以下程式有使用gemini幫忙debug，控制蠑螈跳躍及標記和得分問題皆有參考gemini意見，實際操作還是由我們自己做的


import pygame, random, sys, time            #引用函式庫
from pygame.locals import *                 #引用函式庫
 
#------------------------------設定常數------------------------------
 
WINDOWWIDTH = 900                           #設定視窗寬度
WINDOWHEIGHT = 600                          #設定視窗高度
TEXTCOLOR = (150, 150, 150)                 #文字顏色為灰色
BACKGROUNDCOLOR = (255, 255, 255)           #背景顏色為白色
FPS = 100                                   #程式畫面更新速度
 
ARTICLESIZE = 80                            #物件尺寸
ARTICLEMINSPEED = 2                         #物件移動最小速度
ARTICLEMAXSPEED = 3                        #物件移動最大速度
ADDNEWARTICLERATE = 100                     #新增物件的頻率
PLAYERMOVERATE = 5                          #玩家移動速度(鍵盤控制用)
 
PLAYERJUMPSPEED = 15    #蠑螈跳躍時的初始向上速度
GRAVITY = 0.5          # 重力加速度 (每幀向下加速度)
bestscore=0            #最高分設為零


DOWNLEFT = 'downleft'                       #物件移動方向-左下
DOWNRIGHT = 'downright'                     #物件移動方向-右下
UPLEFT = 'upleft'                           #物件移動方向-左上
UPRIGHT = 'upright'                         #物件移動方向-右上


direction = [DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT]  #將方向存成串列
 
#------------------------------定義函式------------------------------
 
def terminate():                            #結束程式
    pygame.quit()
    sys.exit()
 
def waitForPlayerToPressKey():              #暫停遊戲等待玩家按鍵
    while True:
        for event in pygame.event.get():    #偵測事件發生
            if event.type == QUIT:          #關閉視窗則程式結束
                terminate()
            if event.type == KEYDOWN:       #如果有按下按鍵
                if event.key == K_ESCAPE:   #按下 ESC 鍵則程式結束
                    terminate()
                elif event.key == K_RETURN:  #按下ENTER則繼續遊戲
                    return
 
def drawText(text, font, surface, x, y):    #繪製文字
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)    
   
                   
 
#-------------------------初始化 pygame 和設定視窗-------------------------
 
pygame.init()                               #pygame 初始化
mainClock = pygame.time.Clock()             #設定調整程式執行速度之物件
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("NEWT's HOME")      #設定視窗標題
 
#------------------------------設定字型物件------------------------------
 
font = pygame.font.SysFont(None, 32)        #設定字型
 
#------------------------------設定音效物件------------------------------
 
pygame.mixer.music.load('background .mp3')               #設定背景音樂
gameSuccessSound = pygame.mixer.Sound('success.wav')    #設定遊戲成功音效
gameOverSound = pygame.mixer.Sound('game over.mp3')      #設定遊戲失敗音效
 
#------------------------------設定影像物件------------------------------
 
playerImage = pygame.image.load('happy newt.PNG')            #設定玩家圖像為開心蠑螈
playerRect = playerImage.get_rect()                     #玩家為蠑螈圖像的 Rect 物件
bubbleImage = pygame.image.load('bubble.PNG')                 #設定泡泡圖像
backgroundImage1 = pygame.image.load('start.PNG')         #設定背景圖像
backgroundImage2 = pygame.image.load('規則.PNG')
backgroundImage3 = pygame.image.load('room.PNG')
backgroundImage4 = pygame.image.load('end.PNG')

 
#------------------------------顯示起始畫面------------------------------
 
windowSurface.blit(backgroundImage1, (0, 0))         #畫出背景和顯示文字
pygame.display.update()                     #更新畫面
waitForPlayerToPressKey()                   #暫停遊戲等待玩家按鍵
windowSurface.blit(backgroundImage2, (0, 0))         #畫出背景和顯示文字
pygame.display.update()                     #更新畫面
waitForPlayerToPressKey()                   #暫停遊戲等待玩家按鍵


 
#------------------------------主程式開始------------------------------
 
while True:                                 #主程式是個無窮迴圈
   
                           
    GameStart = True                        #預設遊戲狀態為執行(True)
    bubble=0                                #場上泡泡數量設為零
    stamped_target=[]                       #宣告標記的泡泡的串列
    score = 0                               #分數設為零
    playerImage = pygame.image.load('happy newt.PNG')#設定玩家圖像為開心蠑螈
    
   
    bubbles = []                               #宣告新泡泡字典物件的串列
     
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)    #蠑螈初始位置在畫面中間
    moveLeft = moveRight = moveUp = moveDown = False             #鍵盤控制用的移動變數初始為 False
    bubbleAddCounter = 0                       #泡泡計數器初始為 0
    v_y = 0                                  #y的速度設為零
    pygame.mixer.music.play(-1, 0.0)        #重頭播放背景音樂且為循環播放


#------------------------------遊戲計時開始------------------------------
     
    while  GameStart == True:   #當遊戲時間未歸零的情形下遊戲進行
                               
#------------------------------處理鍵盤事件------------------------------
        for event in pygame.event.get():    #偵測事件發生
            if event.type == QUIT:          #關閉視窗則程式結束
                terminate()
                 
           
            if event.type == KEYDOWN:               #當有按下按鍵
                if event.key == K_LEFT:             #當按下方向左鍵,調整移動變數
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:            #當按下方向右鍵,調整移動變數
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP:               #當按下方向上鍵,調整移動變數
                    if playerRect.bottom >= WINDOWHEIGHT - PLAYERMOVERATE:    # 只有當蠑螈在地面上時才能跳躍 (檢查蠑螈底部是否接近地面)
                        v_y = -PLAYERJUMPSPEED      # 向上賦予初始速度
                if event.key == K_SPACE:            # 【新增：按下空白鍵進行跳躍】
                    if playerRect.bottom >= WINDOWHEIGHT - PLAYERMOVERATE:    # 只有當蠑螈在地面上時才能跳躍 (檢查蠑螈底部是否接近地面)
                        v_y = -PLAYERJUMPSPEED      # 向上賦予初始速度
               



                             
            if event.type == KEYUP:                 #當有放開按鍵
                if event.key == K_ESCAPE:           #當放開鍵盤 ESC 時,程式結束

                    terminate()
                if event.key == K_LEFT:             #當放開方向左鍵,調整移動變數
                    moveLeft = False
                if event.key == K_RIGHT:            #當放開方向右鍵,調整移動變數
                    moveRight = False
                if event.key == K_UP:               #當放開方向上鍵,調整移動變數
                    moveUp = False
                             

             
#-----------------------偵測事件結束,移動蠑螈位置(鍵盤)-----------------------
         
         
        if moveLeft and playerRect.left > 0:        #當玩家在畫面中且有移動時,改變位置
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
       
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
           
        v_y += GRAVITY
        playerRect.move_ip(0, v_y) # 根據垂直速度更新蠑螈位置

                       
        if playerRect.bottom >= WINDOWHEIGHT:
            playerRect.bottom = 600
            v_y = 0
         
#------------------------------新增泡泡------------------------------
         
        bubbleAddCounter += 1                              #泡泡計數累加
        if bubbleAddCounter == ADDNEWARTICLERATE:          #當達到預設之新增物件的頻率時
            bubbleAddCounter = 0                           #累加計數歸 0
            newbubble = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - ARTICLESIZE), 0 - ARTICLESIZE, ARTICLESIZE, ARTICLESIZE),
                      'speed': random.randint(ARTICLEMINSPEED, ARTICLEMAXSPEED),
                      'dir': direction[random.randint(0, 1)]}
            bubbles.append(newbubble)                         #新增新泡泡字典物件並放到串列中
            #bubbles +=1
        if bubble==8:           #控制泡泡在場上的數量
            bubbleAddCounter = 1
       
       
#------------------------------移動泡泡------------------------------
         
        for c in bubbles:                                  #泡泡從天而降,依方向進行移動
            if c['dir'] == DOWNLEFT:
                c['rect'].left -= c['speed']
                c['rect'].top += c['speed']
            if c['dir'] == DOWNRIGHT:
                c['rect'].left += c['speed']
                c['rect'].top += c['speed']
            if c['dir'] == UPLEFT:
                c['rect'].left -= c['speed']
                c['rect'].top -= c['speed']
            if c['dir'] == UPRIGHT:
                c['rect'].left += c['speed']
                c['rect'].top -= c['speed']
 
            if c['rect'].top < 0:                       #泡泡碰到邊界反彈
                if c['dir'] == UPLEFT:
                    c['dir'] = DOWNLEFT
                if c['dir'] == UPRIGHT:
                    c['dir'] = DOWNRIGHT
            if c['rect'].bottom > WINDOWHEIGHT:
                if c['dir'] == DOWNLEFT:
                    c['dir'] = UPLEFT
                if c['dir'] == DOWNRIGHT:
                    c['dir'] = UPRIGHT
            if c['rect'].left < 0:
                if c['dir'] == DOWNLEFT:
                    c['dir'] = DOWNRIGHT
                if c['dir'] == UPLEFT:
                    c['dir'] = UPRIGHT
            if c['rect'].right > WINDOWWIDTH:
                if c['dir'] == DOWNRIGHT:
                    c['dir'] = DOWNLEFT
                if c['dir'] == UPRIGHT:
                    c['dir'] = UPLEFT



#------------------------------得分和碰撞偵測------------------------------
        for c in bubbles:

            if (playerRect.centerx- c['rect'].centerx)**2+((playerRect.centery- c['rect'].centery)*1.1)**2<6200 :       #當玩家被泡泡碰到
                playerImage = pygame.image.load('crying newt.PNG') #換成哭哭蠑螈
                windowSurface.blit(backgroundImage3, (0, 0)) # 畫背景
                for bubble_draw in bubbles: # 畫泡泡
                    windowSurface.blit(bubbleImage, bubble_draw['rect'])
                windowSurface.blit(playerImage, playerRect) # 畫上哭哭蠑螈
                
                pygame.display.update()
                GameStart = False;                      #遊戲狀態為不執行(False)
                time.sleep(0.5)                         #遊戲停止0.5秒
                break;                                  #迴圈中斷表示遊戲結束(失敗)

            
            if  abs(playerRect.centerx - c['rect'].centerx) < 10:  #標記躍過的泡泡
                if playerRect.bottom <= c['rect'].top:
                    stamped_target.append(c)

        if  len(stamped_target) >0:                              #跳到地面時標記的泡泡消失並且加一分
            if playerRect.bottom >=WINDOWHEIGHT:
                for target in stamped_target:
                    if target in bubbles:
                        bubbles.remove(target)
                        score+=1
                        bubble-=1                               #場上的泡泡數量-1
                stamped_target = []                             #清空標記
        if score>bestscore:                                     #如果分數大於最高分
            bestscore=score                                     #更新最高分
      
            
                 
            
#------------------------------繪製視窗------------------------------
         
        windowSurface.blit(backgroundImage3, (0, 0))     #畫出背景圖
         
        for c in bubbles:                                  #畫出每 1 顆泡泡
            windowSurface.blit(bubbleImage, c['rect'])
         
        windowSurface.blit(playerImage, playerRect)     #畫出玩家物件

        drawText('score: %s' % (score), font, windowSurface, 770, 10)   #繪製文字
        drawText('best score: %s' % (bestscore), font, windowSurface, 20, 10)
        
        #pygame.draw.rect(windowSurface, (255,0,0), playerRect, 1)    #蠑螈的碰撞箱
         
        pygame.display.update()                         #更新畫面
        mainClock.tick(FPS)                             #設定程式執行速度
         
#-------------------------遊戲計時結束,顯示遊戲結果-------------------------
     
   
     
    if GameStart == False:
        windowSurface.blit(backgroundImage4, (0, 0))   #切換到結算畫面
        drawText('score: %s' % (score), font, windowSurface, 770, 10)   #繪製文字
        drawText('best score: %s' % (bestscore), font, windowSurface, 20, 10)
        pygame.mixer.music.stop()    #關閉背景音效
        gameOverSound.play()        #開啟失敗音效
        
    pygame.display.update()                 #更新畫面
    waitForPlayerToPressKey()               #等待玩家按鍵繼續
    gameSuccessSound.stop()                 #關閉音效
    gameOverSound.stop()                    #關閉音效
 
#------------------------------主程式結束------------------------------


       
