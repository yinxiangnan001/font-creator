import argparse


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="font-creater",
        description="从 PNG 图像生成彩色字体的完整流水线",
    )

    parser.add_argument(
        "--source",
        required=True,
        choices=["font", "png"],
        help="图像来源：font（从字体渲染）或 png（从已有 PNG 目录）",
    )
    parser.add_argument("--font-path", help="字体文件路径（source=font 时必填）")
    parser.add_argument("--characters-file", help="字符文件路径（每行一个字符或空格分隔，source=font 时必填）")
    parser.add_argument("--png-dir", help="PNG 图像目录（source=png 时必填，文件名为 单字符.png）")
    parser.add_argument("--max-size", type=int, default=512, help="渲染最大像素尺寸（默认 512）")
    parser.add_argument("--family", default="MyFont", help="字体 family 名（默认 MyFont）")
    parser.add_argument("--output", default="MyFont.ttf", help="输出 .ttf 文件名（默认 MyFont.ttf）")
    parser.add_argument("--upem", type=int, default=1024, help="units per em（默认 1024）")
    parser.add_argument("--ascender", type=int, default=800, help="ascender（默认 800）")
    parser.add_argument("--descender", type=int, default=-200, help="descender（默认 -200）")
    parser.add_argument("--color-format", default="glyf_colr_1", help="nanoemoji color format（默认 glyf_colr_1）")
    parser.add_argument("--work-dir", default="./font_build", help="中间产物目录（默认 ./font_build）")

    args = parser.parse_args(argv)

    if args.source == "font":
        if not args.font_path:
            parser.error("--source font 需要指定 --font-path")
        if not args.characters_file:
            parser.error("--source font 需要指定 --characters-file")
    elif args.source == "png":
        if not args.png_dir:
            parser.error("--source png 需要指定 --png-dir")

    return args
