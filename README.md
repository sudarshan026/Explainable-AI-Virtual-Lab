# 🧠 Explainable AI (XAI) Virtual Lab

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python) ![PyTorch](https://img.shields.io/badge/PyTorch-deep_learning-ee4c2c?style=for-the-badge&logo=pytorch) ![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-ff4b4b?style=for-the-badge&logo=streamlit)

## 📖 Overview

### What is this? (In Plain English)
Imagine an AI as a master detective solving a case. When the detective points to a suspect and says "That's the culprit!", you might logically ask, *"How do you know? What exact clues led you to that conclusion?"*

Deep Neural Networks (modern AI) are incredibly smart at classifying images, but they are often "black boxes"—meaning they give us an answer, but they don't tell us *how* they got there. 

The **XAI Virtual Lab** changes that. It acts like an X-ray scanner for AI. When you upload an image and the AI guesses what it is, this tool generates a "heat map" to show you exactly *where* the AI was looking to make its decision. If the AI sees a "Dog", the heatmap will glow brightest right over the dog's face, proving it learned the right real-world features (and wasn't just predicting "dog" based on a green grassy background).

### For the Technical User
This project is an **Explainable AI (XAI) Research Platform** built with **PyTorch** and **Streamlit**. It applies gradient-weighted class activation mapping (**Grad-CAM**) to modern Convolutional Neural Networks (ResNet50 and VGG16) to visualize their spatial attention landscapes. By intercepting the gradients flowing into the final convolutional layers during the backward pass, the lab translates obscure neural activations into interactive 2D heatmaps and 3D topographic surfaces.

---

## ✨ Key Features

- 🌌 **Incredible Visual UI**: A state-of-the-art glassmorphism, cyberpunk-inspired glowing interface with CSS-animated particles, scanlines, and floating holographic elements.
- 🎯 **Grad-CAM Explanations**: Generate highly accurate heatmaps indicating neural attention on a given image.
- 🏔️ **3D Terrain Matrix**: Explore the AI's internal attention landscape as a fully interactive 3D topograph powered by Plotly.
- 🔄 **Multi-Architecture**: Swap between **ResNet50** (sharp, exact residual activations) and **VGG16** (smooth, sequential activations) in real-time.
- 📊 **Automated Diagnostic Reports**: The engine computes peak activations, spatial spread, and confidence heuristics to give an automated "analyst report" on the AI's reasoning.

---

## 🚀 How to Run It

### 📦 Prerequisites
You will need **Python** installed on your computer.

### 🛠️ Installation Steps

1. **Download/Clone the Project Folder** open your terminal or command prompt, and navigate to the project folder:
   ```bash
   cd path/to/your/project
   ```

2. **Create a Virtual Environment** (Optional, but highly recommended to keep your computer's Python environment clean):
   * On **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * On **Mac/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   Run the following command to download the required AI libraries (PyTorch, Streamlit, etc.):
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Lab**:
   Start the application by running:
   ```bash
   streamlit run app.py
   ```
   *Your default web browser will automatically open to `http://localhost:8501`. Have fun exploring the Black Box!*

---

## 📂 Project Architecture

A quick tour of the engine's internal codebase structure:

- `app.py`: The main entry point. Handles the UI routing between the landing page and the active lab workspace.
- `landing_page.py`: Powers the visually stunning homepage, combining complex CSS micro-animations, glitch effects, layered particles, and HTML structures.
- `model_engine.py`: The PyTorch backbone. Responsible for fetching the pre-trained weights (ResNet50/VGG16), preprocessing tensors, fetching ImageNet maps, and handling Inference thresholds.
- `xai_generator.py`: Generates the Grad-CAM payload. Modifies and extracts from the target layers and computes the visual 2D matrix array overlay.
- `insight_generator.py`: Mathematical heuristics that read the Grad-CAM pixel spread to dynamically generate contextual, HTML-styled AI Diagnostic Text Reports.
- `ui_styles.py`: Contains the global Glassmorphism CSS themes and the function to render the 2D array into a Plotly 3D Figure.

---

## 💻 Tech Stack
- **Frontend Engine**: [Streamlit](https://streamlit.io/)
- **Styling**: Vanilla CSS, Keyframe Animation & HTML Injections
- **AI Core / Backend**: [PyTorch](https://pytorch.org/) & [TorchVision](https://pytorch.org/vision/stable/index.html)
- **Interpretability Logic**: [pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam)
- **Data Rendering**: [Plotly Python](https://plotly.com/python/) & OpenCV
