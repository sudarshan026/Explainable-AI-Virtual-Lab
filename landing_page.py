"""
landing_page.py — XAI Virtual Lab Landing Page
================================================
Renders a visually stunning landing / home page with project details,
feature highlights, and navigation to the analysis lab.

Visual effects: CSS particle field, glitch title, scan-line overlay,
floating research formulas, animated data streams, holographic cards,
rotating gradient borders, and micro-animations throughout.
"""

import streamlit as st


# ──────────────────────────────────────────────
# 1.  Landing Page CSS
# ──────────────────────────────────────────────
def get_landing_css() -> str:
    """Return a <style> block for the landing page with glassmorphism,
    neon accents, floating orbs, particles, and rich micro-animations."""

    return """
    <style>
    /* ── Import Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400&display=swap');

    /* ── Root variables ── */
    :root {
        --neon-cyan:    #00f0ff;
        --neon-magenta: #ff00e5;
        --neon-purple:  #a855f7;
        --bg-dark:      #0a0a1a;
        --card-bg:      rgba(15, 15, 35, 0.65);
        --card-border:  rgba(0, 240, 255, 0.25);
        --text-primary: #e0e0ff;
        --text-muted:   #8888aa;
    }

    /* ── Global background ── */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d0d2b 40%, #120826 70%, #0a0a1a 100%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Hide sidebar completely on landing ── */
    section[data-testid="stSidebar"]   { display: none !important; }
    [data-testid="collapsedControl"]   { display: none !important; }
    button[data-testid="baseButton-header"] { display: none !important; }

    /* ── Custom scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-dark); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--neon-cyan), var(--neon-magenta));
        border-radius: 4px;
    }

    /* ═══════════════════════════════════════════════
       BACKGROUND LAYER 1: FLOATING ORBS
       ═══════════════════════════════════════════════ */
    .landing-orbs {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
    }
    .orb-1 {
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(0,240,255,0.14), transparent 70%);
        top: -200px; left: -150px;
        animation: orbFloat1 18s ease-in-out infinite;
    }
    .orb-2 {
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(255,0,229,0.11), transparent 70%);
        bottom: -150px; right: -100px;
        animation: orbFloat2 22s ease-in-out infinite;
    }
    .orb-3 {
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(100,0,255,0.09), transparent 70%);
        top: 30%; left: 50%;
        animation: orbFloat3 15s ease-in-out infinite;
    }
    .orb-4 {
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(0,240,255,0.07), transparent 70%);
        top: 60%; left: 20%;
        animation: orbFloat1 20s ease-in-out infinite reverse;
    }
    @keyframes orbFloat1 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        25%      { transform: translate(80px, -60px) scale(1.12); }
        50%      { transform: translate(-40px, 50px) scale(0.92); }
        75%      { transform: translate(50px, 30px) scale(1.06); }
    }
    @keyframes orbFloat2 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        33%      { transform: translate(-60px, -70px) scale(1.08); }
        66%      { transform: translate(50px, 40px) scale(0.88); }
    }
    @keyframes orbFloat3 {
        0%, 100% { transform: translate(0, 0) scale(1) rotate(0deg); }
        50%      { transform: translate(-50px, -40px) scale(1.1) rotate(5deg); }
    }

    /* ═══════════════════════════════════════════════
       BACKGROUND LAYER 2: GRID OVERLAY
       ═══════════════════════════════════════════════ */
    .grid-overlay {
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(0,240,255,0.022) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,240,255,0.022) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
        z-index: 0;
    }

    /* ═══════════════════════════════════════════════
       BACKGROUND LAYER 3: PARTICLES
       ═══════════════════════════════════════════════ */
    .particles-container {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .ptcl {
        position: absolute;
        border-radius: 50%;
        animation: particleDrift var(--d, 20s) var(--delay, 0s) infinite ease-in-out;
    }
    @keyframes particleDrift {
        0%, 100% {
            transform: translate(0, 0) scale(var(--s-start, 0.5));
            opacity: 0.15;
        }
        25% {
            transform: translate(var(--dx1, 30px), var(--dy1, -60px)) scale(1);
            opacity: var(--max-o, 0.6);
        }
        50% {
            transform: translate(var(--dx2, -20px), var(--dy2, -120px)) scale(0.8);
            opacity: calc(var(--max-o, 0.6) * 0.7);
        }
        75% {
            transform: translate(var(--dx3, 40px), var(--dy3, -50px)) scale(1.1);
            opacity: var(--max-o, 0.6);
        }
    }

    /* ═══════════════════════════════════════════════
       BACKGROUND LAYER 4: FLOATING FORMULAS
       ═══════════════════════════════════════════════ */
    .floating-formulas {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .formula {
        position: absolute;
        font-family: 'JetBrains Mono', monospace;
        white-space: nowrap;
        opacity: 0;
        animation: formulaFloat var(--fd, 30s) var(--f-delay, 0s) infinite;
    }
    @keyframes formulaFloat {
        0%   { opacity: 0; transform: translateY(0) rotate(0deg); }
        5%   { opacity: 1; }
        45%  { opacity: 1; }
        50%  { opacity: 0; transform: translateY(-60px) rotate(var(--f-rot, 3deg)); }
        100% { opacity: 0; }
    }

    /* ═══════════════════════════════════════════════
       BACKGROUND LAYER 5: DATA STREAMS
       ═══════════════════════════════════════════════ */
    .data-streams {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .data-stream {
        position: absolute;
        top: 0;
        width: 1px;
        height: 100vh;
        background: linear-gradient(to bottom,
            transparent 0%,
            var(--stream-color, rgba(0,240,255,0.08)) 30%,
            var(--stream-color, rgba(0,240,255,0.08)) 70%,
            transparent 100%);
        animation: streamPulse var(--sp-d, 6s) var(--sp-delay, 0s) infinite ease-in-out;
    }
    @keyframes streamPulse {
        0%, 100% { opacity: 0; transform: scaleY(0.3); }
        50%      { opacity: 1; transform: scaleY(1); }
    }

    /* ═══════════════════════════════════════════════
       BACKGROUND LAYER 6: SCAN LINES
       ═══════════════════════════════════════════════ */
    .scanlines {
        position: fixed;
        inset: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 0, 0, 0.015) 2px,
            rgba(0, 0, 0, 0.015) 4px
        );
        pointer-events: none;
        z-index: 1;
    }
    .scan-beam {
        position: fixed;
        left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg,
            transparent,
            rgba(0,240,255,0.06),
            rgba(0,240,255,0.12),
            rgba(0,240,255,0.06),
            transparent);
        animation: scanBeam 8s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    @keyframes scanBeam {
        0%   { top: -2px; }
        100% { top: 100vh; }
    }

    /* ═══════════════════════════════════════════════
       SHIMMER / GLITCH KEYFRAMES
       ═══════════════════════════════════════════════ */
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(0,240,255,0.15),
                               inset 0 0 20px rgba(0,240,255,0.05); }
        50%      { box-shadow: 0 0 40px rgba(0,240,255,0.35),
                               inset 0 0 30px rgba(0,240,255,0.10); }
    }
    @keyframes borderGlow {
        0%, 100% { border-color: rgba(0,240,255,0.25); }
        50%      { border-color: rgba(0,240,255,0.6); }
    }
    @keyframes breathe {
        0%, 100% { text-shadow: 0 0 20px rgba(0,240,255,0.3); }
        50%      { text-shadow: 0 0 35px rgba(0,240,255,0.6), 0 0 60px rgba(0,240,255,0.2); }
    }

    /* ═══════════════════════════════════════════════
       HERO SECTION
       ═══════════════════════════════════════════════ */
    .hero-section {
        text-align: center;
        padding: 4rem 1rem 2rem;
        position: relative;
        z-index: 2;
        animation: fadeInUp 1s ease-out;
    }
    .hero-badge {
        display: inline-block;
        padding: 7px 26px;
        border: 1px solid rgba(0,240,255,0.3);
        border-radius: 30px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.55rem;
        letter-spacing: 6px;
        color: var(--neon-cyan);
        background: rgba(0,240,255,0.04);
        margin-bottom: 2rem;
        animation: borderGlow 3s ease-in-out infinite;
        position: relative;
    }
    .hero-badge::before {
        content: '';
        position: absolute;
        inset: -1px;
        border-radius: 30px;
        background: linear-gradient(90deg, transparent, rgba(0,240,255,0.15), transparent);
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
        z-index: -1;
    }

    /* ── Glitch Title Wrapper ── */
    .hero-title-wrapper {
        position: relative;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        font-size: 4rem;
        background: linear-gradient(135deg, #00f0ff 0%, #a855f7 30%, #ff00e5 60%, #00f0ff 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 5s linear infinite;
        letter-spacing: 4px;
        line-height: 1.15;
    }
    .hero-glitch {
        position: absolute;
        top: 0; left: 0; right: 0;
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        font-size: 4rem;
        letter-spacing: 4px;
        line-height: 1.15;
        text-align: center;
        pointer-events: none;
    }
    .hero-glitch-1 {
        color: var(--neon-cyan);
        clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
        animation: glitch1 8s infinite;
        opacity: 0;
    }
    .hero-glitch-2 {
        color: var(--neon-magenta);
        clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%);
        animation: glitch2 8s infinite;
        opacity: 0;
    }
    @keyframes glitch1 {
        0%, 90%, 100%  { opacity: 0; transform: translate(0); }
        91%  { opacity: 0.8; transform: translate(-5px, -2px) skewX(-2deg); }
        92%  { opacity: 0; }
        93%  { opacity: 0.6; transform: translate(4px, 1px) skewX(1deg); }
        94%  { opacity: 0; }
    }
    @keyframes glitch2 {
        0%, 93%, 100%  { opacity: 0; transform: translate(0); }
        94%  { opacity: 0.7; transform: translate(5px, 2px) skewX(2deg); }
        95%  { opacity: 0; }
        96%  { opacity: 0.5; transform: translate(-3px, -1px) skewX(-1deg); }
        97%  { opacity: 0; }
    }

    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #c8c8e0;
        font-weight: 300;
        margin-bottom: 1.2rem;
        letter-spacing: 1.5px;
    }
    .hero-description {
        font-family: 'Inter', sans-serif;
        font-size: 0.92rem;
        color: var(--text-muted);
        max-width: 620px;
        margin: 0 auto;
        line-height: 1.85;
    }

    /* ═══════════════════════════════════════════════
       STAT COUNTERS
       ═══════════════════════════════════════════════ */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 3rem;
        flex-wrap: wrap;
        margin: 2.5rem 0;
        animation: fadeInUp 1s ease-out 0.2s both;
    }
    .stat-item { text-align: center; }
    .stat-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        color: var(--neon-cyan);
        animation: breathe 3s ease-in-out infinite;
    }
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.68rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2.5px;
        margin-top: 6px;
    }

    /* ═══════════════════════════════════════════════
       CTA BUTTON
       ═══════════════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg,
            rgba(0,240,255,0.12), rgba(255,0,229,0.12)) !important;
        border: 1px solid rgba(0,240,255,0.5) !important;
        color: #00f0ff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1rem !important;
        letter-spacing: 3px !important;
        padding: 0.9rem 3rem !important;
        border-radius: 14px !important;
        animation: pulseGlow 3s ease-in-out infinite !important;
        transition: all 0.4s cubic-bezier(0.4,0,0.2,1) !important;
        text-transform: uppercase !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important; left: -100% !important;
        width: 100% !important; height: 100% !important;
        background: linear-gradient(90deg,
            transparent, rgba(0,240,255,0.12), transparent) !important;
        animation: btnSweep 3s ease-in-out infinite !important;
    }
    @keyframes btnSweep {
        0%   { left: -100%; }
        50%  { left: 100%; }
        100% { left: 100%; }
    }
    .stButton > button:hover {
        box-shadow: 0 0 60px rgba(0,240,255,0.35),
                    inset 0 0 40px rgba(0,240,255,0.1),
                    0 0 100px rgba(0,240,255,0.15) !important;
        transform: translateY(-3px) scale(1.03) !important;
        border-color: rgba(0,240,255,0.9) !important;
        color: #ffffff !important;
    }
    .stButton > button:active {
        transform: translateY(0) scale(0.97) !important;
    }

    /* ═══════════════════════════════════════════════
       SECTION DIVIDERS  (with traveling light)
       ═══════════════════════════════════════════════ */
    .section-divider {
        text-align: center;
        margin: 3.5rem 0 2rem;
        position: relative;
        z-index: 2;
    }
    .section-divider::before {
        content: '';
        position: absolute;
        top: 50%; left: 8%; right: 8%;
        height: 1px;
        background: linear-gradient(90deg, transparent,
            rgba(0,240,255,0.15), rgba(255,0,229,0.15), transparent);
    }
    .section-divider::after {
        content: '';
        position: absolute;
        top: calc(50% - 2px);
        width: 30px; height: 4px;
        border-radius: 2px;
        background: var(--neon-cyan);
        box-shadow: 0 0 12px var(--neon-cyan), 0 0 25px rgba(0,240,255,0.4);
        animation: travelLight 5s ease-in-out infinite;
    }
    @keyframes travelLight {
        0%   { left: 8%; opacity: 0; }
        10%  { opacity: 1; }
        90%  { opacity: 1; }
        100% { left: calc(92% - 30px); opacity: 0; }
    }
    .section-divider-text {
        display: inline-block;
        background: var(--bg-dark);
        padding: 0 1.5rem;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.65rem;
        letter-spacing: 5px;
        color: var(--neon-cyan);
        position: relative;
        z-index: 1;
    }

    /* ═══════════════════════════════════════════════
       FEATURE CARDS  (with animated accent border)
       ═══════════════════════════════════════════════ */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
        animation: fadeInUp 1s ease-out 0.4s both;
        position: relative;
        z-index: 2;
    }
    .feature-card {
        background: rgba(15,15,35,0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(0,240,255,0.10);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
        position: relative;
        overflow: hidden;
    }
    /* ── Top accent line ── */
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg,
            var(--neon-cyan), var(--neon-magenta), var(--neon-cyan));
        background-size: 200% 100%;
        transform: scaleX(0);
        transition: transform 0.5s ease;
        transform-origin: left;
        animation: shimmer 3s linear infinite;
    }
    /* ── Bottom glow ── */
    .feature-card::after {
        content: '';
        position: absolute;
        bottom: -60%; left: 10%; right: 10%;
        height: 80%;
        background: radial-gradient(ellipse, rgba(0,240,255,0.06), transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    .feature-card:hover {
        transform: translateY(-8px);
        border-color: rgba(0,240,255,0.35);
        box-shadow: 0 20px 50px rgba(0,0,0,0.4),
                    0 0 40px rgba(0,240,255,0.06);
    }
    .feature-card:hover::before { transform: scaleX(1); }
    .feature-card:hover::after  { opacity: 1; }
    .feature-icon {
        font-size: 2.4rem;
        margin-bottom: 1rem;
        display: block;
    }
    .feature-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.74rem;
        color: var(--neon-cyan);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .feature-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.84rem;
        color: var(--text-muted);
        line-height: 1.75;
    }

    /* ═══════════════════════════════════════════════
       HOW IT WORKS  (3-step timeline)
       ═══════════════════════════════════════════════ */
    .steps-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.5rem;
        margin: 1.5rem 0;
        animation: fadeInUp 1s ease-out 0.5s both;
        position: relative;
        z-index: 2;
    }
    /* ── Connecting line behind all steps ── */
    .steps-grid::before {
        content: '';
        position: absolute;
        top: 27px;
        left: calc(16.66% + 27px);
        right: calc(16.66% + 27px);
        height: 2px;
        background: linear-gradient(90deg,
            rgba(0,240,255,0.3),
            rgba(168,85,247,0.3),
            rgba(255,0,229,0.3));
    }
    .step-card {
        text-align: center;
        padding: 0 1.2rem 2rem;
        position: relative;
    }
    .step-number {
        width: 56px; height: 56px;
        border-radius: 50%;
        border: 2px solid rgba(0,240,255,0.3);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.2rem;
        font-family: 'Orbitron', sans-serif;
        font-size: 1rem;
        color: var(--neon-cyan);
        background: rgba(5,5,20,0.9);
        box-shadow: 0 0 15px rgba(0,240,255,0.08);
        transition: all 0.4s ease;
        position: relative;
        z-index: 1;
    }
    .step-card:hover .step-number {
        box-shadow: 0 0 30px rgba(0,240,255,0.25),
                    inset 0 0 15px rgba(0,240,255,0.08);
        border-color: rgba(0,240,255,0.7);
        transform: scale(1.1);
    }
    .step-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.76rem;
        color: var(--text-primary);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .step-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        color: var(--text-muted);
        line-height: 1.7;
    }

    /* ═══════════════════════════════════════════════
       ABOUT XAI  (holographic glass card)
       ═══════════════════════════════════════════════ */
    .xai-card {
        background: linear-gradient(135deg,
            rgba(15,15,35,0.50) 0%,
            rgba(40,0,60,0.25) 50%,
            rgba(15,15,35,0.50) 100%);
        background-size: 200% 200%;
        animation: holoShift 8s ease-in-out infinite,
                   fadeInUp 1s ease-out 0.5s both;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(255,0,229,0.12);
        border-radius: 18px;
        padding: 2.5rem 2.8rem;
        margin: 1.5rem 0;
        position: relative;
        z-index: 2;
        overflow: hidden;
        transition: border-color 0.4s ease;
    }
    .xai-card:hover {
        border-color: rgba(255,0,229,0.35);
    }
    @keyframes holoShift {
        0%, 100% { background-position: 0% 50%; }
        50%      { background-position: 100% 50%; }
    }
    .xai-card::before {
        content: '';
        position: absolute;
        top: -50%; right: -20%;
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(255,0,229,0.06), transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        animation: orbFloat3 12s ease-in-out infinite;
    }
    .xai-card::after {
        content: '';
        position: absolute;
        bottom: -40%; left: -10%;
        width: 250px; height: 250px;
        background: radial-gradient(circle, rgba(0,240,255,0.04), transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        animation: orbFloat2 15s ease-in-out infinite;
    }
    .xai-card-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        color: var(--neon-magenta);
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        text-shadow: 0 0 10px rgba(255,0,229,0.3);
    }
    .xai-card-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #b8b8d0;
        line-height: 1.85;
        position: relative;
        z-index: 1;
    }
    .xai-card-text b { color: var(--text-primary); }
    .xai-card-text .accent-cyan { color: var(--neon-cyan); font-weight: 500; }
    .xai-card-text .accent-magenta { color: var(--neon-magenta); font-weight: 500; }

    /* ═══════════════════════════════════════════════
       TECH STACK BADGES
       ═══════════════════════════════════════════════ */
    .tech-grid {
        display: flex;
        justify-content: center;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin: 1.5rem 0;
        animation: fadeInUp 1s ease-out 0.6s both;
        position: relative;
        z-index: 2;
    }
    .tech-badge {
        padding: 10px 22px;
        border: 1px solid rgba(0,240,255,0.12);
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.8rem;
        color: #c8c8e0;
        background: rgba(15,15,35,0.45);
        letter-spacing: 1px;
        transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
        position: relative;
        overflow: hidden;
    }
    .tech-badge::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg,
            rgba(0,240,255,0.04), transparent 60%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .tech-badge:hover {
        border-color: rgba(0,240,255,0.5);
        box-shadow: 0 0 25px rgba(0,240,255,0.12),
                    0 4px 15px rgba(0,0,0,0.3);
        color: var(--neon-cyan);
        transform: translateY(-3px);
    }
    .tech-badge:hover::before { opacity: 1; }

    /* ═══════════════════════════════════════════════
       FOOTER
       ═══════════════════════════════════════════════ */
    .landing-footer {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: var(--text-muted);
        letter-spacing: 1px;
        border-top: 1px solid rgba(0,240,255,0.06);
        margin-top: 2.5rem;
        position: relative;
        z-index: 2;
    }
    .landing-footer span { color: var(--neon-cyan); }

    </style>
    """


