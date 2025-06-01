import os
import subprocess
from datetime import datetime


def generate_sd_image(
    prompt: str,
    outdir: str = "/home/hhe/mnt/prj/LinguaCard/output/img/stable_images001",
    ckpt: str = "/home/hhe/mnt/prj/stablediffusion/checkpoints/768-v-ema.ckpt",
    config: str = "/home/hhe/mnt/prj/stablediffusion/configs/stable-diffusion/v2-inference-v.yaml",
    height: int = 768,
    width: int = 768,
    steps: int = 100,
    scale: float = 12.0,
    n_iter: int = 1,
    n_samples: int = 4
) -> list:
    """
    使用 Stable Diffusion 生成插图并返回图像文件路径列表。
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(outdir, exist_ok=True)

    command = [
        "python", "/home/hhe/mnt/prj/stablediffusion/scripts/txt2img.py",
        "--prompt", prompt,
        "--ckpt", ckpt,
        "--config", config,
        "--device", "cuda",
        "--precision", "autocast",
        "--H", str(height),
        "--W", str(width),
        "--n_samples", str(n_samples),
        "--n_iter", str(n_iter),
        "--scale", str(scale),
        "--steps", str(steps),
        "--outdir", outdir
    ]

    print(f"[INFO] 开始生成插图：{prompt}")
    subprocess.run(command, check=True)

    # 获取最新生成的图像列表（按时间排序）
    generated_files = sorted(
        [os.path.join(outdir, f)
         for f in os.listdir(outdir) if f.endswith(".png")],
        key=os.path.getmtime,
        reverse=True
    )
    latest_images = generated_files[:n_samples]

    if latest_images:
        print(f"[SUCCESS] 插图生成完成，共生成 {len(latest_images)} 张图像")
    else:
        print("[WARNING] 插图生成失败或找不到文件")

    return latest_images


if __name__ == "__main__":
    test_prompt = "a cartoon oil painting of a child learning English with flashcards, cheerful, colorful, cozy"
    generate_sd_image(test_prompt)
