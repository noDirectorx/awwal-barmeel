const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const vw=+process.argv[2]||1180,vh=+process.argv[3]||820,pick=+process.argv[4]||0,tag=process.argv[5]||'ipad';
const b=await chromium.launch();const c=await b.newContext({viewport:{width:vw,height:vh},hasTouch:false});const p=await c.newPage();const errs=[];
p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'&&!/fonts|ERR_/.test(m.text()))errs.push(m.text())});
await p.goto('file://'+process.cwd()+'/test.html');await p.waitForFunction('window.__ready',{timeout:60000});
fs.mkdirSync('shots',{recursive:true});let n=0;const shot=async s=>{await p.screenshot({path:`shots/${tag}_${String(n++).padStart(2,'0')}_${s}.png`})};
await p.waitForTimeout(300);await shot('title');await p.click('#go');
let seen=new Set(),t0=Date.now(),boarded=false,mapped=false,log=[];
while(Date.now()-t0<400000){
 const st=await p.evaluate(()=>({mode:__g.S.mode,dlg:!document.querySelector('#dlg').hidden,txt:document.querySelector('#dlg span').textContent,cho:!document.querySelector('#choices').hidden,card:document.querySelector('#card').hidden?'':document.querySelector('#card').textContent,letter:!document.querySelector('#letter').hidden,title:!document.querySelector('#title').hidden,ch:__g.save.ch,t:document.querySelector('#title').textContent}));
 if(st.title&&st.t.includes('نهاية')){await shot('end');log.push('END '+st.t);break}
 if(st.card&&!seen.has(st.card)){seen.add(st.card);await p.waitForTimeout(700);await shot('card');}
 if(st.cho){await p.waitForTimeout(150);await shot('choice');const bs=await p.$$('#choices .btn');await bs[pick].click();await p.waitForTimeout(100);continue}
 if(st.letter){await p.waitForTimeout(6000);await shot('letter');await p.click('#letter');continue}
 if(st.dlg){const k=await p.evaluate(()=>document.querySelector('#dlg b').textContent+document.querySelector('#dlg span').textContent);
   await p.waitForTimeout(500);const full=await p.evaluate(()=>document.querySelector('#dlg span').textContent);if(!seen.has(full)&&seen.size<200){seen.add(full);await p.mouse.click(vw/2,vh-30);await p.waitForTimeout(60);await shot('dlg');log.push(await p.evaluate(()=>document.querySelector('#dlg span').textContent))}
   await p.mouse.click(vw/2,vh-30);await p.waitForTimeout(40);continue}
 if(st.mode==='map'){
  if(!mapped){mapped=true;await p.waitForTimeout(800);await shot('map_start');
    // real movement test: walk with mouse drag
    const x0=await p.evaluate(()=>[__g.M.p.x,__g.M.p.y]);await p.mouse.move(vw/2,vh/2);await p.mouse.down();await p.mouse.move(vw/2-60,vh/2,{steps:4});await p.waitForTimeout(1200);await shot('map_walk');await p.mouse.up();const x1=await p.evaluate(()=>[__g.M.p.x,__g.M.p.y]);log.push('walk '+x0+' -> '+x1);
  }
  const go=async(x,y)=>{await p.evaluate(([x,y])=>{__g.M.p.x=x;__g.M.p.y=y},[x,y]);await p.waitForTimeout(150);};
  const act=async()=>{await p.waitForSelector('#act:not([hidden])',{timeout:3000});await p.click('#act');await p.waitForTimeout(100)};
  const f=()=>p.evaluate(()=>({...__g.save.flags,picks:__g.M.pick.map(i=>[i.x,i.y])}));
  let fl=await f();
  if(!fl.metMubarak){await go(1480,1290);await act();continue}
  if(fl.picks.length){const[i,j]=fl.picks[0];await go(i,j+40);if(fl.picks.length==9)await shot('near_item');await act();continue}
  if(!fl.sold){await go(2130,2120);await shot('near_nasser');await act();continue}
  await go(1480,1290);await act();continue}
 if(st.mode==='board'&&!boarded){boarded=true;await p.waitForTimeout(900);await shot('board');
  const r=await p.evaluate(()=>{const r=document.querySelector('#c').getBoundingClientRect();return{l:r.left,t:r.top,s:r.width/1672}});
  const parts=await p.evaluate(()=>__g.B.list.map(q=>[q.hx,q.hy,q.tx,q.ty]));
  for(const q of parts){await p.mouse.move(r.l+q[0]*r.s,r.t+q[1]*r.s);await p.mouse.down();await p.mouse.move(r.l+q[2]*r.s,r.t+q[3]*r.s,{steps:6});await p.mouse.up();await p.waitForTimeout(200)}
  await shot('board_full');const h=await (await p.$('#hold')).boundingBox();await p.mouse.move(h.x+h.width/2,h.y+h.height/2);await p.mouse.down();await p.waitForTimeout(1600);await p.mouse.up();
  await p.waitForTimeout(700);await shot('run1');await p.waitForTimeout(500);await shot('run2');await p.waitForTimeout(500);await shot('run3');continue}
 await p.waitForTimeout(80);
}
console.log('errors',errs);console.log(log.slice(-4).join('\n'));console.log('elapsed',(Date.now()-t0)/1000,'shots',n);await b.close()})();
