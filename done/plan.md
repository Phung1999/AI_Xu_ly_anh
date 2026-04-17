TÀI LIỆU KỸ THUẬT: HỆ THỐNG NÂNG CẤP VÀ CHỈNH SỬA ẢNH CHUYÊN NGHIỆP (PYTHON-BASED)
1. Mục tiêu và Thư viện yêu cầu
Xây dựng ứng dụng xử lý ảnh tự động và nâng cao, tích hợp các thuật toán mô phỏng Photoshop và mô hình AI hiện đại.
Ngôn ngữ: Python.
Thư viện chính: OpenCV (cv2), NumPy, Keras/TensorFlow (cho AI Deep Learning)
.
Môi trường: Hỗ trợ CUDA/CuDNN để tăng tốc xử lý bằng GPU
.
2. Quy trình xử lý hậu kỳ (Workflow)
Yêu cầu AI lập trình theo đúng thứ tự tiêu chuẩn của studio chuyên nghiệp
:
Cân bằng trắng (White Balance): Điều chỉnh Temperature (nhiệt độ màu) và Tint (sắc độ)
.
Độ phơi sáng (Exposure): Khôi phục chi tiết vùng Highlight và Shadow bằng Levels/Curves
.
Giảm nhiễu (Noise Reduction): Thực hiện trước khi tăng nét để tránh làm nổi hạt nhiễu
.
Sửa lỗi ống kính: Khử méo hình, Vignetting và quang sai màu (Chromatic Aberration)
.
Tăng chi tiết & Nâng nét (Detail/Sharpening): Sử dụng các bộ lọc chuyên sâu
.
3. Các module thuật toán mô phỏng Photoshop
A. Module Điều chỉnh Levels (Photoshop Levels Clone)
Logic: Tính toán bảng tra cứu (Lookup Table - LUT) dựa trên 3 điểm: Shadow, Midtone (Gamma), và Highlight
.
Thuật toán Gamma: Midtone 128 tương đương Gamma = 1.0; vùng 0-128 áp dụng Gamma 9.99 - 1.0; vùng 128-255 áp dụng Gamma 1.0 - 0.01
.
Xử lý: Áp dụng hiệu chỉnh tuyến tính kết hợp nội suy phi tuyến nếu Midtone < 128
.
B. Module Làm nét High Pass (High Pass Filter)
Công thức: hpf = original_img - GaussianBlur(img) + 127
.
Chế độ hòa trộn: Trộn lớp High Pass này với ảnh gốc bằng chế độ Soft Light hoặc Overlay để làm nổi bật các cạnh chi tiết mà không làm thay đổi màu sắc tổng thể
.
C. Module Tăng tương phản thông minh (CLAHE + Dual Gamma)
CLAHE: Chia nhỏ ảnh thành các khối (blocks), thực hiện cân bằng biểu đồ nội bộ để tăng tương phản cục bộ mà không gây nhiễu
.
Dual Gamma Correction: Sử dụng hai lần hiệu chỉnh Gamma (γ1,γ2) để vừa tăng độ sáng vùng tối vừa bảo vệ vùng sáng không bị cháy sáng (wash-out)
.
4. Tích hợp AI Deep Learning để nâng cấp ảnh
A. Siêu độ phân giải (Super-Resolution - EDSR)
Kiến trúc: Sử dụng mô hình Enhanced Deep Super-Resolution (EDSR)
.
Đặc điểm kỹ thuật: Loại bỏ các lớp Batch Normalization để tiết kiệm 40% bộ nhớ GPU và sử dụng lớp Pixel Shuffle để sắp xếp lại tensor theo không gian, giúp phóng to ảnh (upscaling 4x) mà vẫn giữ được độ sắc nét cực cao
.
B. Khử nhòe mù bằng tự khuếch tán (DeblurSDI)
Logic: Sử dụng khung làm việc Self-diffusion không cần huấn luyện trước (zero-shot)
.
Cơ chế: Khôi phục ảnh sắc nét từ nhiễu thông qua quá trình khuếch tán ngược lặp đi lặp lại, đồng thời ước tính hàm nhòe (PSF) của ống kính
.
5. Module AI đánh giá chất lượng (IQA - Image Quality Assessment)
Yêu cầu AI viết code tự động "chấm điểm" ảnh trước và sau khi xử lý bằng các chỉ số
:
PSNR & SSIM: Đo lường độ tương đồng cấu trúc và mức nhiễu so với ảnh gốc (nếu có)
.
Chỉ số CQE (Color Image Quality): Đánh giá dựa trên 3 yếu tố: độ rực rỡ màu sắc (colorfulness), độ sắc nét (sharpness) và độ tương phản (contrast)
.
Chỉ số EME: Đo lường mức độ tăng cường hình ảnh phù hợp với hệ thống thị giác con người (HVS)
.
6. Ghi chú triển khai cho AI
Giao diện thân thiện với người dùng 

Sử dụng model nhẹ , free để đánh giá bức ảnh trước khi sửa 

Tính tùy biến: Tạo các thanh trượt (Trackbars) để người dùng điều chỉnh Shadow, Midtone, Highlight và độ sắc nét theo thời gian thực
.
Xử lý hàng loạt: Thiết kế ứng dụng theo vòng lặp để có thể edit hàng ngàn bức ảnh trong thư mục chỉ bằng một lần chạy
.
Chế độ không phá hủy (Non-destructive): Sử dụng các lớp điều chỉnh (Adjustment Layers) hoặc tạo bản sao trước khi xử lý để giữ nguyên dữ liệu gốc
.

---

## ✅ IMPLEMENTATION STATUS

### Completed Features (2026-04-17)

| Feature | Status | Implementation |
|----------|--------|----------------|
| White Balance | ✅ Done | `src/modules/white_balance.py` |
| Levels Adjustment | ✅ Done | `src/modules/levels.py` |
| High Pass Sharpening | ✅ Done | `src/modules/sharpening.py` |
| CLAHE | ✅ Done | `src/modules/clahe.py` |
| Super Resolution | ✅ Done | `src/ai/enhancement.py` |
| Auto Enhancement | ✅ Done | `src/ai/auto_enhance.py` |
| IQA Metrics | ✅ Done | `src/modules/iqa.py` |
| Batch Processing | ✅ Done | `src/modules/pipeline.py`, `queue.py` |
| PyQt6 UI (Fullscreen) | ✅ Done | `src/ui/main_window.py` (~900 lines) |
| Multi-language | ✅ Done | `src/ui/i18n.py` (EN/VI + bilingual) |
| Drag & Drop | ✅ Done | All viewers |
| Vietnamese Path | ✅ Done | `np.fromfile()` |
| Color Reference / Color Grading | ✅ Done | `src/modules/color_analyzer.py` |
| Notifications | ✅ Done | Popup dialogs |

### Test Results
- **113/113 tests PASSED**

### To Run
```bash
run.bat                      # GUI (Fullscreen)
run_cli.bat input/ -o output/ --preset auto  # CLI
```