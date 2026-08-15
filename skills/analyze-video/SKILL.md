---
name: analyze-video
description: Kỹ năng phân tích video short-form (Instagram Reels, TikTok, YouTube Shorts, bài đăng Instagram Carousel đa video, file MP4) tự động và toàn diện. Tự động nhận diện bài đơn hay Carousel, tải trọn bộ video, bóc tách phân cảnh (OpenCV Shot Detection), trích xuất Keyframes (Start-Mid-End), ghép ảnh so sánh chuyển cảnh (Transitions), bóc tách âm thanh/kịch bản thoại tiếng Việt (nếu là video đơn) hoặc phân tích nhịp thị giác Carousel (nếu là album nhiều slide không lời thoại), xuất Báo cáo Đạo diễn (Director Breakdown) chuẩn Headless Chrome Engine không lỗi font tiếng Việt, tự động đóng gói toàn bộ thư mục dự án và tải lên Google Drive (Work/AI_Video_Analysis) qua Rclone, trả về link Google Drive xem trực tiếp.
---

# KỸ NĂNG PHÂN TÍCH VIDEO & CAROUSEL SERIES CHUYÊN SÂU (ANALYZE VIDEO SKILL)

Khi người dùng gửi một đường link video (Instagram Reels, TikTok, YouTube Shorts, bài đăng Instagram Carousel đa video) hoặc tệp video MP4 cục bộ, Agent BẮT BUỘC thực hiện quy trình tự động sau:

## 1. TỰ ĐỘNG NHẬN DIỆN & TẢI TOÀN BỘ TÀI NGUYÊN (INGESTION)
- Sử dụng `yt-dlp` quét đường link:
  - **Trường hợp 1 (Video đơn lẻ - Reel / TikTok / Shorts)**: Tải video gốc `.mp4` và tách file âm thanh `.mp3`.
  - **Trường hợp 2 (Bài đăng Carousel đa video / Album)**: Tự động tải TOÀN BỘ tất cả các slide video (`slide_01.mp4`, `slide_02.mp4`,...) vào thư mục `carousel_slides/`.
- Tự động tạo thư mục đóng gói chuẩn hóa:
  `Work/AI_Video_Analysis/IG_@[Tên_Kênh]_[Mã_Bài]_[Phân_Loại]/`

## 2. PHÂN TÍCH SHOTS & TRÍCH XUẤT KEYFRAME (OPENCV)
- **Với Video đơn lẻ**:
  - Chạy thuật toán OpenCV HSV Histogram phát hiện toàn bộ các điểm cắt cảnh (Scene Cuts).
  - Trích xuất 3 ảnh Keyframe cho mỗi Shot (`shot_XX_start.jpg`, `shot_XX_mid.jpg`, `shot_XX_end.jpg`).
  - Tạo ảnh ghép so sánh chuyển cảnh `trans_XX_to_YY.jpg`.
- **Với Album Carousel (Nhiều Video)**:
  - Phân tích chi tiết từng Slide Video: độ phân giải, thời lượng, vai trò giữ chân trong chuỗi (Hook ➔ Movement ➔ Detail ➔ Fast-cut ➔ Context ➔ CTA).
  - Trích xuất các khung hình đại diện của từng Slide (`slide_XX_mid.jpg`, `slide_XX_start.jpg`, `slide_XX_end.jpg`).

## 3. ĐỒNG BỘ HÌNH ẢNH VÀO THƯ MỤC ARTIFACTS
- Sao chép toàn bộ ảnh trích xuất sang thư mục Artifacts của phiên làm việc:
  `<appDataDir>/brain/<conversation-id>/extracted_shots/`
- Mọi hình ảnh nhúng vào báo cáo chat đều sử dụng cú pháp: `![Tên ảnh](file://<appDataDir>/brain/<conversation-id>/extracted_shots/...)`.

