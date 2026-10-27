#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
INC = ROOT / "config/includes.chroot"
def ensure(p): p.parent.mkdir(parents=True, exist_ok=True)
def font(size, bold=False):
    choices = [
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
      "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for p in choices:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def logo(draw, cx, cy, scale, fill):
    r = int(58*scale)
    draw.ellipse((cx-r,cy-r,cx+r,cy+r), fill=fill)
    # Bold forward chevrons, matching the supplied SHIFT mark's circle + double-arrow motif.
    for offset in (120, 220):
        pts=[(cx+offset*scale,cy-105*scale),(cx+(offset+75)*scale,cy-105*scale),
             (cx+(offset+125)*scale,cy),(cx+(offset+75)*scale,cy+105*scale),
             (cx+offset*scale,cy+105*scale),(cx+(offset+50)*scale,cy)]
        draw.polygon([(int(x),int(y)) for x,y in pts], fill=fill)

def gradient(w,h):
    stops=[(0.0,(7,13,29)),(.32,(10,29,56)),(.58,(9,68,89)),(.78,(34,45,103)),(1.0,(69,36,103))]
    im=Image.new("RGB",(w,h)); pix=im.load()
    for y in range(h):
      for x in range(w):
        t=min(1,max(0, .7*x/w + .3*y/h))
        for i in range(len(stops)-1):
          if stops[i][0] <= t <= stops[i+1][0]:
            a,ca=stops[i]; b,cb=stops[i+1]; q=(t-a)/(b-a)
            col=tuple(int(ca[k]*(1-q)+cb[k]*q) for k in range(3)); break
        pix[x,y]=col
    return im

wall=gradient(1920,1080).convert("RGBA")
# Soft atmospheric glow layers
glow=Image.new("RGBA",wall.size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
gd.ellipse((900,-350,2000,750), fill=(0,205,220,75))
gd.ellipse((1150,500,2200,1500), fill=(112,65,230,65))
gd.ellipse((-500,500,800,1450), fill=(0,120,190,45))
glow=glow.filter(ImageFilter.GaussianBlur(120)); wall=Image.alpha_composite(wall,glow)
d=ImageDraw.Draw(wall)
# Flowing luminous ribbons, using layered curves.
for idx,(color,width,phase) in enumerate([((22,220,202,45),34,0),((49,154,255,42),23,1.2),((148,92,255,35),18,2.4)]):
    pts=[]
    for x in range(-100,2100,12):
        y=600 + 190*math.sin(x/360+phase) + 55*math.sin(x/125+phase)
        pts.append((x,int(y+idx*48)))
    d.line(pts, fill=color, width=width, joint="curve")
# emblem in a translucent rounded plate
plate=Image.new("RGBA",wall.size,(0,0,0,0)); pd=ImageDraw.Draw(plate)
pd.rounded_rectangle((610,270,1310,690), radius=68, fill=(4,12,28,70), outline=(140,210,245,35), width=2)
wall=Image.alpha_composite(wall,plate); d=ImageDraw.Draw(wall)
# Create centered logo with custom proportional chevrons
logo(d,770,475,1.0,(216,230,242,238))
# Keep the brand mark as the visual focus; title is clean and readable.
title="SHIFT OS"
bbox=d.textbbox((0,0),title,font=font(76,True))
d.text(((1920-(bbox[2]-bbox[0]))/2,735),title,font=font(76,True),fill=(239,247,255,245),stroke_width=1,stroke_fill=(10,20,40,100))
sub="MOVE BEYOND THE DEFAULT"
bbox=d.textbbox((0,0),sub,font=font(22))
d.text(((1920-(bbox[2]-bbox[0]))/2,835),sub,font=font(22),fill=(126,218,232,235))
wallpath=INC/"usr/share/backgrounds/shift-os/shift-os-wallpaper.png"; ensure(wallpath); wall.convert("RGB").save(wallpath,optimize=True)
# transparent simple symbol and square launcher icon
for path,size in [(INC/"usr/share/pixmaps/shift-symbol.png",(512,256)),(INC/"usr/share/pixmaps/shift-os.png",(512,512)),(INC/"etc/calamares/branding/shift/shift-logo.png",(512,512))]:
    ensure(path); icon=Image.new("RGBA",size,(0,0,0,0)); idraw=ImageDraw.Draw(icon)
    if size[0]==512 and size[1]==256:
        logo(idraw,90,128,.55,(215,229,242,255))
    else:
        idraw.rounded_rectangle((0,0,511,511),radius=112,fill=(11,20,39,255))
        logo(idraw,135,256,.62,(36,220,198,255))
    icon.save(path,optimize=True)
# Calamares welcome image
welcome=Image.new("RGB",(1200,700),(11,20,39)); wd=ImageDraw.Draw(welcome)
for x in range(1200):
  col=(int(8+10*x/1200),int(24+24*x/1200),int(48+54*x/1200))
  wd.line((x,0,x,700),fill=col)
wd.ellipse((390,90,510,210),fill=(36,220,198))
wd.polygon([(560,95),(640,95),(700,150),(640,205),(560,205),(615,150)],fill=(36,220,198))
wd.polygon([(680,95),(760,95),(820,150),(760,205),(680,205),(735,150)],fill=(36,220,198))
wd.text((350,285),"SHIFT OS",font=font(68,True),fill=(239,247,255))
wd.text((350,380),"A modern desktop. A fresh direction.",font=font(26),fill=(128,218,235))
p=INC/"etc/calamares/branding/shift/shift-welcome.png"; ensure(p); welcome.save(p,optimize=True)
