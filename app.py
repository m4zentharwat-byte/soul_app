#!/usr/bin/env python3
"""
Soul Recovery & Healing Hearts — A Website by Mazen Tharwat
Run: python app.py
Open: http://localhost:8080
"""

import http.server
import socketserver
import webbrowser
import threading

# ─── CONFIGURATION ───────────────────────────────────────────────────────────
PORT = 8080
CREATOR = "Mazen Tharwat"

# ─── PAGE CONTENT ────────────────────────────────────────────────────────────

def build_page():
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Soul Recovery & Healing Hearts — by Mazen Tharwat</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<script>
tailwind.config = {
  theme: {
    extend: {
      colors: {
        brand: { 400:'#ff8a55', 500:'#ff6b2c', 600:'#e65214', 700:'#c4410d', 800:'#7c2d12', 900:'#431407' }
      },
      letterSpacing: { tighter:'-0.04em' }
    }
  }
}
</script>
<style>
  body { font-family: 'Inter', sans-serif; background: #0a0a0a; color: #e5e5e5; }
  html { scroll-behavior: smooth; }
  .text-outline {
    -webkit-text-stroke: 1px rgba(255,255,255,0.1);
    color: transparent;
  }
  ::-webkit-scrollbar { width: 8px; }
  ::-webkit-scrollbar-track { background: #0a0a0a; }
  ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
  }
  @keyframes pulse-glow {
    0%, 100% { opacity: 0.3; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.05); }
  }
  .animate-float { animation: float 6s ease-in-out infinite; }
  .animate-float-delay { animation: float 6s ease-in-out 2s infinite; }
  .animate-pulse-glow { animation: pulse-glow 4s ease-in-out infinite; }
  .fade-in { opacity: 0; transform: translateY(40px); transition: all 0.8s cubic-bezier(0.22, 1, 0.36, 1); }
  .fade-in.visible { opacity: 1; transform: translateY(0); }
  .card-hover { transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1); }
  .card-hover:hover { transform: translateY(-8px); }
  .breathing-circle {
    animation: breathe 8s ease-in-out infinite;
  }
  @keyframes breathe {
    0%, 100% { transform: scale(1); opacity: 0.4; }
    25% { transform: scale(1.15); opacity: 0.6; }
    50% { transform: scale(1); opacity: 0.4; }
    75% { transform: scale(1.1); opacity: 0.55; }
  }
  .quote-mark {
    font-size: 120px;
    line-height: 1;
    background: linear-gradient(to bottom, rgba(255,107,44,0.3), transparent);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .divider {
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(255,107,44,0.3), transparent);
  }
  .mobile-menu { max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }
  .mobile-menu.open { max-height: 400px; }
</style>
</head>
<body class="antialiased">

<!-- NAVBAR -->
<nav id="navbar" class="fixed top-6 left-1/2 -translate-x-1/2 z-50 w-[95%] max-w-4xl">
  <div class="bg-neutral-900/80 backdrop-blur-xl border border-white/10 rounded-full py-2 pl-3 pr-3 flex items-center justify-between">
    <a href="#hero" class="flex items-center gap-2">
      <div class="w-9 h-9 rounded-full bg-gradient-to-br from-brand-600 to-brand-500 flex items-center justify-center">
        <i data-lucide="heart" class="w-4 h-4 text-white"></i>
      </div>
      <span class="text-lg font-semibold tracking-tight text-white hidden sm:block">Soul Recovery</span>
    </a>
    <div class="hidden md:flex items-center gap-1">
      <a href="#about" class="px-4 py-2 text-sm text-neutral-400 hover:text-white transition-colors rounded-full hover:bg-white/5">About</a>
      <a href="#healing" class="px-4 py-2 text-sm text-neutral-400 hover:text-white transition-colors rounded-full hover:bg-white/5">Healing</a>
      <a href="#positivity" class="px-4 py-2 text-sm text-neutral-400 hover:text-white transition-colors rounded-full hover:bg-white/5">Positivity</a>
      <a href="#steps" class="px-4 py-2 text-sm text-neutral-400 hover:text-white transition-colors rounded-full hover:bg-white/5">Steps</a>
      <a href="#quotes" class="px-4 py-2 text-sm text-neutral-400 hover:text-white transition-colors rounded-full hover:bg-white/5">Quotes</a>
    </div>
    <div class="flex items-center gap-2">
      <a href="#begin" class="hidden sm:inline-flex bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white text-sm font-medium px-5 py-2.5 rounded-full transition-all duration-300 shadow-lg shadow-brand-500/20">
        Begin Healing
      </a>
      <button id="mobileToggle" class="md:hidden w-9 h-9 rounded-full bg-white/5 flex items-center justify-center hover:bg-white/10 transition-colors">
        <i data-lucide="menu" class="w-4 h-4 text-white"></i>
      </button>
    </div>
  </div>
  <div id="mobileMenu" class="mobile-menu md:hidden mt-2 bg-neutral-900/90 backdrop-blur-xl border border-white/10 rounded-2xl px-4">
    <a href="#about" class="block py-3 text-sm text-neutral-400 hover:text-white transition-colors border-b border-white/5">About</a>
    <a href="#healing" class="block py-3 text-sm text-neutral-400 hover:text-white transition-colors border-b border-white/5">Healing</a>
    <a href="#positivity" class="block py-3 text-sm text-neutral-400 hover:text-white transition-colors border-b border-white/5">Positivity</a>
    <a href="#steps" class="block py-3 text-sm text-neutral-400 hover:text-white transition-colors border-b border-white/5">Steps</a>
    <a href="#quotes" class="block py-3 text-sm text-neutral-400 hover:text-white transition-colors border-b border-white/5">Quotes</a>
    <a href="#begin" class="block py-3 text-sm font-medium text-brand-500">Begin Healing &rarr;</a>
  </div>
