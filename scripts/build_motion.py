"""Add self-contained SVG animation to the existing racing artwork."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
banner = ROOT / 'assets/grid-banner.svg'
svg = banner.read_text(encoding='utf-8-sig')
style = '''<style>
@keyframes rush{from{transform:translateX(240px)}to{transform:translateX(-1000px)}}
@keyframes idle{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes wheel{to{transform:rotate(360deg)}}
@keyframes dash{to{stroke-dashoffset:-600}}
@keyframes glow{50%{opacity:.35}}
.speed{animation:rush 1.5s linear infinite}.speed.s2{animation-delay:-.7s;animation-duration:1.9s}.speed.s3{animation-delay:-1.1s;animation-duration:1.2s}
.car{animation:idle .65s ease-in-out infinite}.rim{animation:wheel .5s linear infinite;transform-box:fill-box;transform-origin:center}
.circuit{animation:dash 8s linear infinite}.running{animation:glow 2s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){.speed,.car,.rim,.circuit,.running{animation:none}}
</style>'''
if '@keyframes rush' not in svg:
    svg = svg.replace('</defs>', '</defs>' + style, 1)
    effects = '''<g stroke="#d49ab0" stroke-width="2" opacity=".35">
<path class="speed" d="M1000 365h260"/><path class="speed s2" d="M1090 415h350"/><path class="speed s3" d="M970 550h320"/>
</g>
<path class="circuit" d="M20 576H1420" fill="none" stroke="#a86685" stroke-width="2" stroke-dasharray="80 220"/>
<circle class="running" cx="1384" cy="96" r="4" fill="#e9b2c7"/>
'''
    svg = svg.replace('<ellipse cx="761"', effects + '<ellipse cx="761"', 1)
    svg = svg.replace('<!-- Hand-drawn GT silhouette, three-quarter side view. -->\n<g>', '<!-- Hand-drawn GT silhouette, three-quarter side view. -->\n<g class="car">')
    old = '<g stroke="#a6a8b6" stroke-width="5"><path d="m482 446v102m-45-76 90 50m-90 0 90-50M1042 430v98m-43-73 86 48m-86 0 86-48"/></g>'
    new = '<g stroke="#a6a8b6" stroke-width="5"><g class="rim"><path d="M482 446v102m-45-76 90 50m-90 0 90-50"/></g><g class="rim"><path d="M1042 430v98m-43-73 86 48m-86 0 86-48"/></g></g>'
    if old not in svg:
        raise RuntimeError('Expected wheel illustration not found')
    svg = svg.replace(old, new)
    banner.write_text(svg, encoding='utf-8')

terminal = '''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="340" viewBox="0 0 1440 340" role="img" aria-labelledby="title desc">
<title id="title">Asel / pit wall terminal</title><desc id="desc">Animated terminal introducing Asel, a DHBW student learning C and Java. Code, test, learn, repeat.</desc>
<defs>
<linearGradient id="border"><stop stop-color="#526e96"/><stop offset=".6" stop-color="#53253f"/><stop offset="1" stop-color="#b96888"/></linearGradient>
<clipPath id="typing"><rect x="40" y="81" width="0" height="36"><animate attributeName="width" values="0;0;710;710;710" keyTimes="0;.05;.28;.92;1" dur="12s" repeatCount="indefinite"/></rect></clipPath>
</defs>
<style>
text{font-family:Consolas,monospace}
@keyframes reveal{0%,30%{opacity:0}35%,95%{opacity:1}100%{opacity:0}}
@keyframes cursor{50%{opacity:0}}
@keyframes loading{0%{transform:scaleX(.05)}45%,100%{transform:scaleX(1)}}
.line{animation:reveal 12s infinite}.l2{animation-delay:.6s}.l3{animation-delay:1.2s}.l4{animation-delay:1.8s}
.cursor{animation:cursor 1s step-end infinite}.progress{transform-box:fill-box;transform-origin:left;animation:loading 12s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){.line,.cursor,.progress{animation:none}.line{opacity:1}}
</style>
<rect x="1" y="1" width="1438" height="338" rx="16" fill="#0c1321" stroke="url(#border)" stroke-width="2"/>
<path d="M1 54h1438" stroke="#29364c"/>
<circle cx="32" cy="28" r="6" fill="#a74967"/><circle cx="54" cy="28" r="6" fill="#ac8a9f"/><circle cx="76" cy="28" r="6" fill="#526f95"/>
<text x="720" y="33" text-anchor="middle" fill="#9daac0" font-size="13">asel@midnight-club: ~/garage</text>
<text clip-path="url(#typing)" x="40" y="108" fill="#e6d1dd" font-size="22">❯ ./driver --number 61 --mode build</text>
<g class="line"><text x="41" y="154" fill="#8e9db5" font-size="18">DRIVER</text><text x="240" y="154" fill="#ece4eb" font-size="18">Asel / DHBW student</text></g>
<g class="line l2"><text x="41" y="192" fill="#8e9db5" font-size="18">TOOLKIT</text><text x="240" y="192" fill="#c78da8" font-size="18">C · Java · Git · GitHub</text></g>
<g class="line l3"><text x="41" y="230" fill="#8e9db5" font-size="18">MINDSET</text><text x="240" y="230" fill="#ece4eb" font-size="18">code → test → learn → repeat</text></g>
<g class="line l4"><text x="41" y="286" fill="#c78da8" font-size="19">❯ ready for the next lap.</text><rect class="cursor" x="372" y="267" width="11" height="23" fill="#c78da8"/></g>
<rect x="1000" y="112" width="388" height="151" rx="10" fill="#111d30" stroke="#2c3c57"/>
<text x="1025" y="145" fill="#8e9db5" font-size="12" letter-spacing="2">DEVELOPMENT STATUS</text>
<text x="1023" y="198" fill="#e2c0d0" font-size="31" font-weight="700">WORK IN PROGRESS</text>
<rect x="1025" y="224" width="337" height="4" rx="2" fill="#28354c"/>
<rect class="progress" x="1025" y="224" width="337" height="4" rx="2" fill="#a95d7e"/>
</svg>'''
(ROOT / 'assets/terminal.svg').write_text(terminal, encoding='utf-8')
print('Animated racing banner and terminal generated')
