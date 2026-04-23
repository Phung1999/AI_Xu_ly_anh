"""
AnimeGAN - Anime style transformation using ONNX models
Supports AnimeGANv3: Hayao, Shinkai, Paprika styles
"""

import os
import numpy as np
import cv2
from typing import Optional
from loguru import logger

try:
    import onnxruntime as ort
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False
    logger.warning("onnxruntime not installed, anime transformation disabled")


STYLE_MODELS = {
    "Hayao": "AnimeGANv3_Hayao_36.onnx",
    "Shinkai": "AnimeGANv3_Shinkai_37.onnx",
}

MODEL_BASE_URL = "https://github.com/TachibanaYoshino/AnimeGANv3/releases/download/v1.1.0/"

DEFAULT_MODEL_DIR = "models"


class AnimeGAN:
    """
    AnimeGANv3 ONNX inference.
    Transform photos to anime style.
    """
    
    def __init__(
        self,
        style: str = "Hayao",
        model_dir: Optional[str] = None,
        providers: Optional[list] = None
    ):
        if not ONNX_AVAILABLE:
            raise RuntimeError("onnxruntime is required for AnimeGAN")
        
        self.style = style
        self.model_dir = model_dir or DEFAULT_MODEL_DIR
        self.ort_sess = None
        self.providers = providers or ['CPUExecutionProvider']
        
        self._load_model()
    
    def _get_model_path(self) -> str:
        return os.path.join(self.model_dir, STYLE_MODELS[self.style])
    
    def _ensure_model(self):
        model_path = self._get_model_path()
        if os.path.exists(model_path):
            return
        
        os.makedirs(self.model_dir, exist_ok=True)
        url = MODEL_BASE_URL + STYLE_MODELS[self.style]
        
        logger.info(f"Downloading {self.style} model...")
        try:
            import urllib.request
            urllib.request.urlretrieve(url, model_path)
            logger.info(f"Downloaded {self.style} model to {model_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to download model: {e}")
    
    def _load_model(self):
        self._ensure_model()
        model_path = self._get_model_path()
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        self.ort_sess = ort.InferenceSession(model_path, providers=self.providers)
        logger.info(f"Loaded AnimeGAN model: {self.style}")
    
    def _to_32s(self, x: int) -> int:
        """Resize to multiple of 32."""
        return 256 if x < 256 else x - x % 32
    
    def _preprocess(self, image: np.ndarray) -> np.ndarray:
        h, w = image.shape[:2]
        
        new_h = self._to_32s(h)
        new_w = self._to_32s(w)
        
        if new_h != h or new_w != w:
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        if new_h != 256 or new_w != 256:
            image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_LINEAR)
        
        image = image.astype(np.float32) / 127.5 - 1.0
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def _postprocess(self, output: np.ndarray) -> np.ndarray:
        output = output.squeeze(0)
        output = (output + 1.0) * 127.5
        output = np.clip(output, 0, 255).astype(np.uint8)
        return output
    
    def transform(self, image: np.ndarray) -> np.ndarray:
        """
        Transform image to anime style.
        
        Args:
            image: RGB image (numpy array)
            
        Returns:
            Anime-styled RGB image
        """
        if image is None or image.size == 0:
            return image
        
        original_h, original_w = image.shape[:2]
        
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        elif image.shape[2] == 3:
            pass
        else:
            raise ValueError(f"Invalid image shape: {image.shape}")
        
        input_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        input_tensor = self._preprocess(input_image)
        
        output = self.ort_sess.run(None, {self.ort_sess._inputs_meta[0].name: input_tensor})
        
        result = self._postprocess(output[0])
        
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        
        if original_h != 256 or original_w != 256:
            result = cv2.resize(result, (original_w, original_h), interpolation=cv2.INTER_LINEAR)
        
        return result
    
    @staticmethod
    def get_available_styles() -> list:
        return list(STYLE_MODELS.keys())