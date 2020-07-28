# main.py
# pip install pygame
# pip3 install pygame
# python3 -m pip install pygame
# C:\Python38\python.exe -m pip install pygame
import pygame
import math
import random
import csv

# เซ็ตอัพเริ่มต้นให้ pygame ทำงาน
pygame.init()

# ปรับขนาดหน้าจอหลัก
WIDTH = 1010
HEIGHT = 646
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Covid-19') #set ชื่อเกม
icon = pygame.image.load('icon.png') # โหลดภาพเข้ามาใน pygame
pygame.display.set_icon(icon) #สั่งเซ็ตเป็น icon
background = pygame.image.load('background.png')

###############Player###############
# 1 - player - uncle.png

psize = 128 #ความกว้างของภาพ Player

pimg = pygame.image.load('player.png')
px = 100	#400-(psize/2)	#จุดเริ่มต้นแกน x (แนวนอน)
py = HEIGHT - psize 	#จุดเริ่มต้นแกน y (แนวตั้ง)
pxchange = 0 
def Player(x,y):
	screen.blit(pimg,(x,y)) #blit  คือ วางภาพในหน้าจอ


###############Enemy###############
# 2 - enemy - virus.png
esize = 64
eimg = pygame.image.load('virus.png')
ex = 50
ey = esize
eychange = 1
def Enemy(x,y):
	screen.blit(eimg,(x,y))

########## multi enemy ########
exlist = []	# ตำแน่ง x ของ enemy
eylist = []	# ตำแน่ง y ของ enemy
ey_change_list = [] # ความเร็ว ของ enemy
allenemy = 2	#จำนวน ของ enemy ทั้งหมด

for i in range(allenemy):
	exlist.append(random.randint(50,WIDTH - esize))
	eylist.append(random.randint(0,100))
	ey_change_list.append(random.randint(1,3)) # สุ่มความเร็ว enemy
	#ey_change_list.append(1) #กำหนดความเร็วเป็น 1 แล้วค่อยเพิ่มหลังจากยิงโดน

###############Mask###############
# 3 - mask - mask.png
msize = 32
mimg = pygame.image.load('mask.png')
mx = 100
my = HEIGHT - psize
mychange = 12 # ปรับความเร็วของ player
mstate = 'ready'

def fire_mask(x,y):
	global mstate
	mstate = 'fire'
	screen.blit(mimg,(x,y))

############### apple ###############
# 4 - apple - apple.png

asize = 64
aimg = pygame.image.load('apple.png')
ax = WIDTH / 2
ay = asize
aychange = 1 # ปรับความเร็วของ apple

def apple_drop(x,y):
	screen.blit(aimg,(x,y))
	#ay = ay + aychange

############## collision ##############
def isCollision(ecx,ecy,mcx,mcy):
	# isCollision ชนกันหรือไม่? หากชนกัน ให้คืนค่า True
	distance = math.sqrt(math.pow(ecx - mcx,2)+math.pow(ecy - mcy,2))
	print(distance)
	if distance < (esize /2) + (msize / 2):
		#ระยะที่ชนกัน
		return True
	else:
		return False

############## collision apple vs player ##############
def isCollisionAvP(acx,acy,pcx,pcy):
	# isCollision ชนกันหรือไม่? หากชนกัน ให้คืนค่า True
	distance2 = math.sqrt(math.pow(acx - pcx,2)+math.pow(acy - pcy,2))
	print(distance2)
	if distance2 < (asize /2) + (psize / 2):
		#ระยะที่ชนกัน
		return True
	else:
		return False

############## SCORE ##############
allscore = 0
font = pygame.font.Font('angsana.ttc',30)

def showscore():
	score = font.render('คะแนน : {} คะแนน'.format(allscore),True,(0,0,0))
	screen.blit(score,(10,5))

############## Life ##############
limg = pygame.image.load('heart.png')
plife = 3
font = pygame.font.Font('angsana.ttc',35)

def showlife():
	life = font.render('X {} '.format(plife),True,(22,125,22))
	screen.blit(life,(45,30))
	screen.blit(limg,(10,40))
############# sound ###############
#pygame.mixer.Music.load('')
#pygame.
#pygame.mixer.music.play(-1)

sound = pygame.mixer.Sound('welcome.wav')
#pygame.mixer.music.set_volume(0.1)
sound.play()


############# Game over ###############
fontover = pygame.font.Font('angsana.ttc',150)
fontover2 = pygame.font.Font('angsana.ttc',80)
playsound = False
gameover = False
def GameOver():
	global playsound
	global gameover
	overtext = fontover.render('Game Over',True,(255,0,0))
	screen.blit(overtext,(260,150))
	overtext2 = fontover2.render('Press [N] New game',True,(255,255,0))
	screen.blit(overtext2,(275,300))
	if playsound == False:
		gsound = pygame.mixer.Sound('over.wav')
		gsound.play()
		playsound = True

	#if gameover == False:
	#	gameover == True

