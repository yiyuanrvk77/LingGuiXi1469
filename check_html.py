import shutil

# Backup current file
shutil.copy('C:/Users/AQQW/Desktop/index.html', 'C:/Users/AQQW/Desktop/index_backup_final.html')
print('Backup created')

# Read current HTML
with open('C:/Users/AQQW/Desktop/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')

# Find the line numbers for key sections
for i, line in enumerate(lines):
    if 'let scene, camera, renderer, clock;' in line:
        print(f'Line {i+1}: scene declaration')
    if 'function animate()' in line:
        print(f'Line {i+1}: animate function')
    if 'createParticleSystem()' in line:
        print(f'Line {i+1}: createParticleSystem call')
