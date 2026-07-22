import re

with open(r'C:\Users\AQQW\Desktop\index_backup.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original: {len(content)} chars")

# 1. Add MediaPipe scripts after Three.js
content = content.replace(
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>',
    '''<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>'''
)

# 2. Add new CSS before </style>
new_css = '''        .hud-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 50; pointer-events: none; }
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
        #webcam-preview { position: fixed; bottom: 20px; right: 20px; width: 200px; height: 150px; border-radius: 12px; border: 2px solid rgba(106,180,255,0.4); z-index: 100; object-fit: cover; transform: scaleX(-1); background: rgba(10,15,26,0.9); }
        #hand-canvas { position: fixed; bottom: 20px; right: 20px; width: 200px; height: 150px; border-radius: 12px; z-index: 101; pointer-events: none; transform: scaleX(-1); }
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
        .corner-frame { position: fixed; width: 40px; height: 40px; border-color: rgba(106,180,255,0.3); border-style: solid; z-index: 48; pointer-events: none; }
        .corner-frame.tl { top: 10px; left: 10px; border-width: 2px 0 0 2px; }
        .corner-frame.tr { top: 10px; right: 10px; border-width: 2px 2px 0 0; }
        .corner-frame.bl { bottom: 10px; left: 10px; border-width: 0 0 2px 2px; }
        .corner-frame.br { bottom: 10px; right: 220px; border-width: 0 2px 2px 0; }
        .scan-line { position: fixed; top: 0; left: 0; width: 100%; height: 2px; background: rgba(106,180,255,0.15); animation: scan 6s linear infinite; z-index: 49; pointer-events: none; }
        @keyframes scan { 0% { transform: translateY(-100vh); } 100% { transform: translateY(100vh); } }
'''

content = content.replace('    </style>', new_css + '    </style>')

# 3. Add new HTML elements before <div class="content-layer">
new_html = '''    <div class="scan-line"></div>
    <div class="corner-frame tl"></div>
    <div class="corner-frame tr"></div>
    <div class="corner-frame bl"></div>
    <div class="corner-frame br"></div>
    <video id="webcam-preview" playsinline autoplay muted></video>
    <canvas id="hand-canvas"></canvas>
    <div class="hud-overlay">
        <div class="hud-title">DATA ENTITY NEURAL INTERFACE</div>
        <div class="hud-status" id="statusText">等待摄像头权限...</div>
        <div class="state-badge">
            <h3>当前状态</h3>
            <div class="state-value" id="stateValue">合拢态</div>
        </div>
        <div class="gesture-indicator">
            <h3>手势控制</h3>
            <div class="gesture-item" id="gest-fist"><span class="gesture-icon">F</span><span>握拳 - 合拢态</span></div>
            <div class="gesture-item" id="gest-open"><span class="gesture-icon">O</span><span>张开五指 - 散开态</span></div>
            <div class="gesture-item" id="gest-rotate"><span class="gesture-icon">R</span><span>手旋转 - 相机旋转</span></div>
            <div class="gesture-item" id="gest-grab"><span class="gesture-icon">G</span><span>抓取 - 照片放大</span></div>
        </div>
        <div class="particle-count" id="particleCount">PARTICLES: 0 | FPS: 0</div>
    </div>
'''

content = content.replace('    <div class="content-layer">', new_html + '    <div class="content-layer">')

# 4. Add photo panel before closing </body>
photo_panel = '''
    <div class="photo-upload-panel" id="photoPanel">
        <span class="close-panel" onclick="closePhotoPanel()">x</span>
        <h2>上传照片到数据云</h2>
        <label class="upload-btn">
            选择照片
            <input type="file" id="photoInput" accept="image/*" multiple onchange="handlePhotoUpload(event)">
        </label>
        <div class="photo-grid" id="photoGrid"></div>
    </div>
    <div class="photo-focus-overlay" id="photoFocus" onclick="closePhotoFocus()">
        <img id="focusImage" src="" alt="">
        <div class="photo-focus-info">点击任意处关闭 - 握拳返回合拢态</div>
    </div>
'''

content = content.replace('    </script>\n</body>\n</html>', photo_panel + '    </script>\n</body>\n</html>')

# Now we need to replace the existing Three.js code inside the <script> block
# Find the start of the script and replace everything up to the closing </script>
print(f"After HTML/CSS updates: {len(content)} chars")

with open(r'C:\Users\AQQW\Desktop\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved intermediate version")
