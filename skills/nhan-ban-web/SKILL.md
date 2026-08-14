---
name: Nhân Bản Web
description: Kích hoạt khi người dùng nhắc đến "nhân bản", "tạo web mới từ web mẫu", "clone web". Trợ lý sẽ chủ động thu thập thông tin và tự động hóa quá trình nhân bản mã nguồn thay vì bắt người dùng tự làm.
---

# Hướng dẫn Nhân Bản Website dành cho Trợ lý (AI)

Tuyệt đối KHÔNG ĐƯỢC bảo người dùng tự đi đọc file hướng dẫn. Khi người dùng yêu cầu nhân bản, bạn phải đóng vai trò là một trợ lý chủ động thực hiện theo quy trình sau:

## Bước 1: Thu thập thông tin
Hỏi người dùng cung cấp 4 thông tin sau (bỏ qua nếu họ đã nói trước):
1. Tên thư mục dự án mới muốn tạo (VD: `khoa-hoc-edit`).
2. Giá tiền khóa học (VD: `399000`).
3. Tên khóa học và Danh sách Quà tặng hiển thị ở Popup Thanh toán.
4. Nguồn file ảnh mã QR mới (bảo họ kéo thả ảnh vào máy hoặc chỉ đường dẫn, để bạn tự động thay).

## Bước 2: Tự động hóa nhân bản bằng Tool
Ngay khi có đủ thông tin, bạn sử dụng quyền hạn của mình để TỰ LÀM các bước sau:
1. Copy toàn bộ thư mục `artifacts/mau-landing-page` sang thư mục mới `artifacts/<tên-dự-án>`.
2. Dùng công cụ `replace_file_content` sửa file `src/Checkout.tsx` ở dự án mới:
   - Cập nhật text danh sách quà tặng.
   - Cập nhật tên khóa học.
   - Cập nhật đường dẫn ảnh QR mới (sau khi copy ảnh vào thư mục `public/`).

## Bước 3: Báo cáo và Bàn giao
Sau khi code xong, báo cáo cho người dùng biết bạn đã hoàn tất phần lập trình. 
Lúc này mới nhắc người dùng tự tay làm 2 bước cuối cùng trên nền tảng Vercel:
1. Kéo dự án mới này lên Vercel.
2. Cài đặt 3 biến môi trường (Environment Variables) bắt buộc:
   - `SEPAY_API_KEY`: Sinh từ SePay.
   - `COURSE_AMOUNT`: Nhập đúng số tiền khóa học.
   - `MAKE_WEBHOOK_URL`: Webhook cấp quyền của Make.com.
Dặn họ: "Nếu thêm biến sau khi đã tải code, nhớ bấm Redeploy trên Vercel".