## 4. XUẤT BẢN BÁO CÁO PHÂN TÍCH PDF QUA CHROME HEADLESS (CHỐNG LỖI FONT 100%)
- **BẮT BUỘC**: Tuyệt đối không dùng `xhtml2pdf` cũ. Luôn luôn sử dụng **Headless Chrome / Edge CLI** (`--headless=new --disable-gpu --print-to-pdf="..." --no-pdf-header-footer`) để render từ HTML sang PDF.
- **BẮT BUỘC nhúng font chuẩn tiếng Việt**: Trong HTML luôn có thẻ `<meta charset="UTF-8">` và `@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap')`.
- **Với Video đơn lẻ**: Phân tích cỡ cảnh, góc máy, kỹ thuật Mồi (Out) / Nối (In), ánh sáng, kèm 2 phương án kịch bản thoại mới theo chủ đề yêu cầu.
- **Với Album Carousel**: Phân tích nhịp điệu thị giác (Visual Rhythm), bố cục khung hình 4:5/9:16, động tác máy, nghệ thuật tạo điểm dừng thị giác (Stopping Power), không cần kịch bản thoại nếu là video thuần âm nhạc/lifestyle.

## 5. ĐÓNG GÓI THƯ MỤC DỰ ÁN & TỰ ĐỘNG UPLOAD LÊN GOOGLE DRIVE
- Đóng gói toàn bộ tài nguyên:
  ```
  Work/AI_Video_Analysis/[Tên_Thư_Mục_Package]/
  ├── carousel_slides/ (hoặc video gốc .mp4)
  ├── Bao_Cao_Phan_Tich.pdf
  ├── Bao_Cao_Phan_Tich.html
  ├── carousel_info.json (hoặc shot_info.json)
  └── extracted_shots/ (Chứa toàn bộ Keyframes & Transitions)
  ```
- Chạy lệnh Rclone tự động đồng bộ lên Google Drive:
  `rclone copy "D:\...\output_packages\..." "gdrive:Work/AI_Video_Analysis/..." -v`
- Lấy đường link chia sẻ trực tiếp của Thư Mục (Folder) và tệp PDF từ Google Drive qua `rclone link`.

## 6. TRÌNH BÀY KẾT QUẢ CHO NGƯỜI DÙNG
- Tuân thủ nghiêm ngặt **Quy Tắc Trình Bày Mặc Định (No-Line, Low-Scroll)**:
  - Tuyệt đối KHÔNG dùng đường kẻ ngang (`---`).
  - Tuyệt đối KHÔNG có khoảng trắng thừa giữa các phần.
  - Mỗi đầu mục 1, 2, 3 hoặc dấu `•` BẮT BUỘC nằm riêng một dòng.
  - Bảng 3 cột nén gọn với `<br/>` xuống dòng nội bộ, cột 2 BẮT BUỘC nhúng ảnh Keyframe minh họa trực tiếp `![Ảnh](file://...)`.
  - Cung cấp link Thư Mục Google Drive và Link xem trực tiếp tệp PDF.

## 7. TỰ ĐỘNG BỔ SUNG VÀO TRUNG TÂM TRA CỨU ĐIỆN ẢNH & ĐỒNG BỘ GITHUB PAGES
- Ngay sau khi hoàn thành đóng gói và upload Google Drive, Agent BẮT BUỘC thực thi script cập nhật tự động để bổ sung video mới vào thư viện tra cứu điện ảnh ([scene.html](file:///D:/CODE%20on%20window/vietndj.github.io/scene.html) & [TRUNG_TAM_TRA_CUU_DIEN_ANH.html](file:///D:/CODE%20on%20window/TRUNG_TAM_TRA_CUU_DIEN_ANH.html)) và tự động đồng bộ lên GitHub Pages:
  ```bash
  python "d:\CODE on window\Quản gia\auto_add_to_portal.py" \
    --package-dir "[Đường_dẫn_thư_mục_gói_vừa_tạo]" \
    --title "[Tiêu_đề_tiếng_Việt_mô_tả_nội_dung_chính_và_kỹ_thuật_cốt_lõi]" \
    --creator "@[Tên_kênh_tác_giả]" \
    --desc "[Mô_tả_ngắn_gọn_tiếng_Việt_về_góc_quay_ánh_sáng_và_cách_chuyển_cảnh]" \
    --tech "[Các_kỹ_thuật_trọng_tâm_ví_dụ_Match_Cut_180_Shutter_Parallax]" \
    --ig-url "[Link_Instagram_gốc]" \
    --gdrive-folder "[Link_Google_Drive_Folder]" \
    --gdrive-pdf "[Link_Google_Drive_PDF]"
  ```
  *(Script sẽ tự động cập nhật danh sách JSON, build lại tệp HTML độc lập và gọi GitHub REST API để đưa lên online ngay lập tức)*.

