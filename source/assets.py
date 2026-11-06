import numpy as np,cv2,json,base64,io,os
from PIL import Image
from scipy import ndimage as ni
A='/mnt/user-data/attachments/a43984e7-b446-5fa2-9fd4-fd5dfc8a4638/'
OUT='a/';os.makedirs(OUT,exist_ok=True)
def L(i): return np.array(Image.open(A+i+'-image.png').convert('RGBA')).astype(int)
def key(a,minb=300,fr=False):
    r,g,b,al=[a[...,k] for k in range(4)]
    green=(g>135)&(g>r*1.35)&(g>b*1.35)
    fringe=((r>190)&(g<55)&(b<55))|((r>225)&(g>205)&(b<70))
    m=(al>120)&~green&~(fringe if fr else False)
    m=ni.binary_opening(m,iterations=1)
    lab,c=ni.label(m);sz=ni.sum(m,lab,range(1,c+1))
    return np.isin(lab,[k+1 for k in range(c) if sz[k]>minb]),lab
def despill(a,m):
    o=a.copy();e=m&~ni.binary_erosion(m,iterations=2)
    sp=e&(a[...,1]>a[...,0])&(a[...,1]>a[...,2])
    o[...,1][sp]=np.minimum(a[...,0],a[...,2])[sp];return o
def crop(a,m,box):
    x0,y0,x1,y1=box
    o=np.dstack([a[y0:y1,x0:x1,:3],(m[y0:y1,x0:x1]*255)]).astype('uint8')
    return Image.fromarray(o,'RGBA')
def charcoal(im):
    a=np.array(im).astype(float);r,g,b=a[...,0],a[...,1],a[...,2]
    v=a[...,:3].max(2);mn=a[...,:3].min(2);s=(v-mn)/np.maximum(v,1)
    z=(v<125)&(s<.62);gray=a[...,:3].mean(2)
    for k in range(3):a[...,k][z]=a[...,k][z]*.3+gray[z]*.7
    a[...,2][z]=a[...,2][z]*1.04
    return Image.fromarray(np.clip(a,0,255).astype('uint8'),'RGBA')
meta={}
def save(n,im,q=86,lossless=False):
    im.save(OUT+n+'.webp',quality=q,lossless=lossless,method=6);meta[n]=im.size
def bboxes(m,lab):
    o=ni.find_objects(lab);res=[]
    for k,s in enumerate(o):
        if s is None:continue
        if (lab[s]==k+1).sum()==0:continue
        if m[s][lab[s]==k+1].any():res.append((s[1].start,s[0].start,s[1].stop,s[0].stop))
    return res
# backgrounds
for n,i in dict(desert='0c23956f',gusher='0261b8ea',site='5ce9f162',office='6df3d61d').items():
    save('bg_'+n,Image.fromarray(L(i)[...,:3].astype('uint8')),q=86)
# menu: rope split from the desert scene
_d=L('0c23956f')[...,:3].astype('uint8');_c=_d.copy();_x0,_x1,_y0,_y1=812,850,508,772
for _y in range(_y0,_y1):
    _l=_d[_y,_x0-6:_x0].mean(0);_r=_d[_y,_x1:_x1+6].mean(0)
    for _x in range(_x0,_x1):
        _t=(_x-_x0)/(_x1-_x0);_c[_y,_x]=_l*(1-_t)+_r*_t
_al=(np.abs(_d[_y0:_y1,_x0:_x1].astype(int)-_c[_y0:_y1,_x0:_x1].astype(int)).sum(2)>38)
_al=ni.binary_closing(ni.binary_opening(_al,iterations=1),iterations=2)
save('menu_bg',Image.fromarray(_c),q=86)
save('menu_rope',Image.fromarray(np.dstack([_d[_y0:_y1,_x0:_x1],(_al*255).astype('uint8')]),'RGBA'),q=92);meta['menu_rope_at']=(_x0,_y0)
# portraits
PH=300
def portraits(name,i,names,rows=None,hero=False):
    a=L(i);m,lab=key(a,3000,fr=(name in('salem','young')));a=despill(a,m);bb=bboxes(m,lab)
    bb=[b for b in bb if rows(b)];bb.sort(key=lambda b:(round(b[1]/200),b[0]))
    assert len(bb)==len(names),(name,len(bb),bb)
    for b,n in zip(bb,names):
        im=crop(a,m,b)
        if hero:im=charcoal(im)
        s=PH/im.height;save(f'p_{name}_{n}',im.resize((round(im.width*s),PH),Image.BOX),q=88)