# ──────────────────────────────────────────────
# 2.  Generate particle HTML
# ──────────────────────────────────────────────
def _build_particles(count: int = 30) -> str:
    """Generate CSS-animated particle divs with varied properties."""
    import random
    random.seed(42)  # deterministic for consistent layout

    colors = [
        "rgba(0,240,255,0.5)",
        "rgba(0,240,255,0.4)",
        "rgba(168,85,247,0.4)",
        "rgba(255,0,229,0.35)",
        "rgba(255,255,255,0.3)",
    ]
    particles = []
    for _ in range(count):
        x = random.randint(2, 98)
        y = random.randint(2, 98)
        size = random.choice([2, 2, 3, 3, 4])
        color = random.choice(colors)
        duration = random.randint(12, 30)
        delay = -random.randint(0, 20)
        dx1 = random.randint(-60, 60)
        dy1 = random.randint(-80, 80)
        dx2 = random.randint(-50, 50)
        dy2 = random.randint(-90, 90)
        dx3 = random.randint(-70, 70)
        dy3 = random.randint(-60, 60)
        max_o = round(random.uniform(0.3, 0.7), 2)
        particles.append(
            f'<div class="ptcl" style="left:{x}%;top:{y}%;'
            f"width:{size}px;height:{size}px;"
            f"background:{color};"
            f"box-shadow:0 0 {size * 3}px {color};"
            f"--d:{duration}s;--delay:{delay}s;"
            f"--dx1:{dx1}px;--dy1:{dy1}px;"
            f"--dx2:{dx2}px;--dy2:{dy2}px;"
            f"--dx3:{dx3}px;--dy3:{dy3}px;"
            f'--max-o:{max_o};--s-start:0.4"></div>'
        )
    return "\n".join(particles)


