"""
ui_styles.py — Glassmorphism CSS & 3D Plotly Surface Builder
============================================================
Provides the futuristic dark-mode CSS injection string and a helper
that converts a 2D Grad-CAM heatmap into an interactive Plotly 3D
topographic surface figure.
"""

import numpy as np
import plotly.graph_objects as go


# ──────────────────────────────────────────────
# 1.  Custom CSS (Glassmorphism + Dark Mode)
# ──────────────────────────────────────────────
def get_custom_css() -> str:
    """Return a <style> block with glassmorphism cards, neon borders,
    custom scrollbar, animated header gradient, and styled widgets."""

    return """
    <style>
    /* ── Import Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Inter:wght@300;400;500;600&display=swap');

    /* ── Root variables ── */
    :root {
        --neon-cyan:   #00f0ff;
        --neon-magenta:#ff00e5;
        --bg-dark:     #0a0a1a;
        --card-bg:     rgba(15, 15, 35, 0.65);
        --card-border: rgba(0, 240, 255, 0.25);
        --text-primary:#e0e0ff;
        --text-muted:  #8888aa;
    }

    /* ── Global background ── */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d0d2b 40%, #120826 70%, #0a0a1a 100%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide default Streamlit branding ── */
    #MainMenu, footer, header {visibility: hidden;}

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: rgba(8, 8, 25, 0.92) !important;
        border-right: 1px solid var(--card-border);
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }

    /* ── Glassmorphism card ── */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.06),
                    inset 0 0 60px rgba(0, 240, 255, 0.03);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(0, 240, 255, 0.45);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.12),
                    inset 0 0 60px rgba(0, 240, 255, 0.05);
    }

    /* ── Neon header ── */
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        font-size: 2.4rem;
        text-align: center;
        background: linear-gradient(90deg, var(--neon-cyan), var(--neon-magenta), var(--neon-cyan));
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        letter-spacing: 2px;
        margin-bottom: 0.2rem;
    }
    @keyframes shimmer {
        to { background-position: 200% center; }
    }

    .subtitle {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.95rem;
        margin-bottom: 1.8rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: 1px;
    }

    /* ── Section labels ── */
    .section-label {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.82rem;
        letter-spacing: 2px;
        color: var(--neon-cyan);
        text-transform: uppercase;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .section-label::before {
        content: '';
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--neon-cyan);
        box-shadow: 0 0 6px var(--neon-cyan);
    }

    /* ── Diagnostic terminal ── */
    .diagnostic-terminal {
        background: rgba(5, 5, 18, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 0, 229, 0.3);
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        margin-top: 1.2rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.92rem;
        line-height: 1.75;
        color: #c8c8e0;
        box-shadow: 0 0 25px rgba(255, 0, 229, 0.07);
        position: relative;
        overflow: hidden;
    }
    .diagnostic-terminal::before {
        content: '> DIAGNOSTIC REPORT';
        display: block;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 3px;
        color: var(--neon-magenta);
        margin-bottom: 1rem;
        text-shadow: 0 0 8px rgba(255, 0, 229, 0.5);
    }
    .diagnostic-terminal .highlight-class {
        color: var(--neon-cyan);
        font-weight: 600;
    }
    .diagnostic-terminal .highlight-conf {
        color: var(--neon-magenta);
        font-weight: 600;
    }

    /* ── Metric cards ── */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-top: 0.6rem;
        flex-wrap: wrap;
    }
    .metric-card {
        flex: 1;
        min-width: 140px;
        background: rgba(15, 15, 35, 0.5);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 12px;
        padding: 0.9rem 1rem;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .metric-card:hover { transform: translateY(-2px); }
    .metric-card .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3rem;
        color: var(--neon-cyan);
    }
    .metric-card .metric-label {
        font-size: 0.72rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    /* ── Custom scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-dark); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--neon-cyan), var(--neon-magenta));
        border-radius: 4px;
    }

    /* ── Streamlit widget overrides ── */
    .stSelectbox > div > div,
    .stSlider > div {
        color: var(--text-primary) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, rgba(0,240,255,0.15), rgba(255,0,229,0.15));
        border: 1px solid var(--card-border);
        color: var(--text-primary);
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.55rem 1.6rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        border-color: var(--neon-cyan);
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.2);
    }

    /* ── Image containers ── */
    .stImage > img {
        border-radius: 12px;
        border: 1px solid rgba(0, 240, 255, 0.15);
    }

    /* ── Sidebar logo area ── */
    .sidebar-brand {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        color: var(--neon-cyan);
        text-align: center;
        padding: 1rem 0 0.5rem 0;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    }
    .sidebar-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--card-border), transparent);
        margin: 0.8rem 0;
    }
    </style>
    """


# ──────────────────────────────────────────────
# 2.  3D Plotly Surface Builder
# ──────────────────────────────────────────────
def build_3d_surface(heatmap_2d: np.ndarray) -> go.Figure:
    """Convert a 2D Grad-CAM heatmap (values 0-1) into a visually
    stunning 3D interactive topographic surface plot."""

    fig = go.Figure(
        data=[
            go.Surface(
                z=heatmap_2d,
                colorscale="Turbo",
                cmin=0,
                cmax=1,
                opacity=0.92,
                contours=dict(
                    z=dict(show=True, usecolormap=True,
                           highlightcolor="cyan", project_z=True, width=1),
                ),
                lighting=dict(
                    ambient=0.4, diffuse=0.6,
                    specular=0.3, roughness=0.5,
                ),
                colorbar=dict(
                    title=dict(text="Activation", font=dict(color="#c8c8e0", size=11)),
                    tickfont=dict(color="#8888aa", size=9),
                    thickness=12,
                    len=0.65,
                    bgcolor="rgba(0,0,0,0)",
                    borderwidth=0,
                ),
            )
        ]
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(
                visible=True,
                title="",
                showticklabels=False,
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(0,240,255,0.08)",
            ),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.0)),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=380,
    )

    return fig
