import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageFont


import random
import numpy as np
from PIL import Image, ImageFont, ImageDraw

def apply_gradient_patch(text_image: Image.Image) -> Image.Image:
    """
    接收一张带有 Alpha 通道的白色文字图像，生成随机对角线渐变并染色。
    """
    width, height = text_image.size
    
    # 1. 随机生成两个 RGB 颜色
    color1 = np.array([random.randint(0, 255) for _ in range(3)])
    color2 = np.array([random.randint(0, 255) for _ in range(3)])
    
    # 2. 构建坐标矩阵
    # 使用 linspace 生成 0 到 1 的归一化坐标
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    xv, yv = np.meshgrid(x, y)
    
    # 3. 随机选择对角线方向
    # True: 左上 (0,0) -> 右下 (1,1)
    # False: 右上 (1,0) -> 左下 (0,1)
    if random.choice([True, False]):
        gradient_mask = (xv + yv) / 2
    else:
        gradient_mask = (1 - xv + yv) / 2

    # 4. 计算渐变矩阵 (H, W, 3)
    # 线性插值公式: C = C1 + (C2 - C1) * mask
    gradient_array = color1 + (color2 - color1) * gradient_mask[:, :, np.newaxis]
    gradient_array = gradient_array.astype(np.uint8)
    
    # 转换为带 Alpha 的 PIL 图像
    gradient_patch = Image.fromarray(gradient_array).convert("RGBA")

    # 5. 核心染色步骤：
    # 创建结果图，以文字图像的 Alpha 通道作为掩码 (mask)
    # 只有 text_image 中有像素的地方（文字部分），gradient_patch 才会显现
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    result.paste(gradient_patch, (0, 0), mask=text_image)
    
    return result


def bin_search_font_size(text: str, font_path: str, max_size: int = 512) -> int:
    low, high = 1, 1024
    best_size = low

    while low <= high:
        mid = (low + high) // 2
        font = ImageFont.truetype(font_path, mid)
        bbox = font.getbbox(text)

        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if max(w, h) <= max_size:
            best_size = mid
            low = mid + 1
        else:
            high = mid - 1

    return best_size


def render_text(text: str, font_path: str, max_size: int = 512) -> Image.Image:
    current_font_size = bin_search_font_size(text, font_path, max_size)
    font = ImageFont.truetype(font_path, current_font_size)
    box = font.getbbox(text)

    height = max(1, box[3] - box[1])
    width = max(1, box[2] - box[0])

    # 宽高比超过 4:1 说明字体不支持该字符，用 "口" 替代
    if width == 0 or height == 0 or max(width, height) / min(width, height) > 4:
        return render_text("口", font_path, max_size)

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((-box[0], -box[1]), text, font=font, fill=(255, 255, 255, 255))
    image = apply_gradient_patch(image)
    return image


def _render_one(ch: str, font_path: str, output_dir: str, max_size: int) -> str:
    image = render_text(ch, font_path, max_size)
    image.save(os.path.join(output_dir, f"{ch}.png"))
    return ch


def render_characters(characters: list[str], font_path: str, output_dir: str, max_size: int = 512, workers: int = 8) -> None:
    os.makedirs(output_dir, exist_ok=True)
    count = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_render_one, ch, font_path, output_dir, max_size): ch for ch in characters}
        for future in as_completed(futures):
            ch = future.result()
            count += 1
            print(f"渲染: {ch} -> {ch}.png ({count}/{len(characters)})")
    print(f"共渲染 {count} 个字符到 {output_dir}")
