---
name: sua-phu-de-capcut
description: Kỹ năng tự động tìm dự án CapCut PC mới nhất, sửa phụ đề, đọc sửa ngữ nghĩa tiếng Việt, loại bỏ khẩu ngữ/từ đệm (ờ, à, ừm, kiểu như...), xóa đoạn lặp lại, chuẩn hóa chính tả thương hiệu và cập nhật trực tiếp vào dự án CapCut PC. Kích hoạt khi người dùng yêu cầu: "sửa phụ đề video capcut mới tạo", "sửa phụ đề capcut", "sửa phụ đề video capcut".
---

# KỸ NĂNG SỬA PHỤ ĐỀ CAPCUT TỰ ĐỘNG (CAPCUT SUBTITLE FIXER & SEMANTIC CLEANER)

Khi người dùng yêu cầu "sửa phụ đề video capcut mới tạo" hoặc sử dụng kỹ năng này, agent BẮT BUỘC thực hiện quy trình 4 bước bên dưới:

## 1. Tự Động Tìm Dự Án CapCut PC Mới Nhất & Xử Lý Thô
- Chạy script Python tự động tìm dự án mới nhất trong `~/Movies/CapCut/User Data/Projects/com.lveditor.draft`:
  `python3 /Users/vietmac/.gemini/config/skills/sua-phu-de-capcut/scripts/fix_capcut_subtitles.py`
- Script sẽ tự động:
  - Loại bỏ các từ đệm, khẩu ngữ: *ờ, à, ừm, ừ, hả, kiểu như, ý là, thì là, nói chung là...*
  - Xóa các từ/cụm từ lặp vô nghĩa (vd: *tôi tôi*, *là là*).
  - Chuẩn hóa tên thương hiệu: *ChatGPT, CapCut, TikTok, YouTube, Facebook, App Store, B-roll, Cutaway, Talking Head...*
  - Sửa lỗi viết hoa tùy tiện của CapCut Auto-Caption.
  - Ngắt 2 dòng ngắn chuẩn ngữ pháp (3-4 từ/dòng).
  - Tắt ép cuộn dòng (`force_apply_line_max_width = False`).

## 2. Kiểm Tra Ngữ Nghĩa & Tối Ưu Lặp Đoạn (AI Semantic Polish)
- Đọc nội dung file `draft_info.json` của dự án CapCut vừa tìm được.
- Đọc lại toàn bộ danh sách phụ đề trong `materials.texts`:
  - Rà soát ngữ nghĩa tiếng Việt đảm bảo câu văn mạch lạc, tự nhiên, đúng ngữ pháp.
  - Phát hiện và loại bỏ các đoạn/câu nói lặp lại ý (ý tưởng trùng lặp do người nói ngập ngừng hoặc nói đi nói lại).
  - Đảm bảo giữ nguyên cấu trúc JSON và mốc thời gian (`start`, `duration`).

## 3. Cập Nhật Đồng Bộ Dự Án CapCut
- Ghi lại các thay đổi ngữ nghĩa đã tối ưu vào `draft_info.json` và các file `.json` / `.tmp` trong thư mục dự án CapCut.

## 4. Trình Bảy Kết Quả Cho Người Dùng
- Tuân thủ nghiêm ngặt **Quy Tắc Trình Bày Mặc Định (No-Line, Low-Scroll)**:
  - Tuyệt đối KHÔNG dùng đường kẻ ngang (`---`).
  - Tuyệt đối KHÔNG có khoảng trắng thừa giữa các phần.
  - Báo cáo rõ: Tên dự án CapCut đã sửa, số lượng phụ đề đã xử lý, danh sách các từ đệm/đoạn lặp đã xóa.
  - Nhắc nhở người dùng nhấn `Cmd + Q` để thoát hẳn CapCut PC và mở lại dự án để thấy kết quả.
