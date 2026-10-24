import base64, io, random
from PIL import Image

SRC, OUT = "assets/banner.png", "assets/banner.svg"

im = Image.open(SRC).convert("RGB")
W = 1600
H = int(W * im.height / im.width)
im = im.resize((W, H))
buf = io.BytesIO()
im.save(buf, "JPEG", quality=80)
b64 = base64.b64encode(buf.getvalue()).decode()
S = W / 1600  # scale factor

# ---------------- NAME (futuristic) ----------------
NAME = "VIDHI GARG"
FS = 118 * S
ADV = FS * 0.62
CX, BASE = W * 0.42, H * 0.43            # <- move the name: smaller BASE = higher, bigger CX = more right
x0 = CX - ADV * (len(NAME) - 1) / 2
name_w = ADV * len(NAME)

def letters(animated=True):
    out = ""
    for i, ch in enumerate(NAME):
        if ch == " ":
            continue
        x = x0 + i * ADV
        style = f' style="animation-delay:{0.5 + i * 0.14:.2f}s"' if animated else ""
        out += f'<text class="nm" x="{x:.1f}" y="{BASE:.1f}" text-anchor="middle"{style}>{ch}</text>'
    return out

# HUD brackets around the name
hx1, hx2 = x0 - ADV * 0.75, x0 + ADV * (len(NAME) - 1) + ADV * 0.75
hy1, hy2 = BASE - FS * 0.88, BASE + FS * 0.34
c = 26 * S
brackets = (
    f'M{hx1:.0f},{hy1 + c:.0f} V{hy1:.0f} H{hx1 + c:.0f} '
    f'M{hx2 - c:.0f},{hy1:.0f} H{hx2:.0f} V{hy1 + c:.0f} '
    f'M{hx2:.0f},{hy2 - c:.0f} V{hy2:.0f} H{hx2 - c:.0f} '
    f'M{hx1 + c:.0f},{hy2:.0f} H{hx1:.0f} V{hy2 - c:.0f}'
)
ul_y = BASE + 24 * S
ul_x1, ul_x2 = hx1 + c + 8 * S, hx2 - c - 8 * S
beam_w = 130 * S
beam_dist = (hx2 - hx1) + beam_w * 2

# ---------------- TERMINAL BOX TEXT ----------------
bx, by, bw, bh = W * 0.80, H * 0.083, W * 0.178, H * 0.237
tx = bx + 26 * S
y1, y2 = by + bh * 0.42, by + bh * 0.70      # <- tagline height (smaller = higher)
FSB, AD = 20 * S, 12 * S
L1, L2 = 14 * AD, 15 * AD
cur_h = 20 * S

