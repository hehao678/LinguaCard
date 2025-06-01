
from jinja2 import Environment, FileSystemLoader
import os

# 模板加载路径（项目根目录下的 templates 文件夹）
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
template = env.get_template('card_template.html')


def render_card_to_html(data: dict, output_path: str):
    """
    将生成内容渲染为 HTML 文件
    :param data: 包含卡片字段的 dict（zhuti, zhutien, zhengwen 等）
    :param output_path: 输出 HTML 文件路径
    """

    # 替换本地绝对路径为相对路径
    rel_tupian = os.path.relpath(
        data.get("tupian", ""), start=os.path.dirname(output_path))
    print(f"[DEBUG] 相对路径图像: {rel_tupian}")

    print(rel_tupian)
    rendered_html = template.render(
        zhuti=data.get("zhuti", "未命名"),
        zhutien=data.get("zhutien", "Untitled"),
        jieduan=data.get("jieduan", "小学"),
        dancishu=data.get("dancishu", "60"),
        zhengwen=data.get("zhengwen", ""),
        zhongwenfanyi=data.get("zhongwenfanyi", ""),
        putong=data.get("putong", ""),
        zhongdian=data.get("zhongdian", ""),
        tupian=rel_tupian  # 使用相对路径
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
        print(f"[INFO] HTML 渲染成功: {output_path}")


if __name__ == "__main__":
    demo_data = {
        "zhuti": "美食",
        "zhutien": "Delicious Food",
        "jieduan": "小学",
        "dancishu": "20",
        "zhengwen": "Food is important...",
        "zhongwenfanyi": "食物很重要...",
        "zhongdian": "- food (/fuːd/): 食物<br>- pizza (/ˈpiːtsə/): 披萨",
        "putong": "- tasty (/ˈteɪsti/): 美味的",
        "tupian": "/home/hhe/mnt/prj/LinguaCard/output/img/stable_images001/grid-0000.png"
    }
    render_card_to_html(demo_data, "../output/demo_card.html")
