import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ni
A='art_raw/'
S={'salem':'ac2ab0e4','young':'f88da36b','old':'265d2f50','hamdan':'604f61d1','hero':'d8024ecf','nm':'4ac9bde6','parts':'03945519','walk':'11ef1f94','map':'fd7d9cd1','scrap':'62aac8b0'}
for n,i in S.items():
    a=np.array(Image.open(A+i+'-image.png').convert('RGBA')).astype(int)
    r,g,b,al=[a[...,k] for k in range(4)]
    m=(al>120)&~((g>150)&(r<140)&(b<140))
    m=ni.binary_opening(m,iterations=1)
    lab,c=ni.label(m);sz=ni.sum(m,lab,range(1,c+1));o=ni.find_objects(lab)
    bl=[(o[k][1].start,o[k][0].start,o[k][1].stop,o[k][0].stop) for k in range(c) if sz[k]>300]
    bl.sort(key=lambda t:(t[1]//120,t[0]))
    print(n,a.shape[:2],'alpha0',int((al<10).mean()*100),'blobs',len(bl),bl[:30])
