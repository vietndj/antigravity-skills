---
name: create-landing-page
description: >-
  Kích hoạt khi người dùng yêu cầu tạo web bán hàng, landing page bán hàng,
  trang bán sản phẩm, hoặc web thanh toán tự động. Các từ khóa kích hoạt:
  "web bán hàng", "landing page", "trang bán", "bán sản phẩm", "tạo web bán",
  "tạo trang bán hàng", "bán hàng online".
  KHÔNG kích hoạt cho các yêu cầu tạo web thông thường (portfolio, blog, dashboard).
---

# Skill: Kịch Bản Demo Tạo Landing Page Bán Hàng Tự Động

## KỊCH BẢN 4 NHỊP (BẮT BUỘC TUÂN THỦ TRÊN TẤT CẢ WORKSPACE)

---

### 📍 NHỊP 1: NGƯỜI DÙNG GỬI YÊU CẦU
Người dùng gửi prompt chuẩn demo:
> *"Tạo cho mình landing page bán Bộ Preset Lightroom Chụp Ảnh Cưới giá 199k"*

---

### 📍 NHỊP 2: AI HỎI XÁC NHẬN THÔNG TIN (BẮT BUỘC DÙNG TOOL `ask_question`)

Ngay khi nhận yêu cầu ở Nhịp 1, AI **BẮT BUỘC** gọi tool `ask_question` với đúng 1 câu hỏi duy nhất:

- **Question**: "Bạn muốn sử dụng thông tin người bán & tài khoản nhận tiền nào?"
- **Options**:
  1. "(Recommended) Dùng thông tin mặc định (Nguyễn Đức Việt — 0934.688.632), thanh toán vào TPBank"
  2. "Tự nhập thông tin người bán mới"

---

### 📍 NHỊP 3: NGƯỜI DÙNG PHẢN HỒI
Người dùng bấm chọn option 1: *"Dùng thông tin mặc định (Nguyễn Đức Việt — 0934.688.632), thanh toán vào TPBank"*.

---

### 📍 NHỊP 4: AI TIẾN HÀNH THỰC THI (PLANNING + EXECUTION)

Đường dẫn template: `/Users/vietmac/Documents/CODE/AI Course/mauLandingPage`

AI thực hiện các bước:

#### 1. Lập kế hoạch `implementation_plan.md`
Tạo file kế hoạch ngắn gọn giải thích các file sẽ thay đổi:
- `src/site.config.ts` (Tên sản phẩm, giá bán, mã CK)
- `src/content.ts` (Nội dung marketing, copywriting)

#### 2. Cập nhật `src/site.config.ts`
- `product.name`: Tên sản phẩm người dùng cung cấp (VD: "Bộ Preset Lightroom Chụp Ảnh Cưới")
- `product.price`: Format giá (VD: "199.000")
- `product.category`: Loại ngắn gọn sản phẩm (VD: "preset Lightroom")
- `payment.transferPrefix`: Mã viết tắt IN HOA (VD: "PRESET")
- `seller`: Giữ mặc định (Nguyễn Đức Việt, 0934688632, vietndj@gmail.com)

#### 3. Cập nhật `src/content.ts`
Tự động viết lại toàn bộ copywriting marketing phù hợp sản phẩm mới.

#### 4. Build & Deploy Vercel
```bash
cd "/Users/vietmac/Documents/CODE/AI Course/mauLandingPage"
npm run build && npx vercel --prod --yes --scope viet-s-projects1
```

#### 5. Trả về kết quả hoàn chỉnh
```
🎉 Đã hoàn thành Landing Page bán hàng tự động!

🔗 Website Live: https://bds-video-pro.vercel.app
📦 Sản phẩm: [Tên sản phẩm]
💰 Giá bán: [Giá]
⚡ Thanh toán VietQR tự động (TPBank) & Mail thông báo đã kích hoạt.
```
