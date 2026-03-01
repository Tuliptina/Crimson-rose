"""
🧪 The Fitzroy Collection — ULTIMATE Edition
20 unique bottles, shape-matched 2D zoom, drawers, lock, mixing,
UV canvas reveals, seal-breaking, hold-to-light, nightmare mode,
atmospheric cross-reactions, discovery journal, sound descriptions.
"""

def get_cabinet_3d(mode: str = "gaslight", intensity: int = 3) -> str:
    if mode == "gothic":
        bg="0x0a0505"; wood="0x3a1818"; wood_dark="0x1a0808"
        metal="0x5a5a5a"; light="0xff4422"; text="#cc0000"
        ambient=0.35; uv_color="#ff00ff"; glow="0xff4444"
        panel_bg="rgba(10,5,5,0.97)"; warn_bg="#330505"
    elif mode == "clinical":
        bg="0xe8e8e8"; wood="0xd8d0c8"; wood_dark="0xc0b8b0"
        metal="0xbbbbbb"; light="0xffffff"; text="#2f4f4f"
        ambient=0.7; uv_color="#9900ff"; glow="0xeeeeee"
        panel_bg="rgba(248,248,245,0.97)"; warn_bg="#eedddd"
    else:
        bg="0x1a1410"; wood="0x5a4530"; wood_dark="0x3c2818"
        metal="0xc8a030"; light="0xffbb55"; text="#d4a574"
        ambient=0.5; uv_color="#cc00ff"; glow="0xffcc88"
        panel_bg="rgba(26,20,16,0.97)"; warn_bg="#331a00"

    creep = intensity / 5.0
    nightmare = "true" if intensity >= 5 else "false"

    html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:100%;height:100%;overflow:hidden;background:#111;font-family:Georgia,serif;color:{text};}}
#container{{width:100%;height:100%;position:relative;cursor:grab;}}
#container:active{{cursor:grabbing;}}
canvas{{display:block;width:100%!important;height:100%!important;}}
.ui{{position:absolute;pointer-events:none;z-index:100;text-shadow:0 0 8px rgba(0,0,0,0.8);}}
#title{{top:12px;left:50%;transform:translateX(-50%);font-size:14px;letter-spacing:4px;opacity:0.7;}}
#info{{bottom:12px;left:50%;transform:translateX(-50%);font-size:11px;opacity:0.4;}}
#hint{{bottom:45px;left:50%;transform:translateX(-50%);font-size:13px;background:rgba(0,0,0,0.85);padding:6px 14px;border-radius:4px;opacity:0;transition:opacity 0.3s;max-width:80%;text-align:center;}}
#sounds{{bottom:80px;left:50%;transform:translateX(-50%);font-style:italic;font-size:12px;opacity:0;transition:opacity 1s;}}
#nm-txt{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:22px;color:#880000;opacity:0;transition:opacity 2s;pointer-events:none;z-index:300;text-shadow:0 0 20px #ff0000;}}
.vig{{position:absolute;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at center,transparent 40%,rgba(0,0,0,{0.4+creep*0.2 if mode!='clinical' else 0.05}) 100%);pointer-events:none;z-index:50;}}
#uv-ov{{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(80,0,120,0.15);pointer-events:none;z-index:45;opacity:0;transition:opacity 0.5s;}}
#uv-ov.on{{opacity:1;}}
#hid-flash{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:16px;letter-spacing:3px;color:#aa0000;opacity:0;transition:opacity 0.5s;z-index:160;text-shadow:0 0 15px #ff0000;pointer-events:none;}}
#ctrl{{position:absolute;top:55px;right:12px;display:flex;flex-direction:column;gap:6px;z-index:150;}}
#ctrl button{{padding:7px 12px;background:rgba(0,0,0,0.7);border:1px solid {text}44;color:{text};font-family:Georgia;font-size:11px;cursor:pointer;pointer-events:auto;transition:all 0.3s;border-radius:3px;}}
#ctrl button:hover{{background:{text}22;border-color:{text};}}
#ctrl button.on{{background:{text}33;border-color:{text};}}
#sec-d{{position:absolute;top:12px;right:12px;font-size:11px;opacity:0.6;z-index:150;pointer-events:auto;cursor:pointer;}}
#tooltip{{position:absolute;background:rgba(0,0,0,0.92);color:{text};padding:10px 14px;border-radius:4px;font-size:12px;max-width:240px;line-height:1.5;pointer-events:none;opacity:0;transition:opacity 0.3s;z-index:200;border:1px solid {text}33;}}
#tooltip.vis{{opacity:1;}}
#tooltip .tt{{font-weight:bold;margin-bottom:3px;}}
#tooltip .tl{{font-style:italic;font-size:11px;opacity:0.65;margin-top:4px;border-top:1px solid {text}22;padding-top:4px;}}

/* Zoom Panel */
#zp{{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.93);display:none;z-index:200;}}
#zp.show{{display:flex;}}
#zp-l{{flex:1.1;display:flex;align-items:center;justify-content:center;}}
#zp-r{{flex:1;max-width:380px;padding:30px 25px;display:flex;flex-direction:column;justify-content:center;overflow-y:auto;max-height:100vh;}}
#zp-nm{{font-size:22px;margin-bottom:4px;}}
#zp-sb{{font-size:12px;opacity:0.45;font-style:italic;margin-bottom:14px;border-bottom:1px solid {text}22;padding-bottom:10px;}}
#zp-ds{{font-size:13px;line-height:1.7;margin-bottom:10px;}}
#zp-cn{{font-size:12px;opacity:0.8;padding:10px 12px;background:rgba(255,255,255,0.03);border-left:3px solid {text}33;margin-bottom:10px;line-height:1.5;}}
#zp-wr{{display:inline-block;padding:4px 10px;background:{warn_bg};font-size:10px;letter-spacing:2px;margin-bottom:10px;border-radius:2px;}}
#zp-sc{{color:#bb3333;font-style:italic;margin-top:8px;opacity:0;transition:opacity 1.5s;font-size:12px;}}
#zp-sc.show{{opacity:1;}}
#zp-uv{{color:{uv_color};font-style:italic;margin-top:6px;opacity:0;transition:opacity 0.5s;display:none;font-size:11px;}}
#zp-uv.show{{opacity:1;display:block;}}
#zp-sl{{color:#aa6633;font-size:12px;margin-top:6px;display:none;}}
#zp-sl.show{{display:block;}}
#zp-x{{position:absolute;top:20px;right:25px;font-size:28px;cursor:pointer;opacity:0.5;z-index:210;color:{text};background:none;border:none;}}
#zp-x:hover{{opacity:1;}}
#zp-bt{{display:flex;gap:6px;margin-top:14px;flex-wrap:wrap;}}
.zb{{padding:6px 12px;background:transparent;border:1px solid {text}44;color:{text};font-family:Georgia;font-size:11px;cursor:pointer;border-radius:3px;transition:all 0.3s;}}
.zb:hover{{background:{text}22;}}
.zb:disabled{{opacity:0.25;cursor:not-allowed;}}
.zb.lit{{border-color:{text};background:{text}22;}}

