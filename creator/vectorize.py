from pathlib import Path
import vtracer


def convert_pngs_to_svgs(png_dir: str, svg_dir: str) -> None:
    png_dir = Path(png_dir)
    svg_dir = Path(svg_dir)
    svg_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    png_files = sorted(png_dir.glob("*.png"))

    for file_path in png_files:
        out_path = svg_dir / f"{file_path.stem}.svg"
        vtracer.convert_image_to_svg_py(
            str(file_path),
            str(out_path),
            colormode="color",
            hierarchical="cutout",
            mode="spline",
            filter_speckle=4,
            color_precision=6,
        )
        count += 1
        print(f"转换: {file_path.name} -> {out_path.name} ({count}/{len(png_files)})")

    print(f"共转换 {count} 个 PNG 到 {svg_dir}")
