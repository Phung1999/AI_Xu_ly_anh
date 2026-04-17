"""
IQA Module - Image Quality Assessment
Phase 2 - Task 2.1

Implements automated image quality scoring:
- PSNR (Peak Signal-to-Noise Ratio)
- SSIM (Structural Similarity Index)
- CQE (Color Image Quality Estimator)
- EME (Entropy-based Measure of Enhancement)
"""

import numpy as np
import cv2
from typing import Dict, Tuple, Optional
from skimage.metrics import structural_similarity


class ImageQualityAssessment:
    """
    Image Quality Assessment metrics for evaluating enhancement results.
    """

    def __init__(self):
        self.metrics = {}

    def evaluate(
        self,
        original: np.ndarray,
        enhanced: np.ndarray,
        reference: Optional[np.ndarray] = None,
    ) -> Dict[str, float]:
        """
        Evaluate image quality with multiple metrics.

        Args:
            original: Original (before enhancement) image
            enhanced: Enhanced (after enhancement) image
            reference: Optional reference image for comparison

        Returns:
            Dict with quality scores
        """
        results = {}

        results["psnr"] = self.calculate_psnr(original, enhanced)
        results["ssim"] = self.calculate_ssim(original, enhanced)
        results["cqe"] = self.calculate_cqe(enhanced)
        results["eme"] = self.calculate_eme(enhanced)

        if reference is not None:
            results["psnr_ref"] = self.calculate_psnr(reference, enhanced)
            results["ssim_ref"] = self.calculate_ssim(reference, enhanced)

        self.metrics = results
        return results

    def calculate_psnr(
        self,
        img1: np.ndarray,
        img2: np.ndarray,
        max_value: float = 255.0,
    ) -> float:
        """
        Calculate Peak Signal-to-Noise Ratio.

        Higher is better. Typical values:
        - > 40 dB: Excellent
        - 30-40 dB: Good
        - 20-30 dB: Fair
        - < 20 dB: Poor

        Args:
            img1: First image
            img2: Second image
            max_value: Maximum pixel value (255 for uint8)

        Returns:
            PSNR value in dB
        """
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        mse = np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)

        if mse == 0:
            return float("inf")

        psnr = 20 * np.log10(max_value / np.sqrt(mse))
        return float(psnr)

    def calculate_ssim(
        self,
        img1: np.ndarray,
        img2: np.ndarray,
        multichannel: bool = True,
    ) -> float:
        """
        Calculate Structural Similarity Index.

        Range: -1 to 1, higher is better.
        - 1.0: Identical images
        - 0.9-0.99: Very similar
        - 0.7-0.9: Similar
        - < 0.7: Dissimilar

        Args:
            img1: First image
            img2: Second image
            multichannel: Treat as color image

        Returns:
            SSIM value
        """
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        if len(img1.shape) == 2:
            multichannel = False

        if multichannel:
            img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
            img2_gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        else:
            img1_gray = img1
            img2_gray = img2

        ssim_value = structural_similarity(
            img1_gray, img2_gray, data_range=255
        )

        return float(ssim_value)

    def calculate_cqe(self, image: np.ndarray) -> float:
        """
        Calculate Color Image Quality Estimator.

        Based on 3 factors:
        - Colorfulness: Saturation of colors
        - Sharpness: Edge strength
        - Contrast: Dynamic range

        Range: 0-100, higher is better.

        Args:
            image: Input image (RGB)

        Returns:
            CQE score
        """
        img_float = image.astype(np.float32) / 255.0

        colorfulness = self._measure_colorfulness(img_float)
        sharpness = self._measure_sharpness(image)
        contrast = self._measure_contrast(img_float)

        cqe = (colorfulness * 0.3 + sharpness * 0.4 + contrast * 0.3) * 100

        return float(np.clip(cqe, 0, 100))

    def _measure_colorfulness(self, image: np.float32) -> float:
        """Measure colorfulness (color saturation)."""
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

        rg = r - g
        yb = 0.5 * (r + g) - b

        std_rg = np.std(rg)
        std_yb = np.std(yb)
        mean_rg = np.mean(rg)
        mean_yb = np.mean(yb)

        colorfulness = np.sqrt(std_rg ** 2 + std_yb ** 2) + 0.3 * np.sqrt(
            mean_rg ** 2 + mean_yb ** 2
        )

        return float(np.clip(colorfulness / 0.33, 0, 1))

    def _measure_sharpness(self, image: np.ndarray) -> float:
        """Measure sharpness using Laplacian variance."""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()

        sharpness = np.clip(variance / 1000.0, 0, 1)

        return float(sharpness)

    def _measure_contrast(self, image: np.ndarray) -> float:
        """Measure contrast using RMS contrast."""
        gray = cv2.cvtColor(
            (image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY
        ).astype(np.float32) / 255.0

        contrast = np.std(gray)

        return float(np.clip(contrast / 0.5, 0, 1))

    def calculate_eme(
        self,
        image: np.ndarray,
        block_size: int = 8,
    ) -> float:
        """
        Calculate Entropy-based Measure of Enhancement.

        Based on human visual system (HVS) characteristics.
        Higher values indicate more enhancement.

        Args:
            image: Input image (grayscale or RGB)
            block_size: Size of blocks for local analysis

        Returns:
            EME score
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image

        h, w = gray.shape
        eme_sum = 0.0
        count = 0

        for i in range(0, h - block_size + 1, block_size):
            for j in range(0, w - block_size + 1, block_size):
                block = gray[i : i + block_size, j : j + block_size]

                block_min = block.min()
                block_max = block.max()

                if block_max > 0:
                    ratio = block_max / (block_min + 1e-10)
                    if ratio > 1:
                        eme = 20 * np.log10(ratio)
                        eme_sum += eme
                        count += 1

        if count == 0:
            return 0.0

        return float(eme_sum / count)

    def calculate_brisque(
        self,
        image: np.ndarray,
    ) -> float:
        """
        Calculate BRISQUE-like score (Blind/Referenceless Image Spatial Quality Evaluator).

        Simplified version using natural scene statistics.
        Lower is better (0 = best quality).

        Args:
            image: Input image

        Returns:
            BRISQUE-like score
        """
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.float32)

        mu = cv2.GaussianBlur(gray, (7, 7), 7 / 6)
        mu_sq = mu ** 2
        sigma = np.sqrt(np.abs(cv2.GaussianBlur(gray ** 2, (7, 7), 7 / 6) - mu_sq))

        struct_sim = (2 * mu * (mu + 1) + 1) / (
            2 * mu_sq + 2 * (mu + 1) + sigma + 1
        )

        score = 1 - np.mean(struct_sim)

        return float(np.clip(score * 100, 0, 100))

    def get_summary(self, scores: Dict[str, float]) -> str:
        """
        Get human-readable summary of quality scores.

        Args:
            scores: Dictionary of quality scores

        Returns:
            Formatted summary string
        """
        summary = []
        summary.append("=" * 40)
        summary.append("IMAGE QUALITY ASSESSMENT SUMMARY")
        summary.append("=" * 40)

        if "psnr" in scores:
            psnr = scores["psnr"]
            rating = "Excellent" if psnr > 40 else "Good" if psnr > 30 else "Fair" if psnr > 20 else "Poor"
            summary.append(f"PSNR:  {psnr:.2f} dB ({rating})")

        if "ssim" in scores:
            ssim = scores["ssim"]
            rating = "Identical" if ssim > 0.99 else "Very Similar" if ssim > 0.9 else "Similar" if ssim > 0.7 else "Dissimilar"
            summary.append(f"SSIM:  {ssim:.4f} ({rating})")

        if "cqe" in scores:
            cqe = scores["cqe"]
            rating = "Excellent" if cqe > 80 else "Good" if cqe > 60 else "Fair" if cqe > 40 else "Poor"
            summary.append(f"CQE:   {cqe:.2f}/100 ({rating})")

        if "eme" in scores:
            summary.append(f"EME:   {scores['eme']:.2f}")

        if "psnr_ref" in scores:
            summary.append(f"PSNR-Ref: {scores['psnr_ref']:.2f} dB")

        if "ssim_ref" in scores:
            summary.append(f"SSIM-Ref: {scores['ssim_ref']:.4f}")

        summary.append("=" * 40)

        return "\n".join(summary)
