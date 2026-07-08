from casioplot import *
from random import randint

K_OK=24; K_EX=95; K_4=71; K_5=72; K_6=73; K_SH=31; K_0=91
BK=(0,0,0); WH=(255,255,255); RD=(255,0,0); GN=(0,200,0); BL=(0,80,220); PU=(150,0,220)
LCOLS=[(255,128,0),(255,220,0),(0,200,200),(200,0,200),(255,255,255)]
DCOLS=[(0,180,0),(180,180,0),(180,0,0),(0,0,200)]
LIVES=[10,5,3,1]; BASE_SP=[2,5,9,14]

def detect_screen():
    w=0
    while get_pixel(w,0) is not None:
        w+=1
    h=0
    while get_pixel(0,h) is not None:
        h+=1
    return w,h
SW,SH=detect_screen()
HDR=18; SLX=10; SLH=24; SLW=SW-20; LW=3
SLY=SH//2-SLH//2; GW=42; BLW=24; PUW=14

def fr(x,y,w,h,c):
    for px in range(x,x+w):
        for py in range(y,y+h):
            set_pixel(px,py,c)

def gcol(ci,t=0):
    if ci==5:
        return LCOLS[t%5]
    return LCOLS[ci]

def try_place(zones,w,c,pts):
    for _ in range(50):
        x=SLX+randint(0,SLW-w)
        ok=True
        for oz in zones:
            if x<oz[0]+oz[1]+4 and x+w>oz[0]-4:
                ok=False; break
        if ok:
            zones.append((x,w,c,pts)); return

def make_zones():
    zones=[]
    try_place(zones,GW,GN,10)
    if randint(1,100)<=30:
        try_place(zones,BLW,BL,30)
    if randint(1,100)<=10:
        try_place(zones,PUW,PU,80)
    return zones

def draw_slider(zones):
    fr(SLX,SLY,SLW,SLH,RD)
    for zx,zw,zc,_ in zones:
        fr(zx,SLY+0,zw,SLH-0,zc)

def redraw_at(lx,zones):
    fr(lx,SLY,LW,SLH,RD)
    for zx,zw,zc,_ in zones:
        ix=max(lx,zx); ix2=min(lx+LW,zx+zw)
        if ix<ix2:
            fr(ix,SLY+0,ix2-ix,SLH-0,zc)

def draw_hdr(score,lives,hiscr,inf):
    fr(0,0,SW,HDR,BK)
    draw_string(5,4,"Hi:"+str(hiscr),WH,"small")
    draw_string(SW//2-20,4,"Score:"+str(score),WH,"small")
    if not inf:
        draw_string(SW-45,4,"Lv:"+str(lives),WH,"small")

hscrs=[0,0,0,0]; ihscr=0; lci=0; di=0

def draw_menu():
    fr(0,0,SW,SH,BK)
    draw_string(SW//2-35,5,"Reaction Game",WH,"large")
    draw_string(5,42,"Esy:"+str(hscrs[0]),WH,"small")
    draw_string(SW//4,42,"Med:"+str(hscrs[1]),WH,"small")
    draw_string(SW//2,42,"Hrd:"+str(hscrs[2]),WH,"small")
    draw_string(3*SW//4,42,"Ext:"+str(hscrs[3]),WH,"small")
    lsqx=20; lsqy=68
    draw_string(lsqx,lsqy-13,"Line:",(150,150,150),"small")
    fr(lsqx-1,lsqy-1,52,12,WH)
    if lci==5:
        for ri in range(5):
            fr(lsqx+ri*10,lsqy,10,10,LCOLS[ri])
    else:
        fr(lsqx,lsqy,50,10,gcol(lci))
    draw_string(lsqx,lsqy+13,"[5]toggle",(100,100,100),"small")
    sq_w=46; sq_h=30; sq_y=108; gap=8
    ts=4*sq_w+3*gap; sx=(SW-ts)//2
    for i in range(4):
        x=sx+i*(sq_w+gap)
        if i==di:
            fr(x-2,sq_y-2,sq_w+4,sq_h+4,WH)
        fr(x,sq_y,sq_w,sq_h,DCOLS[i])
    draw_string(sx+5,sq_y+sq_h+5,"[4]<  [6]>  [EXE]Play",(100,100,100),"small")
    draw_string(sx+5,sq_y+sq_h+18,"[Sh+EXE] Infinite  [0]=Exit",(100,100,100),"small")
    show_screen()

def run_game(infinite=False):
    global hscrs,ihscr
    lives=0 if infinite else LIVES[di]
    score=0; frame=0
    hiscr=ihscr if infinite else hscrs[di]
    while True:
        zones=make_zones()
        if infinite:
            sp=2+score//40
        else:
            sp=BASE_SP[di]+score//100
        lpos=SLX; ldir=1
        draw_slider(zones)
        draw_hdr(score,lives,hiscr,infinite)
        show_screen()
        stopped=False
        while not stopped:
            k=getkey()
            if k==K_OK:
                stopped=True
            elif infinite and k==K_0:
                return
            if not stopped:
                redraw_at(lpos,zones)
                lpos+=sp*ldir
                if lpos>=SLX+SLW-LW:
                    lpos=SLX+SLW-LW; ldir=-1
                elif lpos<=SLX:
                    lpos=SLX; ldir=1
                fr(lpos,SLY,LW,SLH,gcol(lci,frame))
                show_screen()
                frame+=1
        pts=0; hit_red=True
        for z in zones[::-1]:
            zx,zw,zc,zpts=z
            if lpos+LW>zx and lpos<zx+zw:
                pts=zpts; hit_red=False; break
        if hit_red and not infinite:
            lives-=1
        if not hit_red:
            score+=pts
            if score>hiscr:
                hiscr=score
                if infinite:
                    ihscr=hiscr
                else:
                    hscrs[di]=hiscr
        fr(SLX,SLY+SLH+2,SLW,16,BK)
        if hit_red:
            draw_string(SW//2-18,SLY+SLH+5,"-LIFE!",RD,"small")
        else:
            draw_string(SW//2-18,SLY+SLH+5,"+"+str(pts)+"pts",GN,"small")
        draw_hdr(score,lives,hiscr,infinite)
        show_screen()
        for _ in range(300000):
            pass
        fr(SLX,SLY+SLH+2,SLW,16,BK)
        if not infinite and lives<=0:
            mx=SW//2-45; my=SLY-28
            fr(mx,my,100,24,BK)
            draw_string(mx+2,my+2,"GAME OVER",WH,"small")
            draw_string(mx+2,my+13,"Score:"+str(score),WH,"small")
            show_screen()
            for _ in range(800000):
                pass
            break

sh=False
draw_menu()
while True:
    k=getkey()
    if k==K_EX:
        run_game(sh)
        draw_menu(); sh=False
    elif k==K_5:
        if sh:
            lci=5
        else:
            if lci==5:
                lci=0
            else:
                lci=(lci+1)%5
        draw_menu(); sh=False
    elif k==K_SH:
        sh=True
    elif k==K_4 and di>0:
        di-=1; draw_menu(); sh=False
    elif k==K_6 and di<3:
        di+=1; draw_menu(); sh=False
