import os
import subprocess
import sys
from pathlib import Path


def _find_nanoemoji() -> str:
    bin_dir = os.path.dirname(sys.executable)
    local = os.path.join(bin_dir, "nanoemoji")
    if os.path.isfile(local):
        return local # /Users/yxn/miniforge3/envs/llm/bin/nanoemoji 
    return "nanoemoji"


def build(svg_dir: str, family: str, output_file: str, build_dir: str, upem: int = 1024, ascender: int = 800, descender: int = -200, color_format: str = "glyf_colr_1") -> None:
    svg_files = sorted(Path(svg_dir).glob("emoji_u*.svg"))
    if not svg_files:
        print(f"错误：{svg_dir} 中没有找到 emoji_u*.svg 文件", file=sys.stderr)
        sys.exit(1)

    cmd = [
        _find_nanoemoji(),
        f"--family={family}",
        f"--output_file={output_file}",
        f"--build_dir={build_dir}",
        f"--upem={upem}",
        f"--ascender={ascender}",
        f"--descender={descender}",
        f"--color_format={color_format}",
    ] + [str(f) for f in svg_files]

    # 确保当前 Python 环境的 bin 目录在 PATH 中（nanoemoji 内部需要找到 ninja）
    env = os.environ.copy()
    bin_dir = os.path.dirname(sys.executable)
    env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")

    print(f"执行: {' '.join(cmd[:7])} [{len(svg_files)} svg files]")
    subprocess.run(cmd, check=True, env=env)
    print(f"字体已生成: {output_file}")
