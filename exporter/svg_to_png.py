import cairosvg


def svg_to_png(svg_path: str, png_path: str):
    cairosvg.svg2png(url=svg_path, write_to=png_path)
    print(f"[INFO] PNG 导出完成: {png_path}")
