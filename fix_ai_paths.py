#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 创造中心.html 中所有 ../A/images/ 路径，并用内联SVG或本地图片替换"""
import sys, io, re, os

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

FILE = r"E:\Ai项目文件\WorkBuddy\商城端\创造中心.html"

# SVG 定义（和创造中心未登录态保持一致）
SVG = {
    # 项目经理 - 橙色
    'AI-1.png': '<svg width="100%" height="100%" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="40" rx="8" fill="#FF5722"/><path d="M17 27L20 22L23 27L22 35L18 35Z" fill="white" opacity="0.9"/><circle cx="15" cy="15" r="2.2" fill="white"/><circle cx="25" cy="15" r="2.2" fill="white"/><path d="M14 22Q20 27 26 22" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
    # 我的秘书头像照片 → 用本地已有图片
    'tx-2.png': None,   # 保留为 images/tx-2.png
    # 销售/产品/其他 → 本地图片
    'tx-1.png': None,   # 保留为 images/tx-1.png
    # 方案工程师 - 蓝色
    'AI-4.png': '<svg width="100%" height="100%" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="40" rx="8" fill="#2196F3"/><path d="M12 14h16v2H12zM14 18h12v2H14zM12 22h16v2H12z" fill="white" opacity="0.8"/><circle cx="20" cy="28" r="5" fill="white" opacity="0.6"/></svg>',
    # 售后工程师 - 绿色
    'AI-3.png': '<svg width="100%" height="100%" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="40" rx="8" fill="#4CAF50"/><path d="M20 12c-3 0-5 2-5 5v2h-2v12h14V19h-2v-2c0-3-2-5-5-5z" fill="white" opacity="0.8"/><circle cx="20" cy="23" r="3" fill="#4CAF50"/></svg>',
    # AI-2 - 紫色
    'AI-2.png': '<svg width="100%" height="100%" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="40" rx="8" fill="#9C27B0"/><circle cx="15" cy="16" r="2.5" fill="white"/><circle cx="25" cy="16" r="2.5" fill="white"/><path d="M13 24 Q20 30 27 24" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/><rect x="16" y="28" width="8" height="3" rx="1.5" fill="white" opacity="0.6"/></svg>',
    # tx-3 - 备用本地图片
    'tx-3.png': None,   # 保留为 images/tx-1.png（tx-3不存在，降级）
}

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

original = content
count = 0

def replace_img_tag(m):
    global count
    img_name = m.group(1)
    rest = m.group(2)
    if img_name in SVG and SVG[img_name] is not None:
        count += 1
        # 替换整个 <img src="..." style="..."/> 为内联SVG
        return SVG[img_name]
    elif img_name == 'tx-2.png':
        count += 1
        return f'<img src="images/tx-2.png"{rest}'
    elif img_name in ('tx-1.png', 'tx-3.png'):
        count += 1
        return f'<img src="images/tx-1.png"{rest}'
    return m.group(0)

# 替换 <img src="../A/images/AI-1.png" ... 这种格式
content = re.sub(
    r'<img src="\.\./A/images/([^"]+)"([^>]*>)',
    replace_img_tag,
    content
)

# 替换 JS 字符串中的 '../A/images/xxx.png'（带单引号或双引号）
def replace_js_path(m):
    global count
    quote = m.group(1)
    img_name = m.group(2)
    count += 1
    if img_name == 'tx-2.png':
        return f"{quote}images/tx-2.png{quote}"
    elif img_name in ('tx-1.png', 'tx-3.png'):
        return f"{quote}images/tx-1.png{quote}"
    elif img_name == 'AI-1.png':
        return f"{quote}images/pm-avatar.svg{quote}"  # 先改成路径，后面再处理
    elif img_name == 'AI-4.png':
        return f"{quote}images/solution-avatar.svg{quote}"
    elif img_name == 'AI-3.png':
        return f"{quote}images/support-avatar.svg{quote}"
    elif img_name == 'AI-2.png':
        return f"{quote}images/ai2-avatar.svg{quote}"
    return f"{quote}images/tx-1.png{quote}"

content = re.sub(
    r"(['\"])\.\./A/images/([^'\"]+)(['\"])",
    lambda m: f"{m.group(1)}images/{m.group(2)}{m.group(3)}".replace('../A/images/', ''),
    content
)

# 再做一次通配处理，确保无残留
remaining = re.findall(r'\.\./A/images/', content)
print(f"替换后残留 ../A/images/ 数量: {len(remaining)}")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 完成！共替换约 {content.count('images/') - original.count('images/')} 处路径")
print(f"   残留 ../A/ 路径: {len(remaining)}")
