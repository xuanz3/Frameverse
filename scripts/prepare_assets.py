"""Curate and downscale supplied Zenless assets into compressed fan-archive visuals."""
from PIL import Image, ImageOps
from pathlib import Path
from collections import defaultdict
import re,json,os
ROOT=Path(__file__).resolve().parents[1]
SRC=Path('/mnt/data/zzz_assets')
OUT=ROOT/'media';OUT.mkdir(exist_ok=True)

def ffiles(sub):
    return sorted([p for p in (SRC/sub).rglob('*') if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg','.png','.webp'} and not p.name.startswith('._') and '__MACOSX' not in str(p)])

def save(p, name, size=1650, quality=83, contain=False):
    dst=OUT/(name+'.webp')
    with Image.open(p) as img:
        im=ImageOps.exif_transpose(img)
        im.thumbnail((size,size if contain else int(size*1.8)), Image.Resampling.LANCZOS) if contain else im.thumbnail((size,max(size,int(size*1.8))),Image.Resampling.LANCZOS)
        im.save(dst,'WEBP',quality=quality,method=5)
    return 'media/'+dst.name

wall=ffiles('wallpaper');cg=ffiles('cg');scenes=ffiles('scene');ui=ffiles('ui');boo=ffiles('bangboo')
wall_by={p.name:p for p in wall}
wall_order=['kv.159fab06..jpg','Key-Art_EN-scaled.jpg','dc0d33bb005fc4d03341775cd1f33f53350254366.png','kv.83046a05..jpg','kv.91aea658..jpg','6a297ab54110a134d35c2fefbdf1c7e5350254366.jpg']
wall_data=[]
for i,n in enumerate(wall_order):
    wall_data.append({'id':f'wall-{i+1:02d}','title':['AFTER THE STATIC','WELCOME TO NEW ERIDU','THE CITY IN MOTION','A DIFFERENT SIDE OF THE CITY','COLOUR IN THE NOISE','BEYOND THE HORIZON'][i], 'tag':['CINEMATIC','KEY ART','KEY ART','SPECTRUM','KEY ART','CITY LIGHTS'][i], 'image':save(wall_by[n],f'wall-{i+1:02d}',1800), 'original':n})

cg_data=[]
for i,p in enumerate(cg):
    name=p.stem
    title={'ChapterLighter_01':'A MOMENT OF HEAT','Imop00_01_01':'ON THE OTHER SIDE','S2Chapter7_03':'MIDNIGHT SIGNAL','S2Chapter7_04':'FRIENDS IN FRAME','S2Chapter7_05':'DREAMS IN MOTION','SayItWithFlowers_01':'A LETTER FROM THE CITY','Special2_01':'THE INNER FREQUENCY','Special3_01':'SOMEWHERE AFTER DARK','Summer2025_05':'SUMMER FRAGMENTS'}.get(name,name.replace('_',' ').upper())
    cg_data.append({'id':f'cg-{i+1:02d}','title':title,'episode':name.replace('_',' / '),'image':save(p,f'cg-{i+1:02d}',2000),'category': 'STORY' if name.startswith(('S2','Chapter','Imop')) else 'SPECIAL'})

# choose 3/4 per scene group. The scene folder names are unicode-escaped by zip metadata.
def decode(s):
    return re.sub(r'#U([0-9a-fA-F]{4})',lambda m:chr(int(m.group(1),16)),s)
SCENE_LABELS={'上午':'DAYLIGHT','下午':'AFTERNOON','夜晚':'AFTER DARK','黄昏':'GOLDEN HOUR','室内':'INTERIOR','材质':'DETAIL STUDY','物件':'STREET OBJECTS'}
scene_groups=defaultdict(list)
for p in scenes:
    parts=[decode(q) for q in p.relative_to(SRC/'scene').parts[:-1]]
    names=[x for x in parts if x in SCENE_LABELS]
    group=names[-1] if names else '其他'
    scene_groups[group].append(p)
scene_data=[]
# prioritize a mix of street and moody captures, rather than all 114 photographs
for group,seq in scene_groups.items():
    if group=='材质':count=2
    elif group=='物件': count=2
    else: count=4
    for p in seq[:count]:
        ix=len(scene_data)+1
        scene_data.append({'id':f'scene-{ix:02d}','title':('NEW ERIDU / '+str(ix).zfill(3)), 'tag':SCENE_LABELS.get(group,'CITY ARCHIVE'), 'category':group,'image':save(p,f'scene-{ix:02d}',1300,quality=78), 'original':p.name,'credit':'In-game scene · contributed screenshot'})

# decode Bangboo directory name; use first highest resolution image for each unique name
bang_g=defaultdict(list)
for p in boo:
    parts=p.relative_to(SRC/'bangboo').parts
    if len(parts)<4:continue
    rank=parts[1]
    if rank not in {'S','A'}:continue
    nm=decode(parts[2]); bang_g[(rank,nm)].append(p)
bang_data=[]
# S first, then A; keep 18 to maintain polished scope
for rank,name in sorted(bang_g, key=lambda x:(x[0]!='S',x[1]))[:22]:
    files=bang_g[(rank,name)]
    def area(p):
        with Image.open(p) as im:return im.width*im.height
    p=max(files,key=area)
    i=len(bang_data)+1
    bang_data.append({'id':f'bang-{i:02d}','name':name,'rank':rank,'image':save(p,f'bang-{i:02d}',620,quality=85,contain=True)})

role_files=sorted([p for p in ui if '角色卡' in str(p)])
# selected role-poster designs / translated tags are editorial visual labels, not game statistics
role_indices=[3,4,5,8,10,11,12,13,18,19,20,22]
role_names=['ANBY','AGENT FILE 02','PULCHRA','AGENT FILE 04','YIXUAN','TRIGGER','VIVIAN','AGENT FILE 08','PULCHRA / ALT','AGENT FILE 10','AGENT FILE 11','AGENT FILE 12']
role_data=[]
for i,(idx,title) in enumerate(zip(role_indices,role_names)):
    p=role_files[idx]
    with Image.open(p) as im:
        w,h=im.size
    role_data.append({'id':f'agent-{i+1:02d}','name':title,'subtitle':'VISUAL DOSSIER / '+str(i+1).zfill(2),'image':save(p,f'agent-{i+1:02d}',780,quality=84,contain=True),'aspect':round(w/h,2),'source':'ZZZ character card artwork'})

# Decorative cards and layouts curated from user-supplied UI archive
ui_posters=sorted([p for p in ui if any(k in str(p) for k in ['插画','节点海报','活动壁纸'])])
ui_more=sorted([p for p in ui if any(k in str(p) for k in ['过塑手账','官方物料'])])
ui_icons=sorted([p for p in ui if any(k in str(p) for k in ['音擎图鉴','驱动盘','邦布说明'])])
selections=[('ILLUSTRATION',ui_posters, [0,1,2,7,11,13,16,17,18,19]),('EDITORIAL',ui_more,[0,1,2,3,4,5,6,7]),('INTERFACE',ui_icons,[0,4,8,12,18,21,32,37])]
ui_data=[]
for tag,source,indices in selections:
    for index in indices:
        if index >= len(source): continue
        i=len(ui_data)+1
        p=source[index]
        ui_data.append({'id':f'ui-{i:02d}','title':tag+' / '+str(i).zfill(3), 'category':tag, 'image':save(p,f'ui-{i:02d}',1120,quality=77),'original':p.name})

result={'wallpapers':wall_data,'cg':cg_data,'scenes':scene_data,'bangboo':bang_data,'agents':role_data,'ui':ui_data}
(ROOT/'data'/'archive.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Processed:',{k:len(v) for k,v in result.items()})
print('Total media MB:',round(sum(p.stat().st_size for p in OUT.glob('*.webp'))/1e6,1))