/* Sub Panels */
.sp{{position:absolute;background:{panel_bg};border:1px solid {text}33;display:none;z-index:250;border-radius:6px;}}
.sp.show{{display:block;}}
.spx{{position:absolute;top:8px;right:12px;font-size:18px;cursor:pointer;opacity:0.5;color:{text};background:none;border:none;}}
.spx:hover{{opacity:1;}}
.spt{{font-size:12px;letter-spacing:2px;margin-bottom:12px;text-align:center;opacity:0.7;}}
.spb{{padding:7px 14px;background:transparent;border:1px solid {text}44;color:{text};font-family:Georgia;cursor:pointer;font-size:11px;border-radius:3px;transition:all 0.2s;}}
.spb:hover{{background:{text}22;}}
#dp{{bottom:0;left:50%;transform:translateX(-50%);width:80%;max-width:650px;padding:18px;border-bottom:none;border-radius:6px 6px 0 0;z-index:180;}}
#dp-it{{display:flex;gap:10px;flex-wrap:wrap;}}
.di{{padding:10px 14px;background:rgba(0,0,0,0.3);border:1px solid {text}22;cursor:pointer;font-size:12px;transition:all 0.3s;border-radius:3px;}}
.di:hover{{background:{text}22;border-color:{text}55;}}
.di.lk{{opacity:0.35;cursor:not-allowed;}}
#lp{{top:50%;left:50%;transform:translate(-50%,-50%);padding:25px;text-align:center;}}
#lp-d{{display:flex;gap:8px;justify-content:center;margin:14px 0;}}
.dl{{width:45px;height:55px;background:rgba(0,0,0,0.4);border:2px solid {text}55;display:flex;align-items:center;justify-content:center;font-size:26px;font-family:monospace;cursor:pointer;user-select:none;border-radius:4px;}}
.dl:hover{{border-color:{text};}}
#lp-h{{font-size:10px;opacity:0.4;margin-top:10px;font-style:italic;}}
#mp{{top:50%;left:50%;transform:translate(-50%,-50%);padding:25px;min-width:310px;}}
#mp-sl{{display:flex;gap:12px;justify-content:center;margin:12px 0;}}
.ms{{width:60px;height:80px;background:rgba(0,0,0,0.3);border:2px dashed {text}33;display:flex;align-items:center;justify-content:center;font-size:10px;opacity:0.5;border-radius:4px;text-align:center;padding:4px;}}
.ms.fl{{border-style:solid;opacity:1;border-color:{text}66;}}
#mp-r{{text-align:center;min-height:45px;padding:10px;background:rgba(0,0,0,0.2);margin:10px 0;font-style:italic;font-size:12px;border-radius:4px;line-height:1.5;}}
#mp-bt{{display:flex;gap:8px;justify-content:center;}}
#jp{{top:50%;left:50%;transform:translate(-50%,-50%);padding:25px;width:85%;max-width:480px;max-height:75vh;overflow-y:auto;}}
#jp-e{{font-size:12px;line-height:1.7;}}
.je{{padding:7px 0;border-bottom:1px solid {text}12;}}.je-t{{font-size:10px;opacity:0.35;}}
@keyframes bshk{{0%,100%{{transform:rotate(0);}}15%{{transform:rotate(-6deg);}}30%{{transform:rotate(5deg);}}45%{{transform:rotate(-4deg);}}60%{{transform:rotate(3deg);}}75%{{transform:rotate(-2deg);}}}}
#zc.shk{{animation:bshk 0.7s ease;}}
</style></head><body>
<div id="container"></div>
<div class="vig"></div>
<div id="uv-ov"></div>
<div id="title" class="ui">THE FITZROY COLLECTION</div>
<div id="info" class="ui">Drag to rotate · Scroll to zoom · Click bottles to examine</div>
<div id="hint" class="ui"></div>
<div id="sounds" class="ui"></div>
<div id="nm-txt"></div>
<div id="hid-flash">SECRET COMPARTMENT FOUND</div>
<div id="sec-d">🕵 <span id="sn">0</span> discoveries</div>
<div id="tooltip"><div class="tt"></div><div class="td"></div><div class="tl"></div></div>
<div id="ctrl">
<button id="b-uv">🔦 UV Light</button>
<button id="b-dr">🗄️ Drawers</button>
<button id="b-mx">⚗️ Mix</button>
<button id="b-jn">📖 Journal</button>
</div>
<div id="zp">
<button id="zp-x" onclick="window.closeZoom()">×</button>
<div id="zp-l"><canvas id="zc" width="340" height="440"></canvas></div>
<div id="zp-r">
<div id="zp-nm"></div><div id="zp-sb"></div>
<div id="zp-ds"></div><div id="zp-cn"></div>
<div id="zp-wr"></div><div id="zp-sl"></div>
<div id="zp-sc"></div><div id="zp-uv"></div>
<div id="zp-bt">
<button class="zb" id="z-shk">🫗 Shake</button>
<button class="zb" id="z-sml">👃 Smell</button>
<button class="zb" id="z-por">💧 Pour</button>
<button class="zb" id="z-lit">🕯️ Hold to Light</button>
<button class="zb" id="z-sel" style="display:none">🔴 Break Seal</button>
<button class="zb" id="z-amx">⚗️ Add to Mix</button>
</div></div></div>
<div id="dp" class="sp"><button class="spx" onclick="document.getElementById('dp').classList.remove('show')">×</button>
<div class="spt">LOWER DRAWERS</div><div id="dp-it"></div></div>
<div id="lp" class="sp"><button class="spx" onclick="document.getElementById('lp').classList.remove('show')">×</button>
<div class="spt">🔒 SOCIETY DRAWER</div>
<div id="lp-d"><div class="dl">0</div><div class="dl">0</div><div class="dl">0</div></div>
<button class="spb" id="lp-go">UNLOCK</button>
<div id="lp-h">"The year the Society was founded..."</div></div>
<div id="mp" class="sp"><button class="spx" onclick="document.getElementById('mp').classList.remove('show')">×</button>
<div class="spt">⚗️ MIXING CHAMBER</div>
<div id="mp-sl"><div class="ms" data-s="0">Empty</div><div class="ms" data-s="1">Empty</div></div>
<div id="mp-r">Add two bottles to combine...</div>
<div id="mp-bt"><button class="spb" id="mp-go">Combine</button><button class="spb" id="mp-cl">Clear</button></div></div>
<div id="jp" class="sp"><button class="spx" onclick="document.getElementById('jp').classList.remove('show')">×</button>
<div class="spt">📖 INVESTIGATION JOURNAL</div>
<div id="jp-e"><div style="opacity:0.35;font-style:italic;text-align:center;font-size:12px;">No discoveries yet...</div></div></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function(){{
'use strict';
const INT={intensity},NM={nightmare},CR={creep},MD='{mode}';
const E=id=>document.getElementById(id);
const Q=s=>document.querySelectorAll(s);
let uvOn=false,litOn=false,hidF=false,bkCl=0;
const fnd=new Set(),mxS=[null,null],jrn=[];
let sel=null,wv=0,shk=false,sealBrk=false;

/* ===== DISCOVERY ===== */
function disc(id,txt){{if(fnd.has(id))return;fnd.add(id);jrn.push({{t:new Date().toLocaleTimeString(),x:txt}});E('sn').textContent=fnd.size;updJ();}}
function updJ(){{const e=E('jp-e');if(!jrn.length)return;e.innerHTML=jrn.map(j=>'<div class="je"><div class="je-t">'+j.t+'</div><div>'+j.x+'</div></div>').join('');}}
function hint(t,d){{const h=E('hint');h.textContent=t;h.style.opacity='1';setTimeout(()=>h.style.opacity='0',d||2500);}}

/* ===== SOUNDS ===== */
const SND=['*Wood creaks as you lean closer...*','*Glass clinks softly...*','*Liquid sloshes against its container...*','*A cork shifts...*','*Something settles on a shelf...*','*You hear your own breathing...*','*Dust drifts in the candlelight...*'];
const NSND=['*Something taps from inside a jar...*','*A wet sound. Behind you.*','*Whispers. Too faint to understand.*','*The leeches are excited.*','*A face. In the reflection. Gone now.*','*"Open me..." Was that a voice?*'];
const sE=E('sounds');let si=0;
function sndT(){{const p=NM?[...SND,...NSND]:SND;sE.textContent=p[si%p.length];sE.style.opacity='0.6';setTimeout(()=>sE.style.opacity='0',3500);si++;}}
setInterval(sndT,Math.max(3000,8000-INT*1000));setTimeout(sndT,3000);
const nmE=E('nm-txt');
const NT=['IT SEES YOU','OPEN THE RED ONE','WE ARE WAITING','JOIN US','YOUR BLOOD NEXT','THEY NEVER LEFT'];
if(NM)setInterval(()=>{{nmE.textContent=NT[Math.random()*NT.length|0];nmE.style.opacity='0.8';setTimeout(()=>nmE.style.opacity='0',2000);}},15000);

/* ===== BOTTLE DATA (20 bottles) ===== */
const B=[
{{id:'laudanum',nm:'Laudanum',sub:'Tincture of Opium',col:0xcc8844,liq:0x553311,lv:0.6,row:0,sl:0,sh:'rect',desc:'Opium dissolved in alcohol. Prescribed for everything from headaches to hysteria.',cnt:'Half empty. Fingerprints on the neck — hurried, frantic grabs.',wrn:'HIGHLY ADDICTIVE',sec:'Note behind label: "Mrs. Harrison — 40 drops. Silence her."',uv:'Hidden text: SILENCE HER',hs:true,seal:false,mix:'sedative',anim:'bubble',sml:'Bitter opium. Sweet alcohol underneath. The smell of dependency.'}},
{{id:'strychnine',nm:'Strychnine',sub:'Nerve Tonic',col:0xdd3333,liq:0xffcccc,lv:0.5,row:0,sl:1,sh:'hex',desc:'Stimulant in minute doses. Fatal in anything more. The margin between cure and death is vanishingly thin.',cnt:'Red warning wax on the cork. Broken and resealed multiple times.',wrn:'LETHAL POISON',sec:'Dosage noted in pencil: "0.3g for 70kg male"',uv:'"For the weak ones" scratched into glass',hs:INT>=3,seal:true,mix:'poison',anim:'pulse',sml:'Intensely bitter. Your tongue goes numb from the fumes alone.'}},
{{id:'mercury_cl',nm:'Mercury Chloride',sub:'Blue Mass',col:0x334455,liq:0x99aaaa,lv:0.5,row:0,sl:2,sh:'banded',desc:'Treatment for syphilis. Causes madness and organ failure with prolonged use.',cnt:'Silver shimmer. Moves too heavily.',wrn:'TOXIC — CUMULATIVE',sec:'Names scratched behind label. Patients? Victims?',uv:'Society rose symbol etched into base',hs:INT>=4,seal:false,mix:'poison',anim:'shimmer',sml:'Metallic. Cold. Like licking a coin in winter.'}},
{{id:'formaldehyde',nm:'Formaldehyde',sub:'Preservation',col:0x888866,liq:0xccccaa,lv:0.85,row:0,sl:3,sh:'jug',desc:'Preservation fluid. Far more than any hospital ward needs.',cnt:'Gallons. Not pints. Someone is preserving more than specimens.',wrn:'TOXIC FUMES',sec:'A ward needs pints. This is gallons. For what?',uv:'Off-site address: 14 Cutter Lane, Whitechapel',hs:INT>=3,seal:false,mix:'preserve',anim:'none',sml:'Sharp. Penetrating. Your eyes water immediately.'}},
{{id:'unmarked',nm:'Bottle #7',sub:'Unmarked',col:0x666666,liq:0xeeeeee,lv:0.5,row:0,sl:4,sh:'hex_plain',desc:'No label. No markings. The glass is warm. Faint smell of almonds.',cnt:'Clear liquid. Water — or cyanide.',wrn:'DO NOT OPEN',sec:'Enough to kill 100 people. Hidden in plain sight.',uv:'Batch number: 1847 — year the Society was founded',hs:INT>=3,seal:true,mix:'poison',anim:'none',sml:'BITTER ALMONDS. Step back. Now.'}},

{{id:'ether',nm:'Ether',sub:'Anaesthetic',col:0x775533,liq:0xffeedd,lv:0.35,row:1,sl:0,sh:'ribbed',desc:'Volatile anaesthetic. Patients sleep. Usually they wake.',cnt:'Flammable. Scratches inside the lid.',wrn:'NO NAKED FLAME',sec:'Claw marks inside the lid. Someone tried to open it from within.',uv:'Claw marks fluoresce — they contain blood',hs:INT>=4,seal:false,mix:'knockout',anim:'bubble',sml:'Sickly sweet. Your head swims after one breath.'}},
{{id:'belladonna',nm:'Belladonna',sub:'Deadly Nightshade',col:0x884488,liq:0xcc88cc,lv:0.65,row:1,sl:1,sh:'oval',desc:'Dilates pupils. Women took this to appear beautiful — and died for vanity.',cnt:'Dark purple extract. Viscous.',wrn:'TOXIC ALKALOID',sec:'"Beautiful lady." The irony is not lost on anyone who knows the body count.',uv:'Patient list: 6 women, all dead within the year',hs:INT>=2,seal:false,mix:'poison',anim:'swirl',sml:'Faintly sweet. Deceptively pleasant. Like a poisoned flower.'}},
{{id:'arsenic',nm:'Arsenic',sub:'Complexion Wafers',col:0x88aa77,liq:0xcceecc,lv:0.65,row:1,sl:2,sh:'perfume',desc:'Sold as beauty aids. Pale complexion guaranteed. Slow death also guaranteed.',cnt:'Sweet-tasting powder in solution.',wrn:'AS DIRECTED ONLY',sec:'Why does a male doctor keep complexion wafers?',uv:'"For V.H. — final dose" in UV-reactive ink',hs:INT>=3,seal:false,mix:'poison',anim:'none',sml:'Almost nothing. Faintly sweet. That is what makes it perfect.'}},
{{id:'chloroform',nm:'Chloroform',sub:'Anaesthetic',col:0x4466bb,liq:0xccddff,lv:0.25,row:1,sl:3,sh:'hex_ridged',desc:'Volatile anaesthetic. Recently used — the level is low.',cnt:'Used without surgeries scheduled.',wrn:'POISON — VOLATILE',sec:'Used 3 times this week. No operations recorded.',uv:'Bloodstain visible under label',hs:INT>=3,seal:false,mix:'knockout',anim:'swirl',sml:'Sickly sweet oblivion. One breath too many and you never wake.'}},
{{id:'leeches',nm:'Leeches',sub:'Live Specimens',col:0xccffcc,liq:0xaaddaa,lv:0.7,row:1,sl:4,sh:'dome_jar',desc:'Medicinal leeches in stagnant water. They sense your warmth.',cnt:'Hungry. Unusually large. How are they being fed?',wrn:'LIVE — HANDLE WITH CARE',sec:'Too large for medicinal species. What are they?',uv:'Feeding log: weekly. Source: "the wards"',hs:INT>=2,seal:false,mix:'none',anim:'leeches',sml:'Stagnant water. Mud. Something organic and wrong.'}},

{{id:'vita',nm:'Vita Aeterna',sub:'Eternal Essence',col:0x880022,liq:0xaa0000,lv:0.55,row:2,sl:0,sh:'teardrop',desc:'The Society communion. The liquid swirls on its own. Too red for wine.',cnt:'Viscous. Warm. Moves without being touched.',wrn:'MEMBERS ONLY',sec:'"Sanguis innocentum" — blood of the innocent.',uv:'BLOOD OF THE UNWILLING — prints of 7 people',hs:true,seal:true,mix:'blood',anim:'swirl',sml:'Iron. Copper. The unmistakable smell of blood.'}},
{{id:'cocaine',nm:'Cocaine 4%',sub:'Local Anaesthetic',col:0xeeeeff,liq:0xffffff,lv:0.12,row:2,sl:1,sh:'dropper',desc:'Anaesthetic and confidence. Nearly empty.',cnt:'Almost gone. Who uses this much?',wrn:'CONTROLLED',sec:"Fitzroy's daily supply. Every 3 hours.",uv:'Usage tally — over 200 doses this month',hs:true,seal:false,mix:'stimulant',anim:'sparkle',sml:'Chemical. Sharp. Your nose goes numb instantly.'}},
{{id:'unwilling',nm:'"Unwilling"',sub:'Special Procurement',col:0x222222,liq:0x332244,lv:0.7,row:2,sl:2,sh:'black_rect',desc:'For resistant subjects. The name is a description.',cnt:'Instant unconsciousness. No resistance possible.',wrn:'SOCIETY USE ONLY',sec:'12 "donations" logged. None listed as willing.',uv:'Map to procurement sites — workhouses, asylums, orphanages',hs:true,seal:true,mix:'knockout',anim:'pulse',sml:'Nothing. Completely odourless. That is the point.'}},
{{id:'mercy',nm:'"Final Mercy"',sub:'Terminal',col:0xaa0000,liq:0x220000,lv:0.9,row:2,sl:3,sh:'tiny_vial',desc:'Ends suffering. Immediately. Three doses missing.',cnt:'Death in seconds. Three doses unaccounted for.',wrn:'AUTHORIZED ONLY',sec:'Three missing. Three "natural" deaths this month.',uv:'"THANK YOU" scratched inside by a fingernail',hs:INT>=4,seal:true,mix:'lethal',anim:'pulse',sml:'Sweet. Gentle. Like falling asleep in a garden. That is the cruelty.'}},
{{id:'blood_sc',nm:'Blood — S.C.',sub:'Specimen',col:0xdddddd,liq:0x660000,lv:0.6,row:2,sl:4,sh:'test_tube',desc:'Initials S.C. — Sebastian Carlisle. Why is his blood preserved?',cnt:'Still viable. Someone tends this regularly.',wrn:'DO NOT DISCARD',sec:'Compatible with Vita Aeterna. That is why he lives.',uv:'TEST RESULTS: Universal compatibility. "ESSENTIAL"',hs:true,seal:false,mix:'blood',anim:'none',sml:'Iron. Warm. Disturbingly fresh.'}},

{{id:'morphine',nm:'Morphine',sub:'Analgesic',col:0x0a2e1c,liq:0x113322,lv:0.4,row:3,sl:0,sh:'dark_cyl',desc:'Distilled mercy. Requisitioned in impossible bulk.',cnt:'40 vials this month. 12 patients on the ward.',wrn:'LOG ALL USAGE',sec:'Where do the other 28 vials go?',uv:'Forged requisition signatures visible',hs:INT>=3,seal:false,mix:'sedative',anim:'bubble',sml:'Almost nothing. A faint bitterness. Then numbness.'}},
{{id:'teeth',nm:'Teeth',sub:'Collection — 47',col:0xffffdd,liq:0xffffcc,lv:0.8,row:3,sl:1,sh:'wide_jar',desc:'47 teeth in alcohol. From at least 12 different sources.',cnt:'Mixed adult and child. Some show no extraction marks.',wrn:'SPECIMEN',sec:'Some have root tissue. Taken from the living.',uv:'Names scratched into individual teeth with a needle',hs:INT>=3,seal:false,mix:'none',anim:'float',sml:'Alcohol. Bone. Something sweet-rotten underneath.'}},
{{id:'phosphorus',nm:'Phosphorus',sub:'Luminescent',col:0xdddd44,liq:0xeeff88,lv:0.5,row:3,sl:2,sh:'wire_flask',desc:'Glows green in darkness. Burns on contact with air.',cnt:'Sealed under water to prevent ignition.',wrn:'INCENDIARY',sec:'Used in "the development process." All records redacted.',uv:'Chemical formula for a compound not yet discovered',hs:INT>=4,seal:false,mix:'none',anim:'sparkle',sml:'Garlic. Faintly. Then your lungs burn.'}},
{{id:'brain',nm:'Nerve Food',sub:'Cerebral Extract',col:0xbbaa88,liq:0xccbbaa,lv:0.5,row:3,sl:3,sh:'ornate_jar',desc:'Grey matter in preservation fluid. Sold as mental energy tonic.',cnt:'Chunks of tissue float in clouded fluid.',wrn:'TWICE DAILY',sec:'Human brain. They call it medicine. It is cannibalism.',uv:'"GENIUS DONOR — St. Mary Bethlem" (Bedlam asylum)',hs:true,seal:false,mix:'none',anim:'float',sml:'Formaldehyde. Fat. Something deeply, instinctively wrong.'}},
{{id:'essence',nm:'"Youth"',sub:'Rejuvenation Cream',col:0xddccbb,liq:0xffffdd,lv:0.6,row:3,sl:4,sh:'ceramic_pot',desc:'Softens wrinkles. Base ingredient: human fat from the unclaimed dead.',cnt:'Thick. Yellowish. Smells of tallow and poverty.',wrn:'EXTERNAL USE',sec:'Supplied by resurrection men. The fat of the forgotten.',uv:'Supplier ledger: Burke & Sons, body dealers',hs:INT>=4,seal:false,mix:'none',anim:'none',sml:'Tallow. Rendered fat. Cheap candles and poverty.'}}
];

/* Mix combos */
const MIX={{
'sedative+sedative':['Lethal Overdose','A dose no one wakes from.','#880000'],
'sedative+knockout':['Deep Sleep','Hours of dreamless unconsciousness.','#666688'],
'sedative+stimulant':['Confusion Tonic','Disorientation and compliance.','#888866'],
'knockout+knockout':['Instant Blackout','Seconds. No resistance.','#444466'],
'poison+poison':['Certain Death','No antidote exists for this.','#880000'],
'poison+blood':['Tainted Blood','For the communion...','#aa0022'],
'blood+blood':['Vita Renewed','The Society\\'s sacrament, replenished.','#cc0000'],
'stimulant+stimulant':['Heart Attack','Too much. The heart cannot take it.','#ff4444'],
'stimulant+poison':['Painful End','Alert and dying. The cruelest combination.','#cc4400'],
'poison+knockout':['Silent Murder','Unconscious, then dead. No struggle.','#553355'],
'preserve+blood':['Eternal Specimen','Preserved forever. Still aware?','#668866'],
'lethal+blood':['Mercy Communion','The final sacrament.','#440000'],
'sedative+blood':['Blood Wine','Drugged communion. Compliance.','#884444'],
'stimulant+blood':['Awakened Blood','The blood quickens. Moves on its own.','#cc2222'],
'knockout+lethal':['Gentle Death','Unconscious first. Then gone.','#443344'],
'preserve+lethal':['Preserved Death','Dead but undecaying. A specimen.','#556655'],
'stimulant+knockout':['Seizure','The body cannot decide. Convulsions.','#996633']
}};

/* Drawer items */
const DI=[
{{id:'scalpel',nm:'Surgical Scalpel',ds:'Initials A.F. on handle. Blade shows dried blood.',lk:false}},
{{id:'letters',nm:'Correspondence',ds:'Letters from T.B. to Fitzroy. Unmistakable blackmail.',lk:false}},
{{id:'journal',nm:'Private Journal',ds:"Fitzroy's personal notes. Encoded in cipher.",lk:false}},
{{id:'society',nm:'🔒 Society Drawer',ds:'Locked. Three-digit combination.',lk:true}},
{{id:'blackbook',nm:'The Black Book',ds:'Ledger of procured subjects. Names, dates, prices.',lk:true}},
{{id:'mask',nm:'Ceremonial Mask',ds:'Red leather. Worn for "special procedures."',lk:true}}
];

/* ===== THREE.JS SETUP ===== */
const ctr=E('container'),scene=new THREE.Scene();
scene.background=new THREE.Color({bg});
if(MD!=='clinical')scene.fog=new THREE.FogExp2({bg},0.025);
function cW(){{return ctr.clientWidth||innerWidth||600;}}
function cH(){{return ctr.clientHeight||innerHeight||500;}}
const cam=new THREE.PerspectiveCamera(50,cW()/cH(),0.1,100);
cam.position.set(0,1.5,6);cam.lookAt(0,1.2,0);
const ren=new THREE.WebGLRenderer({{antialias:true}});
ren.setSize(cW(),cH());ren.setPixelRatio(Math.min(devicePixelRatio,2));
ren.shadowMap.enabled=true;ctr.appendChild(ren.domElement);
const ray=new THREE.Raycaster(),mouse=new THREE.Vector2();

// Lights
scene.add(new THREE.AmbientLight(0xffffff,{ambient}));
scene.add(new THREE.HemisphereLight(0xffffff,{wood_dark},0.4));
const dL=new THREE.DirectionalLight({light},1);dL.position.set(3,5,4);scene.add(dL);
const cndL=new THREE.PointLight({light},0.8,12);cndL.position.set(-1.5,3.4,0.5);cndL.castShadow=true;scene.add(cndL);
const fL=new THREE.PointLight({light},0.3,15);fL.position.set(2,2,3);scene.add(fL);
const uvL=new THREE.PointLight(0x8800ff,0,15);uvL.position.set(0,2,3);scene.add(uvL);

// Materials
const wM=new THREE.MeshLambertMaterial({{color:{wood}}});
const dkM=new THREE.MeshLambertMaterial({{color:{wood_dark}}});
const mtM=new THREE.MeshLambertMaterial({{color:{metal}}});
const bnM=new THREE.MeshLambertMaterial({{color:0xe8dcc8}});
const wxM=new THREE.MeshLambertMaterial({{color:0x880000}});
const ckM=new THREE.MeshLambertMaterial({{color:0x8b7355}});
const lbM=new THREE.MeshLambertMaterial({{color:0xffffee,side:2}});
const cwM=new THREE.MeshBasicMaterial({{color:0xccccbb,transparent:true,opacity:0.12,side:2}});
const blkM=new THREE.MeshLambertMaterial({{color:0x111111}});

/* ===== CABINET BODY ===== */
const CW=4.2,CH=3.4,CD=0.75,ROWS=4,SH=CH/ROWS;
const bk=new THREE.Mesh(new THREE.BoxGeometry(CW,CH,0.05),dkM);
bk.position.set(0,CH/2,-CD/2);bk.userData={{isBack:true}};scene.add(bk);
[-1,1].forEach(s=>{{const sd=new THREE.Mesh(new THREE.BoxGeometry(0.08,CH,CD),wM);sd.position.set(s*CW/2,CH/2,0);scene.add(sd);}});
scene.add(Object.assign(new THREE.Mesh(new THREE.BoxGeometry(CW+0.12,0.1,CD+0.1),wM),{{position:new THREE.Vector3(0,CH+0.05,0)}}));
scene.add(Object.assign(new THREE.Mesh(new THREE.BoxGeometry(CW+0.2,0.06,0.12),wM),{{position:new THREE.Vector3(0,CH+0.13,CD/2-0.06)}}));
scene.add(Object.assign(new THREE.Mesh(new THREE.BoxGeometry(CW,0.08,CD),wM),{{position:new THREE.Vector3(0,0.04,0)}}));
for(let i=0;i<=ROWS;i++)scene.add(Object.assign(new THREE.Mesh(new THREE.BoxGeometry(CW-0.1,0.04,CD-0.08),wM),{{position:new THREE.Vector3(0,i*SH,0)}}));
const drMesh=new THREE.Mesh(new THREE.BoxGeometry(CW-0.15,0.28,CD-0.1),dkM);
drMesh.position.set(0,-0.18,0.05);drMesh.userData={{isDr:true}};scene.add(drMesh);
[-0.9,0,0.9].forEach(x=>scene.add(Object.assign(new THREE.Mesh(new THREE.BoxGeometry(0.15,0.03,0.05),mtM),{{position:new THREE.Vector3(x,-0.18,CD/2)}})));

/* ===== PROPS ===== */
const propG=[];

// Skull
const skG=new THREE.Group();
skG.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.15,12,9),bnM),{{position:new THREE.Vector3(0,0.15,0),scale:new THREE.Vector3(1,1.1,1.2)}}));
[-0.045,0.045].forEach(x=>skG.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.035,5,4),new THREE.MeshBasicMaterial({{color:0x111111}})),{{position:new THREE.Vector3(x,0.14,0.13)}})));
skG.add(Object.assign(new THREE.Mesh(new THREE.BoxGeometry(0.12,0.035,0.07),bnM),{{position:new THREE.Vector3(0,0.04,0.09)}}));
skG.position.set(1.5,CH+0.12,0.1);skG.rotation.y=-0.3;
skG.userData={{type:'prop',title:'Human Skull',desc:'Memento mori. A reminder of mortality.',lore:INT>=3?'The jaw is wired shut. What was it trying to say?':''}};
scene.add(skG);propG.push(skG);

