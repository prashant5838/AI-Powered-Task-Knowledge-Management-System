from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'docs', 'screenshots')
os.makedirs(OUT, exist_ok=True)

def make_img(text, path):
    img = Image.new('RGB', (800, 200), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.load_default()
    except Exception:
        f = None
    d.text((20,80), text, fill=(255,255,255), font=f)
    img.save(path)

if __name__ == '__main__':
    make_img('Backend: /docs (Swagger) running', os.path.join(OUT, 'backend.png'))
    make_img('Frontend: React app running', os.path.join(OUT, 'frontend.png'))
    print('Screenshots generated in', OUT)
