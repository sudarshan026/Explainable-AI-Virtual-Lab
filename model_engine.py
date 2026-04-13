"""
model_engine.py — PyTorch Model Loading, Caching & Inference
=============================================================
Provides cached model loaders for ResNet50 and VGG16, an image
preprocessing pipeline, and ImageNet inference utilities.
"""

import json
import urllib.request
from typing import Tuple, List

import numpy as np
import streamlit as st
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import models, transforms


# ──────────────────────────────────────────────
# 1.  ImageNet Label Map
# ──────────────────────────────────────────────
_IMAGENET_LABELS_URL = (
    "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/"
    "master/imagenet-simple-labels.json"
)


@st.cache_data(show_spinner=False)
def get_imagenet_labels() -> List[str]:
    """Fetch the 1000-class ImageNet human-readable label list."""
    try:
        with urllib.request.urlopen(_IMAGENET_LABELS_URL, timeout=15) as resp:
            labels = json.loads(resp.read().decode())
        return labels
    except Exception:
        # Fallback: numeric labels
        return [f"class_{i}" for i in range(1000)]


# ──────────────────────────────────────────────
# 2.  Model Loaders (cached)
# ──────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading ResNet50…")
def load_resnet50() -> torch.nn.Module:
    """Load a pre-trained ResNet50 and set to eval mode."""
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model.eval()
    return model


@st.cache_resource(show_spinner="Loading VGG16…")
def load_vgg16() -> torch.nn.Module:
    """Load a pre-trained VGG16 and set to eval mode."""
    model = models.vgg16(weights=models.VGG16_Weights.DEFAULT)
    model.eval()
    return model


def get_model(model_name: str) -> torch.nn.Module:
    """Dispatcher — return the requested cached model."""
    if model_name == "VGG16":
        return load_vgg16()
    return load_resnet50()


# ──────────────────────────────────────────────
# 3.  Image Preprocessing
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


def preprocess_image(pil_image: Image.Image) -> torch.Tensor:
    """Convert a PIL image to a (1, 3, 224, 224) ImageNet-ready tensor."""
    img = pil_image.convert("RGB")
    tensor = _preprocess(img)
    return tensor.unsqueeze(0)  # add batch dim


# ──────────────────────────────────────────────
# 4.  Inference
# ──────────────────────────────────────────────
def run_inference(
    model: torch.nn.Module,
    input_tensor: torch.Tensor,
    top_k: int = 5,
) -> Tuple[List[str], List[float], List[int]]:
    """Run forward pass and return top-k (class_names, probs, indices).

    Returns
    -------
    class_names : list[str]   – human-readable class names
    probs       : list[float] – confidence percentages (0-100)
    indices     : list[int]   – raw class indices
    """
    labels = get_imagenet_labels()

    with torch.no_grad():
        logits = model(input_tensor)
        probabilities = F.softmax(logits, dim=1)

    top_probs, top_indices = torch.topk(probabilities, top_k, dim=1)
    top_probs = top_probs.squeeze().cpu().numpy()
    top_indices = top_indices.squeeze().cpu().numpy()

    # handle single-prediction edge case
    if top_probs.ndim == 0:
        top_probs = np.array([top_probs.item()])
        top_indices = np.array([top_indices.item()])

    class_names = [labels[int(idx)] for idx in top_indices]
    probs_pct = [round(float(p) * 100, 2) for p in top_probs]

    return class_names, probs_pct, [int(i) for i in top_indices]