</nav>

<!-- HERO -->
<section id="hero" class="relative min-h-screen flex flex-col justify-end pb-20 pt-32 overflow-hidden">
  <div class="absolute inset-0" style="background: radial-gradient(ellipse at top, rgba(67,20,7,0.2), #0a0a0a 70%);"></div>
  <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full breathing-circle" style="background: radial-gradient(circle, rgba(255,107,44,0.08), transparent 70%);"></div>
  <div class="absolute top-20 right-20 w-[300px] h-[300px] rounded-full animate-float" style="background: radial-gradient(circle, rgba(255,138,85,0.06), transparent 70%);"></div>
  <div class="absolute bottom-40 left-10 w-[200px] h-[200px] rounded-full animate-float-delay" style="background: radial-gradient(circle, rgba(255,107,44,0.05), transparent 70%);"></div>

  <div class="relative max-w-7xl mx-auto px-6 lg:px-12 w-full">
    <div class="grid lg:grid-cols-12 gap-12 items-end">
      <div class="lg:col-span-5 mb-10 lg:mb-20 fade-in">
        <div class="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-2 mb-8">
          <span class="w-2 h-2 rounded-full bg-brand-500 animate-pulse"></span>
          <span class="text-xs font-medium tracking-wider uppercase text-neutral-400">A Journey Within</span>
        </div>
        <p class="text-lg font-light text-neutral-400 leading-relaxed max-w-md">
          Every soul carries wounds invisible to the eye. This is a safe space to acknowledge them, understand them, and gently guide yourself back to wholeness.
        </p>
      </div>

      <div class="lg:col-span-7 fade-in" style="transition-delay: 0.15s;">
        <h1 class="text-5xl sm:text-6xl lg:text-8xl font-medium tracking-tighter leading-[0.9] mb-6">
          <span class="block text-white">Heal Your</span>
          <span class="block bg-gradient-to-r from-brand-500 to-white bg-clip-text text-transparent">Soul</span>
          <span class="block text-white text-outline text-4xl sm:text-5xl lg:text-6xl mt-2">&amp; Recover</span>
        </h1>
        <div class="flex flex-wrap items-center gap-4 mt-8">
          <a href="#healing" class="inline-flex items-center gap-3 bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white text-sm font-medium pl-6 pr-2 py-2 rounded-full transition-all duration-300 shadow-lg shadow-brand-500/20 group">
            Start Your Journey
            <span class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center group-hover:bg-white/30 transition-colors">
              <i data-lucide="arrow-down" class="w-4 h-4"></i>
            </span>
          </a>
          <a href="#about" class="inline-flex items-center gap-2 text-sm text-neutral-400 hover:text-white transition-colors group">
            Learn More
            <i data-lucide="arrow-right" class="w-4 h-4 group-hover:translate-x-1 transition-transform"></i>
          </a>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 mt-16 pt-8 border-t border-white/5 fade-in" style="transition-delay: 0.3s;">
      <div>
        <div class="text-3xl font-semibold tracking-tight text-white">&infin;</div>
        <div class="text-sm text-neutral-500 mt-1">Ways to Heal</div>
      </div>
      <div>
        <div class="text-3xl font-semibold tracking-tight text-white">100%</div>
        <div class="text-sm text-neutral-500 mt-1">Worth the Effort</div>
      </div>
      <div>
        <div class="text-3xl font-semibold tracking-tight text-white">1</div>
        <div class="text-sm text-neutral-500 mt-1">Soul to Protect</div>
      </div>
      <div>
        <div class="text-3xl font-semibold tracking-tight text-brand-500">Now</div>
        <div class="text-sm text-neutral-500 mt-1">Time to Begin</div>
      </div>
    </div>
  </div>
</section>

