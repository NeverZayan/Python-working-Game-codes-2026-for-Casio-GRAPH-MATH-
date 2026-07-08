from casioplot import *
from random import randint

K_OK=24; K_EX=95; K_4=71; K_6=73; K_7=61; K_9=63; K_SH=31
BK=(0,0,0); WH=(255,255,255); SKY=(100,180,255); GND=(120,80,30)
SCOL=[(255,0,0),(255,128,0),(255,255,0),(0,200,0),(0,200,200),(0,0,255),(128,0,128),WH,BK]
DCOLS=[(0,180,0),(180,180,0),(180,0,0),(0,0,200)]
DIFFS=[(3,65,7,-70,90),(6,55,10,-70,80),(9,45,12,-70,70),(12,45,15,-70,70)]

def detect_screen():
    w=0
    while get_pixel(w,0) is not None:
        w+=1
    h=0
    while get_pixel(0,h) is not None:
        h+=1
    return w,h
SW,SH=detect_screen()
HDR=18; GNDH=10; GNDL=SH-GNDH; BX=SW//5; BW=10; BH=8; PW=16

def fr(x,y,w,h,c):
    for px in range(x,x+w):
        for py in range(y,y+h):
            set_pixel(px,py,c)

def gcol(ci,t=0):
    if ci==9:
        return SCOL[t%8]
    return SCOL[ci]

def snext(ci,other,mx):
    n=(ci+1)%mx
    if n<9 and n==other:
        n=(n+1)%mx
    return n

def draw_pcols(px,w,gy,gh,pc):
    x=max(0,px); x2=min(px+w,SW)
    if x>=x2:
        return
    w2=x2-x
    if gy>HDR:
        fr(x,HDR,w2,gy-HDR,pc)
    gb=gy+gh
    if gb<GNDL:
        fr(x,gb,w2,GNDL-gb,pc)

def erase_pcols(px,w,gy,gh):
    x=max(0,px); x2=min(px+w,SW)
    if x>=x2:
        return
    w2=x2-x
    if gy>HDR:
        fr(x,HDR,w2,gy-HDR,SKY)
    gb=gy+gh
    if gb<GNDL:
        fr(x,gb,w2,GNDL-gb,SKY)

def draw_hdr(score):
    fr(0,0,SW,HDR,BK)
    draw_string(5,4,"Hi:"+str(hs),WH,"small")
    draw_string(SW-70,4,"Score:"+str(score),WH,"small")

bci=2; pci=3; di=0; hs=0; ps=0

def draw_menu():
    fr(0,0,SW,SH,BK)
    draw_string(SW//2-30,8,"Flappy Bird",WH,"large")
    draw_string(10,42,"Hi:"+str(hs),WH,"small")
    draw_string(SW-70,42,"Prev:"+str(ps),WH,"small")
    csw=30; csh=24; csy=68
    bsx=SW//4-csw//2; psx=3*SW//4-csw//2
    fr(bsx-2,csy-2,csw+4,csh+4,WH)
    if bci==9:
        for ri in range(8):
            fr(bsx+ri*3,csy,3,csh,SCOL[ri])
    else:
        fr(bsx,csy,csw,csh,SCOL[bci])
    draw_string(bsx,csy+csh+4,"[7]bird",(100,100,100),"small")
    fr(psx-2,csy-2,csw+4,csh+4,WH)
    if pci==9:
        for ri in range(8):
            fr(psx+ri*3,csy,3,csh,SCOL[ri])
    else:
        fr(psx,csy,csw,csh,SCOL[pci])
    draw_string(psx,csy+csh+4,"[9]pipe",(100,100,100),"small")
    sq_w=46; sq_h=30; sq_y=118; gap=8
    ts=4*sq_w+3*gap; sx=(SW-ts)//2
    for i in range(4):
        x=sx+i*(sq_w+gap)
        if i==di:
            fr(x-2,sq_y-2,sq_w+4,sq_h+4,WH)
        fr(x,sq_y,sq_w,sq_h,DCOLS[i])
    draw_string(sx+5,sq_y+sq_h+5,"[4]<  [6]>  [EXE]Play",(100,100,100),"small")
    show_screen()

def run_game():
    global hs,ps
    sp,gap_h,grav10,jump10,pspace=DIFFS[di]
    by10=(HDR+(GNDL-HDR)//2)*10; vel10=0; frame=0; score=0
    pipes=[[SW+10,HDR+20+randint(0,GNDL-HDR-gap_h-40),False]]
    fr(0,HDR,SW,GNDL-HDR,SKY)
    fr(0,GNDL,SW,GNDH,GND)
    pc=gcol(pci,0)
    for p in pipes:
        draw_pcols(p[0],PW,p[1],gap_h,pc)
    by=by10//10
    fr(BX,by,BW,BH,gcol(bci,0))
    draw_hdr(score); show_screen()
    while True:
        k=getkey()
        if k==K_OK:
            vel10=jump10
        vel10+=grav10
        old_by=by10//10
        by10+=vel10
        by=by10//10
        if by<HDR:
            by=HDR; by10=HDR*10; vel10=0
        fr(BX,old_by,BW,BH,SKY)
        pc=gcol(pci,frame); bc=gcol(bci,frame)
        for p in pipes:
            erase_pcols(p[0]+PW-sp,sp,p[1],gap_h)
            p[0]-=sp
            draw_pcols(p[0],sp,p[1],gap_h,pc)
        pipes=[p for p in pipes if p[0]+PW>0]
        if len(pipes)<3 and (not pipes or pipes[-1][0]<SW-pspace):
            gy=HDR+20+randint(0,GNDL-HDR-gap_h-40)
            pipes.append([SW+10,gy,False])
        scored=False
        for p in pipes:
            if not p[2] and p[0]+PW<=BX:
                p[2]=True; score+=1; scored=True
                if score>hs:
                    hs=score
        dead=(by+BH>=GNDL)
        for p in pipes:
            if BX+BW>p[0] and BX<p[0]+PW:
                if by<p[1] or by+BH>p[1]+gap_h:
                    dead=True
        fr(BX,by,BW,BH,bc)
        if scored:
            draw_hdr(score)
        show_screen()
        frame+=1
        if dead:
            break
    ps=score
    mx=SW//2-35; my=(HDR+GNDL)//2-15
    fr(mx,my,80,35,BK)
    draw_string(mx+5,my+3,"GAME OVER",WH,"small")
    draw_string(mx+5,my+18,"Score:"+str(score),WH,"small")
    show_screen()
    for _ in range(800000):
        pass

sh=False
draw_menu()
while True:
    k=getkey()
    if k==K_EX:
        run_game(); draw_menu(); sh=False
    elif k==K_7:
        if sh:
            bci=snext(bci,pci,10)
        else:
            bci=snext(bci,pci,9)
        draw_menu(); sh=False
    elif k==K_9:
        if sh:
            pci=snext(pci,bci,10)
        else:
            pci=snext(pci,bci,9)
        draw_menu(); sh=False
    elif k==K_SH:
        sh=True
    elif k==K_4 and di>0:
        di-=1; draw_menu(); sh=False
    elif k==K_6 and di<3:
        di+=1; draw_menu(); sh=False