def _build_formulas() -> str:
    """Generate floating research formula decorations."""
    formulas = [
        ("∇f(x) = Σ ∂L/∂wᵢ", "8%",  "12%", "0.04",  "28s", "0s",   "-3deg"),
        ("σ(Wx + b)",          "82%", "18%", "0.035", "32s", "-5s",  "4deg"),
        ("softmax(zᵢ)",        "15%", "55%", "0.03",  "26s", "-12s", "2deg"),
        ("∂Loss/∂θ",           "75%", "42%", "0.04",  "30s", "-3s",  "-5deg"),
        ("P(y|x; θ)",          "5%",  "78%", "0.035", "35s", "-8s",  "3deg"),
        ("argmax P(c|I)",      "88%", "70%", "0.03",  "24s", "-15s", "-2deg"),
        ("ReLU(x) = max(0,x)", "45%", "88%", "0.025", "29s", "-7s",  "1deg"),
        ("∑ᵢ αᵢ · Aᵏ",        "60%", "8%",  "0.04",  "33s", "-10s", "-4deg"),
        ("Grad-CAM: αᵏc",      "25%", "35%", "0.03",  "27s", "-2s",  "5deg"),
        ("H(p,q) = -Σp·log(q)","70%", "90%", "0.025", "31s", "-14s", "2deg"),
    ]
    html_parts = []
    for text, left, top, opacity, dur, delay, rot in formulas:
        html_parts.append(
            f'<span class="formula" style="left:{left};top:{top};'
            f"color:rgba(0,240,255,{opacity});"
            f'font-size:0.72rem;--fd:{dur};--f-delay:{delay};--f-rot:{rot}">'
            f"{text}</span>"
        )
    return "\n".join(html_parts)