// Candle
const cdG=new THREE.Group();
cdG.add(new THREE.Mesh(new THREE.CylinderGeometry(0.09,0.11,0.035,10),mtM));
cdG.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.035,0.22,8),new THREE.MeshLambertMaterial({{color:0xfffff0}})),{{position:new THREE.Vector3(0,0.13,0)}}));
const flm=new THREE.Mesh(new THREE.SphereGeometry(0.02,6,4),new THREE.MeshBasicMaterial({{color:{light},transparent:true,opacity:0.9}}));
flm.scale.set(0.7,1.5,0.7);flm.position.set(0,0.27,0);cdG.add(flm);
cdG.position.set(-1.5,CH+0.12,0.2);
cdG.userData={{type:'prop',title:'Tallow Candle',desc:'The only light. It flickers as if breathing.',lore:INT>=3?'The flame leans toward certain bottles. As if drawn.':''}};
scene.add(cdG);propG.push(cdG);

// Books
const bkG=new THREE.Group();
[0x2a1510,0x1a2a1a,0x1a1a2a,0x3a2515].forEach((c,i)=>{{
    const bk2=new THREE.Mesh(new THREE.BoxGeometry(0.18,0.04+i*0.005,0.25),new THREE.MeshLambertMaterial({{color:c}}));
    bk2.position.y=i*0.045;bkG.add(bk2);
}});
bkG.position.set(-0.8,CH+0.14,0.05);
bkG.userData={{type:'prop',title:'Leather-Bound Books',desc:'Medical texts. One is pulled out at an angle.',lore:INT>=3?'The unmarked book falls open to a page about preserving consciousness during vivisection.':''}};
scene.add(bkG);propG.push(bkG);