##################### high score ###########
def showHighScore():
	with open('highscore.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			#print(row)
			highscore = int(row[0])
	fontscore = pygame.font.Font('angsana.ttc',35)
	if highscore>allscore:
		hs = fontscore.render('HScore : {} '.format(highscore),True,(255,125,255))
		screen.blit(hs,(900,15))
	else:
		hs = fontscore.render('HScore : {} '.format(allscore),True,(255,125,255))
		screen.blit(hs,(900,15))
		



############### Game Loop ###############
running = True #บอกให้โปรแกรมทำงาน
pspeed = 10
clock = pygame.time.Clock() # game clock 
FPS = 60 #frame rate

while running:

	#screen.blit(background,(0,0))
	for event in pygame.event.get():
		# รันลูปแล้วเช็คว่ามีการกดปิดเกมหรือไม่ [x]
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				pxchange = -pspeed
			if event.key == pygame.K_RIGHT:
				pxchange = pspeed

			if event.key == pygame.K_SPACE:
				if mstate == 'ready':
					b1 = pygame.mixer.Sound('laser.wav')
					b1.play()
					mx = px + 20  # ขยับหน้ากาก ชิดมือ ด้านขวา
					fire_mask(mx,my)
			if event.key == pygame.K_n:
				with open('highscore.csv', 'w', newline='') as file:
					writer = csv.writer(file)
					writer.writerow([allscore])
				gameover = False
				playsound = False
				plife = 3
				allscore = 0
				pspeed = 10
				for i in range(allenemy):
					eylist[i] = random.randint(0,100)
					exlist[i] = random.randint(50,WIDTH - esize)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				pxchange = 0



	############# run player ############
	# px,py จุดเริ่มต้น 		
	Player(px,py)
	'''
	### ทำให้ player ขยับซ้ายขวา เมื่อชนของจอ
	if px <= 0:
		# หากชนขอบจอซ้าย ให้ปรับค่า pxchange เป็น +1
		pxchange = 1
		px += pxchange # px = px+1
	elif px >= WIDTH - psize:
		# WIDTH (ความกว้างของหน้าจอ - ความกว้างplayer)
		# หากชนขอบจอขวา ให้ปรับค่า pxchange เป็น +1
		pxchange = -1
		px += pxchange
	else:
		# หากอยู่ระหว่างหน้าจอจะทำการบวก/ลบ ตาม pxchange
		px += pxchange
	'''
	### ทำให้ player ขยับซ้ายขวา เมื่อชนของจอ
	if px <= 0:
		# หากชนขอบจอซ้าย ให้ปรับค่า pxchange เป็น +1
		px = 0
		px += pxchange # px = px+1
	elif px >= WIDTH - psize:
		# WIDTH (ความกว้างของหน้าจอ - ความกว้างplayer)
		# หากชนขอบจอขวา ให้ปรับค่า pxchange เป็น +1
		px = WIDTH - psize
		px += pxchange
	else:
		# หากอยู่ระหว่างหน้าจอจะทำการบวก/ลบ ตาม pxchange
		px += pxchange
	
	############### collision apple vs player############
	collisionApple = isCollisionAvP(ax,ay,px,py)
	if collisionApple:
		ay = -200
		ax = 350
		pspeed = 20 # เพิ่มความเร็ว
		


	############### run enemy single############
	#for i in range(5):
	#Enemy(ex,ey)
	#ey += eychange
	# เช็คว่าชนกันหรือไม่
	collision = isCollision(ex,ey,mx,my)
	if collision:
		my = HEIGHT - psize
		mstate = 'ready'
		ey = 0
		ex = random.randint(0 + esize,WIDTH - esize)
		allscore += 1 # เพิ่มคะแนน
		#สุ่มตำแหน่ง

	########### run multi enemy ###########
	for i in range(allenemy):
		#if eylist[i] > HEIGHT - esize:
		#	plife-=1
		#	break
		# เพิ่มความเร็ว enemy
		if eylist[i] > HEIGHT - esize and gameover == False:
		#if plife < 0 and gameover == False:
			plife-=1
			eylist[i] = -500
			if plife<0:
				plife =0
				for i in range(allenemy):
					eylist[i] = 1000
					GameOver()
					break


		eylist[i] += ey_change_list[i]
		collisionmultit = isCollision(exlist[i],eylist[i],mx,my)
		if collisionmultit:
			my = HEIGHT - psize
			mystate = 'ready'
			eylist[i] = 0
			exlist[i] = random.randint(50,WIDTH - esize)
			allscore += 1 #เพิ่มคะแนน
			#ey_change_list[i] += 1 # เพิ่มความเร็ว enemy ขึ้นทีละ 1
			ey_change_list[i] = random.randint(1,3)# สุ่มความเร็ว 1-3
			soundCon = pygame.mixer.Sound('broken.wav')
			soundCon.play()


		Enemy(exlist[i],eylist[i])

	###########fire mask #############
	if mstate == 'fire':
		fire_mask(mx,my)
		my = my - mychange # my -= mychange

	# เช็คว่า mask ชน ขอบหรือยัง? ถ้าชน เปลี่ยน state เป็น ready
	if my <= 0:
		my = HEIGHT - psize
		mstate = 'ready'

	if allscore%10 == 0:
		apple_drop(ax,ay)
		ay = ay + aychange

	showscore()
	showlife()
	showHighScore()
	#apple_drop(allscore)
	print(px)
	pygame.display.update()
	#pygame.display.flip()
	#pygame.event.pump()
	screen.fill((0,0,0))
	screen.blit(background,(0,0))
	clock.tick(FPS)