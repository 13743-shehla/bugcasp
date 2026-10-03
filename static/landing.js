'use strict';
function renderLanding(){
  $('#main').innerHTML=`<div class="landing">
    <section class="intro-hero" aria-labelledby="intro-title">
      <div class="intro-copy"><div class="intro-kicker"><span></span> TƏHLÜKƏSİZLİK BİRLİKDƏ BAŞLAYIR</div>
      <h1 id="intro-title">Zəifliyi tap.<br><em>Güvəni gücləndir.</em></h1>
      <p>BugCasp şirkətləri və təhlükəsizlik tədqiqatçılarını bir araya gətirən bug bounty platformasıdır. Tapıntıları məsuliyyətlə paylaşın, rəqəmsal dünyanı daha təhlükəsiz edin.</p>
      <div class="intro-actions"><button class="btn primary" data-action="join-researcher">Tədqiqatçı kimi qoşul <span aria-hidden="true">↗</span></button><button class="btn" data-action="join-company">Şirkətimi qorumaq istəyirəm</button></div>
      <a class="intro-explore" href="#programs">Proqramları araşdır <span aria-hidden="true">→</span></a>
      </div>
      <div class="security-scene" aria-hidden="true"><div class="scene-grid"></div><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><div class="orbit-dot"></div><div class="shield-core"><img src="/static/logo.png" alt=""><span>BugCasp</span></div><div class="signal signal-one"><span>⌕</span><b>Tapıntı</b><small>01 / DISCOVER</small></div><div class="signal signal-two"><span>✓</span><b>Təsdiq</b><small>02 / VALIDATE</small></div><div class="signal signal-three"><span>◇</span><b>Mükafat</b><small>03 / REWARD</small></div><div class="scene-caption">İnsan bacarığı. Daha güclü müdafiə.</div></div>
    </section>
    <div class="intro-principles"><span>✓ İcazəli araşdırma</span><span>✓ Məxfi hesabatlar</span><span>✓ Şəffaf qiymətləndirmə</span></div>
    <section class="intro-section"><div class="intro-section-head"><div class="intro-kicker">BİZ KİMİK?</div><h2>Təhlükəsizliyə ortaq töhfə.</h2><p>Bir tərəfdə qorunmalı məhsullar, digər tərəfdə zəiflikləri görə bilən insanlar. BugCasp bu əməkdaşlıq üçün ortaq məkan yaradır.</p></div><div class="audience-grid"><article><span class="intro-number">01 / RESEARCHERS</span><h3>Bacarığını real təsirə çevir.</h3><p>İcazəli proqramları seç, qaydaları oxu və tapdığın zəifliyi sübut faylı ilə bildir. Təsdiqlənmiş hesabatlarla reputasiya və proqramın şərtlərinə uyğun mükafat qazan.</p><button class="text-button" data-action="join-researcher">Tədqiqatçı hesabı yarat →</button></article><article><span class="intro-number">02 / COMPANIES</span><h3>Məhsuluna yeni gözlə bax.</h3><p>Proqramını yarat, araşdırma sərhədlərini və mükafatları müəyyən et. Gələn hesabatları bir yerdə yoxla, qiymətləndir və həll prosesini idarə et.</p><button class="text-button" data-action="join-company">Şirkət hesabı yarat →</button></article></div></section>
    <section class="intro-section intro-process"><div class="intro-section-head"><div class="intro-kicker">NECƏ İŞLƏYİR?</div><h2>Tapıntıdan həllə, üç addım.</h2></div><div class="process-grid"><article><span>01</span><h3>Proqramı seç</h3><p>Hədəfləri, icazə verilən testləri və proqramın qaydalarını öyrən.</p></article><article><span>02</span><h3>Hesabatını göndər</h3><p>Tapıntını adlandır, kateqoriyanı seç və sübut faylını əlavə et.</p></article><article><span>03</span><h3>Nəticəni izlə</h3><p>Şirkətin baxışını, hesabatın statusunu və təsdiqlənmiş mükafatını hesabından izlə.</p></article></div></section>
    <section class="intro-finish"><div><div class="intro-kicker">NÖVBƏTİ ADDIM SƏNİNDİR</div><h2>Daha təhlükəsiz gələcəyə qoşul.</h2><p>İstər zəiflikləri tap, istər məhsulunu qoru.</p></div><button class="btn primary" data-action="register">İndi hesab yarat ↗</button></section>
  </div>`;
}
