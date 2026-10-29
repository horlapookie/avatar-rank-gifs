from PIL import Image, ImageDraw, ImageFont, ImageSequence
from pathlib import Path
import math, random, json

OUT = Path('gifs')
FAMILIES = ['rookie', 'veteran', 'elite', 'pro', 'master', 'grandmaster', 'legendary']
ROMAN = ['I', 'II', 'III', 'IV', 'V']
COLORS = [(217,151,98), (203,218,233), (255,209,88), (85,224,238), (239,101,111), (179,140,255), (255,192,64)]
RANKS = [(f, d) for f in range(7) for d in range(1,6)]
SIZE = 320
S = 2
FPS = 10
FRAMES = 50
DURATION = 100
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def name(rank):
    f, d = rank
    return FAMILIES[f] + '-' + ROMAN[d-1]

def star(x, y, radius, points=5, angle=-math.pi/2):
    return [(x + math.cos(angle+i*math.pi/points)*radius*(1 if i%2==0 else .44), y + math.sin(angle+i*math.pi/points)*radius*(1 if i%2==0 else .44)) for i in range(points*2)]

def frame(rank, old, t, promo):
    image = Image.new('RGB', (SIZE*S,SIZE*S), (9,14,22))
    draw = ImageDraw.Draw(image)
    def poly(points, fill, outline=None, width=1):
        draw.polygon([(int(x*S),int(y*S)) for x,y in points], fill=fill)
        if outline:
            pts = [(int(x*S),int(y*S)) for x,y in points]
            draw.line(pts+[pts[0]], fill=outline, width=width*S, joint='curve')
    def line(points, color, width=1):
        draw.line([(int(x*S),int(y*S)) for x,y in points], fill=color, width=width*S)
    def text(value,y,size,color):
        font=ImageFont.truetype(FONT,size*S)
        draw.text((SIZE*S/2,y*S),value,font=font,fill=color,anchor='mm')
    def circle(x,y,r,color,width=1):
        draw.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),outline=color,width=width*S)
    phase = 'old' if promo and t<1.45 else 'new'
    active = old if phase=='old' else rank
    f,d = active
    color=COLORS[f]
    for y in range(0,SIZE,16):
        line([(0,y),(SIZE,y)],(15,23,33))
    for x in range(0,SIZE,16):
        line([(x,0),(x,SIZE)],(15,23,33))
    line([(16,27),(16,16),(42,16)],color,2)
    line([(278,16),(304,16),(304,27)],color,2)
    line([(16,293),(16,304),(42,304)],color,2)
    line([(278,304),(304,304),(304,293)],color,2)
    cx,cy=160,139
    elapsed=max(0,t-1.5) if promo else t
    pulse=math.sin(t*math.pi*1.2)
    for radius in [94,100]:
        circle(cx,cy,radius,(29,41,53))
    for k in range(12):
        a=t*.23+k*math.tau/12
        r1,r2=85,98
        line([(cx+math.cos(a)*r1,cy+math.sin(a)*r1),(cx+math.cos(a)*r2,cy+math.sin(a)*r2)],tuple(int(v*.48) for v in color),2)
    charge=min(t/1.45,1) if phase=='old' else min(elapsed/.75,1)
    scale=.92+.035*pulse
    if phase=='new' and elapsed<.6:
        scale=.7+.35*math.sin(min(elapsed/.6,1)*math.pi/2)
    def shape(points,fill,outline=None,width=1):
        poly([(cx+(x-cx)*scale,cy+(y-cy)*scale) for x,y in points],fill,outline,width)
    outer=[(160,57),(221,89),(215,159),(198,187),(160,211),(122,187),(105,159),(99,89)]
    shape(outer,(24,31,43),color,3)
    shape([(160,67),(210,94),(204,155),(190,179),(160,197),(130,179),(116,155),(110,94)],(15,22,32),tuple(int(v*.52) for v in color),2)
    shape([(160,72),(160,193),(133,177),(120,153),(115,96)],(28,35,45))
    if f<3:
        shape([(140,95),(151,123),(164,115),(154,89)],(86,101,124))
        shape([(166,89),(156,115),(169,123),(181,95)],color)
        circle(cx,143,25,color,4)
        poly(star(cx,143,17,5),color)
    elif f==3:
        shape([(160,94),(188,122),(160,170),(132,122)],color,(224,252,255),2)
        line([(132,122),(188,122)],(21,97,121),2)
        line([(160,94),(150,122),(160,170),(170,122),(160,94)],(21,97,121),2)
    elif f==4:
        for sign in [-1,1]:
            shape([(160-25*sign,104),(160-18*sign,104),(160+24*sign,158),(160+17*sign,163)],color,(255,226,226),1)
            line([(160+8*sign,157),(160+29*sign,141)],color,4)
            line([(160+20*sign,159),(160+28*sign,171)],(228,190,120),5)
    elif f==5:
        poly(star(cx,135,36,8),color,(242,227,255),2)
        poly(star(cx,135,19,5),(24,31,43))
    else:
        shape([(129,150),(122,111),(144,128),(160,101),(176,128),(198,111),(191,150)],color,(255,239,178),2)
        shape([(130,156),(190,156),(190,166),(130,166)],color)
        for x,y in [(122,111),(160,101),(198,111)]:
            circle(x,y,4,(255,240,185),3)
    for i in range(d):
        radius=8
        if phase=='new':
            radius *= max(.05,min(1,(elapsed-.25-i*.07)/.18))
        poly(star(160+(i-(d-1)/2)*23,224,radius),color)
    rng=random.Random(74)
    for i in range(28):
        a=rng.random()*math.tau
        speed=rng.uniform(17,48)
        age=(elapsed+i*.037)%2
        radius=78+age*speed
        x,y=cx+math.cos(a)*radius,cy+math.sin(a)*radius
        if 30<x<290 and 52<y<248:
            brightness=max(.15,1-age/2)
            line([(x,y),(x-math.cos(a)*4,y-math.sin(a)*4)],tuple(int(v*brightness) for v in color),2)
    text('PROMOTION' if promo else 'SEASON RANK',36,10,(147,164,185))
    label='RANK UP!' if phase=='new' and promo else ('RANK REACHED' if not promo else 'CHARGING')
    text(label,260,22,(245,248,251))
    text(FAMILIES[f].upper()+' '+ROMAN[d-1],287,15,color)
    if phase=='old':
        line([(110,242),(110+100*charge,242)],color,3)
    if promo and 1.4<t<1.75:
        strength=max(0,1-abs(t-1.55)/.2)
        image=Image.blend(image,Image.new('RGB',image.size,(247,252,255)),strength*.85)
    return image.resize((SIZE,SIZE),Image.Resampling.LANCZOS).quantize(colors=128)

