from casioplot import *
from random import randint

K_U=14; K_D=34; K_L=23; K_R=25
K_N0=91; K_N2=82; K_N4=71; K_N6=73; K_N8=62; K_OK=24; K_EX=95

BK=(0,0,0); WH=(255,255,255); RD=(255,0,0); GR=(60,60,60)
YL=(220,220,0); GN2=(0,180,0); DM=(150,220,255)
SCOLS=[(255,0,0),(255,128,0),(255,255,0),(0,220,0),(0,200,200),(0,0,255),(128,0,128),(255,255,255)]
DCOLS=[(0,180,0),(180,180,0),(180,0,0),(0,0,200)]
SP=[50000,10000,8000,5000]

def detect_screen():
    w=0
    while get_pixel(w,0) is not None:
        w+=1
    h=0
    while get_pixel(0,h) is not None:
        h+=1
    return w,h
SW,SH=detect_screen()

def fr(x,y,w,h,c):
    for px in range(x,x+w):
        for py in range(y,y+h):
            set_pixel(px,py,c)

def rand_pos(excl,N):
    while True:
        a=(randint(0,N-1),randint(0,N-1))
        if a not in excl:
            return a

def make_apples(snake,N):
    excl=set(snake)
    aps={}
    p=rand_pos(excl,N); aps[p]=(RD,1); excl.add(p)
    if randint(1,100)<=30:
        p=rand_pos(excl,N); aps[p]=(YL,5); excl.add(p)
    if randint(1,100)<=10:
        p=rand_pos(excl,N); aps[p]=(GN2,15); excl.add(p)
    if randint(1,100)<=1:
        p=rand_pos(excl,N); aps[p]=(DM,50); excl.add(p)
    return aps

gn=10; sci=3; di=0; walls=False; hs=0
_ox=0; _oy=0; _cs=1

def dc(gx,gy,c):
    fr(_ox+gx*_cs+1,_oy+gy*_cs+1,_cs-1,_cs-1,c)

def show_hdr(score):
    fr(0,0,SW,20,BK)
    draw_string(5,5,"Score:"+str(score),WH,"small")
    draw_string(SW//2,5,"Best:"+str(hs),WH,"small")

def draw_menu():
    fr(0,0,SW,SH,BK)
    draw_string(SW//2-25,10,"SNAKE",WH,"large")
    draw_string(10,52,"Grid:"+str(gn),WH,"medium")
    draw_string(10,70,"[8]=+ [2]=-",GR,"small")
    cx=SW-55; cy=50
    fr(cx-2,cy-2,22,22,WH)
    if sci==8:
        for ri in range(8):
            fr(cx+ri*2,cy,2,18,SCOLS[ri])
    else:
        fr(cx,cy,18,18,SCOLS[sci])
    draw_string(cx-5,cy+20,"[OK]",GR,"small")
    sq_w=46; sq_h=32; sq_y=105; gap=8
    ts=4*sq_w+3*gap; sx=(SW-ts)//2
    for i in range(4):
        x=sx+i*(sq_w+gap)
        if i==di:
            fr(x-2,sq_y-2,sq_w+4,sq_h+4,WH)
        fr(x,sq_y,sq_w,sq_h,DCOLS[i])
    draw_string(sx+5,sq_y+sq_h+5,"[4]<  [6]>",GR,"small")
    if walls:
        draw_string(SW//2-35,sq_y+sq_h+22,"[0] Walls:ON",WH,"small")
    else:
        draw_string(SW//2-35,sq_y+sq_h+22,"[0] Walls:OFF",WH,"small")
    draw_string(SW//2-20,SH-20,"[EXE] Start",WH,"small")
    if hs>0:
        draw_string(SW-65,15,"Best:"+str(hs),WH,"small")
    show_screen()

def run_game():
    global hs,_ox,_oy,_cs
    N=gn; _cs=min(SW,SH-20)//N; tot=N*_cs
    _ox=(SW-tot)//2; _oy=20+(SH-20-tot)//2
    rainbow=(sci==8); rtick=0
    sc=SCOLS[0] if rainbow else SCOLS[sci]
    sp=SP[di]
    hx=N//2; hy=N//2
    snake=[(hx,hy),(hx-1,hy),(hx-2,hy)]
    dx=1; dy=0; ndx=1; ndy=0
    apples=make_apples(snake,N)
    score=0
    fr(_ox,_oy,tot+1,tot+1,BK)
    for i in range(N+1):
        for p in range(tot+1):
            set_pixel(_ox+i*_cs,_oy+p,GR)
            set_pixel(_ox+p,_oy+i*_cs,GR)
    for seg in snake:
        dc(seg[0],seg[1],sc)
    for pos in apples:
        dc(pos[0],pos[1],apples[pos][0])
    show_hdr(score); show_screen()
    while True:
        k=0
        for i in range(sp):
            if i%5000==0:
                kk=getkey()
                if kk!=0:
                    k=kk
        if k==K_U and dy==0:
            ndx=0; ndy=-1
        elif k==K_D and dy==0:
            ndx=0; ndy=1
        elif k==K_L and dx==0:
            ndx=-1; ndy=0
        elif k==K_R and dx==0:
            ndx=1; ndy=0
        dx=ndx; dy=ndy
        if rainbow:
            sc=SCOLS[rtick%8]; rtick+=1
        nhx=snake[0][0]+dx; nhy=snake[0][1]+dy
        if walls:
            if nhx<0 or nhx>=N or nhy<0 or nhy>=N:
                break
        else:
            nhx=nhx%N; nhy=nhy%N
        if (nhx,nhy) in snake[:-1]:
            break
        ate=apples.get((nhx,nhy))
        snake.insert(0,(nhx,nhy))
        if not ate:
            tail=snake.pop()
            if tail in apples:
                dc(tail[0],tail[1],apples[tail][0])
            else:
                dc(tail[0],tail[1],BK)
        else:
            score+=ate[1]
            if score>hs:
                hs=score
            if ate[1]==1:
                for pos in apples:
                    if pos not in snake:
                        dc(pos[0],pos[1],BK)
                apples=make_apples(snake,N)
                for pos in apples:
                    dc(pos[0],pos[1],apples[pos][0])
            else:
                del apples[(nhx,nhy)]
            show_hdr(score)
        dc(nhx,nhy,sc); show_screen()
    mx=SW//2-35; my=SH//2-15
    fr(mx,my,80,35,BK)
    draw_string(mx+5,my+3,"GAME OVER",WH,"small")
    draw_string(mx+5,my+18,"Score:"+str(score),WH,"small")
    show_screen()
    for _ in range(800000):
        pass

shift_armed=False
draw_menu()
while True:
    k=getkey()
    if k==K_EX:
        run_game()
        draw_menu(); shift_armed=False
    elif k==K_OK:
        if shift_armed:
            sci=8
        elif sci==8:
            sci=0
        else:
            sci=(sci+1)%8
        draw_menu(); shift_armed=False
    elif k==31:
        shift_armed=True
    elif k==K_N8 and gn<30:
        gn+=1; draw_menu(); shift_armed=False
    elif k==K_N2 and gn>5:
        gn-=1; draw_menu(); shift_armed=False
    elif k==K_N4 and di>0:
        di-=1; draw_menu(); shift_armed=False
    elif k==K_N6 and di<3:
        di+=1; draw_menu(); shift_armed=False
    elif k==K_N0:
        walls=not walls; draw_menu(); shift_armed=False