// Scales
const scG=new THREE.Group();
scG.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.08,0.1,0.02,12),mtM),{{position:new THREE.Vector3(0,0,0)}}));
scG.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.02,0.35,8),mtM),{{position:new THREE.Vector3(0,0.18,0)}}));
const beam=new THREE.Mesh(new THREE.BoxGeometry(0.35,0.01,0.015),mtM);
beam.position.set(0,0.36,0);beam.rotation.z=0.08;scG.add(beam);
[-0.15,0.15].forEach((x,i)=>{{
    const pan=new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.06,0.01,12),mtM);
    pan.position.set(x,0.28+i*0.05,0);scG.add(pan);
}});
scG.position.set(0.5,2.58,0.15);scG.scale.set(0.7,0.7,0.7);
scG.userData={{type:'prop',title:'Brass Balance Scales',desc:'For measuring precise doses.',lore:INT>=3?'The lower pan holds reddish organic residue. Not a powder.':''}};
scene.add(scG);propG.push(scG);

// Mortar & Pestle
const mpG=new THREE.Group();
mpG.add(new THREE.Mesh(new THREE.CylinderGeometry(0.07,0.05,0.08,12),new THREE.MeshLambertMaterial({{color:0x888880}})));
const pestle=new THREE.Mesh(new THREE.CylinderGeometry(0.012,0.025,0.16,8),new THREE.MeshLambertMaterial({{color:0x888880}}));
pestle.position.set(0.03,0.08,0);pestle.rotation.z=-0.4;mpG.add(pestle);
mpG.position.set(-0.3,2.58,0.2);mpG.scale.set(0.8,0.8,0.8);
mpG.userData={{type:'prop',title:'Mortar & Pestle',desc:'Stone. Well-used.',lore:INT>=3?'The residue matches no known pharmaceutical compound.':''}};
scene.add(mpG);propG.push(mpG);

// Magnifying Glass
const mgG=new THREE.Group();
mgG.add(Object.assign(new THREE.Mesh(new THREE.TorusGeometry(0.05,0.008,8,16),mtM),{{position:new THREE.Vector3(0,0,0)}}));
const handle=new THREE.Mesh(new THREE.CylinderGeometry(0.008,0.01,0.15,6),mtM);
handle.position.set(0,-0.1,0);handle.rotation.z=0.3;mgG.add(handle);
mgG.position.set(1.1,1.37,0.3);
mgG.userData={{type:'prop',title:'Magnifying Glass',desc:'Brass and crystal.',lore:INT>=3?'Under magnification, the labels reveal a second language.':''}};
scene.add(mgG);propG.push(mgG);

// Syringe
const syG=new THREE.Group();
syG.add(new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.015,0.18,8),new THREE.MeshLambertMaterial({{color:0xdddddd,transparent:true,opacity:0.5}})));
syG.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.002,0.001,0.06,4),mtM),{{position:new THREE.Vector3(0,-0.12,0)}}));
syG.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.018,0.018,0.02,8),mtM),{{position:new THREE.Vector3(0,0.1,0)}}));
syG.position.set(0.2,1.37,0.32);syG.rotation.z=0.1;
syG.userData={{type:'prop',title:'Hypodermic Syringe',desc:'Brass and glass. Victorian design.',lore:INT>=3?'Contains traces of laudanum and something unknown.':''}};
scene.add(syG);propG.push(syG);

// Pocket Watch
const pwG=new THREE.Group();
pwG.add(new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.04,0.01,16),mtM));
pwG.add(Object.assign(new THREE.Mesh(new THREE.CircleGeometry(0.035,16),new THREE.MeshBasicMaterial({{color:0xffffee,side:2}})),{{position:new THREE.Vector3(0,0,0.006)}}));
pwG.position.set(-0.6,1.37,0.35);pwG.rotation.x=-0.5;
pwG.userData={{type:'prop',title:'Pocket Watch',desc:'Gold. Stopped.',lore:INT>=3?'Stopped at 11:47. Time of death?':''}};
scene.add(pwG);propG.push(pwG);

// Cobwebs
[[1.6,2.8,-0.1],[1.6,1.1,0.1],[-1.6,2.5,0],[-1.6,0.8,0.1]].forEach(p=>{{
    const cw=new THREE.Mesh(new THREE.PlaneGeometry(0.35,0.3),cwM);
    cw.position.set(p[0],p[1],p[2]);cw.rotation.y=p[0]>0?-0.3:0.3;scene.add(cw);
}});

// Herbs
const herbs=[];
[{{x:-0.3}},{{x:0.2}},{{x:0.7}},{{x:-0.9}}].forEach((h,i)=>{{
    const hG=new THREE.Group();
    for(let j=0;j<4;j++){{
        const stem=new THREE.Mesh(new THREE.CylinderGeometry(0.003,0.003,0.18+j*0.02,4),new THREE.MeshLambertMaterial({{color:0x2a4a1a}}));
        stem.position.set(j*0.01-0.015,-0.09-j*0.01,0);hG.add(stem);
    }}
    hG.position.set(h.x,CH+0.01,0.2);hG.rotation.z=Math.PI;
    scene.add(hG);herbs.push(hG);
}});

// Dust
const dustN=80+INT*20;
const dustGeo=new THREE.BufferGeometry();
const dPos=new Float32Array(dustN*3),dVel=[];
for(let i=0;i<dustN;i++){{
    dPos[i*3]=Math.random()*CW-CW/2;dPos[i*3+1]=Math.random()*CH;dPos[i*3+2]=Math.random()*CD-CD/2;
    dVel.push({{x:(Math.random()-0.5)*0.001,y:Math.random()*0.002+0.0005}});
}}
dustGeo.setAttribute('position',new THREE.BufferAttribute(dPos,3));
const dustPts=new THREE.Points(dustGeo,new THREE.PointsMaterial({{color:{glow},size:0.02,transparent:true,opacity:0.35}}));
scene.add(dustPts);

// Mouse
let mouseGrp=null;
if(INT>=2){{
    mouseGrp=new THREE.Group();
    const mbod=new THREE.Mesh(new THREE.SphereGeometry(0.03,6,4),new THREE.MeshLambertMaterial({{color:0x666655}}));
    mbod.scale.set(1,0.8,1.5);mouseGrp.add(mbod);
    const mhd=new THREE.Mesh(new THREE.SphereGeometry(0.018,6,4),new THREE.MeshLambertMaterial({{color:0x666655}}));
    mhd.position.set(0,0.005,0.04);mouseGrp.add(mhd);
    [-0.01,0.01].forEach(x=>{{
        const eye=new THREE.Mesh(new THREE.SphereGeometry(0.004,4,3),new THREE.MeshBasicMaterial({{color:0x000000}}));
        eye.position.set(x,0.012,0.054);mouseGrp.add(eye);
    }});
    mouseGrp.position.set(0.9,0.72,0.28);
    mouseGrp.userData={{type:'prop',title:'Mouse',desc:'It watches you.',lore:INT>=4?'It is gnawing on something pink.':''}};
    scene.add(mouseGrp);propG.push(mouseGrp);
}}

/* ===== 3D BOTTLES ===== */
const bottles=[];
function slotPos(row,slot){{
    const sx=-CW/2+0.5,sp=(CW-1)/4;
    return{{x:sx+slot*sp,y:row*SH+0.2,z:0}};
}}

