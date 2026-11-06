import numpy as np,json
from PIL import Image
from scipy import ndimage as ni
A='art_raw/'
for n,i,mn in [('munira','56874955',1500),('truck','f9ffa46d',1500),('items','c8093133',800)]:
    a=np.array(Image.open(A+i+'-image.png').convert('RGBA')).astype(int);r,g,b=a[...,0],a[...,1],a[...,2]
    m=~((g>135)&(g>r*1.35)&(g>b*1.35));m=ni.binary_opening(m,iterations=1);lab,c=ni.label(m);sz=ni.sum(m,lab,range(1,c+1));o=ni.find_objects(lab)
    bb=sorted([(s[1].start,s[0].start,s[1].stop,s[0].stop) for k,s in enumerate(o) if sz[k]>mn],key=lambda t:(t[1]//250,t[0]))
    print(n,a.shape[:2],len(bb),bb[:14])
    # lingering green on kept pixels
    print(' green left',int(((g>r*1.2)&(g>b*1.2)&m).sum()))
for n,i in [('market','eb99eb29'),('workshop','a0b66145'),('barrel','e5b52726')]:
    print(n,Image.open(A+i+'-image.png').size)
