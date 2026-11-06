NAMES.munira='منيرة';
function e0(){return (async()=>{})()}
async function eSel(){S.mode='none';S.fade=1;const r=await choose('تجربة: كيف انتهت الحلقة الأولى؟',[{t:'دفعت الرواتب',s:'مبارك معك، والتسريب مستمر'},{t:'أصلحت الخزان، ومبارك أخذ ألفين',s:'عطاك فرصة أخيرة'},{t:'أصلحت الخزان، وطلع مبارك',s:'بدون ألفين'}]);const f=save.flags;f.decision=r?1:0;f.mubarakAdvance=r===1?1:0;f.mubarakLeft=r===2?1:0;store.put()}
async function eMorning(){S.mode='cine';startScene();setBg('site');S.bars=1;S.fade=1;A.music('music_tension',.5);A.ambience({amb_wind:.4,amb_site:.2});await card('صباح اليوم التالي',1000);
 const h=actor('hero',760,780,290),m=actor('hamdan',1040,770,275);h.dir='r';m.dir='l';await fadeTo(0,800);
 await say('hamdan','worried','الخواجة جاي قبل الظهر. ذاك اليوم ما خليته لحاله في المكتب، واليوم يبغى يشوف البرميل قدامك.');
 await say('hero','neutral','وش يبغى في برميل قديم؟');
 await say('hamdan','neutral','ما عمره زارنا إلا وعينه عليه.');
 if(!save.flags.mubarakLeft){const b=actor('mubarak',1240,790,285);b.dir='l';await say('mubarak','neutral','وفتحه يبغى عدة ما عندنا، وثمنها ما يجي إلا مع حساب الشهر.')}
 else await say('hamdan','sad','وفتحه يبغى واحد يعرف له، وعدة ما عندنا. وثمنها ما يجي إلا مع حساب الشهر.');
 const r=await choose('وش تسوي بالبرميل؟',[{t:'تخليه مكانه',s:'وتواجه الخواجة'},{t:'تخبيه في المظلة',s:'وتعطله لين تخلص'}]);save.flags.hid=r;store.put();await fadeTo(1,600)}
async function eHide(){if(!save.flags.hid)return;S.mode='map';setView(true);startScene();A.music('music_tension',.4);A.ambience({amb_wind:.4,amb_site:.15});M.leaving=false;buildMap();M.pick=[];
 const f=save.flags,P=M.p;P.x=2900;P.y=1600;P.dir='f';M.cam.x=clamp(P.x-W/2,0,MW-W);M.cam.y=clamp(P.y-H/2,0,MH-H);M.lock=false;$('#hud').hidden=false;
 const K={name:'old',x:10*TS+96,y:2240,h:108,dir:'b',step:0,moving:true,dist:0};M.npc.old=K;M.barrel=null;M.slow=false;
 let got={tarp:0,rope:0,carry:0},hold=0,done=false,res;
 const task=()=>{$('#tasks').innerHTML=`<b>خبّ البرميل قبل ما يوصل</b><div class="${got.tarp?'done':''}">جيب الغطاء من عند الخزان</div><div class="${got.rope?'done':''}">جيب الحبل من عند البراميل</div><div class="${got.carry?'done':''}">دحرج البرميل من المكتب</div><div>نزّله في المظلة</div>`;$('#stat').textContent='عطّل الخواجة لو احتجت'};
 const useDelay=(k,t)=>{hold+=13;A.play('fx_assemble',.5);toast(t);M.spots=M.spots.filter(s=>s.k!==k)};
 M.spots=[{k:'tarp',x:3280,y:1240,r:170,label:'خذ الغطاء',fn(){got.tarp=1;A.play('fx_pickup',.9);M.spots=M.spots.filter(s=>s.k!=='tarp');task()}},
 {k:'rope',x:1240,y:1500,r:170,label:'خذ الحبل',fn(){got.rope=1;A.play('fx_pickup',.9);M.spots=M.spots.filter(s=>s.k!=='rope');task()}},
 {k:'barrel',x:2900,y:1590,r:150,label:'دحرج البرميل',cond:()=>got.tarp&&got.rope,fn(){got.carry=1;M.slow=true;M.barrel={r:0};A.play('fx_assemble',.7);M.spots=M.spots.filter(s=>s.k!=='barrel');task()}},
 {k:'shed',x:760,y:1500,r:180,label:'نزّله في المظلة',cond:()=>got.carry,fn(){done=true;A.play('fx_assemble');res&&res()}},
 {k:'pump',x:1560,y:1290,r:150,label:'طفّ المضخة',fn(){useDelay('pump','الخواجة وقف يسأل وش صار')}},
 {k:'nas',x:2190,y:2120,r:150,label:'خل ناصر يقطع الطريق',fn(){useDelay('nas','ناصر: يا مرحبا مستر! الشاحنة تعطلت. ثواني بس!')}},
 {k:'ham',x:2660,y:1620,r:140,label:f.mubarakLeft?'خل حمدان يسأله':'خل مبارك يسأله',fn(){useDelay('ham','سؤال عن العقد عطّله شوي')}}];
 task();toast('دحرج البرميل بعد ما تجمع الغطاء والحبل');
 M.tick=(dt)=>{if(hold>0){hold-=dt;K.moving=false;return}const tx=2900,ty=1620,dx=tx-K.x,dy=ty-K.y,d=Math.hypot(dx,dy);if(d<20){if(res)res();return}K.moving=true;const sp=46;K.x+=dx/d*sp*dt;K.y+=dy/d*sp*dt;K.dist+=sp*dt;K.step=Math.floor(K.dist/30);K.dir=Math.abs(dx)>Math.abs(dy)?(dx>0?'r':'l'):(dy>0?'f':'b')};
 await fadeTo(0,500);await new Promise(r=>res=r);M.tick=null;M.spots=null;M.slow=false;M.barrel=null;delete M.npc.old;A.walk(false);f.caught=done?0:1;store.put();await fadeTo(1,500);$('#hud').hidden=true;$('#act').hidden=true;S.mode='none';setView(false)}
