# exporter/html_to_image.py

from html2image import Html2Image
import os


def html_to_png(html_path: str, output_path: str, width: int = 794, height: int = 1123):
    """
    将 HTML 文件渲染为 PNG 图片（默认宽高为 A4 尺寸的像素）
    :param html_path: 输入 HTML 文件路径
    :param output_path: 输出 PNG 路径
    :param width: 渲染宽度（默认 794px）
    :param height: 渲染高度（默认 1123px）
    """
    hti = Html2Image()
    # # 根据你的系统可能是 chromium
    # hti = Html2Image(browser_path='/usr/bin/chromium-browser')
    hti.output_path = os.path.dirname(output_path)
    hti.screenshot(
        html_file=html_path,
        save_as=os.path.basename(output_path),
        size=(width, height)
    )
    print(f"[INFO] 图片已保存：{output_path}")


if __name__ == "__main__":
    html_to_png("../output/demo_card.html", "../output/demo_card.png")
