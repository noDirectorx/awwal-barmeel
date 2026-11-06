import subprocess,numpy as np,os
S='snd_raw/';O='../snd/';os.makedirs(O,exist_ok=True)
def ff(*a):subprocess.run(['ffmpeg','-y','-v','error',*a],check=True)
def env(f,win):
    r=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','8000','-f','f32le','-'],capture_output=True).stdout
    a=np.frombuffer(r,'f4');n=int(win*8000);e=np.convolve(a**2,np.ones(n),'valid');i=int(e.argmax());return i/8000
for n in ['music_menu','music_desert','music_tension','music_sad']:
    ff('-i',S+n+'.mp3','-af','loudnorm=I=-18:TP=-2:LRA=11','-ar','44100','-ac','2','-b:a','96k',O+n+'.mp3')
for n,cut in [('amb_wind',None),('amb_room',None),('amb_site',None),('pump_loop',None),('fx_steps',14)]:
    ff('-i',S+n+'.mp3',*(['-t',str(cut)] if cut else []),'-af','loudnorm=I=-20:TP=-3','-ar','44100','-ac','1','-b:a','64k',O+n+'.mp3')
ff('-i',S+'pump_motor.mp3','-ss','0','-t','7.4','-af','loudnorm=I=-16:TP=-2','-ar','44100','-ac','1','-b:a','64k',O+'pump_motor.mp3')
ff('-i',S+'pump_quake_blast.mp3','-af','afade=t=out:st=5.6:d=1.3','-ar','44100','-ac','2','-b:a','128k',O+'pump_quake_blast.mp3')
ff('-i',S+'pump_gusher.mp3','-af','afade=t=out:st=2.2:d=0.8','-ar','44100','-ac','1','-b:a','96k',O+'pump_gusher.mp3')
t=env(S+'pump_dig.mp3',.9);print('dig',t);ff('-ss',str(max(t-.03,0)),'-i',S+'pump_dig.mp3','-t','1.0','-af','afade=t=out:st=0.75:d=0.25,loudnorm=I=-14:TP=-2','-ar','44100','-ac','1','-b:a','64k',O+'pump_dig.mp3')
t=env(S+'fx_paper.mp3',1.3);print('paper',t);ff('-ss',str(max(t-.03,0)),'-i',S+'fx_paper.mp3','-t','1.4','-af','afade=t=out:st=1.1:d=0.3,loudnorm=I=-16:TP=-2','-ar','44100','-ac','1','-b:a','64k',O+'fx_paper.mp3')
for n in ['fx_pickup','fx_assemble']:ff('-i',S+n+'.mp3','-af','loudnorm=I=-14:TP=-2','-ar','44100','-ac','1','-b:a','64k',O+n+'.mp3')
ff('-i',S+'fx_trophy.mp3','-t','5.5','-af','afade=t=out:st=4.2:d=1.3,loudnorm=I=-15:TP=-2','-ar','44100','-ac','1','-b:a','80k',O+'fx_trophy.mp3')
print(sum(os.path.getsize(O+f) for f in os.listdir(O))//1024,'KB',len(os.listdir(O)))
def env_on(f,ss=0,t=None,frac=.2):
    a=['ffmpeg','-v','error','-ss',str(ss)]+(['-t',str(t)] if t else [])+['-i',f,'-ac','1','-ar','8000','-f','f32le','-']
    x=np.abs(np.frombuffer(subprocess.run(a,capture_output=True).stdout,'f4'));w=np.convolve(x,np.ones(40)/40,'same');return ss+np.argmax(w>w.max()*frac)/8000
def shot(n,dur,I=-14,out=.15):
    s=max(env_on(S+n+'.mp3')-.008,0);ff('-ss',f'{s:.3f}','-t',str(dur),'-i',S+n+'.mp3','-af',f'afade=t=out:st={dur-out}:d={out},loudnorm=I={I}:TP=-2','-ar','44100','-ac','1','-c:a','libmp3lame','-b:a','64k',O+n+'.mp3')
ff('-i',S+'drv_engine.mp3','-af','loudnorm=I=-16:TP=-2','-ar','44100','-ac','1','-b:a','64k',O+'drv_engine.mp3')
shot('drv_bump',.8);shot('drv_rattle',1.1,-16);shot('drv_barrel',1.2);shot('fx_tape',.4,-14,.05);shot('fx_sand',1.0,-16,.3)
ff('-i',S+'music_drive.mp3','-af','loudnorm=I=-18:TP=-2','-ar','44100','-ac','2','-b:a','96k',O+'music_drive.mp3')
ff('-ss','30','-t','120','-i',S+'amb_night.mp3','-af','loudnorm=I=-20:TP=-3','-ar','44100','-ac','1','-b:a','56k',O+'amb_night.mp3')
ff('-ss','15','-t','45','-i',S+'amb_market.mp3','-af','loudnorm=I=-20:TP=-3','-ar','44100','-ac','1','-b:a','56k',O+'amb_market.mp3')
ff('-i',S+'fx_radio.mp3','-af','loudnorm=I=-20:TP=-3','-ar','44100','-ac','1','-b:a','56k',O+'fx_radio.mp3')
ff('-ss','14','-t','6','-i',S+'fx_cut.mp3','-af','loudnorm=I=-18:TP=-3','-ar','44100','-ac','1','-b:a','64k',O+'fx_cut.mp3')
print(sum(os.path.getsize(O+f) for f in os.listdir(O))//1024,'KB',len(os.listdir(O)))
# قص الصمت من بداية المؤثرات القصيرة
shot('fx_pickup',.85);shot('fx_assemble',.7);shot('fx_paper',.8,-16,.2)
# الأسماء .bin عشان برامج التحميل مثل IDM ما تلقطها
for f in os.listdir(O):
    if f.endswith('.mp3'):os.replace(O+f,O+f[:-4]+'.bin')