function mkBottle(b){{
    const g=new THREE.Group();
    const gM=new THREE.MeshLambertMaterial({{color:b.col,transparent:true,opacity:0.55}});
    const gMs=new THREE.MeshLambertMaterial({{color:b.col,transparent:true,opacity:0.75}});
    const lM=new THREE.MeshLambertMaterial({{color:b.liq,transparent:true,opacity:0.85}});
    const hb=new THREE.Mesh(new THREE.BoxGeometry(0.26,0.48,0.26),new THREE.MeshBasicMaterial({{transparent:true,opacity:0.001,depthWrite:false}}));
    hb.userData={{bRef:b}};g.add(hb);
    const gl=new THREE.Group();
    let nY=0.2;

    if(b.sh==='rect'){{
        gl.add(new THREE.Mesh(new THREE.BoxGeometry(0.12,0.28,0.08),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.04,0.08,8),gM),{{position:new THREE.Vector3(0,0.18,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.BoxGeometry(0.13,0.015,0.09),mtM),{{position:new THREE.Vector3(0,0.08,0)}}));
        g.add(new THREE.Mesh(new THREE.BoxGeometry(0.10,0.24*b.lv,0.065),lM));g.children[g.children.length-1].position.y=-0.14+0.24*b.lv/2+0.02;nY=0.24;
    }}else if(b.sh==='hex'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.065,0.075,0.28,6),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.04,0.07,6),gM),{{position:new THREE.Vector3(0,0.175,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.035,0.035,0.025,12),wxM),{{position:new THREE.Vector3(0,0.22,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.052,0.062,0.24*b.lv,6),lM));g.children[g.children.length-1].position.y=-0.14+0.24*b.lv/2+0.02;nY=0.25;
    }}else if(b.sh==='banded'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.07,0.3,16),gM));
        for(let i=0;i<3;i++){{const r=new THREE.Mesh(new THREE.TorusGeometry(0.065,0.008,8,16),mtM);r.position.y=-0.08+i*0.1;r.rotation.x=Math.PI/2;gl.add(r);}}
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.035,0.06,12),gM),{{position:new THREE.Vector3(0,0.18,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.048,0.058,0.26*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.15+0.26*b.lv/2+0.02;nY=0.23;
    }}else if(b.sh==='jug'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.11,0.32,16),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.06,0.08,12),gM),{{position:new THREE.Vector3(0,0.2,0)}}));
        const hdl=new THREE.Mesh(new THREE.TorusGeometry(0.05,0.012,8,12,Math.PI),gMs);hdl.position.set(0.11,0.05,0);hdl.rotation.set(0,Math.PI/2,Math.PI/2);gl.add(hdl);
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.085,0.095,0.28*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.16+0.28*b.lv/2+0.02;nY=0.26;
    }}else if(b.sh==='hex_plain'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.065,0.07,0.26,6),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.035,0.06,6),gM),{{position:new THREE.Vector3(0,0.16,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.052,0.058,0.22*b.lv,6),lM));g.children[g.children.length-1].position.y=-0.13+0.22*b.lv/2;nY=0.21;
    }}else if(b.sh==='ribbed'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.07,0.08,0.28,12),gM));
        for(let i=0;i<8;i++){{const rb=new THREE.Mesh(new THREE.BoxGeometry(0.008,0.26,0.02),gMs);const a=(i/8)*Math.PI*2;rb.position.set(Math.sin(a)*0.075,0,Math.cos(a)*0.075);rb.rotation.y=a;gl.add(rb);}}
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.028,0.04,0.07,8),gM),{{position:new THREE.Vector3(0,0.175,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.055,0.065,0.24*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.14+0.24*b.lv/2+0.02;nY=0.24;
    }}else if(b.sh==='oval'){{
        const bd=new THREE.Mesh(new THREE.SphereGeometry(0.08,16,12),gM);bd.scale.set(0.8,1.4,0.6);gl.add(bd);
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.02,0.03,0.12,12),gM),{{position:new THREE.Vector3(0,0.15,0)}}));
        g.add(new THREE.Mesh(new THREE.SphereGeometry(0.065,12,8),lM));g.children[g.children.length-1].scale.set(0.75,b.lv*1.2,0.55);g.children[g.children.length-1].position.y=-0.04;nY=0.22;
    }}else if(b.sh==='perfume'){{
        const bd=new THREE.Mesh(new THREE.SphereGeometry(0.08,16,12),gM);bd.scale.set(0.8,1.4,0.6);gl.add(bd);
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.02,0.03,0.12,12),gM),{{position:new THREE.Vector3(0,0.15,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.03,8,6),gMs),{{position:new THREE.Vector3(0,0.24,0)}}));
        g.add(new THREE.Mesh(new THREE.SphereGeometry(0.065,12,8),lM));g.children[g.children.length-1].scale.set(0.75,b.lv*1.2,0.55);g.children[g.children.length-1].position.y=-0.04;nY=0.28;
    }}else if(b.sh==='hex_ridged'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.07,0.08,0.26,6),gM));
        for(let i=0;i<4;i++){{const rd=new THREE.Mesh(new THREE.BoxGeometry(0.005,0.22,0.16),gMs);rd.rotation.y=i*Math.PI/3;gl.add(rd);}}
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.035,0.08,6),gM),{{position:new THREE.Vector3(0,0.17,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.055,0.065,0.22*b.lv,6),lM));g.children[g.children.length-1].position.y=-0.13+0.22*b.lv/2;nY=0.23;
    }}else if(b.sh==='dome_jar'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.09,0.1,0.24,16),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.09,12,8,0,Math.PI*2,0,Math.PI/2),gM),{{position:new THREE.Vector3(0,0.12,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.06,0.03,12),mtM),{{position:new THREE.Vector3(0,0.18,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.075,0.085,0.2*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.1+0.2*b.lv/2;nY=0.22;
    }}else if(b.sh==='teardrop'){{
        const bd=new THREE.Mesh(new THREE.SphereGeometry(0.09,16,16),gM);bd.scale.set(1,1.5,1);bd.position.y=-0.02;gl.add(bd);
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.02,0.04,0.12,12),gM),{{position:new THREE.Vector3(0,0.18,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.025,8,8),wxM),{{position:new THREE.Vector3(0,0.02,0.09),scale:new THREE.Vector3(1,1,0.3)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.ConeGeometry(0.03,0.06,8),gMs),{{position:new THREE.Vector3(0,0.28,0)}}));
        g.add(new THREE.Mesh(new THREE.SphereGeometry(0.075,12,12),lM));g.children[g.children.length-1].scale.set(0.9,b.lv*1.3,0.9);g.children[g.children.length-1].position.y=-0.04;nY=0.32;
    }}else if(b.sh==='dropper'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.055,0.32,12),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.018,0.025,0.08,8),gM),{{position:new THREE.Vector3(0,0.2,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.018,0.06,8),blkM),{{position:new THREE.Vector3(0,0.27,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.025,8,6),blkM),{{position:new THREE.Vector3(0,0.32,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.045,0.28*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.16+0.28*b.lv/2+0.02;nY=0.35;
    }}else if(b.sh==='black_rect'){{
        gl.add(new THREE.Mesh(new THREE.BoxGeometry(0.1,0.3,0.08),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.02,0.035,0.07,8),gM),{{position:new THREE.Vector3(0,0.185,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.03,0.04,12),blkM),{{position:new THREE.Vector3(0,0.24,0)}}));
        g.add(new THREE.Mesh(new THREE.BoxGeometry(0.085,0.26*b.lv,0.065),lM));g.children[g.children.length-1].position.y=-0.15+0.26*b.lv/2+0.02;nY=0.28;
    }}else if(b.sh==='tiny_vial'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.035,0.18,12),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.02,0.04,8),gM),{{position:new THREE.Vector3(0,0.11,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.025,8,6),bnM),{{position:new THREE.Vector3(0,0.16,0),scale:new THREE.Vector3(1,0.8,0.8)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.022,0.028,0.15*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.09+0.15*b.lv/2;nY=0.19;
    }}else if(b.sh==='test_tube'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.025,0.28,12),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.025,12,8,0,Math.PI*2,0,Math.PI/2),gM),{{position:new THREE.Vector3(0,-0.14,0),rotation:new THREE.Euler(Math.PI,0,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.TorusGeometry(0.028,0.006,6,12),gMs),{{position:new THREE.Vector3(0,0.14,0),rotation:new THREE.Euler(Math.PI/2,0,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.02,0.02,0.24*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.12+0.24*b.lv/2;nY=0.18;
    }}else if(b.sh==='dark_cyl'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.055,0.065,0.28,12),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.035,0.06,8),gM),{{position:new THREE.Vector3(0,0.17,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.TorusGeometry(0.015,0.004,6,8,Math.PI),mtM),{{position:new THREE.Vector3(0,0.06,0.065)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.BoxGeometry(0.03,0.02,0.01),mtM),{{position:new THREE.Vector3(0,0.045,0.065)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.042,0.052,0.24*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.14+0.24*b.lv/2+0.02;nY=0.22;
    }}else if(b.sh==='wide_jar'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.09,0.22,16),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.11,0.11,0.04,16),mtM),{{position:new THREE.Vector3(0,0.13,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.085,0.075,0.18*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.09+0.18*b.lv/2;nY=0.18;
    }}else if(b.sh==='wire_flask'){{
        gl.add(new THREE.Mesh(new THREE.SphereGeometry(0.09,16,12),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.04,0.1,8),gM),{{position:new THREE.Vector3(0,0.12,0)}}));
        for(let i=0;i<6;i++){{const a=i*Math.PI/3;const w=new THREE.Mesh(new THREE.CylinderGeometry(0.003,0.003,0.22,3),mtM);w.position.set(Math.sin(a)*0.095,0,Math.cos(a)*0.095);gl.add(w);}}
        for(let y of [-0.05,0.05]){{const r=new THREE.Mesh(new THREE.TorusGeometry(0.095,0.003,4,12),mtM);r.position.y=y;r.rotation.x=Math.PI/2;gl.add(r);}}
        g.add(new THREE.Mesh(new THREE.SphereGeometry(0.075,12,8),lM));g.children[g.children.length-1].scale.set(1,b.lv,1);g.children[g.children.length-1].position.y=-0.03;nY=0.2;
    }}else if(b.sh==='ornate_jar'){{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.09,0.1,0.22,12),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.TorusGeometry(0.095,0.01,6,12),mtM),{{position:new THREE.Vector3(0,0.05,0),rotation:new THREE.Euler(Math.PI/2,0,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.085,12,8,0,Math.PI*2,0,Math.PI/2),mtM),{{position:new THREE.Vector3(0,0.11,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.02,0.04,8),mtM),{{position:new THREE.Vector3(0,0.19,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.075,0.085,0.18*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.09+0.18*b.lv/2;nY=0.22;
    }}else if(b.sh==='ceramic_pot'){{
        const pM=new THREE.MeshLambertMaterial({{color:0xd4c4a8}});
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.08,0.09,0.2,16),pM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.TorusGeometry(0.085,0.015,8,16),pM),{{position:new THREE.Vector3(0,0.1,0),rotation:new THREE.Euler(Math.PI/2,0,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.075,0.08,0.04,12),pM),{{position:new THREE.Vector3(0,0.14,0)}}));
        gl.add(Object.assign(new THREE.Mesh(new THREE.SphereGeometry(0.02,8,6),pM),{{position:new THREE.Vector3(0,0.18,0)}}));
        nY=0.2;
    }}else{{
        gl.add(new THREE.Mesh(new THREE.CylinderGeometry(0.07,0.08,0.3,12),gM));
        gl.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.04,0.06,8),gM),{{position:new THREE.Vector3(0,0.18,0)}}));
        g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.055,0.065,0.26*b.lv,12),lM));g.children[g.children.length-1].position.y=-0.15+0.26*b.lv/2+0.02;nY=0.23;
    }}
    g.add(gl);
    if(!['perfume','dome_jar','wide_jar','ornate_jar','ceramic_pot','dropper'].includes(b.sh)){{
        g.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.035,0.045,8),ckM),{{position:new THREE.Vector3(0,nY,0)}}));
    }}
    if(b.id!=='unmarked'&&b.sh!=='ceramic_pot'){{
        const lW=0.09,lH=0.07,lZ=b.sh==='jug'?0.11:b.sh.includes('wide')||b.sh.includes('dome')||b.sh.includes('ornate')?0.1:b.sh.includes('rect')?0.042:0.085;
        g.add(Object.assign(new THREE.Mesh(new THREE.PlaneGeometry(lW,lH),lbM),{{position:new THREE.Vector3(0,0,lZ)}}));
    }}
    return g;
}}

