# main.py

from generator.text_generator import generate_card_content
from renderer.card_renderer import render_card_to_html
from exporter.html_to_image import html_to_png
from renderer.svg_renderer import render_svg
from exporter.svg_to_png import svg_to_png
import os
import sys
import html


def run_card_pipeline(topic: str, level: str = "小学", word_count: int = 60):
    print(f"[INFO] 开始生成主题：{topic} 的学习卡片")
    data = generate_card_content(topic, level, word_count)
    if data is None:
        print("[ERROR] 文本生成失败，终止流程")
        return

    # 补充一些字段信息
    data["jieduan"] = level
    data["dancishu"] = str(word_count)
    # data["tupian"] = "/api/placeholder/800/400"  # 默认图片占位
    data["tupian"] = "https://source.unsplash.com/800x400/?food"

    output_base = os.path.join("output", topic.replace(" ", "_"))
    # html_path = f"{output_base}.html"
    # png_path = f"{output_base}.png"
    svg_path = f"{output_base}.svg"
    png_path = f"{output_base}.png"

    # render_card_to_html(data, html_path)
    # html_to_png(html_path, png_path)
    for k in ["zhengwen", "zhongwenfanyi", "zhongdian", "putong"]:
        data[k] = html.escape(data.get(k, ""))
    render_svg(data, svg_path)
    svg_to_png(svg_path, png_path)
    print("[SUCCESS] 学习卡片全部生成完成！")


if __name__ == "__main__":
    # 示例用法：python main.py 美食 小学 60
    if len(sys.argv) >= 2:
        topic = sys.argv[1]
        level = sys.argv[2] if len(sys.argv) > 2 else "小学"
        word_count = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    else:
        topic = "美食"
        level = "小学"
        word_count = 60

    run_card_pipeline(topic, level, word_count)
