#!/usr/bin/env python3
"""يستخرج نص القصة (حوار، خيارات، بطاقات) من الكود إلى ملفات markdown.
التشغيل من مجلد source/: python3 tools/extract_script.py
الكود هو المصدر؛ لا تعدل الملفات الناتجة يدويًا."""
import re,sys
AR=re.compile(r'[؀-ۿ]')
STR=re.compile(r"'((?:[^'\\\n]|\\.)*)'|`((?:[^`\\]|\\.)*)`|\"((?:[^\"\\\n]|\\.)*)\"")
FN=re.compile(r'^(?:async )?function ([A-Za-z_]\w*)\s*\(|^const ([A-Za-z_]\w*)\s*=',re.M)
def lines(src):
    out=[]
    for ln in src.split('\n'):
        m=FN.match(ln)
        if m:out.append(('fn',m.group(1) or m.group(2)))
        for call in re.finditer(r"\b(say|choose|card|toast|narr|letter|bubble)\(",ln):pass
        i=0
        for m in STR.finditer(ln):
            t=m.group(1) or m.group(2) or m.group(3) or ''
            if not AR.search(t):continue
            pre=ln[max(0,m.start()-45):m.start()]
            sp=re.search(r"say\('(\w+)','(\w+)',$",pre)
            if sp:out.append(('say',sp.group(1),t))
            elif re.search(r"choose\($",pre):out.append(('choice',t))
            elif re.search(r"card\($",pre):out.append(('card',t))
            elif re.search(r"t:$",pre):out.append(('opt',t))
            elif re.search(r"s:$",pre):out.append(('sub',t))
            elif re.search(r"toast\($",pre):out.append(('toast',t))
            else:out.append(('txt',t))
    return out
def md(src,title,only=None):
    r=[f'# {title}\n','> مستخرج آليًا من الكود. الفروع غير موضحة بالكامل؛ ارجع للكود للشروط.\n'];cur=None
    for x in lines(src):
        if x[0]=='fn':
            cur=x[1];continue
        if only and cur and not only(cur):continue
        if cur:r.append(f'\n## {cur}\n');cur=None
        k=x[0]
        if k=='say':r.append(f'- **{x[1]}** ({x[2 and 1] if False else ""}): {x[2]}'.replace(' ()',''))
        elif k=='choice':r.append(f'\n**قرار: {x[1]}**')
        elif k=='opt':r.append(f'  - خيار: {x[1]}')
        elif k=='sub':r.append(f'    - ({x[1]})')
        elif k=='card':r.append(f'\n— {x[1]} —')
        elif k=='toast':r.append(f'- [تنبيه] {x[1]}')
        else:r.append(f'- {x[1]}')
    return '\n'.join(r)+'\n'
if __name__=='__main__':
    g=open('game.html',encoding='utf8').read();e=open('ep2_ch.js',encoding='utf8').read()
    open('../docs/story/ep1-script.md','w',encoding='utf8').write(md(g,'الحلقة الأولى: كل نصوص اللعبة والمحرك'))
    open('../docs/story/ep2-script.md','w',encoding='utf8').write(md(e,'الحلقة الثانية: النص'))
