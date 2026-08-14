# Hướng dẫn triển khai Google Apps Script

```javascript
// Google Apps Script — Quản lý đơn hàng Landing Page
// Deploy as Web App: Execute as Me, Anyone can access

const SHEET_NAME = "Orders";

function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME) 
    || SpreadsheetApp.getActiveSpreadsheet().insertSheet(SHEET_NAME);
  
  const data = JSON.parse(e.postData.contents);
  
  if (data.action === "append") {
    // Add headers if sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["Thời gian", "Họ tên", "SĐT", "Email", "URL", "Trạng thái"]);
    }
    sheet.appendRow(data.values);
    const row = sheet.getLastRow();
    return ContentService.createTextOutput(JSON.stringify({ success: true, row })).setMimeType(ContentService.MimeType.JSON);
  }
  
  if (data.action === "update_status") {
    const rows = sheet.getDataRange().getValues();
    for (let i = 1; i < rows.length; i++) {
      const cellPhone = String(rows[i][2]).replace(/^'/, "");
      if (cellPhone === data.phone) {
        sheet.getRange(i + 1, 6).setValue(data.status || "Đã thanh toán");
        return ContentService.createTextOutput(JSON.stringify({ 
          success: true, 
          name: rows[i][1], 
          email: rows[i][3] 
        })).setMimeType(ContentService.MimeType.JSON);
      }
    }
    return ContentService.createTextOutput(JSON.stringify({ success: false, error: "Phone not found" })).setMimeType(ContentService.MimeType.JSON);
  }
  
  return ContentService.createTextOutput(JSON.stringify({ success: false, error: "Unknown action" })).setMimeType(ContentService.MimeType.JSON);
}
```

**Các bước triển khai:**
1. Tạo một Google Sheet mới.
2. Mở tab **Tiện ích mở rộng (Extensions)** > **Apps Script**.
3. Dán toàn bộ mã trên vào file `Mã.gs`.
4. Nhấp vào **Triển khai (Deploy)** > **Tùy chọn triển khai mới (New deployment)**.
5. Chọn loại **Web App**.
6. Chọn "Execute as: Me" và "Who has access: Anyone".
7. Nhấn **Deploy** và cấp quyền.
8. Sao chép lại URL Web App và sử dụng.