B.forEach(b=>{{
    try{{
        const g=mkBottle(b);
        const p=slotPos(b.row,b.sl);
        g.position.set(p.x,p.y,p.z);
        g.userData=b;
        scene.add(g);bottles.push(g);
    }}catch(e){{console.error('Bottle err:',b.id,e);}}
}});

/* ===== CAMERA ===== */
let isD=false,hasMv=false,px=0,py=0,theta=0,phi=1.2,dist=6;
const tgt=new THREE.Vector3(0,1.3,0);
function updCam(){{
    cam.position.x=tgt.x+dist*Math.sin(phi)*Math.sin(theta);
    cam.position.y=tgt.y+dist*Math.cos(phi);
    cam.position.z=tgt.z+dist*Math.sin(phi)*Math.cos(theta);
    cam.lookAt(tgt);
}}
ren.domElement.onmousedown=e=>{{isD=true;hasMv=false;px=e.clientX;py=e.clientY;}};
window.onmouseup=()=>{{isD=false;}};
ren.domElement.onmousemove=e=>{{
    mouse.x=(e.clientX/cW())*2-1;mouse.y=-(e.clientY/cH())*2+1;
    if(isD){{const dx=e.clientX-px,dy=e.clientY-py;if(Math.abs(dx)>3||Math.abs(dy)>3)hasMv=true;if(hasMv){{theta+=dx*0.005;phi=Math.max(0.5,Math.min(1.5,phi+dy*0.005));px=e.clientX;py=e.clientY;updCam();}}}}
}};
ren.domElement.onwheel=e=>{{e.preventDefault();dist=Math.max(3.5,Math.min(10,dist+e.deltaY*0.005));updCam();}};
ren.domElement.ontouchstart=e=>{{if(e.touches.length===1){{isD=true;hasMv=false;px=e.touches[0].clientX;py=e.touches[0].clientY;}}}};
ren.domElement.ontouchmove=e=>{{if(!isD||e.touches.length!==1)return;const dx=e.touches[0].clientX-px,dy=e.touches[0].clientY-py;if(Math.abs(dx)>3||Math.abs(dy)>3)hasMv=true;if(hasMv){{theta+=dx*0.005;phi=Math.max(0.5,Math.min(1.5,phi+dy*0.005));px=e.touches[0].clientX;py=e.touches[0].clientY;updCam();}}}};
ren.domElement.ontouchend=()=>{{isD=false;}};
updCam();

/* ===== 2D BOTTLE DRAWING ===== */
const zc=E('zc'),zx=zc.getContext('2d');
const W2=zc.width,H2=zc.height;
function hexS(n){{return'#'+n.toString(16).padStart(6,'0');}}

function draw2d(b){{
    const w=W2,h=H2;
    zx.clearRect(0,0,w,h);
    zx.save();
    const cx=w/2,by=h*0.82;
    if(shk)zx.translate(Math.sin(wv*3)*8,Math.sin(wv*5)*3);
    const col=hexS(b.col),lqc=hexS(b.liq);
    if(litOn){{const bg=zx.createRadialGradient(cx,h*0.45,10,cx,h*0.45,150);bg.addColorStop(0,'rgba(255,200,100,0.15)');bg.addColorStop(1,'transparent');zx.fillStyle=bg;zx.fillRect(0,0,w,h);}}
    const alpha=litOn?'66':'99',fillA=litOn?'44':'dd';
    zx.lineWidth=2;zx.strokeStyle=col;zx.fillStyle=col+alpha;

    // Shape rendering
    const bH=200,ty=by-bH;
    if(b.sh==='rect'||b.sh==='black_rect'){{
        const bW=80,bx=cx-bW/2;
        zx.fillRect(bx,ty,bW,bH);zx.strokeRect(bx,ty,bW,bH);
        zx.fillRect(cx-16,ty-35,32,38);zx.strokeRect(cx-16,ty-35,32,38);
        drawLiq(b,bx+4,by,bW-8,bH-10,lqc,fillA);drawCork(cx,ty-35);
        if(b.id!=='unmarked')drawLbl(b,cx,ty+bH*0.4);
    }}else if(b.sh.startsWith('hex')){{
        const r=45;
        zx.beginPath();for(let i=0;i<6;i++){{const a=i*Math.PI/3-Math.PI/6;zx.lineTo(cx+r*Math.cos(a),ty+bH/2+r*Math.sin(a)*2.1);}}zx.closePath();zx.fill();zx.stroke();
        zx.fillRect(cx-14,ty-30,28,35);zx.strokeRect(cx-14,ty-30,28,35);
        drawLiq(b,cx-r+6,by,r*2-12,bH-15,lqc,fillA);
        if(b.seal&&!sealBrk)drawSeal(cx,ty-30);else drawCork(cx,ty-30);
        if(b.id!=='unmarked')drawLbl(b,cx,ty+bH*0.45);
    }}else if(b.sh==='banded'){{
        const r=38;zx.beginPath();zx.ellipse(cx,ty+bH/2,r,bH/2,0,0,Math.PI*2);zx.fill();zx.stroke();
        zx.strokeStyle='{text}88';zx.lineWidth=3;for(let i=0;i<3;i++){{zx.beginPath();zx.moveTo(cx-r+5,ty+50+i*50);zx.lineTo(cx+r-5,ty+50+i*50);zx.stroke();}}
        zx.lineWidth=2;zx.strokeStyle=col;zx.fillRect(cx-14,ty-28,28,32);zx.strokeRect(cx-14,ty-28,28,32);
        drawLiq(b,cx-r+5,by,r*2-10,bH-20,lqc,fillA);drawCork(cx,ty-28);drawLbl(b,cx,ty+bH*0.45);
    }}else if(b.sh==='jug'){{
        const bW=100,bx=cx-bW/2;
        zx.beginPath();zx.moveTo(bx+5,by);zx.quadraticCurveTo(bx,by-bH*0.3,bx+10,ty+20);zx.lineTo(cx-20,ty);zx.lineTo(cx+20,ty);zx.lineTo(bx+bW-10,ty+20);zx.quadraticCurveTo(bx+bW,by-bH*0.3,bx+bW-5,by);zx.closePath();zx.fill();zx.stroke();
        zx.lineWidth=4;zx.beginPath();zx.arc(cx+bW/2+8,ty+bH*0.4,25,Math.PI*1.5,Math.PI*0.5);zx.stroke();zx.lineWidth=2;
        drawLiq(b,bx+10,by,bW-20,bH-25,lqc,fillA);drawCork(cx,ty);drawLbl(b,cx,ty+bH*0.42);
    }}else if(b.sh==='oval'||b.sh==='perfume'){{
        const rX=45,rY=90,cy2=by-rY;
        zx.beginPath();zx.ellipse(cx,cy2,rX,rY,0,0,Math.PI*2);zx.fill();zx.stroke();
        zx.fillRect(cx-12,cy2-rY-28,24,32);zx.strokeRect(cx-12,cy2-rY-28,24,32);
        if(b.sh==='perfume'){{zx.beginPath();zx.arc(cx,cy2-rY-38,14,0,Math.PI*2);zx.fill();zx.stroke();}}
        drawLiq(b,cx-rX+5,by,rX*2-10,rY*2-15,lqc,fillA);
        if(b.sh!=='perfume')drawCork(cx,cy2-rY-28);
        drawLbl(b,cx,cy2+10);
    }}else if(b.sh==='dome_jar'){{
        const r=55,dH=160,dty=by-dH;
        zx.fillRect(cx-r,dty,r*2,dH);zx.strokeRect(cx-r,dty,r*2,dH);
        zx.beginPath();zx.arc(cx,dty,r,Math.PI,0);zx.fill();zx.stroke();
        zx.fillStyle='{text}44';zx.fillRect(cx-35,dty-35,70,20);zx.strokeRect(cx-35,dty-35,70,20);
        drawLiq(b,cx-r+5,by,r*2-10,dH-10,lqc,fillA);drawLbl(b,cx,dty+dH*0.5);
    }}else if(b.sh==='teardrop'){{
        const rX=50,rY=80,cy2=by-rY-10;
        zx.beginPath();zx.moveTo(cx,cy2-rY-30);zx.quadraticCurveTo(cx-rX*0.8,cy2-rY*0.5,cx-rX,cy2+rY*0.3);zx.quadraticCurveTo(cx-rX,cy2+rY,cx,cy2+rY+5);zx.quadraticCurveTo(cx+rX,cy2+rY,cx+rX,cy2+rY*0.3);zx.quadraticCurveTo(cx+rX*0.8,cy2-rY*0.5,cx,cy2-rY-30);zx.fill();zx.stroke();
        zx.fillStyle='#880022';zx.beginPath();zx.arc(cx,cy2+10,12,0,Math.PI*2);zx.fill();
        zx.fillStyle='#aa0033';for(let i=0;i<5;i++){{const a=i*Math.PI*2/5;zx.beginPath();zx.ellipse(cx+Math.cos(a)*8,cy2+10+Math.sin(a)*8,5,3,a,0,Math.PI*2);zx.fill();}}
        drawLiq(b,cx-rX+10,by,rX*2-20,rY*2-10,lqc,fillA);
        if(b.seal&&!sealBrk)drawSeal(cx,cy2-rY-30);
        drawLbl(b,cx,cy2+40);
    }}else if(b.sh==='dropper'){{
        const r=28,dH=230,dty=by-dH;
        zx.beginPath();zx.ellipse(cx,dty+dH/2,r,dH/2,0,0,Math.PI*2);zx.fill();zx.stroke();
        zx.fillStyle='#333';zx.beginPath();zx.arc(cx,dty-15,18,0,Math.PI*2);zx.fill();zx.fillRect(cx-10,dty-5,20,25);
        drawLiq(b,cx-r+4,by,r*2-8,dH-25,lqc,fillA);drawLbl(b,cx,dty+dH*0.5);
    }}else if(b.sh==='tiny_vial'){{
        const r=20,dH=140,dty=by-dH;
        zx.beginPath();zx.ellipse(cx,dty+dH/2,r,dH/2,0,0,Math.PI*2);zx.fill();zx.stroke();
        zx.fillStyle='#dddccc';zx.beginPath();zx.arc(cx,dty-12,15,0,Math.PI*2);zx.fill();
        zx.fillStyle='#111';zx.beginPath();zx.arc(cx-5,dty-14,3,0,Math.PI*2);zx.arc(cx+5,dty-14,3,0,Math.PI*2);zx.fill();
        if(b.seal&&!sealBrk)drawSeal(cx,dty-5);
        drawLiq(b,cx-r+3,by,r*2-6,dH-15,lqc,fillA);drawLbl(b,cx,dty+dH*0.55);
    }}else if(b.sh==='test_tube'){{
        const r=18,dH=200,dty=by-dH;
        zx.fillRect(cx-r,dty,r*2,dH-r);zx.strokeRect(cx-r,dty,r*2,dH-r);
        zx.beginPath();zx.arc(cx,by-r,r,0,Math.PI);zx.fill();zx.stroke();
        zx.lineWidth=4;zx.beginPath();zx.arc(cx,dty,r+4,Math.PI,0);zx.stroke();zx.lineWidth=2;
        drawCork(cx,dty);drawLiq(b,cx-r+3,by-r,r*2-6,dH-r-5,lqc,fillA);drawLbl(b,cx,dty+dH*0.4);
    }}else if(b.sh==='dark_cyl'){{
        const r=35,dH=200,dty=by-dH;
        zx.beginPath();zx.ellipse(cx,dty+dH/2,r,dH/2,0,0,Math.PI*2);zx.fill();zx.stroke();
        zx.strokeStyle='rgba(255,255,255,0.15)';zx.lineWidth=5;zx.beginPath();zx.moveTo(cx-15,dty+dH*0.3);zx.lineTo(cx+15,dty+dH*0.3);zx.moveTo(cx,dty+dH*0.3-15);zx.lineTo(cx,dty+dH*0.3+15);zx.stroke();
        zx.lineWidth=2;zx.strokeStyle=col;zx.fillRect(cx-12,dty-28,24,32);zx.strokeRect(cx-12,dty-28,24,32);
        drawLiq(b,cx-r+4,by,r*2-8,dH-20,lqc,fillA);drawCork(cx,dty-28);drawLbl(b,cx,dty+dH*0.55);
    }}else if(b.sh==='wide_jar'){{
        const r=60,dH=150,dty=by-dH;
        zx.fillRect(cx-r,dty,r*2,dH);zx.strokeRect(cx-r,dty,r*2,dH);
        zx.fillStyle='{text}55';for(let i=0;i<3;i++)zx.fillRect(cx-r-2,dty-18+i*6,r*2+4,4);
        drawLiq(b,cx-r+5,by,r*2-10,dH-10,lqc,fillA);drawLbl(b,cx,dty+dH*0.45);
    }}else if(b.sh==='wire_flask'){{
        const r=50,cy2=by-r-20;
        zx.beginPath();zx.arc(cx,cy2,r,0,Math.PI*2);zx.fill();zx.stroke();
        zx.fillRect(cx-14,cy2-r-28,28,32);zx.strokeRect(cx-14,cy2-r-28,28,32);
        zx.strokeStyle='{text}55';zx.lineWidth=1;for(let i=0;i<6;i++){{const a=i*Math.PI/3;zx.beginPath();zx.moveTo(cx+Math.cos(a)*r*0.3,cy2-r*0.8);zx.lineTo(cx+Math.cos(a)*r,cy2);zx.lineTo(cx+Math.cos(a)*r*0.3,cy2+r*0.8);zx.stroke();}}
        zx.strokeStyle=col;zx.lineWidth=2;drawLiq(b,cx-r+8,by,r*2-16,r*2-15,lqc,fillA);drawCork(cx,cy2-r-28);drawLbl(b,cx,cy2+10);
    }}else if(b.sh==='ornate_jar'){{
        const r=55,dH=155,dty=by-dH;
        zx.fillRect(cx-r,dty,r*2,dH);zx.strokeRect(cx-r,dty,r*2,dH);
        zx.strokeStyle='{text}88';zx.lineWidth=4;zx.beginPath();zx.moveTo(cx-r,dty+dH*0.4);zx.lineTo(cx+r,dty+dH*0.4);zx.stroke();
        zx.fillStyle='{text}33';zx.beginPath();zx.arc(cx,dty,r*0.85,Math.PI,0);zx.fill();zx.stroke();zx.fillRect(cx-8,dty-45,16,30);
        zx.lineWidth=2;zx.strokeStyle=col;drawLiq(b,cx-r+5,by,r*2-10,dH-10,lqc,fillA);drawLbl(b,cx,dty+dH*0.55);
    }}else if(b.sh==='ceramic_pot'){{
        const r=50,dH=140,dty=by-dH;
        zx.fillStyle='#d4c4a8';zx.strokeStyle='#a09080';
        zx.fillRect(cx-r,dty,r*2,dH);zx.strokeRect(cx-r,dty,r*2,dH);
        zx.lineWidth=6;zx.beginPath();zx.moveTo(cx-r-5,dty);zx.lineTo(cx+r+5,dty);zx.stroke();
        zx.fillRect(cx-r+5,dty-25,r*2-10,22);zx.beginPath();zx.arc(cx,dty-25,10,0,Math.PI*2);zx.fill();
        zx.lineWidth=2;drawLbl(b,cx,dty+dH*0.45);
    }}else{{
        const r=38;zx.beginPath();zx.ellipse(cx,ty+bH/2,r,bH/2,0,0,Math.PI*2);zx.fill();zx.stroke();
        zx.fillRect(cx-14,ty-28,28,32);zx.strokeRect(cx-14,ty-28,28,32);
        drawLiq(b,cx-r+5,by,r*2-10,bH-20,lqc,fillA);drawCork(cx,ty-28);drawLbl(b,cx,ty+bH*0.45);
    }}
    if(uvOn&&b.uv){{zx.fillStyle='{uv_color}';zx.font='italic 12px Georgia';zx.textAlign='center';zx.shadowColor='{uv_color}';zx.shadowBlur=12;zx.fillText(b.uv.substring(0,30),cx,h*0.15);if(b.uv.length>30)zx.fillText(b.uv.substring(30),cx,h*0.15+16);zx.shadowBlur=0;}}
    if(NM&&Math.random()>0.97){{zx.fillStyle='rgba(0,0,0,0.4)';zx.beginPath();zx.arc(cx,h*0.5,20,0,Math.PI*2);zx.fill();zx.fillStyle='rgba(255,255,255,0.5)';zx.beginPath();zx.arc(cx-7,h*0.5-5,4,0,Math.PI*2);zx.arc(cx+7,h*0.5-5,4,0,Math.PI*2);zx.fill();}}
    zx.restore();
}}

