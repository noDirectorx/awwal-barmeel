import numpy as np,os,json,base64
from PIL import Image
from scipy import ndimage as ni
A='/mnt/user-data/attachments/a43984e7-b446-5fa2-9fd4-fd5dfc8a4638/';D=os.path.dirname(os.path.abspath(__file__))+'/'
def load(i):
    a=np.array(Image.open(A+i+'-image.png').convert('RGBA'));r,g,b,al=[a[...,k].astype(int) for k in range(4)]
    fr=((r>170)&(g<70)&(b<70))|((r>215)&(g>195)&(b<90))|((g>r+15)&(g>b+25)&(g>90))
    lab,_=ni.label((al<=120)|fr);out=np.unique(lab[(al<=120)]);rem=np.isin(lab,out[out>0])
    a[...,3]=np.where(rem,0,255);return a
def small(arr,s):
    h,w=arr.shape[:2];W,H=max(1,round(w*s)),max(1,round(h*s));m=(arr[...,3]>0).astype('float32')
    rs=lambda c:np.array(Image.fromarray(c.astype('float32'),'F').resize((W,H),Image.BOX))
    am=rs(m);o=np.zeros((H,W,4),'uint8')
    for k in range(3):o[...,k]=np.clip(rs(arr[...,k]*m)/np.maximum(am,1e-3),0,255)
    o[...,3]=(am>.5)*255;return o
def save(o,n,q=64):
    im=Image.fromarray(o,'RGBA');p=np.array(im.convert('RGB').quantize(q,dither=Image.NONE).convert('RGBA'));p[...,3]=o[...,3]
    Image.fromarray(p,'RGBA').save(D+'px/'+n+'.png',optimize=True)
def nine(a,box,c,s,n,e=4,top=None):
    x0,y0,x1,y1=box;o=small(a[y0:y1,x0:x1],s);C=round(c*s);h,w=o.shape[:2];T=top if top is not None else C
    O=np.zeros((2*C+e,2*C+e,4),'uint8');my,mx=h//2,w//2
    O[:C,:C]=o[:C,:C];O[:C,-C:]=o[:C,-C:];O[-C:,:C]=o[-C:,:C];O[-C:,-C:]=o[-C:,-C:]
    O[:C,C:C+e]=o[:C,C+1:C+1+e];O[-C:,C:C+e]=o[-C:,C+1:C+1+e];O[C:C+e,:C]=o[C+1:C+1+e,:C];O[C:C+e,-C:]=o[C+1:C+1+e,-C:]
    O[C:C+e,C:C+e]=o[my:my+e,mx:mx+e];save(O,n);return C
kit=load('7d39d457');sc=load('532c698c');ic=load('c852558b');S={}
sc=np.array(Image.fromarray(sc,'RGBA').resize((2000,667),Image.NEAREST))
k0=kit.shape[1]/1536
if k0!=1:kit=np.array(Image.fromarray(kit,'RGBA').resize((1536,1024),Image.NEAREST))
S['panel']=nine(kit,(608,140,1006,348),66,1/3,'ui_panel')
S['gold']=nine(kit,(1092,422,1495,543),46,1/3,'ui_gold')
S['pressed']=nine(kit,(64,601,470,720),46,1/3,'ui_pressed')
S['wood']=nine(kit,(570,601,976,720),46,1/3,'ui_wood')
S['gray']=nine(kit,(1074,601,1488,720),46,1/3,'ui_gray')
S['red']=nine(kit,(64,757,470,880),46,1/3,'ui_red')
S['bar']=nine(kit,(66,929,496,998),24,1/3,'ui_barframe')
save(small(kit[942:984,602:1022],1/3),'ui_fill');save(small(kit[908:1006,1216:1326],.4),'ui_x')
S['frame']=nine(sc,(1456,40,1878,652),92,1/2.4,'ui_frame')
S['row']=nine(sc,(155,141,512,244),24,1/2,'ui_row')
save(small(sc[128:487,1484:1844],1/1.4),'ui_radar');save(small(sc[4:96,1590:1745],1/2.4),'ui_crown')
lg=load('e5007c97');ys,xs=np.where(lg[...,3]>0);lg=lg[ys.min():ys.max()+1,xs.min():xs.max()+1];save(small(lg,180/lg.shape[1]),'ui_logo',96)
names='wood stone water food empty oil coin ledger staff shield helmet wrench radar missile warn fire upgrade deal market map'.split()
H,W=ic.shape[:2]
for i,n in enumerate(names):
    r,c=i//5,i%5;cell=ic[int(r*H/4):int((r+1)*H/4),int(c*W/5):int((c+1)*W/5)];m=cell[...,3]>0;l,k=ni.label(m);sz=ni.sum(m,l,range(1,k+1));keep=np.isin(l,[j+1 for j,v in enumerate(sz) if v>.01*m.sum()]);ys,xs=np.where(keep)
    cc=cell[ys.min():ys.max()+1,xs.min():xs.max()+1].copy();cc[...,3]*=keep[ys.min():ys.max()+1,xs.min():xs.max()+1].astype('uint8');side=max(cc.shape[:2]);q=np.zeros((side,side,4),'uint8');y=(side-cc.shape[0])//2;x=(side-cc.shape[1])//2;q[y:y+cc.shape[0],x:x+cc.shape[1]]=cc
    save(small(q,48/side),'i_'+n)
json.dump(S,open(D+'px/ui.json','w'))
data={f[:-4]:'data:image/png;base64,'+base64.b64encode(open(D+'px/'+f,'rb').read()).decode() for f in os.listdir(D+'px') if f.endswith('.png')}
json.dump(data,open(D+'px/data.json','w'));print(S,sum(len(v) for v in data.values())//1024)
