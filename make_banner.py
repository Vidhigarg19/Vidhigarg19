import base64, io, random
from PIL import Image

im = Image.open("assets/banner.png").convert("RGB")
W = 1600
H = int(W * im.height / im.width)
im = im.resize((W, H))
buf = io.BytesIO()
im.save(buf, "JPEG", quality=80)
b64 = base64.b64encode(buf.getvalue()).decode()

random.seed(7)
stars = ""
for i in range(40):
    x, y = random.randint(20, W - 20), random.randint(10, int(H * 0.45))
    r = random.choice([1.2, 1.6, 2])
    d = round(random.uniform(0, 3), 1)
    stars += f'<circle class="s" cx="{x}" cy="{y}" r="{r}" style="animation-delay:{d}s"/>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
.s{{fill:#fff;animation:tw 3s infinite ease-in-out}}
@keyframes tw{{0%,100%{{opacity:.1}}50%{{opacity:1}}}}
.aur{{animation:dr 9s infinite alternate ease-in-out}}
@keyframes dr{{from{{opacity:.15;transform:translateX(-40px)}}to{{opacity:.45;transform:translateX(40px)}}}}
.tx{{font-family:monospace;font-size:34px;fill:#e9d5ff;opacity:0;animation:fi 2s 0.5s forwards}}
@keyframes fi{{to{{opacity:1}}}}
</style>
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#a855f7"/><stop offset="1" stop-color="#ec4899"/></linearGradient>
<filter id="b"><feGaussianBlur stdDeviation="25"/></filter></defs>
<image href="data:image/jpeg;base64,{b64}" width="{W}" height="{H}"/>
<ellipse class="aur" cx="{W//2}" cy="{int(H*0.12)}" rx="{int(W*0.45)}" ry="{int(H*0.12)}" fill="url(#g)" filter="url(#b)"/>
{stars}
<text class="tx" x="{int(W*0.06)}" y="{int(H*0.5)}">Better Code, Bigger Dreams</text>
</svg>'''
open("assets/banner.svg", "w", encoding="utf-8").write(svg)
print("done", len(svg) // 1024, "KB")