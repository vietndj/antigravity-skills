---
name: miss-sale-page
description: >
  Được kích hoạt khi người dùng muốn tạo một landing page bán hàng hoặc setup trang bán hàng (VD: "Tạo landing page bán hàng", "Setup trang bán hàng"). Hướng dẫn agent qua các bước thu thập thông tin, sinh nội dung, cấu hình, và deploy.
---

# Hướng dẫn chi tiết tạo Landing Page

Bạn là chuyên gia thiết kế và viết nội dung Landing Page. Khi skill này được kích hoạt, hãy thực hiện chính xác các PHASE dưới đây:

## PHASE 1: Thu thập thông tin (Interactive 2-Turn Demo Setup)

### 🚀 Quy tắc 2 Nhịp Tương tác (Chuẩn Kịch bản Video Demo)

- **Nhịp 1**: Khi người dùng gõ lệnh tổng quan (VD: *"Tạo landing page bán sản phẩm giá 199k"* hoặc *"Tạo landing page bán hàng"*):
  ➜ Bạn HÃY HỎI 02 CÂU HỎI NGẮN GỌN:
  1. *"Sản phẩm/dịch vụ cụ thể bạn muốn bán là gì?"*
  2. *"Bạn muốn nhận chuyển khoản qua ngân hàng nào? (Ví dụ: TPBank, MB Bank, Techcombank,...)"*

- **Nhịp 2**: Khi người dùng trả lời (VD: *"Thư Viện 300 Sound Effects & Nhạc Nền Cinema, ngân hàng TPBank"*):
  ➜ Tự động bóc tách tên sản phẩm, mức giá (199.000 VNĐ), ngân hàng (TPBank - số tài khoản `88804101986`, tên `NGUYEN DUC VIET` có sẵn trong `site.config.ts`), sau đó CHUYỂN THẲNG sang **PHASE 2** (Sinh nội dung) ➜ **PHASE 3** (Ghi code/cấu hình) ➜ **PHASE 4** (Khởi chạy & Trả link)!

### ⚙️ Cấu hình Mặc định (Default Fallback)
Nếu người dùng không chỉ định cụ thể số tài khoản hoặc API keys:
- **Thông tin ngân hàng**: Tự động lấy số tài khoản & tên chủ tài khoản thật có sẵn trong `src/site.config.ts`.
- **Hệ thống thanh toán & Thông báo (SePay/Telegram/Make/Resend)**: Tự động đọc từ file `.env` hoặc `site.config.ts`.

---

## PHASE 2: Sinh nội dung bằng AI (Content Generation)

Sau khi thu thập xong thông tin, thực hiện:

1. Báo với người dùng: "Đang phân tích sản phẩm và sinh nội dung Landing Page..."
2. Dựa vào thông tin từ Phase 1, bạn HÃY TỰ SINH nội dung cho TOÀN BỘ các phần của landing page. Quá trình suy nghĩ bao gồm:
   - Xác định loại sản phẩm (Vật lý / Dịch vụ / Sản phẩm số)
   - Tạo hero headline, subheadline, CTA text
   - Tạo 3 pain points (nỗi đau) liên quan
   - Tạo cycle of trying (những sai lầm đối thủ hay mắc phải)
   - Tạo discovery story
   - Tạo 4-5 solution benefits (lợi ích)
   - Tạo 4 skill/feature cards
   - Tạo before/after comparison (7 mục cho mỗi bên)
   - Tạo roadmap/modules (lộ trình 4 giai đoạn)
   - Tạo instructor bio (giới thiệu từ thông tin người dùng)
   - Tạo 3-5 bonus items
   - Tạo final CTA
   - Tạo value stack
   - Tạo 5-7 FAQ items
3. Tự động chuyển thẳng sang **PHASE 3** và **PHASE 4** để ghi code, build và trả link web live ngay lập tức (dưới 2 phút) mà không làm ngắt nhịp tương tác của người dùng.

## PHASE 3: Ghi config & Populate template

Thực hiện các bước sau (sử dụng file tool để thay đổi code):

1. **Ghi vào `src/site.config.ts`**: Điền thông tin thanh toán/thông báo thu được ở Phase 1.
2. **Cập nhật `src/content.ts`**: Thay thế object `DEFAULT_CONTENT` bằng nội dung đã sinh ở Phase 2. Giữ nguyên interface `PageContent` và hàm `ContentProvider`, CHỈ chỉnh sửa các giá trị bên trong `DEFAULT_CONTENT`.
3. **Cập nhật file `.env`**:
   - Nếu file `.env` đã có sẵn: Giữ nguyên các API Keys (`SEPAY_API_KEY`, `GOOGLE_SCRIPT_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `RESEND_API_KEY`, `MAKE_WEBHOOK_URL`...) và chỉ cập nhật `COURSE_AMOUNT=<giá bán dạng số, VD: 299000>`.
   - Nếu chưa có: Tạo mới `.env` dựa trên `.env.example`.
4. Chạy lệnh: `npm install` để cài đặt dependencies.
5. Chạy lệnh: `npm run build` để xác nhận dự án biên dịch thành công.

## PHASE 4: Deploy & Trả link

1. Kiểm tra Vercel CLI có sẵn chưa bằng lệnh: `npx vercel whoami`
   - Nếu chưa đăng nhập: Báo người dùng chạy `npx vercel login` và quay lại.
2. Chạy lệnh Deploy: `npx vercel --prod --yes`
3. Trả URL live cho người dùng.
4. Đề xuất bước tiếp theo: "Bạn có thể yêu cầu tôi chỉnh sửa bất kỳ phần nào: nội dung, màu sắc, layout..."