function drawLiq(b,lx,by,lw,lh,lqc,alpha){{
    const fillH=lh*b.lv*0.85,top=by-fillH;
    zx.save();zx.beginPath();zx.rect(lx,by-lh,lw,lh);zx.clip();
    zx.fillStyle=lqc+alpha;zx.beginPath();zx.moveTo(lx,by);
    for(let x=lx;x<=lx+lw;x+=4)zx.lineTo(x,top+Math.sin(wv*3+x*0.06)*4);
    zx.lineTo(lx+lw,by);zx.closePath();zx.fill();
    if(b.anim==='bubble'||b.anim==='swirl')for(let i=0;i<5;i++){{const bx=lx+lw/2+Math.sin(wv*0.5+i*2)*(lw/3),bby=top+10+((wv*20+i*30)%(fillH-15));if(bby<by){{zx.fillStyle='rgba(255,255,255,0.2)';zx.beginPath();zx.arc(bx,bby,2+Math.sin(wv+i)*1.5,0,Math.PI*2);zx.fill();}}}}
    if(b.anim==='swirl'){{zx.strokeStyle='rgba(255,255,255,0.15)';zx.lineWidth=2;for(let i=0;i<3;i++){{zx.beginPath();zx.arc(lx+lw/2+Math.sin(wv+i)*10,top+20+i*25,10+i*5,wv+i,wv+i+Math.PI);zx.stroke();}}}}
    if(b.anim==='pulse'){{zx.fillStyle='rgba(255,100,100,'+(0.08+Math.sin(wv*2)*0.08)+')';zx.fillRect(lx,top,lw,fillH);}}
    if(b.anim==='shimmer')for(let i=0;i<8;i++){{zx.fillStyle='rgba(200,200,220,0.4)';zx.beginPath();zx.arc(lx+lw/2+Math.sin(wv+i)*lw/3,top+10+i*16,2,0,Math.PI*2);zx.fill();}}
    if(b.anim==='sparkle')for(let i=0;i<6;i++){{if(Math.sin(wv*2+i)>0.6){{zx.fillStyle='rgba(255,255,255,0.7)';zx.beginPath();zx.arc(lx+10+Math.random()*lw*0.8,top+10+Math.random()*fillH*0.8,2,0,Math.PI*2);zx.fill();}}}}
    if(b.anim==='float'){{zx.fillStyle='rgba(220,210,190,0.6)';for(let i=0;i<7;i++){{const fx=lx+lw/2+Math.sin(wv*0.3+i*1.5)*lw*0.3,fy=top+10+((wv*8+i*18)%(fillH-15));zx.beginPath();zx.ellipse(fx,fy,5,3,wv+i,0,Math.PI*2);zx.fill();}}if(litOn){{zx.fillStyle='rgba(180,160,140,0.5)';for(let i=0;i<4;i++){{zx.beginPath();zx.ellipse(lx+lw/2+Math.sin(i)*lw*0.25,top+fillH*0.3+i*20,8,5,Math.sin(wv+i)*0.5,0,Math.PI*2);zx.fill();}}}}}}
    if(b.anim==='leeches'){{for(let i=0;i<5;i++){{const lxx=lx+lw/2+Math.sin(wv*0.4+i*2)*lw*0.3,ly=top+25+i*22+Math.cos(wv*0.3+i)*8;zx.fillStyle='#2a3a2a';zx.beginPath();zx.ellipse(lxx,ly,14,7,Math.sin(wv+i)*0.4,0,Math.PI*2);zx.fill();zx.fillStyle='#ff0000';zx.beginPath();zx.arc(lxx+10,ly-2,2,0,Math.PI*2);zx.fill();}}}}
    zx.restore();
}}

function drawCork(cx,ty){{
    const grad=zx.createLinearGradient(cx-16,0,cx+16,0);grad.addColorStop(0,'#6b5440');grad.addColorStop(0.4,'#9b8370');grad.addColorStop(1,'#5b4430');
    zx.fillStyle=grad;zx.fillRect(cx-16,ty-16,32,18);zx.strokeStyle='#5b4430';zx.strokeRect(cx-16,ty-16,32,18);
    zx.strokeStyle='rgba(90,60,40,0.3)';zx.lineWidth=0.5;for(let i=0;i<3;i++){{zx.beginPath();zx.moveTo(cx-13,ty-13+i*5);zx.lineTo(cx+13,ty-13+i*5);zx.stroke();}}zx.lineWidth=2;
}}

function drawSeal(cx,ty){{
    zx.fillStyle='#880000';zx.beginPath();zx.arc(cx,ty-8,18,0,Math.PI*2);zx.fill();
    zx.fillStyle='#660000';zx.beginPath();zx.arc(cx,ty-8,12,0,Math.PI*2);zx.fill();
    zx.fillStyle='#440000';zx.font='bold 10px serif';zx.textAlign='center';zx.fillText('R',cx,ty-4);
}}

function drawLbl(b,cx,y){{
    const lw=65,lh=42;
    zx.fillStyle=uvOn?'#220033':'#ffffee';zx.fillRect(cx-lw/2,y-lh/2,lw,lh);
    zx.strokeStyle='#8b7355';zx.lineWidth=1;zx.strokeRect(cx-lw/2,y-lh/2,lw,lh);
    zx.beginPath();zx.moveTo(cx-lw/3,y-lh/2+6);zx.lineTo(cx+lw/3,y-lh/2+6);zx.stroke();
    zx.beginPath();zx.moveTo(cx-lw/3,y+lh/2-6);zx.lineTo(cx+lw/3,y+lh/2-6);zx.stroke();
    zx.fillStyle=uvOn?'{uv_color}':'#333';zx.font=b.nm.length>12?'9px Georgia':'bold 11px Georgia';zx.textAlign='center';zx.fillText(b.nm,cx,y+4);
}}

