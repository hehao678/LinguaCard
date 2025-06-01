
from generator.text_generator import generate_card_content
from renderer.card_renderer import render_card_to_html
from exporter.html_to_image_firefox import html_to_png_firefox
from generator.llm_prompt_generator import generate_image_prompt_by_llm
from image_gen.local_sd_gen import generate_sd_image

import os
import sys
import html
import re


def truncate_words_block(html_str: str, max_items: int = 5) -> str:
    """
    只选择重点和普通词汇的前5个单词
    从 html 字符串中提取前 max_items 项（以 <br> 或 <li> 分隔）
    """
    # 按行分割
    lines = re.split(r'<br>|<li>|\\n', html_str)
    lines = [line for line in lines if line.strip()]
    return "<br>".join(lines[:max_items])


def run_card_pipeline(topic: str, level: str = "小学", word_count: int = 60):
    print(f"[INFO] 开始生成主题：{topic} 的学习卡片")
    data = generate_card_content(topic, level, word_count)
    if data is None:
        print("[ERROR] 文本生成失败，终止流程")
        return

    # 补充一些字段信息
    data["jieduan"] = level
    data["dancishu"] = str(word_count)
    # 限制重点词汇和普通词汇
    data["zhongdian"] = truncate_words_block(
        data.get("zhongdian", ""), max_items=5)
    data["putong"] = truncate_words_block(data.get("putong", ""), max_items=5)
    img_prompt = generate_image_prompt_by_llm(data)
    print("stable diffusion prompt:", img_prompt)

    images = generate_sd_image(img_prompt)
    data["tupian"] = images[0]  # 选择第一张作为卡片插图

    output_base = os.path.join("output", topic.replace(" ", "_"))
    html_path = f"{output_base}.html"
    png_path = f"{output_base}.png"

    render_card_to_html(data, html_path)
    html_to_png_firefox(html_path, png_path)
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
        word_count = 20

    run_card_pipeline(topic, level, word_count)