def _build_data_streams() -> str:
    """Generate vertical data-stream light columns."""
    streams = [
        ("8%",  "rgba(0,240,255,0.04)", "7s",  "0s"),
        ("23%", "rgba(168,85,247,0.03)","9s",  "-3s"),
        ("41%", "rgba(0,240,255,0.03)", "11s", "-6s"),
        ("58%", "rgba(255,0,229,0.03)", "8s",  "-2s"),
        ("74%", "rgba(0,240,255,0.04)", "10s", "-5s"),
        ("91%", "rgba(168,85,247,0.03)","12s", "-8s"),
    ]
    parts = []
    for left, color, dur, delay in streams:
        parts.append(
            f'<div class="data-stream" style="left:{left};'
            f'--stream-color:{color};--sp-d:{dur};--sp-delay:{delay}"></div>'
        )
    return "\n".join(parts)


# ──────────────────────────────────────────────
# 3.  Render the Landing Page
# ──────────────────────────────────────────────
def render_landing():
    """Build and display the full landing page."""

    # ── Inject CSS ──
    st.markdown(get_landing_css(), unsafe_allow_html=True)

    # ════════════════════════════════════════════
    # BACKGROUND LAYERS
    # ════════════════════════════════════════════
    st.markdown(
        f"""
        <div class="landing-orbs">
            <div class="orb orb-1"></div>
            <div class="orb orb-2"></div>
            <div class="orb orb-3"></div>
            <div class="orb orb-4"></div>
        </div>
        <div class="grid-overlay"></div>
        <div class="particles-container">{_build_particles(30)}</div>
        <div class="floating-formulas">{_build_formulas()}</div>
        <div class="data-streams">{_build_data_streams()}</div>
        <div class="scanlines"></div>
        <div class="scan-beam"></div>
        """,
        unsafe_allow_html=True,
    )

    # ════════════════════════════════════════════
    # HERO
    # ════════════════════════════════════════════
    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-badge">⬡ RESEARCH PLATFORM</div>
            <div class="hero-title-wrapper">
                <div class="hero-title">XAI Virtual Lab</div>
                <div class="hero-glitch hero-glitch-1" aria-hidden="true">XAI Virtual Lab</div>
                <div class="hero-glitch hero-glitch-2" aria-hidden="true">XAI Virtual Lab</div>
            </div>
            <div class="hero-subtitle">Peer Inside the Black Box of Deep Neural Networks</div>
            <div class="hero-description">
                Upload any image, classify it using state-of-the-art convolutional
                neural networks, and explore exactly how the AI makes its decisions
                through interactive Grad-CAM explanations and 3D neural attention
                landscapes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ════════════════════════════════════════════
    # STAT COUNTERS
    # ════════════════════════════════════════════
    st.markdown(
        """
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">1,000+</div>
                <div class="stat-label">ImageNet Classes</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">2</div>
                <div class="stat-label">Model Architectures</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">3D</div>
                <div class="stat-label">Interactive Viz</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">AI</div>
                <div class="stat-label">Diagnostic Reports</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ════════════════════════════════════════════
    # CTA BUTTON
    # ════════════════════════════════════════════
    _cta_left, cta_mid, _cta_right = st.columns([1, 1, 1])
    with cta_mid:
        if st.button("🔬  ENTER THE LAB", use_container_width=True):
            st.session_state.page = "lab"
            st.rerun()

    # ════════════════════════════════════════════
    # CAPABILITIES
    # ════════════════════════════════════════════
    st.markdown(
        '<div class="section-divider"><span class="section-divider-text">CAPABILITIES</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="features-grid">
            <div class="feature-card">
                <span class="feature-icon">🎯</span>
                <div class="feature-title">Grad-CAM Visualization</div>
                <div class="feature-desc">
                    Visual explanations through Gradient-weighted Class
                    Activation Mapping.  See exactly where the neural
                    network focuses when classifying your image.
                </div>
            </div>
            <div class="feature-card">
                <span class="feature-icon">🏔️</span>
                <div class="feature-title">3D Attention Matrix</div>
                <div class="feature-desc">
                    Interactive 3D topographic surfaces revealing the
                    activation landscape.  Rotate, zoom, and explore neural
                    attention from every angle.
                </div>
            </div>
            <div class="feature-card">
                <span class="feature-icon">🔄</span>
                <div class="feature-title">Multi-Architecture</div>
                <div class="feature-desc">
                    Switch seamlessly between ResNet50 and VGG16
                    architectures.  Compare how different networks
                    attend to visual features.
                </div>
            </div>
            <div class="feature-card">
                <span class="feature-icon">📊</span>
                <div class="feature-title">AI Diagnostics</div>
                <div class="feature-desc">
                    Automated analysis reports with quantitative metrics.
                    Understand confidence levels, attention spread, and
                    potential biases at a glance.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ════════════════════════════════════════════
    # ABOUT EXPLAINABLE AI
    # ════════════════════════════════════════════
    st.markdown(
        '<div class="section-divider"><span class="section-divider-text">ABOUT EXPLAINABLE AI</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="xai-card">
            <div class="xai-card-title">⬡ Why Explainability Matters</div>
            <div class="xai-card-text">
                Deep neural networks achieve remarkable accuracy, but they
                operate as <b>black boxes</b> — making decisions through
                millions of learned parameters that are opaque to human
                understanding.  <b>Explainable AI (XAI)</b> bridges this gap
                by providing visual and quantitative methods to interpret
                <i>what</i> the network sees and <i>why</i> it makes specific
                predictions.
                <br><br>
                This lab uses <span class="accent-cyan">Grad-CAM</span>
                (Gradient-weighted Class Activation Mapping), a technique
                that leverages the <span class="accent-magenta">gradients
                flowing into the final convolutional layer</span> to produce
                a coarse localization map highlighting the important regions
                for predicting a concept.  The result is a powerful lens into
                the model's reasoning — essential for building
                <b>trust</b>, <b>debugging failures</b>, and identifying
                <b>dataset biases</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ════════════════════════════════════════════
    # HOW IT WORKS
    # ════════════════════════════════════════════
    st.markdown(
        '<div class="section-divider"><span class="section-divider-text">HOW IT WORKS</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="steps-grid">
            <div class="step-card">
                <div class="step-number">01</div>
                <div class="step-title">Upload</div>
                <div class="step-desc">
                    Select any image in JPG, PNG, or WebP format.
                    The lab accepts photographs, illustrations, and any
                    visual content.
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">02</div>
                <div class="step-title">Classify</div>
                <div class="step-desc">
                    A pre-trained CNN processes your image through
                    millions of parameters and produces a classification
                    with confidence scores.
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">03</div>
                <div class="step-title">Explain</div>
                <div class="step-desc">
                    Grad-CAM generates heatmaps and 3D attention surfaces
                    revealing exactly which regions influenced the AI's
                    decision.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ════════════════════════════════════════════
    # TECH STACK
    # ════════════════════════════════════════════
    st.markdown(
        '<div class="section-divider"><span class="section-divider-text">TECH STACK</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tech-grid">
            <div class="tech-badge">🔥 PyTorch</div>
            <div class="tech-badge">🎨 Streamlit</div>
            <div class="tech-badge">📊 Plotly</div>
            <div class="tech-badge">🧠 Grad-CAM</div>
            <div class="tech-badge">🏗️ ResNet50</div>
            <div class="tech-badge">🔲 VGG16</div>
            <div class="tech-badge">🖼️ ImageNet</div>
            <div class="tech-badge">🐍 Python</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ════════════════════════════════════════════
    # FOOTER
    # ════════════════════════════════════════════
    st.markdown(
        """
        <div class="landing-footer">
            Built with 🧠 for Explainable AI Research &nbsp;•&nbsp;
            Powered by <span>PyTorch</span> &amp; <span>Streamlit</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