/* ===== ZOOM PANEL ===== */
function showZoom(b){{
    sel=b;sealBrk=!b.seal;litOn=false;
    E('zp-nm').textContent=b.nm;E('zp-sb').textContent=b.sub;E('zp-ds').textContent=b.desc;E('zp-cn').textContent=b.cnt;E('zp-wr').textContent='⚠ '+b.wrn;
    const slEl=E('zp-sl'),selBtn=E('z-sel');
    if(b.seal){{slEl.textContent='🔴 Wax seal intact.';slEl.className='';slEl.classList.add('show');selBtn.style.display='';E('z-sml').disabled=true;E('z-por').disabled=true;sealBrk=false;}}
    else{{slEl.style.display='none';selBtn.style.display='none';E('z-sml').disabled=false;E('z-por').disabled=false;}}
    const sc=E('zp-sc');sc.classList.remove('show');
    if(b.hs){{sc.textContent='🔍 '+b.sec;setTimeout(()=>{{sc.classList.add('show');disc(b.id,b.nm+': '+b.sec);}},1200);}}else sc.textContent='';
    const uv=E('zp-uv');uv.textContent='☢ UV: '+b.uv;uv.className=uvOn?'show':'';uv.style.display=uvOn?'block':'none';
    E('z-lit').classList.remove('lit');E('zp').classList.add('show');
}}
window.closeZoom=function(){{E('zp').classList.remove('show');sel=null;litOn=false;}};
E('zp').onclick=e=>{{if(e.target===E('zp'))window.closeZoom();}};
E('z-shk').onclick=()=>{{shk=true;zc.classList.remove('shk');void zc.offsetWidth;zc.classList.add('shk');setTimeout(()=>{{shk=false;zc.classList.remove('shk');}},700);}};
E('z-sml').onclick=()=>{{if(sel)hint(sel.sml,3500);}};
E('z-por').onclick=()=>{{if(sel){{sel.lv=Math.max(0.05,sel.lv-0.08);hint('*A drop falls... the liquid level decreases.*',2500);crossReact('pour',sel.id);}}}};
E('z-lit').onclick=()=>{{litOn=!litOn;E('z-lit').classList.toggle('lit',litOn);hint(litOn?'*You hold the bottle up to the candlelight...*':'*You lower the bottle.*',2000);}};
E('z-sel').onclick=()=>{{if(!sel||!sel.seal)return;sealBrk=true;sel.seal=false;E('zp-sl').textContent='🔴 Seal BROKEN.';E('zp-sl').style.color='#cc0000';E('z-sel').style.display='none';E('z-sml').disabled=false;E('z-por').disabled=false;hint('*CRACK — the wax seal shatters. There is no going back.*',3000);disc('seal_'+sel.id,'Broke the seal on '+sel.nm+'.');crossReact('seal',sel.id);}};
E('z-amx').onclick=()=>{{if(!sel||sel.mix==='none')return;const slot=mxS[0]===null?0:(mxS[1]===null?1:-1);if(slot>=0){{mxS[slot]=sel;const sl=Q('.ms[data-s="'+slot+'"]')[0];sl.textContent=sel.nm;sl.classList.add('fl');hint('Added to mixing chamber.',1500);}}}};

/* ===== CROSS-REACTIONS ===== */
function crossReact(type,id){{
    if(type==='seal'){{cndL.intensity=3;setTimeout(()=>cndL.intensity=0.8,2000);
        if(id==='vita'){{if(skG.children[1])skG.children[1].material=new THREE.MeshBasicMaterial({{color:0xff0000}});if(skG.children[2])skG.children[2].material=new THREE.MeshBasicMaterial({{color:0xff0000}});setTimeout(()=>{{if(skG.children[1])skG.children[1].material=new THREE.MeshBasicMaterial({{color:0x111111}});if(skG.children[2])skG.children[2].material=new THREE.MeshBasicMaterial({{color:0x111111}});}},3000);}}
    }}
    if(type==='open'&&id==='leeches'&&mouseGrp){{mouseGrp.visible=false;setTimeout(()=>mouseGrp.visible=true,5000);}}
    if(type==='pour'&&id==='mercy'){{window._dustFreeze=true;setTimeout(()=>window._dustFreeze=false,3000);}}
}}

/* ===== DRAWERS ===== */
E('b-dr').onclick=()=>{{const p=E('dp');p.classList.toggle('show');if(p.classList.contains('show')){{const it=E('dp-it');it.innerHTML='';DI.forEach(d=>{{const div=document.createElement('div');div.className='di'+(d.lk?' lk':'');div.textContent=d.nm;div.onclick=()=>{{if(d.lk&&d.id==='society')E('lp').classList.add('show');else if(!d.lk){{hint(d.nm+' — '+d.ds,3500);disc('dr_'+d.id,'Drawer: '+d.ds);}}}};it.appendChild(div);}});}}}};

/* ===== LOCK ===== */
Q('.dl').forEach(d=>d.onclick=()=>{{let v=parseInt(d.textContent);d.textContent=(v+1)%10;}});
E('lp-go').onclick=()=>{{const code=Array.from(Q('.dl')).map(d=>d.textContent).join('');if(code==='847'){{E('lp').classList.remove('show');DI.forEach(d=>d.lk=false);E('dp').classList.remove('show');setTimeout(()=>E('b-dr').click(),300);disc('lock','Combination lock solved: 847 — the year the Society was founded.');}}else E('lp-h').textContent='Incorrect. The Society was founded in 18__...';}};

/* ===== MIXING ===== */
E('b-mx').onclick=()=>E('mp').classList.toggle('show');
E('mp-cl').onclick=()=>{{mxS[0]=mxS[1]=null;Q('.ms').forEach(s=>{{s.textContent='Empty';s.classList.remove('fl');}});E('mp-r').innerHTML='Add two bottles to combine...';}};
E('mp-go').onclick=()=>{{if(!mxS[0]||!mxS[1])return;const t1=mxS[0].mix,t2=mxS[1].mix,k1=t1+'+'+t2,k2=t2+'+'+t1;const r=MIX[k1]||MIX[k2];if(r){{E('mp-r').innerHTML='<span style="color:'+r[2]+';font-weight:bold">'+r[0]+'</span><br><br>'+r[1];disc('mix_'+k1,'Mixed: '+r[0]+' — '+r[1]);}}else E('mp-r').innerHTML='No reaction. These substances do not combine.';}};

/* ===== JOURNAL ===== */
E('b-jn').onclick=()=>E('jp').classList.toggle('show');

/* ===== UV ===== */
E('b-uv').onclick=()=>{{uvOn=!uvOn;E('b-uv').classList.toggle('on',uvOn);E('uv-ov').classList.toggle('on',uvOn);uvL.intensity=uvOn?2:0;dL.intensity=uvOn?0.3:1;if(sel){{const u=E('zp-uv');u.textContent='☢ UV: '+sel.uv;u.className=uvOn?'show':'';u.style.display=uvOn?'block':'none';}}}};

/* ===== HIDDEN COMPARTMENT ===== */
function checkHidden(){{bkCl++;if(bkCl>=3&&!hidF){{hidF=true;E('hid-flash').style.opacity='1';setTimeout(()=>E('hid-flash').style.opacity='0',2500);disc('hidden','SECRET COMPARTMENT — A false panel behind the cabinet.');
    const eb={{id:'elixir',nm:'THE ELIXIR',sub:'Unknown Origin',col:0x110011,liq:0x220011,lv:0.95,sh:'teardrop',desc:'Found behind false panel. Ancient. Terrible.',cnt:'Older than Fitzroy. Older than the Society.',wrn:'DO NOT DRINK',sec:'This is what they worship.',uv:'ANNO DOMINI 1666',hs:true,seal:true,mix:'blood',anim:'swirl',sml:'Blood. Ash. Eternity.'}};
    const eg=new THREE.Group();eg.add(new THREE.Mesh(new THREE.BoxGeometry(0.26,0.48,0.26),new THREE.MeshBasicMaterial({{transparent:true,opacity:0.001,depthWrite:false}})));eg.children[0].userData={{bRef:eb}};
    const egl=new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.11,0.38,12),new THREE.MeshLambertMaterial({{color:0x111111,transparent:true,opacity:0.8}}));eg.add(egl);
    const elq=new THREE.Mesh(new THREE.CylinderGeometry(0.08,0.09,0.32,12),new THREE.MeshLambertMaterial({{color:0x220011,transparent:true,opacity:0.9}}));elq.position.y=-0.02;eg.add(elq);
    eg.position.set(0,1.6,0.35);eg.userData=eb;scene.add(eg);bottles.push(eg);
}}}};

/* ===== CLICK ===== */
ren.domElement.onclick=e=>{{
    if(hasMv)return;
    const cm=new THREE.Vector2((e.clientX/cW())*2-1,-(e.clientY/cH())*2+1);
    ray.setFromCamera(cm,cam);
    const bH=ray.intersectObjects(bottles,true);
    if(bH.length){{let o=bH[0].object;if(o.userData.bRef){{showZoom(o.userData.bRef);crossReact('open',o.userData.bRef.id);return;}}while(o){{if(o.userData&&o.userData.id){{showZoom(o.userData);crossReact('open',o.userData.id);return;}}o=o.parent;}}}}
    const pH=ray.intersectObjects(propG,true);
    if(pH.length){{let o=pH[0].object;while(o&&!o.userData.type)o=o.parent;if(o&&o.userData.type){{const tip=E('tooltip');tip.querySelector('.tt').textContent=o.userData.title||'';tip.querySelector('.td').textContent=o.userData.desc||'';tip.querySelector('.tl').textContent=o.userData.lore||'';tip.querySelector('.tl').style.display=o.userData.lore?'block':'none';tip.style.left=Math.min(e.clientX+15,cW()-260)+'px';tip.style.top=Math.min(e.clientY+15,cH()-130)+'px';tip.classList.add('vis');return;}}}}
    const bkH=ray.intersectObject(bk);if(bkH.length)checkHidden();
    E('tooltip').classList.remove('vis');
}};

/* ===== ANIMATION ===== */
const clk=new THREE.Clock();
function animate(){{
    requestAnimationFrame(animate);
    const t=clk.getElapsedTime();
    cndL.intensity=Math.max(0.3,(uvOn?0.2:0.8)+Math.sin(t*18)*0.15+Math.sin(t*37)*0.08);
    flm.scale.y=1.5+Math.sin(t*12)*0.2;flm.position.x=Math.sin(t*7)*0.003;
    if(!window._dustFreeze){{const dp=dustPts.geometry.attributes.position.array;for(let i=0;i<dustN;i++){{dp[i*3]+=dVel[i].x+Math.sin(t+i)*0.0002;dp[i*3+1]+=dVel[i].y;if(dp[i*3+1]>CH){{dp[i*3+1]=0;dp[i*3]=Math.random()*CW-CW/2;}}}}dustPts.geometry.attributes.position.needsUpdate=true;}}
    herbs.forEach((h,i)=>h.rotation.z=Math.PI+Math.sin(t*0.8+i)*0.05);
    if(mouseGrp&&mouseGrp.visible){{const mp=Math.sin(t*2);mouseGrp.position.z=0.28+(mp>0.7?0.04:0);mouseGrp.rotation.y=mp>0.7?0.3:0;}}
    wv+=shk?0.4:0.03;
    if(sel)draw2d(sel);
    if(NM&&Math.random()>0.998){{const rb=bottles[Math.random()*bottles.length|0];rb.rotation.z=0.1;setTimeout(()=>rb.rotation.z=0,200);}}
    if(!isD&&!E('zp').classList.contains('show')){{theta+=0.0005;updCam();}}
    if(uvOn)uvL.intensity=2+Math.sin(t*10)*0.3;
    ren.render(scene,cam);
}}
window.onresize=()=>{{cam.aspect=cW()/cH();cam.updateProjectionMatrix();ren.setSize(cW(),cH());}};
setTimeout(()=>{{cam.aspect=cW()/cH();cam.updateProjectionMatrix();ren.setSize(cW(),cH());}},100);
animate();
}})();
</script></body></html>'''
    return html