async function eVisit(){const f=save.flags;S.mode='cine';startScene();setBg(f.hid?'office_empty':'office');S.bars=1;S.fade=1;A.music('music_tension',.6);A.ambience({amb_room:.5});
 const o=actor('old',420,840,330),e=actor('hero',1240,860,340);o.dir='r';e.dir='l';await fadeTo(0,700);
 if(!f.hid){await say('old','cunning','ملحوم. حتى أنت ما تدري وش فيه؟');
  const r=await timedChoice('وش ترد؟',['قديم، وما يهمني','وأنت ليش يهمك؟'],6000);f.answer=r;
  await say('old',r===0?'polite':r===1?'cunning':'polite',r===0?'أجل ما يضرك تبيعه.':r===1?'كل واحد يهمه شي يا ولد سالم.':'هذي أول مرة تعجبني.');
  await say('old','neutral','خمسين ألف مقابل البرميل وحده. تغطي رواتب كم شهر.');
  await say('hero','firm','وأبوي رفض ثلاثة ريالات عشانه. قبل أبيع، أبي أعرف ليش.');f.khawajaSuspect=r===1?1:0}
 else if(f.caught){await say('old','cunning','قالوا لي إن البرميل ما له حركة.');await say('old','neutral','خمسين ألف مقابله. تغطي رواتب كم شهر.');await say('hero','firm','وأبوي رفض ثلاثة ريالات عشانه. قبل أبيع، أبي أعرف ليش.');f.khawajaSuspect=1}
 else{await say('old','surprised','ما شاء الله. لقيتوا له مكان أحسن؟');await say('old','neutral','خمسين ألف مقابله، وين ما كان. تغطي رواتب كم شهر.');await say('hero','firm','وأبوي رفض ثلاثة ريالات عشانه. قبل أبيع، أبي أعرف ليش.');o.name='oldnh';S.prop={k:'i_helmet',x:META.office_stand[0],y:META.office_stand[1],w:105};A.play('fx_assemble',.5);await say('old','cunning','احتفظ بخوذتي. يوم ترجع البرميل مكانه، رجّعها لي.');f.khawajaSuspect=1;f.helmetLeft=1}
 store.put();await walk(o,-120,840,200);await fadeTo(1,700);S.prop=null}
function timedChoice(title,opts,ms){return new Promise(res=>{const c=$('#choices');c.innerHTML=`<h3>${title}</h3>`;let done=false;const go=i=>{if(done)return;done=true;clearTimeout(tm);c.hidden=true;res(i)};opts.forEach((t,i)=>{const b=document.createElement('button');b.className='btn';b.textContent=t;b.onclick=()=>go(i);c.appendChild(b)});const s=document.createElement('button');s.className='btn ghost';s.textContent='تسكت';s.onclick=()=>go(2);c.appendChild(s);c.hidden=false;const tm=setTimeout(()=>go(2),ms)})}
async function eMunira(){S.mode='cine';startScene();setBg('site');S.bars=1;S.fade=1;A.music('music_desert',.5);A.ambience({amb_wind:.4,amb_site:.2});
 const h=actor('hero',760,780,290),m=actor('hamdan',1020,780,270),n=actor('munira',1660,800,285);h.dir='r';m.dir='l';await fadeTo(0,700);await walk(n,1240,800,200);n.dir='l';
 await say('hamdan','warm','هذي بنتي منيرة، مهندسة في الميناء.');
 await say('munira','annoyed','سمعت إن ولد سالم صار يدير الشركة. وريني شغل المضخة، وبعدها نتكلم.');
 await say('hero','neutral','حياك.');
 await fadeTo(1,700)}
async function eDemoEnd(){S.mode='none';A.music('music_menu',.5);A.ambience({});const c=$('#title');c.innerHTML=`<h1 style="font-size:clamp(34px,8vmin,72px)">انتهى الجزء الأول من التجربة</h1><p>اللي بعده: أسابيع الشغل مع منيرة، وآخر حمولة، والسوق، وفتح البرميل.</p><div style="display:flex;gap:.7em;margin-top:1em;flex-wrap:wrap;justify-content:center"><a class="btn go" href="drive.html" style="text-decoration:none">جرّب القيادة</a><button class="btn ghost go" id="again">من جديد</button></div>`;c.hidden=false;c.style.background='#000';c.style.justifyContent='center';S.fade=1;$('#again').onclick=()=>{store.clear();location.reload()}}
