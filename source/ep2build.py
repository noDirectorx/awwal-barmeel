import json,base64,os
m=json.load(open('meta.json'));d={}
for f in os.listdir('a'):
    if f.endswith('.webp'):d[f[:-5]]='data:image/webp;base64,'+base64.b64encode(open('a/'+f,'rb').read()).decode()
s=open('game.html',encoding='utf8').read()
c=open('ep2_ch.js',encoding='utf8').read()
def R(a,b):
    global s
    assert a in s,a[:60]
    s=s.replace(a,b,1)
R("const CH=[ch0,ch1,ch2,ch3,ch4,ch5,ch6];",c+"\nconst CH=[eSel,eMorning,eHide,eVisit,eMunira,eWeeks,eDrive,eMarket,eMubarak,eOpen,eEnd];")
R("KEY='awwal-barmeel-ep1'","KEY='awwal-barmeel-ep2test'")
R('<span class="k">الحلقة الأولى</span><span class="v" style="color:#f2b84b">بريال</span>','<span class="k">الحلقة الثانية</span><span class="v" style="color:#f2b84b">الزائر</span>')
R("<title>أول برميل</title>","<title>الحلقة الثانية: تجربة</title>")
# generic spots on the map
R(" for(const i of M.pick)look(i.x,i.y,120,()=>takeItem(i),'التقط: '+i.name);"," if(M.spots){for(const sp of M.spots){if(!sp.cond||sp.cond())look(sp.x,sp.y,sp.r,sp.fn,sp.label)}}else{for(const i of M.pick)look(i.x,i.y,120,()=>takeItem(i),'التقط: '+i.name);")
R(" look(M.npc.hamdan.x,M.npc.hamdan.y,135,talkHamdan,'كلّم حمدان');look(M.npc.mubarak.x,M.npc.mubarak.y,135,talkMubarak,'كلّم مبارك');look(M.npc.nasser.x,M.npc.nasser.y,145,talkNasser,'كلّم ناصر');"," look(M.npc.hamdan.x,M.npc.hamdan.y,135,talkHamdan,'كلّم حمدان');look(M.npc.mubarak.x,M.npc.mubarak.y,135,talkMubarak,'كلّم مبارك');look(M.npc.nasser.x,M.npc.nasser.y,145,talkNasser,'كلّم ناصر')}")
R("const v=inputVec(),SP=450,","if(M.tick)M.tick(dt);const v=inputVec(),SP=M.slow?290:450,")
R(" list.push({y:M.p.y,d(){drawWalker(X,M.p,cx,cy)}});"," if(M.barrel){M.barrel.r+=M.vx*.002;const b=img.o_barrel,w=b.width*.8,h=b.height*.8,px=M.p.x+(M.p.dir==='l'?-58:58),py=M.p.y+10;list.push({y:py,d(){X.save();X.translate(px-cx,py-h/2-cy);X.rotate(M.barrel.r);X.drawImage(b,-w/2,-h/2,w,h);X.restore()}})}\n list.push({y:M.p.y,d(){drawWalker(X,M.p,cx,cy)}});")
R("function nextPoint(){","function nextPoint(){if(M.spots){const q=M.spots.find(s=>!s.opt&&!['pump','nas','ham'].includes(s.k)&&(!s.cond||s.cond()));return q||null}")
R("function nextTarget(){","function nextTarget(){if(M.spots)return null;")
R(" if(S.drops>0)drawDrops(false);"," if(S.prop){const q=img[S.prop.k],h=q.height*S.prop.w/q.width;X.drawImage(q,S.prop.x-S.prop.w/2,S.prop.y-h,S.prop.w,h)}\n if(S.drops>0)drawDrops(false);")
R("if(S.mode==='menu'){Menu.upd(dt);Menu.draw()}else if","if(S.mode==='patch'){updPatch(dt);drawPatch()}else if(S.mode==='menu'){Menu.upd(dt);Menu.draw()}else if")
R("if(S.mode==='pipes')tapPipes(e);","if(S.onTap)S.onTap(e);else if(S.mode==='patch')tapPatch();else if(S.mode==='pipes')tapPipes(e);")
R("function cover(c,im){c.drawImage(im,0,0,W,H)}","function cover(c,im){if(Math.abs(im.width-im.height)<4){c.fillStyle='#120803';c.fillRect(0,0,W,H);c.drawImage(im,(W-H)/2,0,H,H)}else c.drawImage(im,0,0,W,H)}")
R(" drawDust();\n if(S.tint){"," if(S.over)S.over();\n drawDust();\n if(S.tint){")
R(" const t=nextPoint();if(t)edgeArrow"," if(M.night){X.fillStyle='rgba(12,18,60,.62)';X.fillRect(0,0,W,H)}\n const t=nextPoint();if(t)edgeArrow") if False else None
R("const fl=save.flags;if(fl.q1on&&!fl.q1)marker","const fl=save.flags;if(fl.q1on&&!fl.q1)marker")
R("const t=nextPoint();if(t)edgeArrow(t.x-cx,t.y-cy);","const t=nextPoint();if(t)edgeArrow(t.x-cx,t.y-cy);if(t&&M.spots)marker(t.x-cx,t.y-cy-95);/* on-screen objective */")
R(" if(S.tint&&S.bg!==img.bg_office_night){sun.a*=.15;"," if(m==='map'&&M.night){sun={x:W*.16,y:-40,r:W*.9,a:.16,c:'150,180,255'};warm='70,90,170';wa=.05;vig=.42}\n if(S.bg===img.bg_barrel1||S.bg===img.bg_barrel3){sun={x:390,y:150,r:620,a:.2,c:'255,180,90'};wa=.02;vig=.25;motesOn=false}/* night grade */\n if(S.tint&&S.bg!==img.bg_office_night){sun.a*=.15;")
R("c.drawImage(im,k*cw,0,cw,ch,-dw/2,-dh,dw,dh);c.restore()}","c.drawImage(im,k*cw,0,cw,ch,-dw/2,-dh,dw,dh);if(S.mode==='map'&&M.night){c.globalAlpha=.42;c.drawImage(sil('w_'+a.name),k*cw,0,cw,ch,-dw/2,-dh,dw,dh)}c.restore()}")
s=s.replace('/*ASSETS*/null',json.dumps(d)).replace('/*META*/null',json.dumps(m))
open('www/ep2t.html','w',encoding='utf8').write(s.replace('/*TESTHOOK*/','window.__g={M,S,PT,tapPatch,get save(){return save}};'))
open('ep2.html','w',encoding='utf8').write(s.replace('/*TESTHOOK*/\n',''));print(len(s)//1024)
