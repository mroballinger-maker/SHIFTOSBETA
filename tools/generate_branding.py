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


# SHIFT OS first-run art: a quiet star field, ocean light and warm horizon.
hero_stops=[(0.0,(12,18,47)),(.42,(21,35,82)),(.68,(8,75,112)),(.86,(13,100,116)),(1.0,(170,103,79))]
hero=Image.new("RGBA",(1920,1080),(0,0,0,255))
hd=ImageDraw.Draw(hero)
for y in range(1080):
    t=y/1079
    for i in range(len(hero_stops)-1):
        if hero_stops[i][0] <= t <= hero_stops[i+1][0]:
            a,ca=hero_stops[i]; b,cb=hero_stops[i+1]; q=(t-a)/(b-a)
            c=tuple(int(ca[k]*(1-q)+cb[k]*q) for k in range(3))
            break
    hd.line((0,y,1920,y),fill=c+(255,))
# Small, restrained stars above the flowing ribbons.
for i in range(92):
    x=(i*337+83)%1920
    y=(i*149+37)%510
    radius=1+(i%3==0)
    shade=150+(i*29)%90
    hd.ellipse((x-radius,y-radius,x+radius,y+radius),fill=(shade,211,255,150+(i%4)*20))
# Add the colored glow under each ribbon before drawing its crisp edge.
ribbons=Image.new("RGBA",hero.size,(0,0,0,0))
rd=ImageDraw.Draw(ribbons)
for idx,(color,width,phase) in enumerate([((20,225,210,110),22,0.2),((30,149,255,95),18,1.5),((163,104,255,75),14,2.7),((255,184,112,65),10,3.8)]):
    pts=[]
    for x in range(-80,2001,10):
        y=680+135*math.sin(x/380+phase)+48*math.sin(x/145+phase)+idx*36
        pts.append((x,int(y)))
    rd.line(pts,fill=color,width=width,joint="curve")
ribbon_glow=ribbons.filter(ImageFilter.GaussianBlur(26))
hero=Image.alpha_composite(hero,ribbon_glow)
hero=Image.alpha_composite(hero,ribbons)
hero_bg=Image.new("RGB",hero.size,(0,0,0))
hero_bg.paste(hero.convert("RGB"))
welcome_bg_path=INC/"usr/share/backgrounds/shift-os/shift-os-welcome.png"
ensure(welcome_bg_path)
hero_bg.save(welcome_bg_path,optimize=True)

brand_dir=INC/"etc/calamares/branding/shift"
brand_dir.mkdir(parents=True,exist_ok=True)
# Calamares fills the welcome page and subsequent steps with this night-sky artwork.
installer_wall=hero_bg.resize((1024,700),Image.Resampling.LANCZOS).convert("RGBA")
shade=Image.new("RGBA",installer_wall.size,(3,10,25,92))
installer_wall=Image.alpha_composite(installer_wall,shade).convert("RGB")
installer_wall.save(brand_dir/"shift-installer-wallpaper.png",optimize=True)
# The welcome illustration is deliberately simpler than the desktop wallpaper so Calamares text stays legible.
welcome_art=Image.new("RGBA",(760,320),(0,0,0,0))
aw=ImageDraw.Draw(welcome_art)
aw.rounded_rectangle((3,3,756,316),radius=34,fill=(7,17,39,225),outline=(91,199,228,90),width=2)
for idx,(color,width,phase) in enumerate([((20,225,210,150),8,0.3),((45,139,255,130),6,1.7),((161,101,255,100),4,2.9)]):
    pts=[]
    for x in range(0,761,8):
        y=210+28*math.sin(x/112+phase)+idx*14
        pts.append((x,int(y)))
    aw.line(pts,fill=color,width=width,joint="curve")
mark=Image.open(INC/"usr/share/pixmaps/shift-symbol.png").convert("RGBA")
mark.thumbnail((210,105),Image.Resampling.LANCZOS)
welcome_art.alpha_composite(mark,((760-mark.width)//2,48))
aw=ImageDraw.Draw(welcome_art)
title_font=font(48,True)
small_font=font(20)
tb=aw.textbbox((0,0),"SHIFT OS",font=title_font)
aw.text(((760-(tb[2]-tb[0]))/2,166),"SHIFT OS",font=title_font,fill=(241,248,255,255))
tag="A fresh direction for your desktop"
tb=aw.textbbox((0,0),tag,font=small_font)
aw.text(((760-(tb[2]-tb[0]))/2,232),tag,font=small_font,fill=(143,226,238,255))
welcome_art.convert("RGB").save(brand_dir/"shift-welcome.png",optimize=True)

branding_desc="""---
componentName: shift
welcomeStyleCalamares: false
welcomeExpandingLogo: false
windowExpanding: normal
windowSize: 1024px,700px
windowPlacement: center
sidebar: widget
navigation: widget
strings:
  productName: SHIFT OS
  shortProductName: SHIFT OS
  version: "1.0"
  shortVersion: "1.0"
  versionedName: SHIFT OS 1.0
  shortVersionedName: SHIFT OS 1.0
  bootloaderEntryName: SHIFT OS
  productUrl: ""
  supportUrl: ""
  knownIssuesUrl: ""
  releaseNotesUrl: ""
  donateUrl: ""
images:
  productIcon: shift-logo.png
  productLogo: shift-logo.png
  productWallpaper: shift-installer-wallpaper.png
  productWelcome: shift-welcome.png
style:
  SidebarBackground: "#0B1427"
  SidebarText: "#EAF4FF"
  SidebarBackgroundCurrent: "#15364B"
  SidebarTextCurrent: "#41DCC9"
"""
(brand_dir/"branding.desc").write_text(branding_desc,encoding="utf-8")
stylesheet="""QWidget { color: #EAF4FF; }
QMainWindow, QDialog { background-color: #0B1427; }
QLabel { background: transparent; }
QPushButton {
  color: #071625; background-color: #42DCC9; border: 0;
  border-radius: 9px; padding: 9px 17px; font-weight: 600;
}
QPushButton:hover { background-color: #74E8D9; }
QPushButton:disabled { color: #8291A3; background-color: #28384C; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit {
  color: #F2F6FC; background-color: #13243D; border: 1px solid #33516E;
  border-radius: 6px; padding: 6px;
}
QListView, QTreeView, QTableView, QPlainTextEdit, QTextEdit {
  color: #EAF4FF; background-color: #101D34;
  alternate-background-color: #142743; selection-background-color: #176A78;
  selection-color: #FFFFFF; border: 1px solid #294761;
}
QHeaderView::section { color: #EAF4FF; background-color: #142743; padding: 6px; border: 0; }
QCheckBox, QRadioButton { color: #EAF4FF; spacing: 8px; }
QToolTip { color: #F2F6FC; background-color: #13243D; border: 1px solid #42DCC9; }
"""
(brand_dir/"stylesheet.qss").write_text(stylesheet,encoding="utf-8")
