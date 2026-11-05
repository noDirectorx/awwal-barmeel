import numpy as np, json, base64, io, os
from PIL import Image
from scipy import ndimage as ni
A='/mnt/user-data/attachments/a43984e7-b446-5fa2-9fd4-fd5dfc8a4638/'
D=os.path.dirname(os.path.abspath(__file__))+'/'
# id, name, art-pixel width
L=[('edde3552','sapling',26),('3a224814','acacia',84),('0a40afe6','well',54),('532e440d','stump',28),
('13048d55','rock',46),('6747b60b','derrick',84),('45ec5ab4','palm',46),('7d6bd4d8','shop',72),('53f05066','hut',76),
('ecda1b83','house',92),('6bcc634d','office',88),('12d1d2d4','tank1',46),('43042339','farm',118),('7980471d','tank2',60),
('28f6d7e3','yard',96),('2930ce29','transport',124),('00228770','tank3',78),('f7e1c3fc','radar',74),('701dffc0','security',62),
('ca666189','dock',88),('d0c67228','fire',94),('d69ff51e','tank4',112),('efb48b24','forklift',42),('94ac3cdd','defense',82),
('e9efe724','p_nasser',128),('69229b29','p_abu',128),('d4a79724','p_abdullah',128),('389cbfe3','p_khawaja',128),('cdaab2f5','jeep',58),('7ad0b347','camel',54),('15c1d0ce','sheep',20),('707ed8dc','kitchen',100),('09984c0a','billboard',66),('e882889e','wall1',192),('efdfe95e','cow',32),('bd0523d4','wall2',192),('71ad573c','pump',62),('7c172806','nursery',72),('0f1790ff','gate',60),('75fe4be9','derrick2',90),('38baadac','dock2',98),('b32a2af6','office2',94),('f67f553f','hut2',78),('fece9628','shop2',84)]
def load(i): return np.array(Image.open(A+i+'-image.png').convert('RGBA')).astype(np.int32)
def process(i,name,tw):
    a=load(i); r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
    if name=='sapling':                       # came on a white background
        wh=(r>238)&(g>238)&(b>238); lab,_=ni.label(wh); ed=np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]); al=np.where(np.isin(lab,ed[ed>0]),0,255); dk=(r<26)&(g<26)&(b<26); l2,_=ni.label(dk); e2=np.unique(np.r_[l2[0],l2[-1],l2[:,0],l2[:,-1]]); al=np.where(np.isin(l2,e2[e2>0]),0,al)
    if name=='farm':                          # white matte painted inside the fence
        al=np.where((r>222)&(g>222)&(b>215),0,al)
    if name=='office':                        # replace the national emblem on the banner with plain cloth
        yy,xx=np.mgrid[:a.shape[0],:a.shape[1]]; reg=(xx>462)&(xx<592)&(yy>705)&(yy<815)
        m=reg&(r>170)&(g>120)&(b<140); a[...,0][m]=163;a[...,1][m]=42;a[...,2][m]=48
    fringe=((r>190)&(g<55)&(b<55))|((r>225)&(g>205)&(b<70))
    mask=(al>120)&~fringe
    mask=ni.binary_opening(mask,iterations=1)
    lab,n=ni.label(mask); sz=ni.sum(mask,lab,range(1,n+1)); mask=np.isin(lab,[k+1 for k,s in enumerate(sz) if s>.004*mask.sum()])
    ys,xs=np.where(mask); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    rgb=a[y0:y1,x0:x1,:3].astype(float); m=mask[y0:y1,x0:x1].astype(float)
    tw2=tw; th=max(1,round((y1-y0)*tw/(x1-x0)))
    def rs(c): return np.array(Image.fromarray(c.astype('float32'),'F').resize((tw2,th),Image.BOX))
    am=rs(m); out=np.zeros((th,tw2,4),'uint8')
    for k in range(3): out[...,k]=np.clip(rs(rgb[...,k]*m)/np.maximum(am,1e-3),0,255)
    out[...,3]=(am>.5)*255
    im=Image.fromarray(out,'RGBA')
    q=im.convert('RGB').quantize(48,method=Image.MEDIANCUT,dither=Image.NONE).convert('RGB')
    o=np.array(q.convert('RGBA'));o[...,3]=out[...,3]
    return Image.fromarray(o,'RGBA')
res={}
os.makedirs(D+'px',exist_ok=True)
for i,n,w in L:
    im=process(i,n,w); im.save(D+f'px/{n}.png',optimize=True); res[n]=im
# sand: use the clean top part (the tile has a seam near the middle), calm it, tile it
s=np.array(Image.open(A+'33a4051b-image.png').convert('RGB')).astype(float)[:600,:600]
s=np.array(Image.fromarray(s.astype('uint8')).resize((200,200),Image.BOX)).astype(float)
B=20
wx=np.linspace(0,1,B)[None,:,None];o=s[:,:200-B].copy();o[:,:B]=s[:,200-B:]*(1-wx)+s[:,:B]*wx
wy=np.linspace(0,1,B)[:,None,None];p=o[:200-B].copy();p[:B]=o[200-B:]*(1-wy)+o[:B]*wy
base=np.array([236,186,118.]);p=base+(p-p.mean((0,1)))*.34
q=Image.fromarray(np.clip(p,0,255).astype('uint8')).quantize(8,dither=Image.NONE).convert('RGB');q.save(D+'px/sand.png',optimize=True)
def tile(fid,out,size,base,calm,n=8):
    s=np.array(Image.open(A+fid+'-image.png').convert('RGB').resize((size+24,size+24),Image.BOX)).astype(float);B=24;S=size+24
    wx=np.linspace(0,1,B)[None,:,None];o=s[:,:S-B].copy();o[:,:B]=s[:,S-B:]*(1-wx)+s[:,:B]*wx
    wy=np.linspace(0,1,B)[:,None,None];p=o[:S-B].copy();p[:B]=o[S-B:]*(1-wy)+o[:B]*wy
    p=np.array(base,float)+(p-p.mean((0,1)))*calm
    Image.fromarray(np.clip(p,0,255).astype('uint8')).quantize(n,dither=Image.NONE).convert('RGB').save(D+'px/'+out+'.png',optimize=True)
tile('2524b0d6','earth',180,[214,158,100],.72)
tile('25bbee41','road',96,[168,116,74],.6)
data={f[:-4]:'data:image/png;base64,'+base64.b64encode(open(D+'px/'+f,'rb').read()).decode() for f in os.listdir(D+'px') if f.endswith('.png')}
json.dump(data,open(D+'px/data.json','w'))
print(sum(len(v) for v in data.values())//1024,'KB')
# contact sheet at 2x on sand
sh=Image.new('RGB',(1500,1000),(236,186,118));x=y=rowh=0
for i,n,w in L:
    im=res[n];z=im.resize((im.width*2,im.height*2),Image.NEAREST)
    if x+z.width>1500:x=0;y+=rowh+4;rowh=0
    sh.paste(z,(x,y),z);x+=z.width+6;rowh=max(rowh,z.height)
sh.save(D+'px_sheet.png')
