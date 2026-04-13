"""
insight_generator.py — XAI Diagnostic Text Report Generator
=============================================================
Produces a dynamic, HTML-formatted diagnostic report that explains
the Grad-CAM visualisation in accessible yet academic language.
"""

import textwrap

import numpy as np


def generate_report(
    class_name: str,
    confidence: float,
    raw_heatmap: np.ndarray,
    model_name: str,
) -> str:
    """Build an HTML-formatted diagnostic report.

    Parameters
    ----------
    class_name   : Predicted class label (human-readable).
    confidence   : Confidence percentage (0-100).
    raw_heatmap  : 2D numpy array (0-1) from Grad-CAM.
    model_name   : "ResNet50" or "VGG16".

    Returns
    -------
    report_html : str – Styled HTML string for Streamlit markdown.
    """

    # ── Heatmap statistics ──
    peak_activation = float(np.max(raw_heatmap))
    mean_activation = float(np.mean(raw_heatmap))
    hot_pixel_ratio = float(np.mean(raw_heatmap > 0.5)) * 100  # % of pixels above 0.5

    # ── Confidence interpretation ──
    if confidence >= 90:
        conf_interp = "extremely high certainty"
        conf_emoji = "🟢"
    elif confidence >= 70:
        conf_interp = "high confidence"
        conf_emoji = "🟢"
    elif confidence >= 50:
        conf_interp = "moderate confidence"
        conf_emoji = "🟡"
    else:
        conf_interp = "low confidence — consider alternative classes"
        conf_emoji = "🔴"

    # ── Attention spread interpretation ──
    if hot_pixel_ratio > 40:
        spread_note = (
            "The attention is <b>broadly distributed</b> across the image, "
            "suggesting the model uses global context (e.g., shape, texture, "
            "scene composition) rather than a single localised feature."
        )
    elif hot_pixel_ratio > 15:
        spread_note = (
            "The attention shows a <b>moderately focused</b> pattern, "
            "indicating the model is anchoring its decision on a distinct "
            "region while also incorporating surrounding context."
        )
    else:
        spread_note = (
            "The attention is <b>highly concentrated</b> in a small spatial "
            "region, meaning the model relies on a very specific visual cue — "
            "verify that this aligns with the subject and not an artefact."
        )

    # ── Architecture-specific note ──
    if model_name == "ResNet50":
        arch_note = (
            "ResNet50's skip connections allow gradient signals to flow "
            "through 50 layers without vanishing, producing sharper and "
            "more spatially accurate Grad-CAM heatmaps."
        )
    else:
        arch_note = (
            "VGG16's uniform sequential convolution stack tends to produce "
            "smoother, more diffuse attention maps compared to residual "
            "architectures."
        )

    # ── Assemble report ──
    report = textwrap.dedent(f"""\
    <p>
        {conf_emoji} The model is
        <span class="highlight-conf">{confidence:.1f}%</span> sure this is a
        <span class="highlight-class">"{class_name}"</span>
        — classified with <b>{conf_interp}</b>.
    </p>

    <p>
        The red/yellow "mountain peaks" visible in the <b>3D Neural Attention
        Matrix</b> represent the highest gradient-weighted activations
        extracted from the <b>final convolutional layer</b> of {model_name}.
        These peaks indicate the spatial regions where the network
        concentrated its discriminative attention during classification.
    </p>

    <p>{spread_note}</p>

    <p>
        <b>Quantitative Metrics:</b> Peak activation =
        <span class="highlight-conf">{peak_activation:.3f}</span>, mean
        activation = <span class="highlight-conf">{mean_activation:.3f}</span>,
        hot-pixel coverage (&gt;0.5) =
        <span class="highlight-conf">{hot_pixel_ratio:.1f}%</span> of the
        spatial map.
    </p>

    <p><b>Architecture Note:</b> {arch_note}</p>

    <p style="color: #8888aa; font-size: 0.82rem; margin-top: 0.8rem;">
        💡 <i>Verify that the hotspots align with the main subject of the
        image and not the background.  Misaligned attention may indicate
        dataset bias or spurious correlations learned during training
        (e.g., a "Clever Hans" effect).</i>
    </p>
    """).strip()
    return report
