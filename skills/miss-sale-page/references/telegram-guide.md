# Hướng dẫn tạo Telegram Bot và lấy thông tin

1. Truy cập Telegram, tìm kiếm và bắt đầu chat với **@BotFather**
2. Sử dụng lệnh `/newbot` để tạo bot mới, làm theo hướng dẫn của hệ thống
3. Bạn sẽ nhận được **Bot Token** (dạng `123456789:ABCdefGHIjklmNOPQrstUVwXYZ`). Hãy lưu lại Token này.
4. Để lấy **Chat ID**:
   - Bắt đầu chat với Bot bạn vừa tạo và gửi một tin nhắn bất kỳ (VD: "hello")
   - Gọi API bằng trình duyệt hoặc CURL: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Tìm tới object `"chat"` và lấy giá trị `"id"` (đó chính là Chat ID của bạn)