<!-- ABOUT -->
<section id="about" class="relative py-32 overflow-hidden">
  <div class="absolute top-0 left-0 right-0 divider"></div>
  <div class="max-w-7xl mx-auto px-6 lg:px-12">
    <div class="grid lg:grid-cols-2 gap-16 items-center">
      <div class="fade-in relative">
        <div class="relative rounded-3xl overflow-hidden border border-white/10 group">
          <img src="https://picsum.photos/seed/sunrise-hope/800/600.jpg" alt="Hope and healing" class="w-full h-80 lg:h-[480px] object-cover transition-transform duration-700 group-hover:scale-105">
          <div class="absolute inset-0" style="background: linear-gradient(to top, rgba(10,10,10,0.8), transparent 60%);"></div>
          <div class="absolute bottom-6 left-6 right-6">
            <p class="text-sm font-medium text-brand-500 mb-1">Understanding</p>
            <p class="text-white text-lg font-medium tracking-tight">"The wound is the place where the Light enters you." &mdash; Rumi</p>
          </div>
        </div>
        <div class="absolute -bottom-4 -right-4 w-24 h-24 rounded-2xl bg-gradient-to-br from-brand-600/20 to-brand-500/10 border border-brand-500/20 backdrop-blur-sm animate-float flex items-center justify-center">
          <i data-lucide="sparkles" class="w-8 h-8 text-brand-500"></i>
        </div>
      </div>

      <div class="fade-in" style="transition-delay: 0.15s;">
        <span class="text-xs font-semibold tracking-wider uppercase text-brand-500 mb-4 block">About Soul Recovery</span>
        <h2 class="text-3xl lg:text-5xl font-medium tracking-tighter leading-[1.1] text-white mb-6">
          Your Soul Is<br>Worth Saving
        </h2>
        <p class="text-lg font-light text-neutral-400 leading-relaxed mb-6">
          Soul recovery is the gentle process of reclaiming the parts of yourself that were lost through trauma, grief, heartbreak, or the simple weight of living. It's not about erasing the past &mdash; it's about integrating it with compassion.
        </p>
        <p class="text-lg font-light text-neutral-400 leading-relaxed mb-8">
          When we experience deep pain, fragments of our soul can feel scattered. Recovery means gathering those pieces back with patience, love, and intentional practices that reconnect you to your true essence.
        </p>
        <div class="flex flex-wrap gap-3">
          <span class="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-neutral-300">Self-Awareness</span>
          <span class="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-neutral-300">Compassion</span>
          <span class="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-neutral-300">Patience</span>
          <span class="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-neutral-300">Acceptance</span>
          <span class="px-4 py-2 rounded-full bg-brand-500/10 border border-brand-500/20 text-sm text-brand-400">Love</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- HEALING METHODS -->
<section id="healing" class="relative py-32 overflow-hidden">
  <div class="absolute top-0 left-0 right-0 divider"></div>
  <div class="absolute inset-0" style="background: radial-gradient(ellipse at center, rgba(67,20,7,0.1), transparent 70%);"></div>

  <div class="relative max-w-7xl mx-auto px-6 lg:px-12">
    <div class="text-center max-w-2xl mx-auto mb-20 fade-in">
      <span class="text-xs font-semibold tracking-wider uppercase text-brand-500 mb-4 block">Paths to Healing</span>
      <h2 class="text-3xl lg:text-5xl font-medium tracking-tighter leading-[1.1] text-white mb-6">
        Ways to Heal Your Heart
      </h2>
      <p class="text-lg font-light text-neutral-400 leading-relaxed">
        There is no single path to healing. Here are six powerful approaches that can guide you back to emotional wholeness.
      </p>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="card-hover fade-in group bg-neutral-900/50 border border-white/5 rounded-3xl p-8 hover:border-brand-500/30">
        <div class="w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
          <i data-lucide="pen-tool" class="w-6 h-6 text-brand-500"></i>
        </div>
        <h3 class="text-xl font-medium text-white mb-3">Journaling &amp; Reflection</h3>
        <p class="text-sm text-neutral-400 leading-relaxed">
          Write without judgment. Let your thoughts flow onto paper. Journaling helps process emotions, identify patterns, and release what's been bottled up inside.
        </p>
      </div>

      <div class="card-hover fade-in group bg-neutral-900/50 border border-white/5 rounded-3xl p-8 hover:border-brand-500/30" style="transition-delay: 0.1s;">
        <div class="w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
          <i data-lucide="wind" class="w-6 h-6 text-brand-500"></i>
        </div>
        <h3 class="text-xl font-medium text-white mb-3">Breathwork &amp; Meditation</h3>
        <p class="text-sm text-neutral-400 leading-relaxed">
          Your breath is the bridge between body and soul. Deep, intentional breathing calms the nervous system and creates space for healing to begin naturally.
        </p>
      </div>

      <div class="card-hover fade-in group bg-neutral-900/50 border border-white/5 rounded-3xl p-8 hover:border-brand-500/30" style="transition-delay: 0.2s;">
        <div class="w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
          <i data-lucide="users" class="w-6 h-6 text-brand-500"></i>
        </div>
        <h3 class="text-xl font-medium text-white mb-3">Connection &amp; Community</h3>
        <p class="text-sm text-neutral-400 leading-relaxed">
          You don't have to heal alone. Sharing your story with trusted people or support groups creates bonds that remind you: you are seen, you matter.
        </p>
      </div>

      <div class="card-hover fade-in group bg-neutral-900/50 border border-white/5 rounded-3xl p-8 hover:border-brand-500/30">
        <div class="w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
          <i data-lucide="trees" class="w-6 h-6 text-brand-500"></i>
        </div>
        <h3 class="text-xl font-medium text-white mb-3">Nature Therapy</h3>
        <p class="text-sm text-neutral-400 leading-relaxed">
          Walk among trees, sit by water, feel the earth beneath you. Nature has a profound ability to absorb our pain and return us to a state of peace.
        </p>
      </div>

      <div class="card-hover fade-in group bg-neutral-900/50 border border-white/5 rounded-3xl p-8 hover:border-brand-500/30" style="transition-delay: 0.1s;">
        <div class="w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
          <i data-lucide="music" class="w-6 h-6 text-brand-500"></i>
        </div>
        <h3 class="text-xl font-medium text-white mb-3">Sound &amp; Art Therapy</h3>
        <p class="text-sm text-neutral-400 leading-relaxed">
          Music, painting, dancing &mdash; creative expression bypasses the logical mind and reaches directly into the soul, unlocking emotions words cannot describe.
        </p>
      </div>

      <div class="card-hover fade-in group bg-neutral-900/50 border border-white/5 rounded-3xl p-8 hover:border-brand-500/30" style="transition-delay: 0.2s;">
        <div class="w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
          <i data-lucide="heart-handshake" class="w-6 h-6 text-brand-500"></i>
        </div>
        <h3 class="text-xl font-medium text-white mb-3">Self-Compassion Practice</h3>
        <p class="text-sm text-neutral-400 leading-relaxed">
          Treat yourself as you would treat a dear friend. Replace self-criticism with kindness. Forgiving yourself is often the most powerful act of healing.
        </p>
      </div>
    </div>
  </div>
