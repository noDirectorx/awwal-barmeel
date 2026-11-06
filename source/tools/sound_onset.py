import subprocess,numpy as np,sys
for n in sys.argv[1:]:
    r=subprocess.run(['ffmpeg','-v','error','-i',f'site_snd/{n}.mp3','-ac','1','-ar','8000','-f','f32le','-'],capture_output=True).stdout
    a=np.abs(np.frombuffer(r,'f4'));w=np.convolve(a,np.ones(40)/40,'same');pk=w.max()
    print(n,'len',round(len(a)/8000,2),'first10%',round(np.argmax(w>pk*.1)/8000,3),'first30%',round(np.argmax(w>pk*.3)/8000,3),'peak',round(w.argmax()/8000,3))
