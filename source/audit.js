const {chromium}=require('playwright');const fs=require('fs');
const wrap='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}[hidden]{display:none!important}</style></head><body>'+fs.readFileSync('audit.html','utf8')+'</body></html>';
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:390,height:800}})).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.route('http://g.test/',r=>r.fulfill({contentType:'text/html',body:wrap}));
await p.goto('http://g.test/');await p.getByRole('button',{name:'ابدأ القصة'}).click();await p.getByRole('button',{name:'تخطّي'}).click();await p.waitForTimeout(300);
const out=await p.evaluate(()=>{const g=window.__g,S=g.S(),log=[];let simT=0,lastM=-1,stall=0;
 const step=n=>{for(let i=0;i<n;i++){g.sim(.1);g.move(.1);simT+=.1}g.hud()};
 const goto_=t=>{S.px=t.x;S.py=t.y+ (t.hp!==undefined&&t.st?10:0)};
 for(let it=0;it<80000&&S.mi<g.M.length;it++){const m=g.curMission();if(!m)break;if(S.mi!==lastM){log.push(Math.round(simT/60*10)/10+'د '+m.t);lastM=S.mi;stall=0}stall++;if(stall>70000){log.push('STALL '+m.t+' | '+g.guide(m)[1]+' | '+JSON.stringify({w:S.wood,st:S.stone,m:S.money,e:S.empty,c:S.carry,sd:S.stored}));break}
  /* behave like a player: follow the game's own guidance */
  const q=g.guide(m),t=q[0];if(t){if(t.st!==undefined||t.hp!==undefined&&!t.n){S.px=t.x;S.py=t.y+6}else if((t===g.B.yard&&S.built.yard)||(t===g.B.dock&&S.built.dock)||(t===g.B.shop&&S.built.shop)){S.px=t.x;S.py=t.y+30}else{S.px=t.x;S.py=t.y}}
  /* office actions */
  if(m.t.startsWith('وظّف')&&S.money>=30){if(!S.apps.length)S.apps=g.newApps();const a=S.apps.shift();S.money-=30;a.role='haul';S.staff.push(a)}
  if(m.t.startsWith('ابن السور'))g.buildWall();if(m.t.startsWith('اصنع مطرقة'))g.makeHammer();
  if(m.t.startsWith('طوّر التخزين')||m.t.startsWith('وصّل'))g.upgradeTier();
  /* extra staff so late game moves, as a player would */
  if(S.mi>12&&S.staff.length<4&&S.money>200&&S.apps.length){const a=S.apps.shift();S.money-=30;a.role=['barrel','sell','wood','stone'][S.staff.length%4];S.staff.push(a)}
  if(S.pumpLvl<8&&S.built.pump&&S.money>400*Math.pow(2.6,S.pumpLvl)){S.money-=200*Math.pow(2.6,S.pumpLvl);S.pumpLvl++}
  if(S.fleetLvl<8&&S.contract&&S.money>600*Math.pow(2.6,S.fleetLvl)){S.money-=300*Math.pow(2.6,S.fleetLvl);S.fleetLvl++}
  S.fires={};g.dlgOff();step(3)}
 return {log,end:{mi:S.mi,total:g.M.length,mins:Math.round(simT/60),money:Math.round(S.money),stored:Math.round(S.stored),tier:S.tier,sold:Math.round(S.sold)}}});
console.log(out.log.join('\n'));console.log(out.end);console.log('errs',errs);await b.close()})().catch(e=>{console.error('FAIL',e.message);process.exit(1)});