</section>

<!-- POSITIVITY -->
<section id="positivity" class="relative py-32 overflow-hidden">
  <div class="absolute top-0 left-0 right-0 divider"></div>

  <div class="max-w-7xl mx-auto px-6 lg:px-12">
    <div class="grid lg:grid-cols-2 gap-16 items-center">
      <div class="fade-in order-2 lg:order-1">
        <span class="text-xs font-semibold tracking-wider uppercase text-brand-500 mb-4 block">The Power of Positivity</span>
        <h2 class="text-3xl lg:text-5xl font-medium tracking-tighter leading-[1.1] text-white mb-6">
          Positivity Is Not<br>Ignoring Pain
        </h2>
        <p class="text-lg font-light text-neutral-400 leading-relaxed mb-6">
          True positivity isn't about pretending everything is fine. It's about choosing hope while honoring your reality. It's the quiet strength that says "I'm hurting, but I believe it will get better."
        </p>

        <div class="space-y-5 mt-8">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
              <i data-lucide="sun" class="w-5 h-5 text-brand-500"></i>
            </div>
            <div>
              <h4 class="text-white font-medium mb-1">Reframe Your Thoughts</h4>
              <p class="text-sm text-neutral-400 leading-relaxed">Instead of "I'll never recover," try "I'm taking it one day at a time." Small shifts create big changes.</p>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
              <i data-lucide="shield-check" class="w-5 h-5 text-brand-500"></i>
            </div>
            <div>
              <h4 class="text-white font-medium mb-1">Protect Your Energy</h4>
              <p class="text-sm text-neutral-400 leading-relaxed">Set boundaries with people and situations that drain you. Your energy is sacred &mdash; guard it wisely.</p>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
              <i data-lucide="smile" class="w-5 h-5 text-brand-500"></i>
            </div>
            <div>
              <h4 class="text-white font-medium mb-1">Practice Gratitude Daily</h4>
              <p class="text-sm text-neutral-400 leading-relaxed">Even on the hardest days, find three small things to be grateful for. This rewires your brain toward hope.</p>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
              <i data-lucide="star" class="w-5 h-5 text-brand-500"></i>
            </div>
            <div>
              <h4 class="text-white font-medium mb-1">Celebrate Small Wins</h4>
              <p class="text-sm text-neutral-400 leading-relaxed">Got out of bed? That's a win. Ate a meal? That's a win. Every step forward matters, no matter how small.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="fade-in order-1 lg:order-2 relative" style="transition-delay: 0.15s;">
        <div class="relative rounded-3xl overflow-hidden border border-white/10 group">
          <img src="https://picsum.photos/seed/peaceful-light/800/700.jpg" alt="Positivity and light" class="w-full h-80 lg:h-[520px] object-cover transition-transform duration-700 group-hover:scale-105">
          <div class="absolute inset-0" style="background: linear-gradient(to top, rgba(10,10,10,0.7), transparent 50%);"></div>
        </div>
        <div class="absolute -bottom-6 -left-6 bg-neutral-900/90 backdrop-blur-xl border border-white/10 rounded-2xl p-5 max-w-[240px] animate-float">
          <div class="flex items-center gap-2 mb-2">
            <i data-lucide="trending-up" class="w-4 h-4 text-brand-500"></i>
            <span class="text-xs font-semibold tracking-wider uppercase text-brand-500">Research Shows</span>
          </div>
          <p class="text-sm text-neutral-300 leading-relaxed">Optimistic people have 35% better physical health and recover from illness faster.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- HEALING STEPS -->