def generate():
    OUT.mkdir(exist_ok=True)
    manifest=[]
    for index,rank in enumerate(RANKS):
        variants=[(None,False,name(rank)+'.gif')]
        if index>0:
            variants.append((RANKS[index-1],True,name(RANKS[index-1])+'-to-'+name(rank)+'.gif'))
        for old,promo,filename in variants:
            images=[frame(rank,old,i/FPS,promo) for i in range(FRAMES)]
            images[0].save(OUT/filename,save_all=True,append_images=images[1:],duration=DURATION,loop=0,optimize=True,disposal=2)
            manifest.append({'file':filename,'kind':'promotion' if promo else 'rank','rank':name(rank),'stars':rank[1],'from':name(old) if old else None,'duration_ms':5000})
            print(filename,flush=True)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    validate()

def validate():
    files=list(OUT.glob('*.gif'))
    assert len(files)==69, f'Expected 69 separate GIFs, got {len(files)}'
    expected={name(r)+'.gif' for r in RANKS}
    expected.update(name(a)+'-to-'+name(b)+'.gif' for a,b in zip(RANKS,RANKS[1:]))
    assert {p.name for p in files}==expected
    for path in files:
        with Image.open(path) as im:
            assert im.size==(320,320), path
            assert im.info.get('loop')==0, path
            frames=list(ImageSequence.Iterator(im))
            assert len(frames)==50, (path,len(frames))
            duration=sum(f.info.get('duration',0) for f in frames)
            assert duration==5000, (path,duration)
    print('Verified 69 separate GIFs, 320x320, 50 frames, exactly 5 seconds each.')

if __name__=='__main__':
    generate()
