#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Video & Carousel Analysis, Chrome Headless PDF & Google Drive Automation Pipeline
"""
import os
import sys
import json
import re
import shutil
import base64
import subprocess
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_BIN):
    CHROME_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

RCLONE_EXE = r"C:\Users\NC\AppData\Local\Programs\rclone\rclone.exe"
GDRIVE_REMOTE_BASE = "gdrive:Work/AI_Video_Analysis"

def sanitize_name(name):
    clean = re.sub(r'[\\/*?:"<>|]', "", name)
    clean = re.sub(r'\s+', "_", clean)
    return clean[:45].strip("._")

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def img_to_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

def render_html_to_pdf(html_path, pdf_path):
    cmd = f'"{CHROME_BIN}" --headless=new --disable-gpu --print-to-pdf="{pdf_path}" --no-pdf-header-footer "{html_path}"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.returncode == 0 and os.path.exists(pdf_path)

def get_post_metadata(url_or_path):
    if os.path.isfile(url_or_path):
        stem = Path(url_or_path).stem
        return [{
            "id": stem,
            "uploader": "local_creator",
            "title": stem,
            "url": url_or_path,
            "is_carousel": False
        }]
    
    cmd = f'yt-dlp --no-warnings --dump-json "{url_or_path}"'
    code, out, _ = run_cmd(cmd)
    items = []
    if code == 0 and out:
        lines = [l for l in out.strip().split('\n') if l.strip()]
        for l in lines:
            try:
                data = json.loads(l)
                items.append({
                    "id": data.get("id", "video"),
                    "uploader": data.get("uploader") or data.get("uploader_id") or data.get("channel") or "creator",
                    "title": data.get("title", "video"),
                    "url": data.get("webpage_url", url_or_path),
                    "duration": data.get("duration"),
                    "is_carousel": len(lines) > 1
                })
            except Exception:
                pass
    
    if not items:
        match = re.search(r'/(?:p|reel|shorts)/([A-Za-z0-9_-]+)', url_or_path)
        shortcode = match.group(1) if match else "video"
        items.append({
            "id": shortcode,
            "uploader": "creator",
            "title": f"Video_{shortcode}",
            "url": url_or_path,
            "is_carousel": False
        })
    return items

def process_video_or_carousel(url_or_path, output_base=r"D:\CODE on window\Video phan tich\output_packages", brain_artifact_dir=None):
    os.makedirs(output_base, exist_ok=True)
    import cv2
    import numpy as np

    items = get_post_metadata(url_or_path)
    is_carousel = len(items) > 1
    uploader_clean = sanitize_name(items[0]["uploader"])
    shortcode = sanitize_name(items[0]["id"])
    title_clean = sanitize_name(items[0]["title"])

    if is_carousel:
        folder_name = f"IG_@{uploader_clean}_{shortcode}_Carousel_Analysis".strip("_")
    else:
        folder_name = f"IG_@{uploader_clean}_{shortcode}_{title_clean}".strip("_")

    project_dir = os.path.join(output_base, folder_name)
    os.makedirs(project_dir, exist_ok=True)

    brain_shots_dir = None
    if brain_artifact_dir:
        brain_shots_dir = os.path.join(brain_artifact_dir, "extracted_shots")
        os.makedirs(brain_shots_dir, exist_ok=True)

    if is_carousel:
        print(f"[*] Phát hiện bài Carousel gồm {len(items)} videos/slides. Đang tải và phân tích...")
        slides_dir = os.path.join(project_dir, "carousel_slides")
        os.makedirs(slides_dir, exist_ok=True)
        
        dl_cmd = f'yt-dlp -o "{slides_dir}/slide_%(autonumber)02d.%(ext)s" "{url_or_path}"'
        run_cmd(dl_cmd)

        video_files = sorted([f for f in os.listdir(slides_dir) if f.endswith(".mp4")])
        slides_data = []

        for i, vf in enumerate(video_files):
            s_num = i + 1
            v_path = os.path.join(slides_dir, vf)
            cap = cv2.VideoCapture(v_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            dur = round(total / fps, 2)

            cap.set(cv2.CAP_PROP_POS_FRAMES, total // 2)
            ret, frame = cap.read()
            mid_name = f"slide_{s_num:02d}_mid.jpg"
            if ret:
                cv2.imwrite(os.path.join(slides_dir, mid_name), frame)
                if brain_shots_dir:
                    cv2.imwrite(os.path.join(brain_shots_dir, mid_name), frame)
            cap.release()

            slides_data.append({
                "slide_num": s_num,
                "filename": vf,
                "duration": dur,
                "resolution": f"{w}x{h}",
                "aspect_ratio": "4:5 (Dọc)" if h > w else "9:16",
                "mid_img": mid_name
            })

        html_src = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
@page {{ size: A4 portrait; margin: 12mm; }}
* {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; }}
body {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #0f172a; font-size: 13px; line-height: 1.5; }}
.header {{ background: #0f172a; border-radius: 12px; padding: 20px; color: #fff; margin-bottom: 16px; }}
.badge {{ background: #06b6d4; color: #082f49; font-weight: 800; font-size: 11px; padding: 4px 8px; border-radius: 4px; }}
h1 {{ font-size: 20px; color: #f8fafc; margin-top: 8px; }}
.card {{ border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 12px; display: flex; gap: 14px; page-break-inside: avoid; }}
.img-box {{ width: 130px; height: 162px; background: #000; border-radius: 6px; overflow: hidden; }}
.img-box img {{ width: 100%; height: 100%; object-fit: cover; }}
.info {{ flex: 1; }}
</style>
</head>
<body>
<div class="header">
    <span class="badge">CAROUSEL SERIES BREAKDOWN</span>
    <h1>Báo Cáo Phân Tích Tuyển Tập Video Carousel</h1>
    <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Creator: @{uploader_clean} | Mã bài: {shortcode} | Quy mô: {len(slides_data)} Slides</div>
</div>
"""
        for s in slides_data:
            b64 = img_to_b64(os.path.join(slides_dir, s["mid_img"]))
            html_src += f"""
<div class="card">
    <div class="img-box"><img src="{b64}" /></div>
    <div class="info">
        <div style="font-weight:700; font-size:14px;">Slide {s['slide_num']:02d} [{s['duration']}s | {s['resolution']}]</div>
        <div style="font-size:12px; color:#475569; margin-top:6px;"><b>Phân loại:</b> {s['aspect_ratio']} &bull; Khung hình video trích xuất tự động.</div>
    </div>
</div>
"""
        html_src += "</body></html>"
        html_file = os.path.join(project_dir, "Bao_Cao_Phan_Tich_Carousel.html")
        pdf_file = os.path.join(project_dir, "Bao_Cao_Phan_Tich_Carousel.pdf")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_src)
        render_html_to_pdf(html_file, pdf_file)

    else:
        print(f"[*] Phát hiện Video đơn lẻ. Đang tải và bóc tách Shots OpenCV...")
        shots_dir = os.path.join(project_dir, "extracted_shots")
        trans_dir = os.path.join(shots_dir, "transitions")
        os.makedirs(trans_dir, exist_ok=True)

        video_dest = os.path.join(project_dir, f"{shortcode}.mp4")
        if os.path.isfile(url_or_path):
            shutil.copy2(url_or_path, video_dest)
        else:
            run_cmd(f'yt-dlp --no-warnings "{url_or_path}" -o "{video_dest}" --force-overwrites')

        cap = cv2.VideoCapture(video_dest)
        fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration_sec = round(total_frames / fps, 2)

        hists = []
        while True:
            ret, frame = cap.read()
            if not ret: break
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
            cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            hists.append(hist)
        cap.release()

        diffs = [0.0]
        for i in range(1, len(hists)):
            comp = cv2.compareHist(hists[i-1], hists[i], cv2.HISTCMP_CORREL)
            diffs.append(1.0 - comp)

        cut_frames = []
        min_shot = max(6, int(fps * 0.3))
        i = 1
        while i < len(diffs):
            if diffs[i] > 0.40:
                win = diffs[i:min(i+6, len(diffs))]
                m_idx = int(i + np.argmax(win))
                if not cut_frames or (m_idx - cut_frames[-1]) >= min_shot:
                    cut_frames.append(m_idx)
                i = m_idx + min_shot
            else:
                i += 1

        ranges = []
        st_f = 0
        for cf in cut_frames:
            ranges.append((st_f, cf - 1))
            st_f = cf
        ranges.append((st_f, total_frames - 1))

        cap = cv2.VideoCapture(video_dest)
        shot_info = []
        curr = 0
        s_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret or s_idx >= len(ranges): break
            s_st, s_en = ranges[s_idx]
            sid = s_idx + 1

            if curr == (s_st + s_en) // 2:
                m_name = f"shot_{sid:02d}_mid.jpg"
                cv2.imwrite(os.path.join(shots_dir, m_name), frame)
                if brain_shots_dir:
                    cv2.imwrite(os.path.join(brain_shots_dir, m_name), frame)
            
            if curr == s_en:
                shot_info.append({
                    "shot_id": sid,
                    "start_time": round(s_st / fps, 2),
                    "end_time": round(s_en / fps, 2),
                    "duration": round((s_en - s_st + 1) / fps, 2),
                    "mid_keyframe": f"shot_{sid:02d}_mid.jpg"
                })
                s_idx += 1
            curr += 1
        cap.release()

        with open(os.path.join(project_dir, "shot_info.json"), "w", encoding="utf-8") as f:
            json.dump(shot_info, f, ensure_ascii=False, indent=2)

        html_src = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