<section id="steps" class="relative py-32 overflow-hidden">
  <div class="absolute top-0 left-0 right-0 divider"></div>
  <div class="absolute inset-0" style="background: radial-gradient(ellipse at bottom left, rgba(67,20,7,0.15), transparent 60%);"></div>

  <div class="relative max-w-7xl mx-auto px-6 lg:px-12">
    <div class="text-center max-w-2xl mx-auto mb-20 fade-in">
      <span class="text-xs font-semibold tracking-wider uppercase text-brand-500 mb-4 block">Your Path Forward</span>
      <h2 class="text-3xl lg:text-5xl font-medium tracking-tighter leading-[1.1] text-white mb-6">
        5 Steps to Soul Recovery
      </h2>
      <p class="text-lg font-light text-neutral-400 leading-relaxed">
        Healing is not linear, but having a roadmap can make the journey feel less overwhelming.
      </p>
    </div>

    <div class="max-w-3xl mx-auto space-y-0">
      <div class="fade-in flex gap-6 group">
        <div class="flex flex-col items-center">
          <div class="w-12 h-12 rounded-full bg-brand-500/10 border border-brand-500/30 flex items-center justify-center text-brand-500 font-semibold text-sm group-hover:bg-brand-500 group-hover:text-white transition-all duration-300">01</div>
          <div class="w-px flex-1 bg-gradient-to-b from-brand-500/30 to-transparent mt-2"></div>
        </div>
        <div class="pb-12">
          <h3 class="text-xl font-medium text-white mb-2 group-hover:text-brand-500 transition-colors">Acknowledge Your Pain</h3>
          <p class="text-sm text-neutral-400 leading-relaxed max-w-lg">The first step is always the hardest. Sit with your pain without trying to fix it. Say out loud: "I am hurting, and that is okay." This acknowledgment is the door to healing.</p>
        </div>
      </div>

      <div class="fade-in flex gap-6 group" style="transition-delay: 0.1s;">
        <div class="flex flex-col items-center">
          <div class="w-12 h-12 rounded-full bg-brand-500/10 border border-brand-500/30 flex items-center justify-center text-brand-500 font-semibold text-sm group-hover:bg-brand-500 group-hover:text-white transition-all duration-300">02</div>
          <div class="w-px flex-1 bg-gradient-to-b from-brand-500/30 to-transparent mt-2"></div>
        </div>
        <div class="pb-12">
          <h3 class="text-xl font-medium text-white mb-2 group-hover:text-brand-500 transition-colors">Release What You Cannot Control</h3>
          <p class="text-sm text-neutral-400 leading-relaxed max-w-lg">Much of our suffering comes from trying to control the uncontrollable. Practice surrender &mdash; not giving up, but making peace with what is beyond your power.</p>
        </div>
      </div>

      <div class="fade-in flex gap-6 group" style="transition-delay: 0.2s;">
        <div class="flex flex-col items-center">
          <div class="w-12 h-12 rounded-full bg-brand-500/10 border border-brand-500/30 flex items-center justify-center text-brand-500 font-semibold text-sm group-hover:bg-brand-500 group-hover:text-white transition-all duration-300">03</div>
          <div class="w-px flex-1 bg-gradient-to-b from-brand-500/30 to-transparent mt-2"></div>
        </div>
        <div class="pb-12">
          <h3 class="text-xl font-medium text-white mb-2 group-hover:text-brand-500 transition-colors">Rebuild Your Relationship with Yourself</h3>
          <p class="text-sm text-neutral-400 leading-relaxed max-w-lg">Start talking to yourself with kindness. Create rituals that nourish you &mdash; morning walks, warm tea, reading, silence. Relearn who you are beyond the pain.</p>
        </div>
      </div>

      <div class="fade-in flex gap-6 group" style="transition-delay: 0.3s;">
        <div class="flex flex-col items-center">
          <div class="w-12 h-12 rounded-full bg-brand-500/10 border border-brand-500/30 flex items-center justify-center text-brand-500 font-semibold text-sm group-hover:bg-brand-500 group-hover:text-white transition-all duration-300">04</div>
          <div class="w-px flex-1 bg-gradient-to-b from-brand-500/30 to-transparent mt-2"></div>
        </div>
        <div class="pb-12">
          <h3 class="text-xl font-medium text-white mb-2 group-hover:text-brand-500 transition-colors">Find Meaning in Your Experience</h3>
          <p class="text-sm text-neutral-400 leading-relaxed max-w-lg">Pain often carries a gift: wisdom, empathy, strength, purpose. Ask yourself: "How can what I've been through help me grow or help others?"</p>
        </div>
      </div>

      <div class="fade-in flex gap-6 group" style="transition-delay: 0.4s;">
        <div class="flex flex-col items-center">
          <div class="w-12 h-12 rounded-full bg-brand-500 flex items-center justify-center text-white font-semibold text-sm shadow-lg shadow-brand-500/30">05</div>
        </div>
        <div>
          <h3 class="text-xl font-medium text-white mb-2 group-hover:text-brand-500 transition-colors">Embrace Your New Beginning</h3>
          <p class="text-sm text-neutral-400 leading-relaxed max-w-lg">You are not the same person you were before &mdash; and that's beautiful. You are stronger, deeper, more compassionate. Step into this new version of yourself with pride.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- QUOTES -->
