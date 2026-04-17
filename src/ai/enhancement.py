"""
AI Model Module - Task 2.2 & 2.3
Phase 2: AI Foundation

Super Resolution and Enhancement using lightweight models.
Optimized for CPU inference with ONNX.
"""

import numpy as np
import cv2
from pathlib import Path
from typing import Literal, Optional, Tuple
from loguru import logger


class SuperResolutionModel:
    """
    Lightweight Super Resolution model for CPU.
    
    Supports:
    - Real-ESRGAN (ONNX)
    - SwinIR-style enhancement
    - Bicubic upscaling
    """

    def __init__(self, model_type: Literal["realesrgan", "swinir", "bicubic"] = "bicubic"):
        self.model_type = model_type
        self.onnx_session = None
        self.model_loaded = False

        if model_type == "bicubic":
            self.model_loaded = True
            logger.info("Bicubic upscaling initialized")

    def load(self, model_path: Optional[str] = None):
        """Load ONNX model for inference."""
        if self.model_type == "bicubic":
            self.model_loaded = True
            return True

        try:
            import onnxruntime as ort

            if model_path and Path(model_path).exists():
                providers = ['CPUExecutionProvider']
                self.onnx_session = ort.InferenceSession(model_path, providers=providers)
                self.model_loaded = True
                logger.info(f"ONNX model loaded from {model_path}")
                return True
            else:
                logger.warning(f"Model not found: {model_path}, using bicubic fallback")
                self.model_type = "bicubic"
                self.model_loaded = True
                return False

        except ImportError:
            logger.warning("onnxruntime not available, using bicubic fallback")
            self.model_type = "bicubic"
            self.model_loaded = True
            return False

    def upscale(
        self,
        image: np.ndarray,
        scale: int = 2,
    ) -> np.ndarray:
        """
        Upscale image using selected model.

        Args:
            image: Input RGB image
            scale: Upscaling factor (2 or 4)

        Returns:
            Upscaled image
        """
        if not self.model_loaded:
            raise RuntimeError("Model not loaded. Call load() first.")

        if self.model_type == "bicubic":
            return self._bicubic_upscale(image, scale)

        elif self.model_type == "realesrgan":
            return self._realesrgan_inference(image, scale)

        else:
            logger.warning(f"Unknown model type {self.model_type}, using bicubic")
            return self._bicubic_upscale(image, scale)

    def _bicubic_upscale(self, image: np.ndarray, scale: int) -> np.ndarray:
        """Bicubic interpolation upscaling."""
        h, w = image.shape[:2]
        new_w, new_h = w * scale, h * scale

        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        upscaled = cv2.resize(img_bgr, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        return cv2.cvtColor(upscaled, cv2.COLOR_BGR2RGB)

    def _realesrgan_inference(self, image: np.ndarray, scale: int) -> np.ndarray:
        """Real-ESRGAN ONNX inference."""
        if self.onnx_session is None:
            return self._bicubic_upscale(image, scale)

        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        h, w = img_bgr.shape[:2]
        new_h, new_w = h * scale, w * scale

        img_input = img_bgr.astype(np.float32) / 255.0
        img_input = np.transpose(img_input, (2, 0, 1))
        img_input = np.expand_dims(img_input, axis=0)

        output = self.onnx_session.run(None, {"input": img_input})[0]
        output = np.squeeze(output, axis=0)
        output = np.clip(output.transpose(1, 2, 0), 0, 1)
        output = (output * 255).astype(np.uint8)

        return cv2.cvtColor(output, cv2.COLOR_BGR2RGB)


class ImageEnhancer:
    """
    AI-powered image enhancement using traditional + lightweight AI methods.
    """

    def __init__(self):
        self.sr_model = SuperResolutionModel("bicubic")
        self.sr_model.load()

    def enhance(
        self,
        image: np.ndarray,
        denoise: bool = True,
        sharpen: bool = True,
        upscale: bool = False,
        scale: int = 2,
    ) -> np.ndarray:
        """
        Apply AI-powered enhancement.

        Args:
            image: Input RGB image
            denoise: Apply denoising
            sharpen: Apply sharpening
            upscale: Apply super-resolution
            scale: Upscale factor

        Returns:
            Enhanced image
        """
        result = image.copy()

        if denoise:
            result = self._denoise(result)

        if sharpen:
            result = self._sharpen(result)

        if upscale:
            result = self.sr_model.upscale(result, scale)

        return result

    def _denoise(self, image: np.ndarray) -> np.ndarray:
        """Non-local means denoising."""
        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        denoised = cv2.fastNlMeansDenoisingColored(img_bgr, None, 10, 10, 7, 21)
        return cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB)

    def _sharpen(self, image: np.ndarray) -> np.ndarray:
        """Edge-enhancing sharpening."""
        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpened = cv2.filter2D(img_bgr, -1, kernel)

        result = cv2.addWeighted(img_bgr, 0.7, sharpened, 0.3, 0)

        return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    def analyze_image(self, image: np.ndarray) -> dict:
        """
        Analyze image quality and suggest enhancements.

        Args:
            image: Input RGB image

        Returns:
            Dictionary with analysis and suggestions
        """
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        brightness = gray.mean()
        brightness_score = 50 if 50 < brightness < 200 else 20

        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharpness_score = min(100, laplacian_var / 10)

        hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
        hist_normalized = hist / hist.sum()
        entropy = -np.sum(hist_normalized * np.log2(hist_normalized + 1e-10))
        contrast_score = (entropy / 8.0) * 100

        suggestions = []
        if brightness_score < 40:
            suggestions.append("Increase brightness")
        elif brightness_score > 80:
            suggestions.append("Reduce brightness")
        if sharpness_score < 40:
            suggestions.append("Apply sharpening")
        if contrast_score < 50:
            suggestions.append("Increase contrast")

        return {
            "brightness": brightness_score,
            "sharpness": sharpness_score,
            "contrast": contrast_score,
            "suggestions": suggestions,
        }
