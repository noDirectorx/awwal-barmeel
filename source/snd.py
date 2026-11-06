import subprocess,numpy as np,os
S='snd/';O='site_snd/';os.makedirs(O,exist_ok=True)
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