<section id="quotes" class="relative py-32 overflow-hidden">
  <div class="absolute top-0 left-0 right-0 divider"></div>
  <div class="absolute inset-0" style="background: radial-gradient(ellipse at top right, rgba(67,20,7,0.1), transparent 60%);"></div>

  <div class="relative max-w-7xl mx-auto px-6 lg:px-12">
    <div class="text-center max-w-2xl mx-auto mb-20 fade-in">
      <span class="text-xs font-semibold tracking-wider uppercase text-brand-500 mb-4 block">Words of Light</span>
      <h2 class="text-3xl lg:text-5xl font-medium tracking-tighter leading-[1.1] text-white">
        Healing Quotes
      </h2>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="fade-in bg-neutral-900/50 border border-white/5 rounded-3xl p-8 relative overflow-hidden group hover:border-brand-500/20 transition-all duration-500">
        <div class="quote-mark absolute -top-4 -left-2 font-serif">&ldquo;</div>
        <div class="relative">
          <p class="text-neutral-300 leading-relaxed mb-6 font-light italic">"The wound is the place where the Light enters you."</p>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="feather" class="w-3.5 h-3.5 text-brand-500"></i></div>
            <div><p class="text-sm font-medium text-white">Rumi</p><p class="text-xs text-neutral-500">Poet &amp; Mystic</p></div>
          </div>
        </div>
      </div>

      <div class="fade-in bg-neutral-900/50 border border-white/5 rounded-3xl p-8 relative overflow-hidden group hover:border-brand-500/20 transition-all duration-500" style="transition-delay: 0.1s;">
        <div class="quote-mark absolute -top-4 -left-2 font-serif">&ldquo;</div>
        <div class="relative">
          <p class="text-neutral-300 leading-relaxed mb-6 font-light italic">"You don't have to control your thoughts. You just have to stop letting them control you."</p>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="book-open" class="w-3.5 h-3.5 text-brand-500"></i></div>
            <div><p class="text-sm font-medium text-white">Dan Millman</p><p class="text-xs text-neutral-500">Author</p></div>
          </div>
        </div>
      </div>

      <div class="fade-in bg-neutral-900/50 border border-white/5 rounded-3xl p-8 relative overflow-hidden group hover:border-brand-500/20 transition-all duration-500" style="transition-delay: 0.2s;">
        <div class="quote-mark absolute -top-4 -left-2 font-serif">&ldquo;</div>
        <div class="relative">
          <p class="text-neutral-300 leading-relaxed mb-6 font-light italic">"There is a crack in everything, that's how the light gets in."</p>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="mic" class="w-3.5 h-3.5 text-brand-500"></i></div>
            <div><p class="text-sm font-medium text-white">Leonard Cohen</p><p class="text-xs text-neutral-500">Musician &amp; Poet</p></div>
          </div>
        </div>
      </div>

      <div class="fade-in bg-neutral-900/50 border border-white/5 rounded-3xl p-8 relative overflow-hidden group hover:border-brand-500/20 transition-all duration-500">
        <div class="quote-mark absolute -top-4 -left-2 font-serif">&ldquo;</div>
        <div class="relative">
          <p class="text-neutral-300 leading-relaxed mb-6 font-light italic">"Healing takes courage, and we all have courage, even if we have to dig a little to find it."</p>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="heart" class="w-3.5 h-3.5 text-brand-500"></i></div>
            <div><p class="text-sm font-medium text-white">Tori Amos</p><p class="text-xs text-neutral-500">Singer-Songwriter</p></div>
          </div>
        </div>
      </div>

      <div class="fade-in bg-neutral-900/50 border border-white/5 rounded-3xl p-8 relative overflow-hidden group hover:border-brand-500/20 transition-all duration-500" style="transition-delay: 0.1s;">
        <div class="quote-mark absolute -top-4 -left-2 font-serif">&ldquo;</div>
        <div class="relative">
          <p class="text-neutral-300 leading-relaxed mb-6 font-light italic">"Out of suffering have emerged the strongest souls; the most massive characters are seared with scars."</p>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="flame" class="w-3.5 h-3.5 text-brand-500"></i></div>
            <div><p class="text-sm font-medium text-white">Kahlil Gibran</p><p class="text-xs text-neutral-500">Writer &amp; Philosopher</p></div>
          </div>
        </div>
      </div>

      <div class="fade-in bg-neutral-900/50 border border-white/5 rounded-3xl p-8 relative overflow-hidden group hover:border-brand-500/20 transition-all duration-500" style="transition-delay: 0.2s;">
        <div class="quote-mark absolute -top-4 -left-2 font-serif">&ldquo;</div>
        <div class="relative">
          <p class="text-neutral-300 leading-relaxed mb-6 font-light italic">"You are allowed to be both a masterpiece and a work in progress simultaneously."</p>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="palette" class="w-3.5 h-3.5 text-brand-500"></i></div>
            <div><p class="text-sm font-medium text-white">Sophia Bush</p><p class="text-xs text-neutral-500">Actress &amp; Activist</p></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- DAILY AFFIRMATION -->
