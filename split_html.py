import shutil, re

# Read original file
with open(r'C:\Users\AQQW\Desktop\index_backup.html', 'r', encoding='utf-8') as f:
    original = f.read()

# Split into parts
lines = original.split('\n')
print(f"Total lines: {len(lines)}")

# Find where <script> starts
script_line = 0
for i, line in enumerate(lines):
    if '<script>' in line:
        script_line = i
        print(f"Found <script> at line {i+1}")
        break

# Original content before script
html_part = '\n'.join(lines[:script_line])
print(f"HTML part: {len(html_part)} chars")

# Write part
with open(r'C:\Users\AQQW\Desktop\temp_html.txt', 'w', encoding='utf-8') as f:
    f.write(html_part)

print("Done")