# ---------------- STARS ----------------
random.seed(7)
stars, n = "", 0
while n < 45:
    x, y = random.randint(20, W - 20), random.randint(10, int(H * 0.45))
    if x > W * 0.78 and y < H * 0.34:
        continue
    r = random.choice([1.2, 1.6, 2])
    d = round(random.uniform(0, 3), 1)
    stars += f'<circle class="s" cx="{x}" cy="{y}" r="{r}" style="animation-delay:{d}s"/>'
    n += 1

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
.s{{fill:#fff;animation:tw 3s infinite ease-in-out}}
@keyframes tw{{0%,100%{{opacity:.1}}50%{{opacity:1}}}}
.aur{{animation:dr 9s infinite alternate ease-in-out}}
@keyframes dr{{from{{transform:translateX(-50px)}}to{{transform:translateX(50px)}}}}

/* ===== NAME: neon boot-up flicker, glitch burst, light sweep ===== */
.nm{{font-family:Consolas,'Courier New',monospace;font-weight:700;font-size:{FS:.0f}px}}
.main .nm{{fill:url(#chrome);stroke:#22e6ff;stroke-opacity:.8;stroke-width:{1.6 * S:.1f};
  animation:flick 1.2s both}}
@keyframes flick{{0%{{opacity:0}}8%{{opacity:1}}14%{{opacity:.1}}22%{{opacity:1}}30%{{opacity:.3}}42%,100%{{opacity:1}}}}
.cy .nm{{fill:#22e6ff}} .mg .nm{{fill:#ff2bd6}}
.gl{{opacity:0}}
.gc{{animation:gc 7s 3s infinite}}
.gm{{animation:gm 7s 3s infinite}}
@keyframes gc{{0%,91%{{opacity:0;transform:translate(0,0)}}92%{{opacity:.9;transform:translate(-7px,1px)}}94%{{opacity:.9;transform:translate(4px,-2px)}}96%{{opacity:.8;transform:translate(-3px,0)}}97%,100%{{opacity:0;transform:translate(0,0)}}}}
@keyframes gm{{0%,91%{{opacity:0;transform:translate(0,0)}}92%{{opacity:.9;transform:translate(7px,-1px)}}94%{{opacity:.9;transform:translate(-4px,2px)}}96%{{opacity:.8;transform:translate(3px,0)}}97%,100%{{opacity:0;transform:translate(0,0)}}}}
.jit{{transform-box:fill-box;transform-origin:center;animation:jit 7s 3s infinite}}
@keyframes jit{{0%,91%{{transform:none}}93%{{transform:translateX(4px) skewX(-7deg)}}95%{{transform:translateX(-3px) skewX(4deg)}}97%,100%{{transform:none}}}}
.beam{{animation:bm 6s 3.4s infinite ease-in-out both}}
@keyframes bm{{0%{{transform:translateX(0)}}30%,100%{{transform:translateX({beam_dist:.0f}px)}}}}

/* ===== HUD brackets + marching underline ===== */
.hud{{fill:none;stroke:#22e6ff;stroke-width:{3 * S:.1f};stroke-linecap:square;animation:hin 1s 1.4s both}}
@keyframes hin{{from{{opacity:0}}to{{opacity:1}}}}
.hp{{animation:hp 3s infinite ease-in-out}}
@keyframes hp{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
.ul{{stroke:url(#ug);stroke-width:{4 * S:.1f};fill:none;stroke-dasharray:{16 * S:.0f} {8 * S:.0f};
  animation:hin 1s 1.8s both,march 1.2s linear infinite}}
@keyframes march{{to{{stroke-dashoffset:-{24 * S:.0f}}}}}

/* ===== terminal box: type, hold, erase, repeat ===== */
.tb{{font-family:Consolas,'Courier New',monospace;font-size:{FSB:.1f}px;fill:#e9d5ff}}
.pr{{fill:#4ade80}}
.c1{{animation:t1 9s infinite steps(14,end)}}
.c2{{animation:t2 9s infinite steps(15,end)}}
@keyframes t1{{0%{{width:0}}20%,90%{{width:{L1 + 4:.0f}px}}96%,100%{{width:0}}}}
@keyframes t2{{0%,24%{{width:0}}46%,90%{{width:{L2 + 4:.0f}px}}96%,100%{{width:0}}}}
.k{{fill:#4ade80}}
.k1{{animation:kx1 9s infinite steps(14,end),ko1 9s infinite}}
.k2{{animation:kx2 9s infinite steps(15,end),ko2 9s infinite}}
@keyframes kx1{{0%{{transform:translateX(0)}}20%,100%{{transform:translateX({L1:.0f}px)}}}}
@keyframes ko1{{0%,20%{{opacity:1}}20.1%,100%{{opacity:0}}}}
@keyframes kx2{{0%,24%{{transform:translateX(0)}}46%,100%{{transform:translateX({L2:.0f}px)}}}}
@keyframes ko2{{0%,23.9%{{opacity:0}}24%,46%{{opacity:1}}46.1%,90%{{opacity:.9}}90.1%,100%{{opacity:0}}}}
.ht{{animation:hr 9s infinite}}
@keyframes hr{{0%,46%{{opacity:0}}50%,90%{{opacity:1}}93%,100%{{opacity:0}}}}
</style>

<defs>
  <!-- chrome gradient, applied per letter: white-cyan on top, pink-violet below -->
  <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".46" stop-color="#7df3ff"/>
    <stop offset=".54" stop-color="#e9a8ff"/><stop offset="1" stop-color="#ff5fd2"/>
  </linearGradient>
  <linearGradient id="ug" gradientUnits="userSpaceOnUse" x1="{ul_x1:.0f}" y1="0" x2="{ul_x2:.0f}" y2="0">
    <stop offset="0" stop-color="#22e6ff"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#ff2bd6"/>
  </linearGradient>
  <linearGradient id="bm" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="a1"><stop offset="0" stop-color="#22d3ee" stop-opacity=".45"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>
  <radialGradient id="a2"><stop offset="0" stop-color="#a855f7" stop-opacity=".5"/><stop offset="1" stop-color="#a855f7" stop-opacity="0"/></radialGradient>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feDropShadow dx="0" dy="5" stdDeviation="5" flood-color="#07051a" flood-opacity=".75" result="a"/>
    <feDropShadow in="a" dx="0" dy="0" stdDeviation="9" flood-color="#22e6ff" flood-opacity=".7"/>
  </filter>
  <clipPath id="nmclip">{letters(False)}</clipPath>
  <clipPath id="cp1"><rect class="c1" x="{tx:.1f}" y="{y1 - FSB:.1f}" width="{L1 + 4:.0f}" height="{FSB * 1.4:.1f}"/></clipPath>
  <clipPath id="cp2"><rect class="c2" x="{tx:.1f}" y="{y2 - FSB:.1f}" width="{L2 + 4:.0f}" height="{FSB * 1.4:.1f}"/></clipPath>
</defs>

<image href="data:image/jpeg;base64,{b64}" width="{W}" height="{H}"/>

<ellipse class="aur" cx="{W * 0.35:.0f}" cy="{H * 0.14:.0f}" rx="{W * 0.38:.0f}" ry="{H * 0.2:.0f}" fill="url(#a1)"/>
<ellipse class="aur" cx="{W * 0.62:.0f}" cy="{H * 0.12:.0f}" rx="{W * 0.38:.0f}" ry="{H * 0.2:.0f}" fill="url(#a2)" style="animation-direction:alternate-reverse"/>
{stars}

<g class="hud-wrap"><g class="hp"><path class="hud" d="{brackets}"/></g></g>

<g class="gl gc"><g class="cy">{letters(False)}</g></g>
<g class="gl gm"><g class="mg">{letters(False)}</g></g>
<g filter="url(#glow)"><g class="main jit">{letters(True)}</g></g>
<g clip-path="url(#nmclip)"><rect class="beam" x="{hx1 - beam_w:.0f}" y="{hy1:.0f}" width="{beam_w:.0f}" height="{hy2 - hy1:.0f}" fill="url(#bm)"/></g>
<line class="ul" x1="{ul_x1:.0f}" y1="{ul_y:.0f}" x2="{ul_x2:.0f}" y2="{ul_y:.0f}"/>

<g clip-path="url(#cp1)"><text class="tb" x="{tx:.1f}" y="{y1:.1f}" textLength="{L1:.0f}" lengthAdjust="spacingAndGlyphs"><tspan class="pr">&gt;</tspan> Better Code,</text></g>
<g clip-path="url(#cp2)"><text class="tb" x="{tx:.1f}" y="{y2:.1f}" textLength="{L2:.0f}" lengthAdjust="spacingAndGlyphs"><tspan class="pr">&gt;</tspan> Bigger Dreams</text></g>
<rect class="k k1" x="{tx:.1f}" y="{y1 - cur_h * 0.85:.1f}" width="{8 * S:.1f}" height="{cur_h:.1f}"/>
<rect class="k k2" x="{tx:.1f}" y="{y2 - cur_h * 0.85:.1f}" width="{8 * S:.1f}" height="{cur_h:.1f}"/>
<path class="ht" fill="#ec4899" transform="translate({tx + L2 + 14 * S:.1f},{y2 - 17 * S:.1f}) scale({0.8 * S:.2f})"
 d="M12 21C5 15 2 11 2 7.5 2 4.5 4.3 2.5 6.8 2.5 9 2.5 11 3.8 12 5.8 13 3.8 15 2.5 17.2 2.5 19.7 2.5 22 4.5 22 7.5 22 11 19 15 12 21Z"/>
</svg>'''

open(OUT, "w", encoding="utf-8").write(svg)
print("done:", len(svg) // 1024, "KB  (agar 1500 KB se zyada ho to quality=80 ko 65 kar do)")