portraits('salem','ac2ab0e4',['tired','pain','shock','hope','firm','joy'],lambda b:True)
portraits('young','f88da36b',['neutral','smile','doubt','sly','laugh','serious'],lambda b:True)
low=lambda b:b[1]>600
portraits('old','265d2f50',['neutral','polite','cunning','surprised','angry'],low)
portraits('hamdan','604f61d1',['neutral','warm','worried','sad','angry'],low)
portraits('hero','d8024ecf',['neutral','firm','worried','angry','smile'],low,hero=True)
a=L('4ac9bde6');m,lab=key(a,3000);a=despill(a,m);bb=bboxes(m,lab)
for nm,y0,y1 in(('nasser',400,700),('mubarak',1200,1536)):
    r=sorted([b for b in bb if y0<=b[1]<y1],key=lambda b:b[0]);assert len(r)==3,(nm,r)
    for b,n in zip(r,['neutral','happy','angry']):
        im=crop(a,m,b);s=PH/im.height;save(f'p_{nm}_{n}',im.resize((round(im.width*s),PH),Image.BOX),q=88)
# walk strips: 9 frames [front a,s,b, back a,s,b, side(right) a,s,b]; feet at cell bottom, head centred
def strip(name,frames,hero=False):
    H=max(f.height for f in frames);W=max(f.width for f in frames)+24
    S=Image.new('RGBA',(W*9,H),(0,0,0,0))
    for k,f in enumerate(frames):
        arr=np.array(f)[...,3]>0;top=arr[:f.height//4];hx=np.where(top)[1].mean()
        x=round(W/2-hx);x=max(0,min(W-f.width,x));S.paste(f,(k*W+x,H-f.height),f)
    if hero:S=charcoal(S)
    k=1
    save('w_'+name,S,q=90);meta['w_'+name+'_cell']=(W*k,H*k)
a=L('781de63d');m,lab=key(a,1500);a=despill(a,m);bb=bboxes(m,lab);assert len(bb)==16
G={}
for b in bb:G[(int(((b[1]+b[3])/2)//(a.shape[0]/4)),int(((b[0]+b[2])/2)//(a.shape[1]/4)))]=b
fr=[crop(a,m,G[(0,c)]) for c in range(3)]+[crop(a,m,G[(1,c)]) for c in range(3)]+[crop(a,m,G[(2,c)]).transpose(Image.FLIP_LEFT_RIGHT) for c in range(3)]
strip('hero',fr,True)
a=L('11ef1f94');m,lab=key(a,700);a=despill(a,m);bb=bboxes(m,lab)
Hh,Ww=a.shape[:2];G={}
for b in bb:
    if b[3]-b[1]>400:continue
    G.setdefault((int(((b[1]+b[3])/2)//(Hh/7)),int(((b[0]+b[2])/2)//(Ww/9))),[]).append(b)
WALK=dict(salem='02ec4eeb',young='f1f1142a',old='d5f225d7',hamdan='ebc1e6ed',nasser='8752a95a',mubarak='54fb9a6a')
for nm,i in WALK.items():
    w=L(i);m2,lab2=key(w,1500);w=despill(w,m2);bx=bboxes(m2,lab2);assert len(bx)==16,(nm,len(bx))
    Gg={}
    for b_ in bx:Gg[(int(((b_[1]+b_[3])/2)//(w.shape[0]/4)),int(((b_[0]+b_[2])/2)//(w.shape[1]/4)))]=b_
    fs=[crop(w,m2,Gg[(0,c)]) for c in range(3)]+[crop(w,m2,Gg[(1,c)]) for c in range(3)]+[crop(w,m2,Gg[(2,c)]).transpose(Image.FLIP_LEFT_RIGHT) for c in range(3)]
    strip(nm,fs)
tr=sorted([b for b in bb if b[1]>940 and b[2]-b[0]>120],key=lambda b:b[0])
print('truck',tr)
for b,n in zip(tr,['front','back','side']):save('truck_'+n,crop(a,m,b),q=90)
tb=tr[2];tc=crop(a,m,tb);tw=tc.crop((40,72,102,129));ta=np.array(tw);yy,xx=np.mgrid[:ta.shape[0],:ta.shape[1]];ta[...,3]=np.where((xx-31)**2+(yy-28)**2<30**2,ta[...,3],0);save('s_tire',Image.fromarray(ta,'RGBA'),q=92)
# map
def seamless(arr,B=44):
    a=arr.astype(float);h,w=a.shape[:2]
    wx=np.linspace(0,1,B)[None,:,None];o=a[:,:w-B].copy();o[:,:B]=a[:,w-B:]*(1-wx)+a[:,:B]*wx
    wy=np.linspace(0,1,B)[:,None,None];p=o[:h-B].copy();p[:B]=o[h-B:]*(1-wy)+o[:B]*wy
    return p.astype('uint8')
a=L('fd7d9cd1');rgb=a[...,:3].astype('uint8')
for k,(n,x) in enumerate(zip(['sand','stones','dirt','road','curve','tee'],[32,322,613,903,1193,1483])):
    raw=rgb[34:288,x+2:x+256]
    if n=='sand':t=Image.fromarray(seamless(raw))
    elif n=='stones':
        yy,xx=np.mgrid[:254,:254];ed=np.minimum.reduce([yy,xx,253-yy,253-xx]);al=np.clip(ed/26,0,1)*255;t=Image.fromarray(np.dstack([raw,al.astype('uint8')]),'RGBA')
    else:t=Image.fromarray(raw)
    save('t_'+n,t,q=88)
rd=rgb[34:288,905:1159].astype(float)/255
bw=np.clip(1-np.abs(np.linspace(-1,1,254))/0.62,0,1)*5;bw=np.clip(bw,0,1)
save('t_band',Image.fromarray(np.dstack([rgb[34:288,905:1159],(np.tile(bw,(254,1))*255).astype('uint8')]),'RGBA'),q=88)
m,lab=key(a,300);a=despill(a,m)
O=dict(office=(29,364,297,615),tanks=(337,394,547,607),pump=(576,337,903,615),shed=(919,371,1206,609),fence=(1242,419,1460,552),gate=(1500,417,1735,552),barrel=(60,720,139,846),barrels=(215,678,361,846),crate=(432,719,558,846),pipes=(613,698,788,846),marker=(845,736,986,838),rock=(1040,732,1192,838),pebble=(1245,768,1322,822),shrub=(1376,732,1484,828),scrappile=(1538,710,1722,841))
for n,b in O.items():save('o_'+n,crop(a,m,b),q=90)
# Munira (temporary: standing poses until her walk sheet arrives)
_a=L('0051108d');_m,_l=key(_a,3000);_a=despill(_a,_m);_bb=bboxes(_m,_l)
_low=sorted([b for b in _bb if b[1]>600],key=lambda b:b[0]);_top=sorted([b for b in _bb if b[1]<600],key=lambda b:b[0])
for _b,_n in zip(_low,['neutral','firm','annoyed','worried','smile']):
    _i=crop(_a,_m,_b);_s=PH/_i.height;save(f'p_munira_{_n}',_i.resize((round(_i.width*_s),PH),Image.BOX),q=88)
def walk4(i):
    w=L(i);m2,lab2=key(w,1500);w=despill(w,m2);bx=bboxes(m2,lab2);assert len(bx)==16,len(bx)
    G2={}
    for b_ in bx:G2[(int(((b_[1]+b_[3])/2)//(w.shape[0]/4)),int(((b_[0]+b_[2])/2)//(w.shape[1]/4)))]=b_
    return [crop(w,m2,G2[(0,c)]) for c in range(3)]+[crop(w,m2,G2[(1,c)]) for c in range(3)]+[crop(w,m2,G2[(2,c)]).transpose(Image.FLIP_LEFT_RIGHT) for c in range(3)]
strip('munira',walk4('9248cde5'));strip('oldnh',walk4('fb5accaa'))
# Episode 2 art
for _n,_i in dict(market='eb99eb29',workshop='a0b66145').items():save('bg_'+_n,Image.fromarray(L(_i)[...,:3].astype('uint8')),q=86)
save('bg_office_night',Image.fromarray(L('df303adb')[...,:3].astype('uint8')),q=88);save('bg_barrel1',Image.fromarray(L('7c8d6d20')[...,:3].astype('uint8')),q=88);save('bg_barrel3',Image.fromarray(L('0e00ee81')[...,:3].astype('uint8')),q=88)
_t=L('f9ffa46d');_mt,_=key(_t,1500);_t=despill(_t,_mt);save('q_truck',crop(_t,_mt,(74,223,1323,668)),q=92);save('q_barrel',crop(_t,_mt,(1523,485,1699,700)),q=92)
_it=L('c8093133');_mi,_=key(_it,800);_it=despill(_it,_mi)
for _n,_b in dict(tarp=(20,84,350,333),rope=(391,78,694,342),radio=(755,50,1081,341),antenna=(1173,39,1391,342),speaker=(50,410,337,701),knob=(436,438,641,639),receipts=(745,392,1011,694),notebook=(1104,399,1411,694),stone=(1120,732,1407,1051),tape=(20,777,333,1023),box=(375,760,694,1032),helmet=(728,765,1086,1025)).items():save('i_'+_n,crop(_it,_mi,_b),q=90)
# office without the barrel (Episode 2, hidden path)
save('bg_office_empty',Image.fromarray(L('fb42533c')[...,:3].astype('uint8')),q=86);meta['office_stand']=(1365,566)
# tank patch scene
_tk=L('02b74886')[...,:3].astype('uint8');save('bg_tank',Image.fromarray(_tk),q=88)
for _n,_b in zip(['p1','p2','p3'],[(190,632,525,748),(605,634,1065,750),(1142,632,1480,748)]):
    _c=_tk[_b[1]:_b[3],_b[0]:_b[2]].astype(int);_sandm=(_c[...,0]>205)&(_c[...,1]>125)&(_c[...,2]<120)
    _lb,_cn=ni.label(~_sandm);_sz=ni.sum(~_sandm,_lb,range(1,_cn+1));_big=_lb==(int(np.argmax(_sz))+1);_big=ni.binary_fill_holes(_big)
    save('tp_'+_n,Image.fromarray(np.dstack([_c.astype('uint8'),(_big*255).astype('uint8')]),'RGBA'),q=92);meta['tp_'+_n+'_at']=(_b[0],_b[1])
# real wheel art
_w=L('b31563f7');print('wheel alpha0',int((_w[...,3]<10).mean()*100));_mw=_w[...,3]>120;_ys,_xs=np.where(_mw);_wi=crop(_w,_mw,(int(_xs.min()),int(_ys.min()),int(_xs.max())+1,int(_ys.max())+1));_wn=np.array(_wi.resize((128,128),Image.LANCZOS));_yy,_xx=np.mgrid[:128,:128];_wn[...,3]=np.where((_xx-63.5)**2+(_yy-63.5)**2<64**2,_wn[...,3],0);save('s_tire',Image.fromarray(_wn,'RGBA'),q=92)
# parts
a=L('03945519');m,lab=key(a,300);a=despill(a,m)
for n,b in dict(head=(135,311,348,653),rod=(481,327,552,628),weight=(684,311,930,653),belt=(1013,421,1283,546),valve=(1362,380,1540,587)).items():save('q_'+n,crop(a,m,b),q=92)
# scrap + letter
a=L('62aac8b0');m,lab=key(a,300);a=despill(a,m)
for n,b in dict(s1=(53,88,273,303),s2=(317,74,548,310),s3=(593,70,836,305),s4=(892,74,1097,303),s5=(1143,99,1371,279),s6=(1416,88,1621,297),letter=(364,398,1308,897)).items():save('s_'+n,crop(a,m,b),q=90)
# pump board: split the walking beam and polished rod out, inpaint behind them
a=L('4421752f')[...,:3].astype('uint8');bgr=a[...,::-1].copy()
beam=np.array([[345,92],[432,108],[1142,236],[1128,325],[1122,385],[1045,385],[1040,325],[425,212],[418,245],[345,240]],np.int32)
pm=np.zeros(a.shape[:2],'uint8');cv2.fillPoly(pm,[beam],1)
g=np.where(cv2.dilate(pm,np.ones((3,3),'uint8'))>0,cv2.GC_PR_FGD,cv2.GC_BGD).astype('uint8')
g[cv2.erode(pm,np.ones((25,25),'uint8'))>0]=cv2.GC_FGD
bm=np.zeros((1,65));fm=np.zeros((1,65));cv2.grabCut(bgr,g,None,bm,fm,4,cv2.GC_INIT_WITH_MASK)
bmask=((g==1)|(g==3))
bmask=ni.binary_fill_holes(ni.binary_closing(bmask,iterations=2))
# saddle stays on top of the beam
yy,xx=np.mgrid[:a.shape[0],:a.shape[1]]
saddle=(((xx-735)**2+(yy-247)**2<43**2)|((xx>693)&(xx<778)&(yy>=247)&(yy<285)))
prodk=((xx>=374)&(xx<=396)&(yy>=272)&(yy<=570))|((xx>=361)&(xx<=409)&(yy>=236)&(yy<=276))
hole=(cv2.dilate(pm,np.ones((27,27),'uint8'))>0)|(cv2.dilate(prodk.astype('uint8'),np.ones((13,13),'uint8'))>0)|(cv2.dilate(bmask.astype('uint8'),np.ones((9,9),'uint8'))>0)
hole&=~((xx>655)&(xx<814)&(yy>=284))
hole&=~(yy>=563)
hole&=~saddle
clean=a.copy()
for y in range(a.shape[0]):
    xs=np.where(hole[y])[0]
    if not len(xs):continue
    l,r=xs[0]-1,xs[-1]+1
    L_=a[y,max(l-5,0):max(l,1)].mean(0);R_=a[y,r:r+5].mean(0)
    for x in xs:
        t=(x-l)/max(r-l,1);clean[y,x]=L_*(1-t)+R_*t
save('pump_bg',Image.fromarray(clean),q=88)
def sprite(n,mask):
    ys,xs=np.where(mask);x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
    o=np.dstack([a[y0:y1,x0:x1],(mask[y0:y1,x0:x1]*255).astype('uint8')]);save(n,Image.fromarray(o,'RGBA'),q=92);meta[n+'_at']=(int(x0),int(y0))
sprite('pump_beam',bmask);sprite('pump_saddle',saddle&(ni.binary_dilation(pm)|True));sprite('pump_prod',prodk)
json.dump(meta,open('meta.json','w'))
print(len(meta),sum(os.path.getsize(OUT+f) for f in os.listdir(OUT))//1024,'KB')
# review sheets
c=Image.new('RGB',(1672,941),(120,120,120));c.paste(Image.open(OUT+'pump_bg.webp'),(0,0));c.save('rv_pump_bg.png')
v=Image.new('RGB',(1672,941),(40,120,200));b=Image.open(OUT+'pump_beam.webp');v.paste(b,tuple(meta['pump_beam_at']),b);s=Image.open(OUT+'pump_saddle.webp');p=Image.open(OUT+'pump_prod.webp');v.paste(p,tuple(meta['pump_prod_at']),p);v.save('rv_beam.png')
W=Image.new('RGB',(1500,1000),(236,186,118));y=0
for n in ['hero','salem','young','old','hamdan','nasser','mubarak']:
    im=Image.open(OUT+'w_'+n+'.webp');s=130/im.height;i=im.resize((round(im.width*s),130),Image.BOX);W.paste(i,(0,y),i);y+=135
W.save('rv_walk.png')