<section class="relative py-32 overflow-hidden">
  <div class="absolute top-0 left-0 right-0 divider"></div>
  <div class="max-w-7xl mx-auto px-6 lg:px-12">
    <div class="fade-in relative bg-neutral-900/50 border border-white/5 rounded-3xl p-10 lg:p-16 text-center overflow-hidden">
      <div class="absolute inset-0" style="background: radial-gradient(ellipse at center, rgba(255,107,44,0.05), transparent 70%);"></div>
      <div class="relative">
        <i data-lucide="sparkles" class="w-8 h-8 text-brand-500 mx-auto mb-6"></i>
        <span class="text-xs font-semibold tracking-wider uppercase text-brand-500 mb-4 block">Daily Affirmation</span>
        <h2 id="affirmationText" class="text-2xl lg:text-4xl font-medium tracking-tight text-white leading-snug max-w-3xl mx-auto mb-8 transition-opacity duration-500">
          "I am worthy of love, healing, and all the good things life has to offer."
        </h2>
        <button id="newAffirmation" class="inline-flex items-center gap-2 bg-white/5 border border-white/10 hover:border-brand-500/30 text-white text-sm font-medium px-6 py-3 rounded-full transition-all duration-300 group">
          <i data-lucide="refresh-cw" class="w-4 h-4 group-hover:rotate-180 transition-transform duration-500"></i>
          New Affirmation
        </button>
      </div>
    </div>
  </div>
</section>

<!-- BEGIN HEALING CTA -->
<section id="begin" class="relative py-32 overflow-hidden">
  <div class="absolute top-0 left-0 right-0 divider"></div>
  <div class="absolute inset-0" style="background: radial-gradient(ellipse at center, rgba(67,20,7,0.2), #0a0a0a 70%);"></div>

  <div class="relative max-w-7xl mx-auto px-6 lg:px-12">
    <div class="grid lg:grid-cols-2 gap-16 items-center">
      <div class="fade-in">
        <span class="text-xs font-semibold tracking-wider uppercase text-brand-500 mb-4 block">Take the First Step</span>
        <h2 class="text-3xl lg:text-5xl font-medium tracking-tighter leading-[1.1] text-white mb-6">
          Your Healing<br>Starts Today
        </h2>
        <p class="text-lg font-light text-neutral-400 leading-relaxed mb-8">
          You've read the words, felt the resonance. Now it's time to act. Write down one thing you want to release. Say it out loud. Then let it go &mdash; even just a little. That's where healing begins.
        </p>

        <div class="bg-neutral-900/50 border border-white/10 rounded-2xl p-6">
          <label class="text-sm text-neutral-400 mb-3 block">Write something you want to let go of:</label>
          <textarea id="releaseText" rows="3" placeholder="I release..." class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-neutral-600 focus:outline-none focus:border-brand-500/50 resize-none transition-colors"></textarea>
          <button id="releaseBtn" class="mt-4 w-full bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white text-sm font-medium py-3 rounded-xl transition-all duration-300 shadow-lg shadow-brand-500/20 flex items-center justify-center gap-2">
            <i data-lucide="wind" class="w-4 h-4"></i>
            Release It
          </button>
          <div id="releaseMsg" class="mt-3 text-sm text-brand-400 text-center hidden">You have taken a powerful step. Breathe and let go.</div>
        </div>
      </div>

      <div class="fade-in flex justify-center" style="transition-delay: 0.15s;">
        <div class="relative">
          <div class="w-72 h-72 lg:w-96 lg:h-96 rounded-full border border-brand-500/20 flex items-center justify-center breathing-circle">
            <div class="w-56 h-56 lg:w-72 lg:h-72 rounded-full border border-brand-500/15 flex items-center justify-center" style="animation: breathe 6s ease-in-out 1s infinite;">
              <div class="w-40 h-40 lg:w-48 lg:h-48 rounded-full bg-gradient-to-br from-brand-600/20 to-brand-500/5 border border-brand-500/20 flex items-center justify-center">
                <i data-lucide="heart" class="w-16 h-16 text-brand-500/60"></i>
              </div>
            </div>
          </div>
          <div class="absolute top-0 -left-4 animate-float text-sm text-brand-400/60 font-light">peace</div>
          <div class="absolute top-12 -right-8 animate-float-delay text-sm text-brand-400/60 font-light">love</div>
          <div class="absolute bottom-16 -left-8 animate-float-delay text-sm text-brand-400/60 font-light">hope</div>
          <div class="absolute bottom-0 -right-4 animate-float text-sm text-brand-400/60 font-light">strength</div>
          <div class="absolute top-1/2 -left-12 animate-float text-sm text-brand-400/60 font-light">courage</div>
          <div class="absolute top-1/3 -right-12 animate-float-delay text-sm text-brand-400/60 font-light">light</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="relative py-16 border-t border-white/5">
  <div class="max-w-7xl mx-auto px-6 lg:px-12">
    <div class="flex flex-col lg:flex-row items-center justify-between gap-8">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-full bg-gradient-to-br from-brand-600 to-brand-500 flex items-center justify-center">
          <i data-lucide="heart" class="w-4 h-4 text-white"></i>
        </div>
        <div>
          <span class="text-white font-medium tracking-tight">Soul Recovery</span>
          <p class="text-xs text-neutral-500">Healing Hearts, One Breath at a Time</p>
        </div>
      </div>

      <div class="flex items-center gap-6 text-sm text-neutral-500">
        <a href="#hero" class="hover:text-white transition-colors">Home</a>
        <a href="#about" class="hover:text-white transition-colors">About</a>
        <a href="#healing" class="hover:text-white transition-colors">Healing</a>
        <a href="#positivity" class="hover:text-white transition-colors">Positivity</a>
      </div>

      <div class="text-center lg:text-right">
        <p class="text-sm text-neutral-400">Created with <span class="text-brand-500">&hearts;</span> by</p>
        <p class="text-white font-medium tracking-tight">""" + CREATOR + """</p>
      </div>
    </div>

    <div class="divider mt-10 mb-6"></div>
    <div class="text-center">
      <p class="text-xs text-neutral-600">&copy; 2025 Soul Recovery. Your journey is uniquely yours. Be gentle with yourself.</p>
    </div>
  </div>
