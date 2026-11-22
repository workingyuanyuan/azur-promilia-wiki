"""Cut a character out of an official illustration: public/art/characters/<slug>.webp.

Usage (vision venv with onnxruntime-gpu, pillow, numpy, huggingface_hub):
  python -I pipeline/cut_art.py cache/art-tw/01-background-*.png public/art/characters/tushan-xiaoyu.webp

skytnt/anime-seg (isnetis) gives the matte; faint haze below 22 % is dropped; the crop is the
figure's bounds plus 2 %; where the figure runs off the source canvas the alpha fades out over 16 % (smoothstep).
"""
import sys, numpy as np, onnxruntime as ort
from PIL import Image
from pathlib import Path
from huggingface_hub import hf_hub_download
M=hf_hub_download('skytnt/anime-seg','isnetis.onnx')
sess=ort.InferenceSession(M,providers=['CUDAExecutionProvider','CPUExecutionProvider'])
def mask(img, s=1024):
    a=np.asarray(img.convert('RGB')).astype(np.float32)/255
    h,w=a.shape[:2]; r=s/max(h,w); nh,nw=int(h*r),int(w*r)
    small=np.asarray(img.convert('RGB').resize((nw,nh),Image.BICUBIC)).astype(np.float32)/255
    pad=np.zeros((s,s,3),np.float32); ph,pw=(s-nh)//2,(s-nw)//2
    pad[ph:ph+nh,pw:pw+nw]=small
    m=sess.run(None,{'img':pad.transpose(2,0,1)[None]})[0][0,0]
    m=m[ph:ph+nh,pw:pw+nw]
    return Image.fromarray((np.clip(m,0,1)*255).astype(np.uint8)).resize((w,h),Image.BICUBIC)
src, out = sys.argv[1], sys.argv[2]
img=Image.open(src).convert('RGB'); m=mask(img)
am=np.asarray(m).astype(np.float32)/255
am=np.clip((am-0.22)/0.6,0,1)
m=Image.fromarray((am*255).astype(np.uint8))
rgba=img.copy(); rgba.putalpha(m)
a=np.asarray(m); ys,xs=np.where(a>24)
y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
H,W=a.shape; pad=int(0.02*H)
box=(max(0,x0-pad),max(0,y0-pad),min(W,x1+pad),min(H,y1+pad))
edges=[n for n,c in (('top',y0<4),('bottom',y1>H-5),('left',x0<4),('right',x1>W-5)) if c]
c=rgba.crop(box)
# fade the alpha over the last 8% where the figure runs off the source canvas
al=np.asarray(c.getchannel('A')).astype(np.float32); h,w=al.shape
def ramp(n):  # smoothstep from 0 to 1 over n pixels
    t=np.linspace(0,1,n); return t*t*(3-2*t)
fy,fx=int(0.16*h),int(0.16*w)
for e in edges:
    if e=='bottom': al[-fy:,:]*=ramp(fy)[::-1][:,None]
    if e=='top': al[:fy,:]*=ramp(fy)[:,None]
    if e=='left': al[:,:fx]*=ramp(fx)[None,:]
    if e=='right': al[:,-fx:]*=ramp(fx)[::-1][None,:]
c.putalpha(Image.fromarray(al.astype(np.uint8)))
c.thumbnail((720,880),Image.LANCZOS)
c.save(out,'WEBP',quality=82,method=6)
print(Path(out).name,c.size,'edges:',edges)
