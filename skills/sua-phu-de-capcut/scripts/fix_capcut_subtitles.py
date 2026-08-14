#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CÔNG CỤ SỬA PHỤ ĐỀ CAPCUT PC TỰ ĐỘNG - PHIÊN BẢN NÂNG CẤP V3
Hỗ trợ:
1. Tự động phát hiện Dự án CapCut PC mới nhất.
2. Xóa bỏ khẩu ngữ / từ đệm / từ thừa (ờ, à, ừm, kiểu như, ý là, thì là, nói chung là...).
3. Xóa bỏ từ lặp vô nghĩa (vd: "tôi tôi", "là là", "thì thì").
4. Chuẩn hóa tên thương hiệu (ChatGPT, CapCut, TikTok, YouTube, Facebook, App Store, B-roll...).
5. Khắc phục lỗi viết hoa tùy tiện giữa câu của CapCut Auto-Caption.
6. Tự động ngắt 2 dòng ngắn chuẩn ngữ pháp.
7. Tắt ép cuộn dòng (force_apply_line_max_width = False) để tránh xé từ.
8. Cập nhật trực tiếp vào tất cả file cấu hình json/tmp của dự án CapCut.
"""

import sys
import os
import json
import re

def get_latest_project():
    capcut_dir = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
    projects = []
    if not os.path.exists(capcut_dir):
        return None, None
    for item in os.listdir(capcut_dir):
        p_path = os.path.join(capcut_dir, item)
        if os.path.isdir(p_path) and not item.startswith('.'):
            draft_file = os.path.join(p_path, 'draft_info.json')
            if os.path.exists(draft_file):
                mtime = os.path.getmtime(draft_file)
                projects.append((mtime, item, p_path))
    if not projects:
        return None, None
    projects.sort(reverse=True)
    return projects[0][1], projects[0][2]

def clean_vietnamese_subtitles(text):
    if not text or not isinstance(text, str):
        return text

    # 1. Xóa từ đệm, khẩu ngữ thừa
    fillers = [
        r'\b(ờ|ừm|ừ|hả|hờ|à)\b',
        r'\bkiểu như\b',
        r'\bthì là\b',
        r'\bý là\b',
        r'\bnói chung là\b',
        r'\bkiểu kiểu\b',
        r'\bdạng như\b'
    ]
    for pattern in fillers:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # 2. Sửa từ lặp lại vô nghĩa (vd: "tôi tôi", "là là", "và và")
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text, flags=re.IGNORECASE)

    # 3. Chuẩn hóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()

    # 4. Sửa chính tả thương hiệu & thuật ngữ
    typo_map = {
        r'\bpromt\b': 'prompt',
        r'\bti VI\b': 'TV',
        r'\bti vi\b': 'TV',
        r'\b0/0 phẩy\b': '0,0 phẩy',
        r'\b0/0\b': '0,0',
        r'\bchat gpt\b': 'ChatGPT',
        r'\bchatgpt\b': 'ChatGPT',
        r'\byoutube\b': 'YouTube',
        r'\btiktok\b': 'TikTok',
        r'\bfacebook\b': 'Facebook',
        r'\bapp store\b': 'App Store',
        r'\bappstore\b': 'App Store',
        r'\bplay store\b': 'Play Store',
        r'\bch play\b': 'CH Play',
        r'\bcapcut\b': 'CapCut',
        r'\bcapcut pc\b': 'CapCut PC',
        r'\bbroll\b': 'B-roll',
        r'\bcutaway\b': 'Cutaway',
        r'\btalking head\b': 'Talking Head',
    }
    for k, v in typo_map.items():
        text = re.sub(k, v, text, flags=re.IGNORECASE)

    # 5. Khắc phục lỗi viết hoa tùy tiện của CapCut Auto-Caption
    proper_nouns = {'AI', 'TV', 'Grab', 'Hà', 'Nội', 'Vincom', 'CapCut', 'Google', 'Python', 'YouTube', 'TikTok', 'Facebook', 'ChatGPT', 'App', 'Store', 'Play', 'CH', 'B-roll', 'Cutaway', 'Talking', 'Head', 'Air', 'Alt', 'Drive', 'Chrome'}
    capcut_bad_caps = {
        'Cho', 'Sao', 'Ra', 'Sai', 'Theo', 'Chung', 'Ba', 'Hóa', 'Chi', 'Nó', 'Tức', 'Bởi', 
        'Và', 'Nhưng', 'Thì', 'Có', 'Từ', 'Trên', 'Trong', 'Đó', 'Thấy', 'Cho nên', 'Bởi vì', 
        'Nên', 'Là', 'Về', 'Để', 'Của', 'Được', 'Khi', 'Nếu', 'Thực', 'Nơi', 'Đấy', 'Ấy', 'Hơn',
        'Hiển', 'Thị', 'Hiển thị', 'Tạo', 'Thêm', 'Chọn', 'Mở', 'Xóa', 'Cắt', 'Chạy', 'Xem', 'Kéo', 'Nhấn', 'Bấm', 'Ấn', 'Nói', 'Gõ', 'Cài', 'Tải', 'Chỉnh', 'Sửa', 'Xuất', 'Lưu', 'Đổi', 'Nhập',
        'Bành', 'Bôi', 'Băm', 'Bạn', 'Bất', 'Bắc', 'Bắt', 'Bằng', 'Bội', 'Cao', 'Chan', 'Chen', 'Chu', 'Chun', 'Chính', 'Chưa', 'Chỉ', 'Chị', 'Chồng', 'Chủ', 'Cách', 'Công', 'Cùng', 'Cảnh', 'Cấp', 'Cận', 'Duy', 'Dò', 'Dòng', 'Dùng', 'Dễ', 'Định', 'Đồng', 'Động', 'Đi', 'Điểm', 'Đều', 'Đưa', 'Đứng', 'Hình', 'Hành', 'Học', 'Hỏi', 'Hủy', 'Khu', 'Kho', 'Không', 'Khác', 'Khóa', 'Làm', 'Lên', 'Lại', 'Lấy', 'Lớp', 'Lần', 'Lớn', 'Mới', 'Một', 'Mọi', 'Nào', 'Này', 'Nhiều', 'Nhà', 'Nhìn', 'Nhớ', 'Phải', 'Phần', 'Phát', 'Phòng', 'Qua', 'Quản', 'Quá', 'Rồi', 'Sau', 'Sang', 'Số', 'Sắp', 'Thế', 'Thường', 'Thành', 'Thời gian', 'Thử', 'Tên', 'Tự', 'Tốc độ', 'Tới', 'Từng', 'Vào', 'Với', 'Việc', 'Xoá', 'Xử lý', 'Yêu cầu'
    }
    
    words = text.split()
    fixed_words = []
    for i, w in enumerate(words):
        match = re.match(r'^([^\w]*)([\w\d]+)([^\w]*)$', w, re.UNICODE)
        if match:
            prefix, core, suffix = match.groups()
            if core in proper_nouns:
                fixed_words.append(w)
            elif core in capcut_bad_caps or (core.isupper() and core not in proper_nouns and len(core) > 1):
                fixed_words.append(prefix + core.lower() + suffix)
            else:
                fixed_words.append(w)
        else:
            fixed_words.append(w)
            
    cleaned = ' '.join(fixed_words)

    # Viết hoa chữ cái đầu tiên của câu nếu câu bắt đầu bằng chữ thường
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]

    # 6. Ngắt 2 dòng ngắn chuẩn ngữ pháp nếu câu quá dài (> 4 từ và > 22 ký tự)
    words = cleaned.split()
    if len(words) > 4 and len(cleaned) > 22:
        mid = len(words) // 2
        best_idx = mid
        for offset in [0, -1, 1, -2, 2]:
            idx = mid + offset
            if 2 <= idx <= len(words) - 2:
                w_clean = words[idx].lower().strip('.,?!')
                if w_clean in ['và', 'hoặc', 'nhưng', 'thì', 'là', 'để', 'cho', 'của', 'với', 'bởi', 'vì', 'tại', 'sao', 'nếu', 'khi', 'cho nên', 'thấy', 'nhé', 'nhá', 'mà', 'đó', 'ấy', 'được', 'này', 'ý']:
                    best_idx = idx
                    break
        line1 = ' '.join(words[:best_idx])
        line2 = ' '.join(words[best_idx:])
        cleaned = line1 + '\n' + line2

    return cleaned

def process_project_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return False, 0

    modified = False
    sub_count = 0
    texts = data.get('materials', {}).get('texts', [])
    for item in texts:
        item['force_apply_line_max_width'] = False
        item['line_max_width'] = 1.0
        item['fixed_width'] = -1.0
        item['fixed_height'] = -1.0

        raw_content = item.get('content', '')
        if raw_content and 'text' in raw_content:
            try:
                content_obj = json.loads(raw_content)
                txt = content_obj.get('text', '')
                if txt:
                    new_txt = clean_vietnamese_subtitles(txt)
                    if new_txt != txt or content_obj.get('text') != new_txt:
                        content_obj['text'] = new_txt
                        if 'styles' in content_obj and len(content_obj['styles']) > 0:
                            for st in content_obj['styles']:
                                if 'range' in st:
                                    st['range'] = [0, len(new_txt)]
                        item['content'] = json.dumps(content_obj, ensure_ascii=False)
                        modified = True
                        sub_count += 1
            except Exception:
                pass

    if modified or len(texts) > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True, sub_count
    return False, 0

def main():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        project_name = sys.argv[1].strip()
        capcut_dir = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
        project_folder = os.path.join(capcut_dir, project_name)
    else:
        project_name, project_folder = get_latest_project()

    if not project_name or not project_folder or not os.path.exists(project_folder):
        print("RESULT_JSON:" + json.dumps({"status": "error", "message": "Không tìm thấy dự án CapCut nào!"}))
        return

    updated_files = 0
    total_scanned = 0
    total_subs_fixed = 0

    for root, dirs, files in os.walk(project_folder):
        for f in files:
            if f.endswith('.json') or f.endswith('.tmp'):
                total_scanned += 1
                is_mod, count = process_project_file(os.path.join(root, f))
                if is_mod:
                    updated_files += 1
                    total_subs_fixed += count

    res = {
        "status": "success",
        "project_name": project_name,
        "project_folder": project_folder,
        "updated_files": updated_files,
        "total_scanned": total_scanned,
        "subs_fixed": total_subs_fixed
    }
    print("RESULT_JSON:" + json.dumps(res, ensure_ascii=False))

if __name__ == "__main__":
    main()