@font-face {{
    font-family: 'SVN-Aeonik';
    src: url('file:///d:/CODE%20on%20window/Qu%E1%BA%A3n%20gia/fonts/SVN-AEONIK-REGULAR.TTF') format('truetype');
    font-weight: 400;
}}
@font-face {{
    font-family: 'SVN-Aeonik';
    src: url('file:///d:/CODE%20on%20window/Qu%E1%BA%A3n%20gia/fonts/SVN-AEONIK-BOLD.TTF') format('truetype');
    font-weight: 700;
}}
@font-face {{
    font-family: 'SVN-Acta';
    src: url('file:///d:/CODE%20on%20window/Qu%E1%BA%A3n%20gia/fonts/SVN-Acta-Bold.ttf') format('truetype');
    font-weight: 700;
}}
@page {{ size: A4 portrait; margin: 12mm; }}
* {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; font-family: 'SVN-Aeonik', sans-serif !important; }}
body {{ font-family: 'SVN-Aeonik', sans-serif; color: #0f172a; font-size: 13px; line-height: 1.5; }}
h1, h2, .header h1 {{ font-family: 'SVN-Aeonik', 'SVN-Acta', sans-serif !important; }}
.header {{ background: #0f172a; border-radius: 12px; padding: 20px; color: #fff; margin-bottom: 16px; }}
.badge {{ background: #f59e0b; color: #0f172a; font-weight: 800; font-size: 11px; padding: 4px 8px; border-radius: 4px; }}
h1 {{ font-size: 20px; color: #f8fafc; margin-top: 8px; }}
.shot-card {{ border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 12px; display: flex; gap: 14px; page-break-inside: avoid; }}
.img-box {{ width: 120px; aspect-ratio: 9/16; background: #000; border-radius: 6px; overflow: hidden; flex-shrink: 0; }}
.img-box img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.trans-img {{ max-width: 440px; width: auto; height: auto; max-height: 180px; object-fit: contain; border-radius: 6px; display: block; margin: 6px auto; }}
.info {{ flex: 1; }}
</style>
</head>
<body>
<div class="header">
    <span class="badge">DIRECTOR BREAKDOWN REPORT</span>
    <h1>Báo Cáo Phân Tích Phân Cảnh &amp; Quay Dựng</h1>
    <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Creator: @{uploader_clean} | Thời lượng: {duration_sec}s | {len(shot_info)} Shots</div>
</div>
"""
        for s in shot_info:
            b64 = img_to_b64(os.path.join(shots_dir, s["mid_keyframe"]))
            html_src += f"""
<div class="shot-card">
    <div class="img-box"><img src="{b64}" /></div>
    <div class="info">
        <div style="font-weight:700; font-size:14px;">Shot {s['shot_id']:02d} [{s['start_time']}s - {s['end_time']}s ({s['duration']}s)]</div>
        <div style="font-size:12px; color:#475569; margin-top:6px;">Phân tích chi tiết góc máy, ánh sáng và chuyển cảnh.</div>
    </div>
</div>
"""
        html_src += "</body></html>"
        html_file = os.path.join(project_dir, "Bao_Cao_Phan_Tich_Dao_Dien.html")
        pdf_file = os.path.join(project_dir, "Bao_Cao_Phan_Tich_Dao_Dien.pdf")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_src)
        render_html_to_pdf(html_file, pdf_file)

    print(f"[*] Uploading trọn bộ package lên Google Drive: {GDRIVE_REMOTE_BASE}/{folder_name}")
    run_cmd(f'"{RCLONE_EXE}" copy "{project_dir}" "{GDRIVE_REMOTE_BASE}/{folder_name}" -v')

    _, f_link, _ = run_cmd(f'"{RCLONE_EXE}" link "{GDRIVE_REMOTE_BASE}/{folder_name}"')
    pdf_target_name = "Bao_Cao_Phan_Tich_Carousel.pdf" if is_carousel else "Bao_Cao_Phan_Tich_Dao_Dien.pdf"
    _, p_link, _ = run_cmd(f'"{RCLONE_EXE}" link "{GDRIVE_REMOTE_BASE}/{folder_name}/{pdf_target_name}"')

    res = {
        "success": True,
        "is_carousel": is_carousel,
        "folder_name": folder_name,
        "gdrive_folder_link": f_link if "http" in f_link else "",
        "gdrive_pdf_link": p_link if "http" in p_link else ""
    }
    return res

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_and_upload.py <url_or_path> [brain_dir]")
        sys.exit(1)
    url = sys.argv[1]
    b_dir = sys.argv[2] if len(sys.argv) > 2 else None
    result = process_video_or_carousel(url, brain_artifact_dir=b_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
