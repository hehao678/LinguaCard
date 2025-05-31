from jinja2 import Environment, FileSystemLoader
import os


def render_svg(data: dict, output_path: str):
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    template = env.get_template('card_template.svg')

    svg_content = template.render(data)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
        print(f"[INFO] SVG 渲染完成: {output_path}")
