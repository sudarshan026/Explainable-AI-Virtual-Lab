"""
xai_generator.py — Grad-CAM Heatmap Generator
===============================================
Uses the ``pytorch-grad-cam`` library to produce both a 2D
colour-overlay image and the raw heatmap array for 3D rendering.
"""

from typing import Tuple

import cv2
import numpy as np
import torch
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from torchvision import transforms


# ──────────────────────────────────────────────
# 1.  Target layer resolver
# ──────────────────────────────────────────────
def get_target_layer(model: torch.nn.Module, model_name: str):
    """Return the final convolutional layer for the given architecture."""
    if model_name == "VGG16":
        return [model.features[-1]]
    # ResNet50 — last bottleneck block
    return [model.layer4[-1]]


# ──────────────────────────────────────────────
# 2.  Preprocessing (matches model_engine.py)
# ──────────────────────────────────────────────
_preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])


def _pil_to_rgb_array(pil_image: Image.Image) -> np.ndarray:
    """Convert PIL image to a 224×224 float32 RGB array scaled [0,1]."""
    img = pil_image.convert("RGB")
    img = img.resize((224, 224), Image.LANCZOS)
    return np.float32(img) / 255.0


# ──────────────────────────────────────────────
# 3.  Grad-CAM generator
# ──────────────────────────────────────────────
def generate_gradcam(
    pil_image: Image.Image,
    model: torch.nn.Module,
    model_name: str,
    target_class_idx: int | None = None,
) -> Tuple[Image.Image, np.ndarray]:
    """Generate Grad-CAM visualisation.

    Parameters
    ----------
    pil_image        : The uploaded PIL image.
    model            : Pre-trained PyTorch model in eval mode.
    model_name       : "ResNet50" or "VGG16".
    target_class_idx : Class index to explain (None → top prediction).

    Returns
    -------
    overlay_pil : PIL.Image  – 224×224 colour overlay image.
    raw_heatmap : np.ndarray – 2D float array (0-1) for 3D rendering.
    """
    # Prepare inputs
    rgb_array = _pil_to_rgb_array(pil_image)
    input_tensor = _preprocess(pil_image.convert("RGB")).unsqueeze(0)

    target_layers = get_target_layer(model, model_name)

    # Define targets
    targets = None
    if target_class_idx is not None:
        targets = [ClassifierOutputTarget(target_class_idx)]

    # Run Grad-CAM
    with GradCAM(model=model, target_layers=target_layers) as cam:
        grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
        raw_heatmap = grayscale_cam[0, :]                     # (H, W) floats 0-1

    # Build colour overlay
    overlay_bgr = show_cam_on_image(rgb_array, raw_heatmap, use_rgb=True)
    overlay_pil = Image.fromarray(overlay_bgr)

    return overlay_pil, raw_heatmap
