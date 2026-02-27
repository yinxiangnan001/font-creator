import os


def rename_to_unicode(svg_dir: str) -> None:
    count = 0
    for filename in os.listdir(svg_dir):
        if not filename.endswith(".svg"):
            continue
        char = os.path.splitext(filename)[0]
        if len(char) != 1:
            continue

        unicode_hex = hex(ord(char))[2:]
        new_name = f"emoji_u{unicode_hex}.svg"
        old_path = os.path.join(svg_dir, filename)
        new_path = os.path.join(svg_dir, new_name)

        os.rename(old_path, new_path)
        print(f"重命名: {filename} -> {new_name}")
        count += 1

    print(f"共重命名 {count} 个 SVG 文件")
