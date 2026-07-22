import os

# Read original for content extraction
with open(r'C:\Users\AQQW\Desktop\index_backup.html', 'r', encoding='utf-8') as f:
    orig_lines = f.readlines()

# Extract original content sections
orig_text = ''.join(orig_lines)

print(f"Original file: {len(orig_lines)} lines, {len(orig_text)} chars")
print("Now building new file...")

# ===== PART 1: HTML head + CSS =====
head = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>金鑫 · 数据生命体 | 数据治理 & 合规管理</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #0a0f1a; color: #e0e8ff; overflow-x: hidden; -webkit-font-smoothing: antialiased; }
        #canvas-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; }
        #webcam-preview { position: fixed; bottom: 20px; right: 20px; width: 200px; height: 150px; border-radius: 12px; border: 2px solid rgba(106,180,255,0.4); z-index: 100; object-fit: cover; transform: scaleX(-1); background: rgba(10,15,26,0.9); }
        #hand-canvas { position: fixed; bottom: 20px; right: 20px; width: 200px; height: 150px; border-radius: 12px; z-index: 101; pointer-events: none; transform: scaleX(-1); }
        .content-layer { position: relative; z-index: 10; pointer-events: none; }
        .content-layer > * { pointer-events: auto; }
        .boot-sequence { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0a0f1a; z-index: 1000; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Courier New', monospace; }
        .boot-text { color: #6ab4ff; font-size: 14px; letter-spacing: 2px; margin-bottom: 8px; opacity: 0; text-align: center; padding: 0 20px; }
        .boot-progress { width: 200px; height: 2px; background: rgba(106,180,255,0.1); border-radius: 1px; margin-top: 24px; overflow: hidden; }
        .boot-progress-fill { height: 100%; background: #6ab4ff; width: 0; border-radius: 1px; }
        @keyframes fadeIn { to { opacity: 1; } }
        @keyframes fillProgress { to { width: 100%; } }
        .scan-line { position: fixed; top: 0; left: 0; width: 100%; height: 2px; background: rgba(106,180,255,0.15); animation: scan 6s linear infinite; z-index: 49; pointer-events: none; }
        @keyframes scan { 0% { transform: translateY(-100vh); } 100% { transform: translateY(100vh); } }
        .corner-frame { position: fixed; width: 40px; height: 40px; border-color: rgba(106,180,255,0.3); border-style: solid; z-index: 48; pointer-events: none; }
        .corner-frame.tl { top: 10px; left: 10px; border-width: 2px 0 0 2px; }
        .corner-frame.tr { top: 10px; right: 10px; border-width: 2px 2px 0 0; }
        .corner-frame.bl { bottom: 10px; left: 10px; border-width: 0 0 2px 2px; }
        .corner-frame.br { bottom: 10px; right: 220px; border-width: 0 2px 2px 0; }
        .hud-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 50; pointer-events: none; }
        .hud-title { position: absolute; top: 20px; left: 50%; transform: translateX(-50%); font-size: 14px; color: #6ab4ff; letter-spacing: 4px; font-family: 'Courier New', monospace; text-shadow: 0 0 20px rgba(106,180,255,0.5); }
        .hud-status { position: absolute; top: 44px; left: 50%; transform: translateX(-50%); font-size: 12px; color: #8aa8d8; font-family: 'Courier New', monospace; }
        .gesture-indicator { position: absolute; top: 20px; right: 240px; background: rgba(10,15,26,0.85); border: 1px solid rgba(106,180,255,0.3); border-radius: 12px; padding: 16px 20px; backdrop-filter: blur(10px); }
        .gesture-indicator h3 { font-size: 11px; color: #6ab4ff; letter-spacing: 2px; margin-bottom: 10px; font-family: 'Courier New', monospace; }
        .gesture-item { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 12px; color: #a0b8e0; transition: all 0.3s ease; }
        .gesture-item.active { color: #6ab4ff; text-shadow: 0 0 10px rgba(106,180,255,0.5); }
        .gesture-icon { font-size: 16px; width: 24px; text-align: center; }
        .state-badge { position: absolute; top: 20px; left: 20px; background: rgba(10,15,26,0.85); border: 1px solid rgba(106,180,255,0.3); border-radius: 12px; padding: 16px 20px; backdrop-filter: blur(10px); }
        .state-badge h3 { font-size: 11px; color: #6ab4ff; letter-spacing: 2px; margin-bottom: 8px; font-family: 'Courier New', monospace; }
        .state-value { font-size: 20px; font-weight: 700; color: #e0e8ff; transition: all 0.5s ease; }
        .particle-count { position: absolute; bottom: 20px; left: 20px; font-family: 'Courier New', monospace; font-size: 11px; color: #6a8ab8; }
        .hero-section { min-height: 100vh; display: flex; align-items: center; padding: 0 5%; position: relative; }
        .intro-card { margin-left: auto; width: 50%; max-width: 600px; background: rgba(10,15,26,0.8); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(106,180,255,0.2); border-radius: 20px; padding: 40px; opacity: 0; transform: translateX(60px); animation: slideIn 1.2s cubic-bezier(0.16,1,0.3,1) 3.5s forwards; }
        @keyframes slideIn { to { opacity: 1; transform: translateX(0); } }
        .data-tag { display: inline-block; background: rgba(106,180,255,0.15); border: 1px solid rgba(106,180,255,0.4); color: #6ab4ff; padding: 5px 14px; border-radius: 20px; font-size: 12px; font-family: 'Courier New', monospace; letter-spacing: 2px; margin-bottom: 16px; }
        .intro-card h1 { font-size: 42px; font-weight: 700; margin-bottom: 8px; background: linear-gradient(135deg,#fff 0%,#6ab4ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .intro-card .subtitle { font-size: 16px; color: #8aa8d8; margin-bottom: 16px; font-weight: 300; }
        .intro-card .meta { font-size: 13px; color: #6a8ab8; margin-bottom: 16px; }
        .intro-card p { font-size: 14px; line-height: 1.8; color: #a0b8e0; margin-bottom: 14px; }
        .contact-row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(106,180,255,0.15); }
        .contact-item { display: flex; align-items: center; gap: 6px; color: #8aa8d8; font-size: 13px; }
        .contact-item span { color: #6ab4ff; font-size: 16px; }
        .download-btn { display: inline-flex; align-items: center; gap: 8px; margin-top: 16px; padding: 10px 24px; background: rgba(106,180,255,0.15); border: 1px solid rgba(106,180,255,0.4); color: #6ab4ff; border-radius: 12px; font-size: 13px; font-weight: 500; text-decoration: none; transition: all 0.3s ease; }
        .download-btn:hover { background: rgba(106,180,255,0.25); box-shadow: 0 0 20px rgba(106,180,255,0.2); }
        .section-wrapper { padding: 80px 5%; max-width: 1200px; margin: 0 auto; }
        .section-title { font-size: 32px; font-weight: 700; text-align: center; margin-bottom: 48px; background: linear-gradient(135deg,#fff 0%,#6ab4ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .edu-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; }
        .edu-card { background: rgba(106,180,255,0.05); border: 1px solid rgba(106,180,255,0.12); border-radius: 16px; padding: 28px; transition: all 0.4s ease; position: relative; overflow: hidden; }
        .edu-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg,#6ab4ff,transparent); }
        .edu-card:hover { border-color: rgba(106,180,255,0.3); transform: translateY(-4px); }
        .edu-card .school { font-size: 16px; font-weight: 700; color: #e0e8ff; margin-bottom: 6px; }
        .edu-card .degree { font-size: 13px; color: #6ab4ff; margin-bottom: 6px; }
        .edu-card .time { font-size: 12px; color: #6a8ab8; margin-bottom: 10px; }
        .edu-card .highlight { font-size: 12px; color: #8aa8d8; line-height: 1.6; }
        .timeline { position: relative; padding-left: 24px; }
        .timeline::before { content: ''; position: absolute; left: 6px; top: 0; bottom: 0; width: 2px; background: linear-gradient(180deg,#6ab4ff,rgba(106,180,255,0.1)); }
        .timeline-item { position: relative; margin-bottom: 40px; padding-left: 28px; }
        .timeline-item::before { content: ''; position: absolute; left: -22px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: #6ab4ff; box-shadow: 0 0 10px rgba(106,180,255,0.5); }
        .timeline-item:last-child { margin-bottom: 0; }
        .job-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; flex-wrap: wrap; gap: 6px; }
        .job-title { font-size: 18px; font-weight: 700; color: #e0e8ff; }
        .job-company { font-size: 14px; color: #6ab4ff; }
        .job-time { font-size: 12px; color: #6a8ab8; font-family: 'Courier New', monospace; }
        .job-desc { background: rgba(106,180,255,0.05); border: 1px solid rgba(106,180,255,0.1); border-radius: 12px; padding: 20px; }
        .job-desc li { font-size: 13px; color: #a0b8e0; line-height: 1.7; margin-bottom: 6px; padding-left: 18px; position: relative; }
        .job-desc li::before { content: '▸'; position: absolute; left: 0; color: #6ab4ff; }
        .job-desc li:last-child { margin-bottom: 0; }
        .job-desc li strong { color: #c0d4f0; }
        .project-card { background: rgba(106,180,255,0.05); border: 1px solid rgba(106,180,255,0.12); border-radius: 16px; padding: 32px; margin-bottom: 20px; transition: all 0.4s ease; }
        .project-card:hover { border-color: rgba(106,180,255,0.3); box-shadow: 0 15px 30px rgba(106,180,255,0.08); }
        .project-card:last-child { margin-bottom: 0; }
        .project-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; flex-wrap: wrap; gap: 6px; }
        .project-name { font-size: 17px; font-weight: 700; color: #e0e8ff; line-height: 1.4; }
        .project-badge { display: inline-block; background: rgba(106,180,255,0.15); color: #6ab4ff; padding: 3px 10px; border-radius: 10px; font-size: 11px; white-space: nowrap; }
        .project-time { font-size: 12px; color: #6a8ab8; }
        .project-desc li { font-size: 13px; color: #a0b8e0; line-height: 1.7; margin-bottom: 6px; padding-left: 18px; position: relative; }
        .project-desc li::before { content: '▸'; position: absolute; left: 0; color: #6ab4ff; }
        .project-desc li strong { color: #c0d4f0; }
        .works-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 20px; }
        .work-card { background: rgba(106,180,255,0.05); border: 1px solid rgba(106,180,255,0.12); border-radius: 16px; overflow: hidden; transition: all 0.4s ease; }
        .work-card:hover { border-color: rgba(106,180,255,0.3); transform: translateY(-4px); box-shadow: 0 15px 30px rgba(106,180,255,0.08); }
        .work-preview { height: 140px; background: linear-gradient(135deg,rgba(106,180,255,0.1),rgba(106,180,255,0.05)); display: flex; align-items: center; justify-content: center; font-size: 40px; }
        .work-body { padding: 24px; }
        .work-body h3 { font-size: 16px; color: #e0e8ff; margin-bottom: 6px; }
        .work-body .work-link { font-size: 12px; color: #6ab4ff; text-decoration: none; word-break: break-all; display: block; margin-bottom: 10px; }
        .work-body .work-link:hover { text-decoration: underline; }
        .work-body p { font-size: 13px; color: #8aa8d8; line-height: 1.6; }
        .work-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
        .work-tag { background: rgba(106,180,255,0.1); color: #6ab4ff; padding: 3px 8px; border-radius: 6px; font-size: 11px; }
        .skills-self-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
        .skill-block h3 { font-size: 18px; color: #e0e8ff; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid rgba(106,180,255,0.2); }
        .skill-item { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px; }
        .skill-item .icon { font-size: 18px; margin-top: 2px; flex-shrink: 0; }
        .skill-item .text { font-size: 13px; color: #a0b8e0; line-height: 1.6; }
        .skill-item .text strong { color: #c0d4f0; }
        .self-eval { background: rgba(106,180,255,0.05); border: 1px solid rgba(106,180,255,0.12); border-radius: 16px; padding: 28px; }
        .self-eval h3 { font-size: 18px; color: #e0e8ff; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid rgba(106,180,255,0.2); }
        .self-eval p { font-size: 14px; color: #a0b8e0; line-height: 1.8; }
        .self-eval .tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
        .self-eval .tag { background: rgba(106,180,255,0.1); border: 1px solid rgba(106,180,255,0.2); color: #6ab4ff; padding: 5px 12px; border-radius: 16px; font-size: 12px; }
        .footer { padding: 48px 5% 32px; text-align: center; border-top: 1px solid rgba(106,180,255,0.1); }
        .footer .contact-footer { display: flex; justify-content: center; gap: 24px; margin-bottom: 24px; flex-wrap: wrap; }
        .footer .contact-footer a { color: #6ab4ff; text-decoration: none; font-size: 13px; transition: all 0.3s ease; }
        .footer .contact-footer a:hover { text-shadow: 0 0 10px rgba(106,180,255,0.5); }
        .footer p { color: #4a6a98; font-size: 12px; }
        .photo-upload-panel { position: fixed; top: 50%; left: 50%; transform: translate(-50%,-50%); background: rgba(10,15,26,0.95); border: 1px solid rgba(106,180,255,0.3); border-radius: 20px; padding: 32px; z-index: 200; display: none; text-align: center; backdrop-filter: blur(20px); min-width: 320px; }
        .photo-upload-panel.show { display: block; }
        .photo-upload-panel h2 { font-size: 18px; color: #e0e8ff; margin-bottom: 16px; }
        .photo-upload-panel input[type="file"] { display: none; }
        .upload-btn { display: inline-block; padding: 12px 32px; background: rgba(106,180,255,0.15); border: 1px solid rgba(106,180,255,0.4); color: #6ab4ff; border-radius: 12px; font-size: 14px; cursor: pointer; transition: all 0.3s ease; margin: 8px; }
        .upload-btn:hover { background: rgba(106,180,255,0.25); box-shadow: 0 0 20px rgba(106,180,255,0.2); }
        .photo-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-top: 16px; max-height: 200px; overflow-y: auto; }
        .photo-grid img { width: 80px; height: 80px; object-fit: cover; border-radius: 8px; border: 1px solid rgba(106,180,255,0.3); cursor: pointer; transition: all 0.3s ease; }
        .photo-grid img:hover { transform: scale(1.1); border-color: #6ab4ff; }
        .close-panel { position: absolute; top: 12px; right: 16px; color: #6a8ab8; cursor: pointer; font-size: 20px; line-height: 1; }
        .close-panel:hover { color: #e0e8ff; }
        .photo-focus-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 150; display: none; align-items: center; justify-content: center; }
        .photo-focus-overlay.show { display: flex; }
        .photo-focus-overlay img { max-width: 70vw; max-height: 70vh; border-radius: 16px; border: 2px solid rgba(106,180,255,0.5); box-shadow: 0 0 60px rgba(106,180,255,0.3); }
        .photo-focus-info { position: absolute; bottom: 15vh; left: 50%; transform: translateX(-50%); color: #a0b8e0; font-size: 14px; text-align: center; }
        .scroll-reveal { opacity: 0; transform: translateY(30px); transition: all 0.8s cubic-bezier(0.16,1,0.3,1); }
        .scroll-reveal.visible { opacity: 1; transform: translateY(0); }
        @media (max-width: 768px) {
            .hero-section { flex-direction: column; padding-top: 60px; padding-bottom: 40px; min-height: auto; }
            .intro-card { width: 100%; margin: 0 auto; margin-top: 65vh; padding: 24px; border-radius: 16px; }
            .intro-card h1 { font-size: 28px; }
            .intro-card .subtitle { font-size: 14px; }
            .intro-card .meta { font-size: 12px; }
            .intro-card p { font-size: 13px; }
            .contact-row { flex-direction: column; gap: 8px; }
            .contact-item { font-size: 12px; }
            .download-btn { width: 100%; justify-content: center; margin-top: 12px; }
            .section-wrapper { padding: 60px 4%; }
            .section-title { font-size: 24px; margin-bottom: 32px; }
            .edu-grid { grid-template-columns: 1fr; gap: 16px; }
            .edu-card { padding: 20px; }
            .edu-card .school { font-size: 15px; }
            .timeline { padding-left: 16px; }
            .timeline::before { left: 4px; }
            .timeline-item { padding-left: 20px; margin-bottom: 32px; }
            .timeline-item::before { left: -16px; width: 8px; height: 8px; }
            .job-header { flex-direction: column; gap: 4px; }
            .job-title { font-size: 16px; }
            .job-company { font-size: 13px; }
            .job-time { font-size: 11px; }
            .job-desc { padding: 16px; }
            .job-desc li { font-size: 12px; padding-left: 14px; }
            .project-card { padding: 24px; }
            .project-header { flex-direction: column; gap: 4px; }
            .project-name { font-size: 15px; }
            .project-desc li { font-size: 12px; padding-left: 14px; }
            .works-grid { grid-template-columns: 1fr; gap: 16px; }
            .work-preview { height: 120px; font-size: 36px; }
            .work-body { padding: 20px; }
            .work-body h3 { font-size: 15px; }
            .work-body p { font-size: 12px; }
            .skills-self-grid { grid-template-columns: 1fr; gap: 24px; }
            .skill-block h3 { font-size: 16px; }
            .skill-item .text { font-size: 12px; }
            .self-eval { padding: 20px; }
            .self-eval h3 { font-size: 16px; }
            .self-eval p { font-size: 13px; }
            .self-eval .tag { font-size: 11px; padding: 4px 10px; }
            .footer .contact-footer { flex-direction: column; gap: 12px; }
            .footer .contact-footer a { font-size: 12px; }
            .gesture-indicator, .state-badge, .particle-count { display: none; }
            .corner-frame.br { bottom: 10px; right: 10px; }
        }
        @media (max-width: 480px) {
            .intro-card { margin-top: 60vh; padding: 20px; }
            .intro-card h1 { font-size: 26px; }
            .boot-text { font-size: 12px; letter-spacing: 1px; }
        }
    </style>
</head>
<body>
'''

# ===== PART 2: New HTML body elements (boot, scan, corners, canvas, webcam, HUD) =====
html_body = '''
    <div class="boot-sequence" id="bootSequence">
        <div class="boot-text" style="animation: fadeIn 0.3s 0.2s forwards">INITIALIZING NEURAL NETWORK...</div>
        <div class="boot-text" style="animation: fadeIn 0.3s 0.6s forwards">CONNECTING TO DATA ENTITY...</div>
        <div class="boot-text" style="animation: fadeIn 0.3s 1.0s forwards">SYNCHRONIZING HOLOGRAM...</div>
        <div class="boot-text" style="animation: fadeIn 0.3s 1.4s forwards">ENTITY MANIFESTATION COMPLETE</div>
        <div class="boot-progress">
            <div class="boot-progress-fill" style="animation: fillProgress 2s 0.5s ease-out forwards"></div>
        </div>
    </div>
    <div class="scan-line"></div>
    <div class="corner-frame tl"></div>
    <div class="corner-frame tr"></div>
    <div class="corner-frame bl"></div>
    <div class="corner-frame br"></div>
    <div id="canvas-container"></div>
    <video id="webcam-preview" playsinline autoplay muted></video>
    <canvas id="hand-canvas"></canvas>
    <div class="hud-overlay">
        <div class="hud-title">&#9670; DATA ENTITY NEURAL INTERFACE &#9670;</div>
        <div class="hud-status" id="statusText">等待摄像头权限...</div>
        <div class="state-badge">
            <h3>&#9670; 当前状态 &#9670;</h3>
            <div class="state-value" id="stateValue">合拢态</div>
        </div>
        <div class="gesture-indicator">
            <h3>&#9670; 手势控制 &#9670;</h3>
            <div class="gesture-item" id="gest-fist"><span class="gesture-icon">✊</span><span>握拳 - 合拢态</span></div>
            <div class="gesture-item" id="gest-open"><span class="gesture-icon">🖐</span><span>张开五指 - 散开态</span></div>
            <div class="gesture-item" id="gest-rotate"><span class="gesture-icon">👋</span><span>手旋转 - 相机旋转</span></div>
            <div class="gesture-item" id="gest-grab"><span class="gesture-icon">👌</span><span>抓取 - 照片放大</span></div>
        </div>
        <div class="particle-count" id="particleCount">PARTICLES: 0 | FPS: 0</div>
    </div>
'''

# ===== PART 3: Original content layer (personal info) - extracted from backup =====
with open(r'C:\Users\AQQW\Desktop\index_backup.html', 'r', encoding='utf-8') as f:
    orig_text = f.read()

# Extract content layer from original
import re
content_match = re.search(r'<div class="content-layer">.*?</div>\s*</div>\s*<footer', orig_text, re.DOTALL)
if content_match:
    print("Found content-layer block")
else:
    print("Could not find content-layer, trying alternate")
    content_match = re.search(r'<div class="content-layer">.*?</footer>', orig_text, re.DOTALL)

print(f"Content match: {content_match is not None}")

# For simplicity, extract sections individually from original
# Find and extract all sections between <div class="content-layer"> and </footer>
start_idx = orig_text.find('<div class="content-layer">')
end_idx = orig_text.rfind('</footer>') + len('</footer>')
content_section = orig_text[start_idx:end_idx]

# Now also extract the photo panels after footer
photo_start = orig_text.find('<div class="photo-upload-panel"', end_idx)
photo_section = ""
if photo_start > 0:
    photo_section = orig_text[photo_start:]

print(f"Content section: {len(content_section)} chars")
print(f"Photo section: {len(photo_section)} chars")

# ===== PART 4: JavaScript (particle system + hand tracking) =====
js_part = '''
    <script>
    const STATE = { COLLAPSED: 0, SCATTERED: 1, PHOTO_FOCUS: 2 };
    let currentState = STATE.COLLAPSED, targetState = STATE.COLLAPSED, stateTransition = 0;
    let photos = [], photoTextures = [], photoMeshes = [], selectedPhotoIndex = -1;
    let gestureConfidence = 0, lastGesture = null, gestureHoldTime = 0;
    const GESTURE_THRESHOLD = 10;
    let cameraAngleX = 0, cameraAngleY = 0, targetCameraAngleX = 0, targetCameraAngleY = 0;
    let cameraRadius = 35, targetCameraRadius = 35;
    let particleCount = 5000;
    let particlesGeometry, particlesMaterial, particlesMesh;
    let particlePositions, particleTargetPositions, particleVelocities;
    let particleColors, particleSizes;
    let particleOriginalPositions = [], particleScatteredPositions = [];
    let dataElements = [];
    const ELEMENT_TYPES = ['sphere', 'cube', 'cylinder', 'torus'];
    let scene, camera, renderer, clock;
    let ambientLight, pointLight1, pointLight2, pointLight3;
    let hands, cameraUtils;
    let videoElement, canvasElement, canvasCtx;
    let handLandmarks = null, isHandDetected = false;
    let frameCount = 0, lastFpsTime = 0, fps = 0;

    setTimeout(() => {
        const boot = document.getElementById('bootSequence');
        boot.style.transition = 'opacity 1s ease'; boot.style.opacity = '0';
        setTimeout(() => { boot.remove(); initApp(); }, 1000);
    }, 3500);

    function initThreeJS() {
        const container = document.getElementById('canvas-container');
        scene = new THREE.Scene(); scene.fog = new THREE.FogExp2(0x0a0f1a, 0.008);
        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 35);
        const isMobile = window.innerWidth <= 768 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        renderer = new THREE.WebGLRenderer({ antialias: !isMobile, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1 : 2));
        renderer.setClearColor(0x0a0f1a, 1);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        container.appendChild(renderer.domElement);
        clock = new THREE.Clock();
        ambientLight = new THREE.AmbientLight(0x1a2a4a, 0.3); scene.add(ambientLight);
        pointLight1 = new THREE.PointLight(0x6ab4ff, 2, 100); pointLight1.position.set(10, 20, 10); scene.add(pointLight1);
        pointLight2 = new THREE.PointLight(0xff6b6b, 1.5, 80); pointLight2.position.set(-15, 10, -10); scene.add(pointLight2);
        pointLight3 = new THREE.PointLight(0xffd700, 1.2, 60); pointLight3.position.set(0, -10, 15); scene.add(pointLight3);
        const dirLight = new THREE.DirectionalLight(0x4a6a9a, 0.5); dirLight.position.set(5, 10, 5); scene.add(dirLight);
        createParticleSystem(); createDataElements(); createEnvironment();
        window.addEventListener('resize', onWindowResize);
    }

    function createParticleSystem() {
        particleCount = 6000;
        particlesGeometry = new THREE.BufferGeometry();
        particlePositions = new Float32Array(particleCount * 3);
        particleTargetPositions = new Float32Array(particleCount * 3);
        particleVelocities = new Float32Array(particleCount * 3);
        particleColors = new Float32Array(particleCount * 3);
        particleSizes = new Float32Array(particleCount);
        const colorPalette = [
            new THREE.Color(0x6ab4ff), new THREE.Color(0xffd700),
            new THREE.Color(0xff6b6b), new THREE.Color(0x4ecdc4),
            new THREE.Color(0xffa07a), new THREE.Color(0x9370db)
        ];
        for (let i = 0; i < particleCount; i++) {
            const angle = Math.random() * Math.PI * 2, height = Math.random() * 25 - 5;
            const radiusAtHeight = (25 - height) * 0.15 * Math.random();
            const x = Math.cos(angle) * radiusAtHeight, y = height, z = Math.sin(angle) * radiusAtHeight;
            particlePositions[i*3] = x; particlePositions[i*3+1] = y; particlePositions[i*3+2] = z;
            particleTargetPositions[i*3] = x; particleTargetPositions[i*3+1] = y; particleTargetPositions[i*3+2] = z;
            particleVelocities[i*3] = 0; particleVelocities[i*3+1] = 0; particleVelocities[i*3+2] = 0;
            particleOriginalPositions.push({x, y, z});
            const scatterRadius = 40;
            particleScatteredPositions.push({
                x: (Math.random() - 0.5) * scatterRadius * 2,
                y: (Math.random() - 0.5) * scatterRadius * 2,
                z: (Math.random() - 0.5) * scatterRadius * 2
            });
            const color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
            particleColors[i*3] = color.r; particleColors[i*3+1] = color.g; particleColors[i*3+2] = color.b;
            particleSizes[i] = Math.random() * 2 + 0.5;
        }
        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
        particlesGeometry.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
        particlesGeometry.setAttribute('size', new THREE.BufferAttribute(particleSizes, 1));
        const vertexShader = \`attribute float size; varying vec3 vColor; varying float vAlpha; uniform float uTime;
            void main() { vColor = color; vec3 pos = position;
            pos.y += sin(uTime * 0.5 + position.x * 0.1) * 0.3;
            pos.x += cos(uTime * 0.3 + position.z * 0.1) * 0.2;
            vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
            gl_PointSize = size * (300.0 / -mvPosition.z); gl_Position = projectionMatrix * mvPosition;
            vAlpha = 0.6 + 0.4 * sin(uTime + position.x); }\`;
        const fragmentShader = \`varying vec3 vColor; varying float vAlpha;
            void main() { float dist = length(gl_PointCoord - vec2(0.5)); if (dist > 0.5) discard;
            float glow = 1.0 - smoothstep(0.0, 0.5, dist); glow = pow(glow, 1.5);
            vec3 finalColor = vColor * glow * 2.0; float alpha = glow * vAlpha;
            gl_FragColor = vec4(finalColor, alpha); }\`;
        particlesMaterial = new THREE.ShaderMaterial({
            vertexShader, fragmentShader, uniforms: { uTime: { value: 0 } },
            vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false
        });
        particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particlesMesh);
    }

    function createDataElements() {
        const elementCount = 80;
        const geometries = [
            new THREE.SphereGeometry(0.4, 16, 16), new THREE.BoxGeometry(0.6, 0.6, 0.6),
            new THREE.CylinderGeometry(0.2, 0.2, 0.8, 12), new THREE.TorusGeometry(0.3, 0.1, 8, 16)
        ];
        const materials = [
            new THREE.MeshStandardMaterial({ color: 0x6ab4ff, metalness: 0.8, roughness: 0.2, emissive: 0x1a4a8a, emissiveIntensity: 0.3 }),
            new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 0.9, roughness: 0.1, emissive: 0x8a6a00, emissiveIntensity: 0.3 }),
            new THREE.MeshStandardMaterial({ color: 0xff6b6b, metalness: 0.7, roughness: 0.3, emissive: 0x8a2a2a, emissiveIntensity: 0.2 }),
            new THREE.MeshStandardMaterial({ color: 0x4ecdc4, metalness: 0.6, roughness: 0.4, emissive: 0x1a6a6a, emissiveIntensity: 0.2 })
        ];
        for (let i = 0; i < elementCount; i++) {
            const typeIdx = Math.floor(Math.random() * 4);
            const geo = geometries[typeIdx], mat = materials[typeIdx].clone();
            const mesh = new THREE.Mesh(geo, mat);
            const angle = Math.random() * Math.PI * 2, height = Math.random() * 22 - 3;
            const radiusAtHeight = (22 - height) * 0.18 * (0.5 + Math.random() * 0.5);
            mesh.position.set(Math.cos(angle) * radiusAtHeight, height, Math.sin(angle) * radiusAtHeight);
            mesh.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
            mesh.userData = {
                originalPos: mesh.position.clone(), originalRot: mesh.rotation.clone(),
                scatteredPos: new THREE.Vector3((Math.random() - 0.5) * 50, (Math.random() - 0.5) * 50, (Math.random() - 0.5) * 50),
                scatteredRot: new THREE.Vector3(Math.random() * Math.PI * 2, Math.random() * Math.PI * 2, Math.random() * Math.PI * 2),
                type: ELEMENT_TYPES[typeIdx],
                rotationSpeed: { x: (Math.random() - 0.5) * 0.02, y: (Math.random() - 0.5) * 0.02, z: (Math.random() - 0.5) * 0.02 },
                floatOffset: Math.random() * Math.PI * 2, floatSpeed: 0.5 + Math.random() * 1.5
            };
            scene.add(mesh); dataElements.push(mesh);
        }
    }

    function createEnvironment() {
        const ringGeometry = new THREE.RingGeometry(8, 12, 64);
        const ringMaterial = new THREE.MeshBasicMaterial({ color: 0x6ab4ff, transparent: true, opacity: 0.1, side: THREE.DoubleSide });
        const ring = new THREE.Mesh(ringGeometry, ringMaterial); ring.rotation.x = -Math.PI / 2; ring.position.y = -8; scene.add(ring);
        for (let i = 0; i < 5; i++) {
            const rGeo = new THREE.TorusGeometry(3 + i * 2, 0.03, 8, 64);
            const rMat = new THREE.MeshBasicMaterial({ color: i % 2 === 0 ? 0x6ab4ff : 0xffd700, transparent: true, opacity: 0.15 });
            const rMesh = new THREE.Mesh(rGeo, rMat); rMesh.rotation.x = Math.PI / 2 + (Math.random() - 0.5) * 0.5;
            rMesh.position.y = -5 + i * 3; rMesh.userData = { rotationSpeed: 0.002 * (i % 2 === 0 ? 1 : -1) }; scene.add(rMesh);
        }
        const starCount = 2000, starGeo = new THREE.BufferGeometry();
        const starPos = new Float32Array(starCount * 3), starColors = new Float32Array(starCount * 3);
        for (let i = 0; i < starCount; i++) {
            starPos[i*3] = (Math.random() - 0.5) * 200; starPos[i*3+1] = (Math.random() - 0.5) * 200; starPos[i*3+2] = (Math.random() - 0.5) * 200;
            const brightness = 0.5 + Math.random() * 0.5; starColors[i*3] = brightness; starColors[i*3+1] = brightness * 0.9; starColors[i*3+2] = brightness;
        }
        starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3)); starGeo.setAttribute('color', new THREE.BufferAttribute(starColors, 3));
        const starMat = new THREE.PointsMaterial({ size: 0.5, vertexColors: true, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending });
        const stars = new THREE.Points(starGeo, starMat); scene.add(stars);
    }

    function handlePhotoUpload(event) {
        const files = event.target.files, grid = document.getElementById('photoGrid');
        for (let file of files) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgData = e.target.result; photos.push(imgData);
                const img = document.createElement('img'); img.src = imgData;
                img.onclick = () => focusPhoto(photos.length - 1); grid.appendChild(img);
                createPhotoMesh(imgData);
            }; reader.readAsDataURL(file);
        }
    }

    function createPhotoMesh(imgData) {
        const textureLoader = new THREE.TextureLoader();
        textureLoader.load(imgData, (texture) => {
            const aspect = texture.image.width / texture.image.height, width = 3, height = width / aspect;
            const geometry = new THREE.PlaneGeometry(width, height);
            const material = new THREE.MeshBasicMaterial({ map: texture, transparent: true, opacity: 0.9, side: THREE.DoubleSide });
            const mesh = new THREE.Mesh(geometry, material);
            const angle = Math.random() * Math.PI * 2, h = Math.random() * 20 - 2, radius = (20 - h) * 0.2;
            mesh.position.set(Math.cos(angle) * radius, h, Math.sin(angle) * radius);
            mesh.rotation.y = Math.random() * Math.PI * 2;
            mesh.userData = {
                originalPos: mesh.position.clone(), originalRot: mesh.rotation.clone(),
                scatteredPos: new THREE.Vector3((Math.random() - 0.5) * 45, (Math.random() - 0.5) * 45, (Math.random() - 0.5) * 45),
                scatteredRot: new THREE.Vector3(Math.random() * Math.PI, Math.random() * Math.PI * 2, Math.random() * Math.PI),
                isPhoto: true, photoIndex: photoMeshes.length, floatOffset: Math.random() * Math.PI * 2
            };
            scene.add(mesh); photoMeshes.push(mesh); photoTextures.push(texture);
        });
    }

    function focusPhoto(index) {
        if (index < 0 || index >= photoMeshes.length) return;
        selectedPhotoIndex = index; targetState = STATE.PHOTO_FOCUS;
        const img = document.getElementById('focusImage'); img.src = photos[index];
        document.getElementById('photoFocus').classList.add('show');
    }

    function closePhotoFocus() {
        document.getElementById('photoFocus').classList.remove('show');
        if (currentState === STATE.PHOTO_FOCUS) targetState = STATE.SCATTERED; selectedPhotoIndex = -1;
    }

    function closePhotoPanel() { document.getElementById('photoPanel').classList.remove('show'); }

    function initMediaPipe() {
        videoElement = document.getElementById('webcam-preview');
        canvasElement = document.getElementById('hand-canvas');
        canvasCtx = canvasElement.getContext('2d');
        canvasElement.width = 200; canvasElement.height = 150;
        hands = new Hands({ locateFile: (file) => \`https://cdn.jsdelivr.net/npm/@mediapipe/hands/\${file}\` });
        hands.setOptions({ maxNumHands: 1, modelComplexity: 1, minDetectionConfidence: 0.5, minTrackingConfidence: 0.5 });
        hands.onResults(onHandResults);
        cameraUtils = new Camera(videoElement, {
            onFrame: async () => { await hands.send({ image: videoElement }); }, width: 320, height: 240
        });
        cameraUtils.start().then(() => { document.getElementById('statusText').textContent = '摄像头已启动 - 请展示手势'; }).
            catch(err => { console.error('Camera error:', err); document.getElementById('statusText').textContent = '摄像头访问失败 - 请检查权限'; });
    }

    function onHandResults(results) {
        canvasCtx.save(); canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            isHandDetected = true; handLandmarks = results.multiHandLandmarks[0];
            drawConnectors(canvasCtx, handLandmarks, HAND_CONNECTIONS, { color: '#6ab4ff', lineWidth: 2 });
            drawLandmarks(canvasCtx, handLandmarks, { color: '#ff6b6b', lineWidth: 1, radius: 2 });
            const gesture = detectGesture(handLandmarks); processGesture(gesture);
            document.getElementById('statusText').textContent = \`检测到: \${getGestureName(gesture)}\`;
        } else { isHandDetected = false; handLandmarks = null; document.getElementById('statusText').textContent = '等待手势...'; resetGestureIndicators(); }
        canvasCtx.restore();
    }

    function detectGesture(landmarks) {
        const tips = [8, 12, 16, 20], pips = [6, 10, 14, 18]; let extendedFingers = 0;
        for (let i = 0; i < 4; i++) { if (landmarks[tips[i]].y < landmarks[pips[i]].y) extendedFingers++; }
        const thumbTip = landmarks[4], thumbIp = landmarks[3], thumbExtended = thumbTip.x < thumbIp.x;
        const thumbIndexDist = Math.sqrt(Math.pow(landmarks[4].x - landmarks[8].x, 2) + Math.pow(landmarks[4].y - landmarks[8].y, 2));
        const isPinching = thumbIndexDist < 0.08;
        const wrist = landmarks[0], middleMcp = landmarks[9], handRotation = Math.atan2(middleMcp.y - wrist.y, middleMcp.x - wrist.x);
        return { extendedFingers, thumbExtended, isPinching, handRotation, thumbIndexDist, landmarks };
    }

    function getGestureName(gesture) {
        if (gesture.isPinching) return '抓取 (Pinch)';
        if (gesture.extendedFingers === 0) return '握拳 (Fist)';
        if (gesture.extendedFingers === 5 || (gesture.extendedFingers === 4 && gesture.thumbExtended)) return '张开五指 (Open)';
        if (gesture.extendedFingers >= 3) return '张开手掌 (Open Palm)';
        return '其他手势';
    }

    function processGesture(gesture) {
        resetGestureIndicators();
        if (gesture.isPinching) {
            document.getElementById('gest-grab').classList.add('active');
            if (currentState === STATE.SCATTERED && photoMeshes.length > 0) {
                const handX = (0.5 - gesture.landmarks[9].x) * 60, handY = (0.5 - gesture.landmarks[9].y) * 40;
                let nearestIdx = -1, nearestDist = Infinity;
                photoMeshes.forEach((mesh, idx) => { const dist = Math.sqrt(Math.pow(mesh.position.x - handX, 2) + Math.pow(mesh.position.y - handY, 2)); if (dist < nearestDist) { nearestDist = dist; nearestIdx = idx; } });
                if (nearestIdx >= 0 && nearestDist < 10) focusPhoto(nearestIdx);
            } return;
        }
        if (gesture.extendedFingers === 0) { document.getElementById('gest-fist').classList.add('active'); targetState = STATE.COLLAPSED; gestureHoldTime++; }
        else if (gesture.extendedFingers >= 4) {
            document.getElementById('gest-open').classList.add('active'); targetState = STATE.SCATTERED; gestureHoldTime++;
            if (currentState === STATE.SCATTERED || currentState === STATE.PHOTO_FOCUS) {
                const handX = gesture.landmarks[9].x, handY = gesture.landmarks[9].y;
                targetCameraAngleY = (0.5 - handX) * Math.PI; targetCameraAngleX = (0.5 - handY) * Math.PI * 0.5;
            }
        } else if (gesture.extendedFingers >= 2 && gesture.extendedFingers < 4) {
            document.getElementById('gest-rotate').classList.add('active');
            const handX = gesture.landmarks[9].x, handY = gesture.landmarks[9].y;
            targetCameraAngleY += (0.5 - handX) * 0.02; targetCameraAngleX += (0.5 - handY) * 0.01;
        }
    }

    function resetGestureIndicators() { document.querySelectorAll('.gesture-item').forEach(el => el.classList.remove('active')); }

    function updateState(deltaTime) {
        const transitionSpeed = 1.5 * deltaTime;
        if (targetState !== currentState) {
            if (targetState === STATE.COLLAPSED) { stateTransition -= transitionSpeed; if (stateTransition <= 0) { stateTransition = 0; currentState = STATE.COLLAPSED; } }
            else if (targetState === STATE.SCATTERED) { stateTransition += transitionSpeed; if (stateTransition >= 1) { stateTransition = 1; currentState = STATE.SCATTERED; } }
            else if (targetState === STATE.PHOTO_FOCUS) { stateTransition += transitionSpeed; if (stateTransition >= 1) { stateTransition = 1; currentState = STATE.PHOTO_FOCUS; } }
        }
        const stateNames = ['合拢态', '散开态', '照片放大态'];
        document.getElementById('stateValue').textContent = stateNames[currentState];
        cameraAngleX += (targetCameraAngleX - cameraAngleX) * 0.05;
        cameraAngleY += (targetCameraAngleY - cameraAngleY) * 0.05;
        cameraRadius += (targetCameraRadius - cameraRadius) * 0.05;
        camera.position.x = Math.sin(cameraAngleY) * Math.cos(cameraAngleX) * cameraRadius;
        camera.position.y = Math.sin(cameraAngleX) * cameraRadius + 5;
        camera.position.z = Math.cos(cameraAngleY) * Math.cos(cameraAngleX) * cameraRadius;
        camera.lookAt(0, 5, 0);
    }

    function updateParticles(time, deltaTime) {
        const positions = particlesGeometry.attributes.position.array;
        const t = stateTransition, easeT = t * t * (3 - 2 * t);
        for (let i = 0; i < particleCount; i++) {
            const orig = particleOriginalPositions[i], scatter = particleScatteredPositions[i];
            const targetX = orig.x * (1 - easeT) + scatter.x * easeT;
            const targetY = orig.y * (1 - easeT) + scatter.y * easeT;
            const targetZ = orig.z * (1 - easeT) + scatter.z * easeT;
            const floatY = Math.sin(time * 0.5 + i * 0.1) * 0.3 * easeT;
            const floatX = Math.cos(time * 0.3 + i * 0.15) * 0.2 * easeT;
            positions[i*3] += (targetX + floatX - positions[i*3]) * 0.05;
            positions[i*3+1] += (targetY + floatY - positions[i*3+1]) * 0.05;
            positions[i*3+2] += (targetZ - positions[i*3+2]) * 0.05;
        }
        particlesGeometry.attributes.position.needsUpdate = true;
        particlesMaterial.uniforms.uTime.value = time;
    }

    function updateDataElements(time, deltaTime) {
        const t = stateTransition, easeT = t * t * (3 - 2 * t);
        dataElements.forEach((mesh) => {
            const data = mesh.userData;
            if (currentState === STATE.PHOTO_FOCUS && selectedPhotoIndex >= 0) return;
            const targetX = data.originalPos.x * (1 - easeT) + data.scatteredPos.x * easeT;
            const targetY = data.originalPos.y * (1 - easeT) + data.scatteredPos.y * easeT;
            const targetZ = data.originalPos.z * (1 - easeT) + data.scatteredPos.z * easeT;
            const floatY = Math.sin(time * data.floatSpeed + data.floatOffset) * 0.5 * easeT;
            mesh.position.x += (targetX - mesh.position.x) * 0.03;
            mesh.position.y += (targetY + floatY - mesh.position.y) * 0.03;
            mesh.position.z += (targetZ - mesh.position.z) * 0.03;
            const targetRotX = data.originalRot.x * (1 - easeT) + data.scatteredRot.x * easeT;
            const targetRotY = data.originalRot.y * (1 - easeT) + data.scatteredRot.y * easeT;
            const targetRotZ = data.originalRot.z * (1 - easeT) + data.scatteredRot.z * easeT;
            mesh.rotation.x += (targetRotX - mesh.rotation.x) * 0.03 + data.rotationSpeed.x * easeT;
            mesh.rotation.y += (targetRotY - mesh.rotation.y) * 0.03 + data.rotationSpeed.y * easeT;
            mesh.rotation.z += (targetRotZ - mesh.rotation.z) * 0.03 + data.rotationSpeed.z * easeT;
        });
    }

    function updatePhotoMeshes(time, deltaTime) {
        const t = stateTransition, easeT = t * t * (3 - 2 * t);
        photoMeshes.forEach((mesh, i) => {
            const data = mesh.userData;
            if (currentState === STATE.PHOTO_FOCUS && i === selectedPhotoIndex) {
                mesh.position.x += (0 - mesh.position.x) * 0.05; mesh.position.y += (5 - mesh.position.y) * 0.05; mesh.position.z += (15 - mesh.position.z) * 0.05;
                mesh.rotation.x += (0 - mesh.rotation.x) * 0.05; mesh.rotation.y += (0 - mesh.rotation.y) * 0.05; mesh.rotation.z += (0 - mesh.rotation.z) * 0.05;
                mesh.scale.setScalar(1 + (3 - 1) * 0.05); mesh.material.opacity = 1;
            } else if (currentState === STATE.PHOTO_FOCUS) { mesh.material.opacity = Math.max(0, mesh.material.opacity - 0.05); }
            else {
                const targetX = data.originalPos.x * (1 - easeT) + data.scatteredPos.x * easeT;
                const targetY = data.originalPos.y * (1 - easeT) + data.scatteredPos.y * easeT;
                const targetZ = data.originalPos.z * (1 - easeT) + data.scatteredPos.z * easeT;
                const floatY = Math.sin(time * 0.8 + data.floatOffset) * 0.3 * easeT;
                mesh.position.x += (targetX - mesh.position.x) * 0.03; mesh.position.y += (targetY + floatY - mesh.position.y) * 0.03; mesh.position.z += (targetZ - mesh.position.z) * 0.03;
                mesh.rotation.y += (data.scatteredRot.y * easeT - mesh.rotation.y) * 0.03; mesh.scale.setScalar(1); mesh.material.opacity = 0.9;
            }
        });
    }

    function updateLights(time) {
        pointLight1.position.x = Math.sin(time * 0.5) * 15; pointLight1.position.z = Math.cos(time * 0.5) * 15;
        pointLight2.position.x = Math.sin(time * 0.3 + 2) * 12; pointLight2.position.z = Math.cos(time * 0.3 + 2) * 12;
        pointLight3.position.y = Math.sin(time * 0.4) * 8 - 5;
    }

    function animate() {
        requestAnimationFrame(animate);
        const time = clock.getElapsedTime(), deltaTime = clock.getDelta();
        updateState(deltaTime); updateParticles(time, deltaTime); updateDataElements(time, deltaTime);
        updatePhotoMeshes(time, deltaTime); updateLights(time); particlesMesh.rotation.y = time * 0.05; renderer.render(scene, camera);
        frameCount++;
        if (time - lastFpsTime >= 1) { fps = frameCount; frameCount = 0; lastFpsTime = time;
            document.getElementById('particleCount').textContent = \`PARTICLES: \${particleCount} | ELEMENTS: \${dataElements.length} | PHOTOS: \${photoMeshes.length} | FPS: \${fps}\`;
        }
    }

    function onWindowResize() { camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight); }

    document.addEventListener('keydown', (e) => {
        switch(e.key) { case '1': targetState = STATE.COLLAPSED; break; case '2': targetState = STATE.SCATTERED; break;
            case '3': if (photoMeshes.length > 0) focusPhoto(0); break; case 'Escape': closePhotoFocus(); closePhotoPanel(); break;
            case 'u': case 'U': document.getElementById('photoPanel').classList.toggle('show'); break; }
    });

    const observer = new IntersectionObserver((entries) => { entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); }); }, { threshold: 0.1 });
    document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el));

    function initApp() { initThreeJS(); initMediaPipe(); animate(); setTimeout(() => { document.getElementById('photoPanel').classList.add('show'); }, 1000); }
    </script>
</body>
</html>
'''

# Now assemble everything
# For content, let's extract the original content layer sections
content_parts = []

# Extract from backup: sections within content-layer
content_start = orig_text.find('<div class="content-layer">')
content_end = orig_text.rfind('</footer>') + len('</footer>')
if content_start > 0 and content_end > content_start:
    content_section = orig_text[content_start:content_end]
    print(f"Extracted content section: {len(content_section)} chars")
else:
    print("Could not extract content, using fallback")
    content_section = ""

# Extract photo panels
photo_start = orig_text.find('<div class="photo-upload-panel"')
photo_end = orig_text.rfind('</body>')
if photo_start > 0 and photo_end > photo_start:
    photo_section = orig_text[photo_start:photo_end]
else:
    photo_section = ""
print(f"Photo section: {len(photo_section)} chars")

# Build the complete file
final = head + html_body + content_section + "\n" + photo_section + "\n" + js_part

# Write
with open(r'C:\Users\AQQW\Desktop\index.html', 'w', encoding='utf-8') as f:
    f.write(final)

print(f"Written: {len(final)} chars, file saved to index.html")
