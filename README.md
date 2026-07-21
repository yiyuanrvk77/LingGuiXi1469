# Personal Resume Site - 金鑫 · 数据生命体

A futuristic 3D interactive personal resume site built with Three.js.

## 部署到 Cloudflare Pages

### 1. 注册账号
- GitHub: https://github.com
- Cloudflare: https://dash.cloudflare.com

### 2. 推送代码到 GitHub

```bash
# 在项目目录下初始化 Git
cd "C:\Users\AQQW\Desktop"
git init
git add .
git commit -m "init: 个人简历网站"

# 关联远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/你的用户名/jinxin-resume.git
git branch -M main
git push -u origin main
```

### 3. Cloudflare Pages 部署
1. 登录 https://dash.cloudflare.com
2. 左侧菜单 → **Workers & Pages** → **Pages**
3. 点击 **Connect to Git**
4. 选择刚才的 GitHub 仓库 → **Begin setup**
5. **Project name**: `jinxin-resume` (会变成 `jinxin-resume.pages.dev`)
6. **Build command**: 留空（不需要构建）
7. **Build output directory**: 留空（直接用根目录）
8. 点击 **Save and Deploy**

等待几分钟后，访问 `https://jinxin-resume.pages.dev` 就能看到你的网站。

### 4. 绑定自定义域名（可选）
1. 在 Cloudflare 注册域名（推荐 `.dev` 或 `.top`，便宜）
2. Cloudflare Pages → 你的项目 → **Custom domains** → **Set up a custom domain**
3. 输入你的域名，Cloudflare 会自动配置 DNS

## 本地预览

由于使用了 WebGL 和本地图片，建议用本地服务器预览：

```bash
# Python 3
python -m http.server 8080

# 或 Node.js
npx serve .
```

然后浏览器打开 http://localhost:8080

## 文件结构

```
.
├── index.html          # 主页面（含所有代码）
├── df681eb7-70c0-4c79-9253-58ead2b6544b.png  # 角色图片
└── README.md
```

## 交互方式

| 操作 | 效果 |
|------|------|
| 按 `1` | 粒子合拢（围绕角色） |
| 按 `2` | 粒子散开 |
| 按 `3` | 照片放大模式 |
| 按 `Esc` | 关闭弹窗 |
| 按 `U` / `u` | 切换照片上传面板 |
| 手势：握拳 | 合拢态 |
| 手势：张开五指 | 散开态 |
| 手势：抓取 | 照片放大 |

## 技术栈

- Three.js (3D 渲染)
- MediaPipe (手势识别)
- Tailwind CSS
- 原生 JavaScript