# exporter/html_to_image_firefox.py

from playwright.sync_api import sync_playwright
import os


def html_to_png_firefox(html_path: str, output_path: str, width: int = 794, height: int = 1123):
    """
    使用 Firefox 截图 HTML 页面生成 PNG 图像（基于 Playwright）
    :param html_path: HTML 文件路径（本地）
    :param output_path: PNG 输出路径
    :param width: 浏览器视口宽度
    :param height: 浏览器视口高度
    """
    abs_html_path = os.path.abspath(html_path)
    url = f"file://{abs_html_path}"

    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(url)
        page.screenshot(path=output_path, full_page=True)
        print(f"[INFO] 使用 Firefox 截图完成：{output_path}")
        browser.close()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "../output/美食.html")
    html_path = os.path.abspath(html_path)
    png_path = html_path.replace(".html", "_firefox.png")

    html_to_png_firefox(html_path, png_path)
