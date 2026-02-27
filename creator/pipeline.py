import argparse
import os
import shutil

from . import render, vectorize, rename, build_font


def run(args: argparse.Namespace) -> None:
    png_dir = os.path.join(args.work_dir, "png")
    svg_dir = os.path.join(args.work_dir, "svg")

    # Step 1: 获取 PNG 图像
    if args.source == "font":
        characters = _load_characters(args)
        print(f"\n=== Step 1/4: 渲染 {len(characters)} 个字符 ===")
        render.render_characters(characters, args.font_path, png_dir, args.max_size)
    else:
        # print(f"\n=== Step 1/4: 复制 PNG 从 {args.png_dir} ===")
        # _copy_pngs(args.png_dir, png_dir)
        png_dir = args.png_dir  

    # Step 2: PNG → SVG
    print(f"\n=== Step 2/4: PNG 转 SVG ===")
    vectorize.convert_pngs_to_svgs(png_dir, svg_dir)

    # Step 3: 重命名 SVG 为 unicode 格式
    print(f"\n=== Step 3/4: 重命名 SVG ===")
    rename.rename_to_unicode(svg_dir)

    # Step 4: 构建字体
    print(f"\n=== Step 4/4: 构建字体 ===")
    build_font.build(
        svg_dir,
        family=args.family,
        output_file=args.output,
        build_dir=os.path.join(args.work_dir, "build"),
        upem=args.upem,
        ascender=args.ascender,
        descender=args.descender,
        color_format=args.color_format,
    )

    print(f"\n完成! 字体文件: {args.output}")


def _load_characters(args: argparse.Namespace) -> list[str]:
    with open(args.characters_file, "r", encoding="utf-8") as f:
        text = f.read().strip().split()
    text = ''.join(text) 
    text = list(set(text))
    return text
