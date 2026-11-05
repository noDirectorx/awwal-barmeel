import json,base64,os
m=json.load(open('meta.json'));d={}
for f in os.listdir('a'):
    if f.endswith('.webp'):d[f[:-5]]='data:image/webp;base64,'+base64.b64encode(open('a/'+f,'rb').read()).decode()
s=open('game.html',encoding='utf8').read()
s=s.replace('/*ASSETS*/null',json.dumps(d)).replace('/*META*/null',json.dumps(m))
open('test.html','w',encoding='utf8').write(s.replace('/*TESTHOOK*/','window.__g={S,M,B,PZ,JK,ROOM,SOL,checkPipes,tapJack,findSecret,get meta(){return meta},get save(){return save},tryPlace,jump:(n)=>{run(n)}};'))
open('awwal-barmeel.html','w',encoding='utf8').write(s.replace('/*TESTHOOK*/\n',''))
print(len(s)//1024,'KB')
