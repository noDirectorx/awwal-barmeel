import json,base64
d={k:'data:image/webp;base64,'+base64.b64encode(open(f'a/{k}.webp','rb').read()).decode() for k in ['menu_bg','q_truck','s_tire','q_barrel']}
s=open('drive_src.html',encoding='utf8').read().replace('/*ASSETS*/null',json.dumps(d));open('drive.html','w',encoding='utf8').write(s);print(len(s)//1024)
