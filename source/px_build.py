import json,os
D=os.path.dirname(os.path.abspath(__file__))+'/'
s=open(D+'px_game.html',encoding='utf8').read()
d=open(D+'px/data.json').read()
assert s.count('/*ASSETS*/null')==1
s=s.replace('/*ASSETS*/null',d)
open(D+'audit_src.html','w',encoding='utf8').write(s)
s=s.replace('/*TESTHOOK*/\n','')
open(D+'awwal-barmeel-px.html','w',encoding='utf8').write(s);print(len(s)//1024,'KB')
