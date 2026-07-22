import re

# Read current file
with open('C:/Users/AQQW/Desktop/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Three.js setup with optimized version
old_three_js = '''        // ===== Three.js Setup =====
        const container = document.getElementById('canvas-container');
        scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x0a0f1a, 0.008);
        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 35);
        renderer = new THREE.WebGLRenderer({ antialias: false, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(1);
        renderer.setClearColor(0x0a0f1a, 1);
        renderer.toneMapping = THREE.LinearToneMapping;
        container.appendChild(renderer.domElement);
        clock = new THREE.Clock();

        // Lights - 简化
        ambientLight = new THREE.AmbientLight(0x1a2a4a, 0.3); scene.add(ambientLight);
        pointLight1 = new THREE.PointLight(0x6ab4ff, 1, 80); pointLight1.position.set(10, 20, 10); scene.add(pointLight1);
        pointLight2 = new THREE.PointLight(0xff6b6b, 0.5, 60); pointLight2.position.set(-15, 10, -10); scene.add(pointLight2);'''

new_three_js = '''        // ===== Three.js Setup =====
        const container = document.getElementById('canvas-container');
        scene = new THREE.Scene();
        // Remove fog for performance
        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 35);
        
        // Optimize renderer
        renderer = new THREE.WebGLRenderer({ 
            antialias: false, 
            alpha: true,
            powerPreference: 'low-power',
            precision: 'mediump'
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1));
        renderer.setClearColor(0x0a0f1a, 1);
        container.appendChild(renderer.domElement);
        clock = new THREE.Clock();

        // Minimal lights - only one
        ambientLight = new THREE.AmbientLight(0x1a2a4a, 0.5); scene.add(ambientLight);'''

content = content.replace(old_three_js, new_three_js)

# Replace animate function with optimized version
old_animate = '''        // 页面可见性控制 - 不可见时暂停渲染
        let isVisible = true;
        document.addEventListener('visibilitychange', () => {
            isVisible = !document.hidden;
        });

        function animate() {
            requestAnimationFrame(animate); 
            if (!isVisible) return; // 页面不可见时跳过渲染
            const time = clock.getElapsedTime();
            updateParticles(time, 0);
            particlesMesh.rotation.y = time * 0.02; 
            renderer.render(scene, camera);
        }'''

new_animate = '''        // Performance optimization
        let isVisible = true;
        let isInViewport = true;
        let frameCount = 0;
        const targetFPS = 30;
        const frameInterval = 1000 / targetFPS;
        let lastFrameTime = 0;
        
        document.addEventListener('visibilitychange', () => {
            isVisible = !document.hidden;
        });
        
        // Check if canvas is in viewport
        const canvasObserver = new IntersectionObserver((entries) => {
            isInViewport = entries[0].isIntersecting;
        }, { threshold: 0.1 });
        
        if (container) canvasObserver.observe(container);

        function animate(currentTime) {
            requestAnimationFrame(animate);
            
            // Skip if not visible or not in viewport
            if (!isVisible || !isInViewport) return;
            
            // Frame rate limiting
            if (currentTime - lastFrameTime < frameInterval) return;
            lastFrameTime = currentTime;
            
            const time = clock.getElapsedTime();
            updateParticles(time, 0);
            particlesMesh.rotation.y = time * 0.02; 
            renderer.render(scene, camera);
        }'''

content = content.replace(old_animate, new_animate)

# Write optimized file
with open('C:/Users/AQQW/Desktop/index_optimized.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Optimized file created: index_optimized.html")
print("Changes made:")
print("1. Removed fog for performance")
print("2. Added powerPreference: low-power")
print("3. Added precision: mediump")
print("4. Reduced lights to one ambient light")
print("5. Added FPS limiting to 30fps")
print("6. Added IntersectionObserver for viewport detection")
print("7. Kept all other content intact")
