"""
app.py — Explainable AI (XAI) Virtual Lab
==========================================
Main Streamlit entry-point.  Routes between the landing page and the
analysis lab, injects Glassmorphism CSS, and orchestrates the
3-column analysis layout with a full-width diagnostic terminal below.
"""

import streamlit as st
from PIL import Image

# ── Local modules ──
from ui_styles import get_custom_css, build_3d_surface
from model_engine import get_model, preprocess_image, run_inference
from xai_generator import generate_gradcam
from insight_generator import generate_report
from landing_page import render_landing

# ──────────────────────────────────────────────
# Page config (must be first Streamlit call)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="XAI Virtual Lab",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Session State
# ──────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "landing"


# ──────────────────────────────────────────────
# Page Routing
# ──────────────────────────────────────────────
if st.session_state.page == "landing":
    render_landing()

else:
    # ══════════════════════════════════════════
    #  LAB PAGE  (existing functionality)
    # ══════════════════════════════════════════

    # ── Inject Glassmorphism CSS ──
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # Sidebar
    # ──────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🧠 XAI LAB</div>', unsafe_allow_html=True)
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        # ── Back to Home ──
        if st.button("← Back to Home"):
            st.session_state.page = "landing"
            st.rerun()

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        model_name = st.selectbox(
            "Select Model Architecture",
            ["ResNet50", "VGG16"],
            index=0,
            help="Choose the pre-trained CNN backbone for classification.",
        )

        confidence_threshold = st.slider(
            "Confidence Threshold (%)",
            min_value=0,
            max_value=100,
            value=20,
            step=5,
            help="Minimum confidence to display a prediction.",
        )

        top_k = st.slider(
            "Top-K Predictions",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of top predictions to display.",
        )

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload Image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload an image to analyse with Grad-CAM.",
        )

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size:0.75rem; color:#8888aa; line-height:1.6;">
            <b>About</b><br>
            This lab uses <b>Grad-CAM</b> (Gradient-weighted Class Activation
            Mapping) to visualise which spatial regions a Deep Neural Network
            attends to when classifying an image.<br><br>
            Built with PyTorch, Streamlit & Plotly.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ──────────────────────────────────────────
    # Header
    # ──────────────────────────────────────────
    st.markdown(
        '<div class="neon-title">Explainable AI Virtual Lab</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitle">Upload an image → Classify with a Deep Neural Network → Visualise attention with Grad-CAM</div>',
        unsafe_allow_html=True,
    )

    # ──────────────────────────────────────────
    # Main logic
    # ──────────────────────────────────────────
    if uploaded_file is not None:
        pil_image = Image.open(uploaded_file).convert("RGB")

        # ── Load model ──
        with st.spinner(f"Loading {model_name}…"):
            model = get_model(model_name)

        # ── Inference ──
        input_tensor = preprocess_image(pil_image)
        class_names, probs, indices = run_inference(model, input_tensor, top_k=top_k)

        # ── Filter by confidence ──
        filtered = [
            (cn, p, idx) for cn, p, idx in zip(class_names, probs, indices)
            if p >= confidence_threshold
        ]
        if not filtered:
            filtered = [(class_names[0], probs[0], indices[0])]

        top_class = filtered[0][0]
        top_conf = filtered[0][1]
        top_idx = filtered[0][2]

        # ── Grad-CAM ──
        with st.spinner("Generating Grad-CAM…"):
            overlay_img, raw_heatmap = generate_gradcam(
                pil_image, model, model_name, target_class_idx=top_idx
            )

        # ──────────────────────────────────────
        # Top Row: 3-Column Layout
        # ──────────────────────────────────────
        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            st.markdown('<div class="section-label">Input Image</div>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.image(pil_image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-label">Grad-CAM Overlay</div>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.image(overlay_img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="section-label">3D Neural Attention Matrix</div>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig_3d = build_3d_surface(raw_heatmap)
            st.plotly_chart(fig_3d, use_container_width=True, config={"displayModeBar": True})
            st.markdown('</div>', unsafe_allow_html=True)

        # ──────────────────────────────────────
        # Prediction Metrics Row
        # ──────────────────────────────────────
        st.markdown('<div class="section-label" style="margin-top:1rem;">Prediction Results</div>', unsafe_allow_html=True)

        metric_cards_html = '<div class="metric-row">'
        for cn, p, _ in filtered:
            metric_cards_html += f"""
            <div class="metric-card">
                <div class="metric-value">{p:.1f}%</div>
                <div class="metric-label">{cn}</div>
            </div>
            """
        metric_cards_html += '</div>'
        st.markdown(metric_cards_html, unsafe_allow_html=True)

        # ──────────────────────────────────────
        # Bottom Row: Diagnostic Terminal
        # ──────────────────────────────────────
        report_html = generate_report(top_class, top_conf, raw_heatmap, model_name)
        st.markdown(
            f'<div class="diagnostic-terminal">{report_html}</div>',
            unsafe_allow_html=True,
        )

    else:
        # ── Empty state ──
        st.markdown(
            """
            <div class="glass-card" style="text-align:center; padding:4rem 2rem;">
                <div style="font-size:3.5rem; margin-bottom:1rem;">🔬</div>
                <div style="font-family:'Orbitron',sans-serif; font-size:1.1rem;
                            color:#00f0ff; margin-bottom:0.6rem;">
                    Awaiting Input
                </div>
                <div style="color:#8888aa; font-size:0.88rem; max-width:420px;
                            margin:0 auto; line-height:1.7;">
                    Upload an image in the sidebar to begin analysis.
                    The lab will classify the image using a pre-trained Deep
                    Neural Network and generate an interactive Grad-CAM
                    explanation of the model's decision.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