</footer>

<!-- SCRIPTS -->
<script>
  lucide.createIcons();

  var mobileToggle = document.getElementById('mobileToggle');
  var mobileMenu = document.getElementById('mobileMenu');
  mobileToggle.addEventListener('click', function() {
    mobileMenu.classList.toggle('open');
  });
  mobileMenu.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', function() { mobileMenu.classList.remove('open'); });
  });

  var fadeElements = document.querySelectorAll('.fade-in');
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
  fadeElements.forEach(function(el) { observer.observe(el); });

  var affirmations = [
    '"I am worthy of love, healing, and all the good things life has to offer."',
    '"I release what no longer serves me and make room for what does."',
    '"I am not my pain. I am the awareness behind it."',
    '"Every day, in every way, I am getting better and better."',
    '"I choose to forgive \\u2014 not for them, but for me."',
    '"I trust the process of my unfolding."',
    '"I am strong enough to face my shadows and wise enough to welcome them."',
    '"My heart is open, my mind is calm, my soul is at peace."',
    '"I have survived 100% of my worst days. I can handle today."',
    '"I am becoming the person I needed when I was hurting."',
    '"Healing is not a race. I honor my pace."',
    '"I deserve the love I keep giving to everyone else."',
    '"I am not broken. I am breaking open into something more beautiful."',
    '"Today I choose progress over perfection."',
    '"My scars tell a story of survival, not defeat."'
  ];
  var currentAffirmation = 0;
  var affirmationText = document.getElementById('affirmationText');
  var newAffirmationBtn = document.getElementById('newAffirmation');
  newAffirmationBtn.addEventListener('click', function() {
    affirmationText.style.opacity = '0';
    setTimeout(function() {
      currentAffirmation = (currentAffirmation + 1) % affirmations.length;
      affirmationText.textContent = affirmations[currentAffirmation];
      affirmationText.style.opacity = '1';
    }, 300);
  });

  var releaseBtn = document.getElementById('releaseBtn');
  var releaseText = document.getElementById('releaseText');
  var releaseMsg = document.getElementById('releaseMsg');
  releaseBtn.addEventListener('click', function() {
    if (releaseText.value.trim()) {
      releaseMsg.classList.remove('hidden');
      releaseText.value = '';
      releaseBtn.innerHTML = 'Released';
      releaseBtn.disabled = true;
      releaseBtn.classList.add('opacity-60');
      setTimeout(function() {
        releaseMsg.classList.add('hidden');
        releaseBtn.innerHTML = 'Release It';
        releaseBtn.disabled = false;
        releaseBtn.classList.remove('opacity-60');
      }, 4000);
    }
  });

  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        var offset = 100;
        var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });
</script>
</body>
</html>"""


# ─── HTTP HANDLER ────────────────────────────────────────────────────────────

class SoulRecoveryHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(build_page().encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('404 - Page not found. Return to /'.encode('utf-8'))

    def log_message(self, format, *args):
        print(f"  * {self.address_string()} - {args[0]}")


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    port_str = str(PORT)
    print()
    print("  ============================================")
    print("                                              ")
    print("     Soul Recovery & Healing Hearts           ")
    print("                                              ")
    print(f"     Created by {CREATOR:<29s}")
    print("                                              ")
    print(f"     Server: http://localhost:{port_str:<5s}          ")
    print("                                              ")
    print("     Press Ctrl+C to stop                     ")
    print("                                              ")
    print("  ============================================")
    print()

    def open_browser():
        webbrowser.open(f'http://localhost:{PORT}')
    threading.Timer(1.5, open_browser).start()

    with socketserver.TCPServer(("", PORT), SoulRecoveryHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Server stopped. May your soul continue to heal.\n")
            httpd.server_close()


if __name__ == '__main__':
    main()