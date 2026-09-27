import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public"))

def create_base_icon(size=1024):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    rx = int(size * 0.24)
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=rx, fill="#030712")
    
    # Outer subtle border
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=rx, outline=(255, 255, 255, 30), width=max(2, int(size * 0.015)))
    
    stroke_w = int(size * 0.10)
    
    # Path 1: (25%, 30%) -> (45%, 50%) -> (25%, 70%) in #38bdf8
    p1 = (int(size * 0.25), int(size * 0.30))
    p2 = (int(size * 0.45), int(size * 0.50))
    p3 = (int(size * 0.25), int(size * 0.70))
    
    draw.line([p1, p2], fill="#38bdf8", width=stroke_w)
    draw.line([p2, p3], fill="#38bdf8", width=stroke_w)
    
    r_cap = stroke_w // 2
    for pt in [p1, p2, p3]:
        draw.ellipse([pt[0] - r_cap, pt[1] - r_cap, pt[0] + r_cap, pt[1] + r_cap], fill="#38bdf8")
        
    # Path 2: (55%, 70%) -> (75%, 70%) in #10b981
    q1 = (int(size * 0.55), int(size * 0.70))
    q2 = (int(size * 0.75), int(size * 0.70))
    draw.line([q1, q2], fill="#10b981", width=stroke_w)
    for pt in [q1, q2]:
        draw.ellipse([pt[0] - r_cap, pt[1] - r_cap, pt[0] + r_cap, pt[1] + r_cap], fill="#10b981")
        
    return img

def generate_favicons():
    base = create_base_icon(1024)
    icons_dir = os.path.join(base_dir, "icons")
    os.makedirs(icons_dir, exist_ok=True)
    
    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "apple-touch-icon.png": 180,
        "android-chrome-192x192.png": 192,
        "android-chrome-512x512.png": 512
    }
    
    for filename, s in sizes.items():
        resized = base.resize((s, s), Image.Resampling.LANCZOS)
        out_path = os.path.join(icons_dir, filename)
        resized.save(out_path, format="PNG", optimize=True)
        print(f"Generated {filename} ({s}x{s})")
        
    # Multi-size ICO
    ico_16 = base.resize((16, 16), Image.Resampling.LANCZOS)
    ico_32 = base.resize((32, 32), Image.Resampling.LANCZOS)
    ico_48 = base.resize((48, 48), Image.Resampling.LANCZOS)
    ico_path = os.path.join(icons_dir, "favicon.ico")
    ico_32.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[ico_16, ico_48])
    print(f"Generated favicon.ico (16, 32, 48)")

def create_og_image():
    W, H = 1200, 630
    base = Image.new("RGBA", (W, H), (3, 7, 18, 255))
    
    # 1. Ambient Glows
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([-80, -80, 500, 500], fill=(56, 189, 248, 55))
    g_draw.ellipse([800, 200, 1350, 750], fill=(16, 185, 129, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    base = Image.alpha_composite(base, glow)
    
    # 2. Glassmorphism Card
    card_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(card_layer)
    card_box = [50, 45, W - 50, H - 45]
    c_draw.rounded_rectangle(card_box, radius=24, fill=(15, 23, 42, 220), outline=(255, 255, 255, 30), width=1)
    base = Image.alpha_composite(base, card_layer)
    
    # 3. Transparent badges and overlays
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    
    font_dir = "C:/Windows/Fonts"
    f_badge = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 14)
    f_title = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 54)
    f_role = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 26)
    f_desc = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 22)
    f_tag = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 16)
    f_url = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 18)
    
    # Badge: DIAGNÓSTICO & SOLUCIÓN TI
    badge_text = "DIAGNÓSTICO & SOLUCIÓN TI"
    badge_x, badge_y = 95, 88
    bbox = f_badge.getbbox(badge_text)
    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    o_draw.rounded_rectangle([badge_x - 14, badge_y - 8, badge_x + bw + 14, badge_y + bh + 8], 
                             radius=8, fill=(56, 189, 248, 30), outline=(56, 189, 248, 90), width=1)
    
    # URL: sandrapuerto.com
    url_text = "sandrapuerto.com"
    u_bbox = f_url.getbbox(url_text)
    uw = u_bbox[2] - u_bbox[0]
    
    # Tags at bottom
    tags = [
        ("PHP / Laravel", (119, 123, 180, 255)),
        ("Infraestructura On-Premises", (56, 189, 248, 255)),
        ("Proxmox & Linux", (229, 112, 0, 255)),
        ("Reducción OPEX (-60%)", (16, 185, 129, 255)),
        ("Ciberseguridad & Zero Trust", (56, 189, 248, 255))
    ]
    
    tag_x = 95
    tag_y = 490
    tag_elements = []
    
    for t_text, t_color in tags:
        t_box = f_tag.getbbox(t_text)
        tw = t_box[2] - t_box[0]
        th = t_box[3] - t_box[1]
        
        # Translucent pill
        o_draw.rounded_rectangle([tag_x, tag_y - 7, tag_x + tw + 28, tag_y + th + 9], 
                                 radius=8, fill=(30, 41, 59, 180), outline=(255, 255, 255, 25), width=1)
        tag_elements.append((tag_x, tag_y, tw, th, t_text, t_color))
        tag_x += tw + 38
        
    base = Image.alpha_composite(base, overlay)
    
    # 4. Text and opaque graphics
    draw = ImageDraw.Draw(base)
    draw.text((badge_x, badge_y), badge_text, font=f_badge, fill="#38bdf8")
    draw.text((W - 95 - uw, badge_y + 1), url_text, font=f_url, fill="#94a3b8")
    
    # Icon
    icon_img = create_base_icon(256)
    icon_resized = icon_img.resize((108, 108), Image.Resampling.LANCZOS)
    base.paste(icon_resized, (95, 160), icon_resized)
    
    # Title
    title_x = 230
    title_y = 165
    draw.text((title_x, title_y), "Sandra Puerto", font=f_title, fill="#f8fafc")
    sp_bbox = f_title.getbbox("Sandra Puerto")
    dot_x = title_x + (sp_bbox[2] - sp_bbox[0]) + 4
    draw.ellipse([dot_x, title_y + 36, dot_x + 12, title_y + 48], fill="#38bdf8")
    
    # Role
    draw.text((title_x, 235), "Desarrollo de Software & Dirección TI", font=f_role, fill="#38bdf8")
    
    # Description lines
    desc_y = 310
    draw.text((95, desc_y), "Sistemas que fallan en el peor momento y presupuestos que suben sin justificación.", font=f_desc, fill="#94a3b8")
    draw.text((95, desc_y + 38), "Desarrollo backend con conciencia de costo, riesgo y continuidad operativa.", font=f_desc, fill="#e2e8f0")
    
    # Draw tag text and dots
    for tx, ty, tw, th, t_text, t_color in tag_elements:
        draw.ellipse([tx + 10, ty + (th // 2) - 2, tx + 16, ty + (th // 2) + 4], fill=t_color)
        draw.text((tx + 22, ty), t_text, font=f_tag, fill="#f1f5f9")
        
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    og_path = os.path.join(images_dir, "og-image.png")
    base.save(og_path, format="PNG", optimize=True)
    print("Generated refined og-image.png (1200x630) in public/images/")

def create_linkedin_cover():
    W, H = 1584, 396
    base = Image.new("RGBA", (W, H), (3, 7, 18, 255))
    
    # 1. Ambient Glows
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([-100, -100, 600, 600], fill=(56, 189, 248, 55))
    g_draw.ellipse([1000, 50, 1700, 600], fill=(16, 185, 129, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    base = Image.alpha_composite(base, glow)
    
    # 2. Glassmorphism Card (Centered)
    card_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(card_layer)
    card_box = [60, 40, W - 60, H - 40]
    c_draw.rounded_rectangle(card_box, radius=24, fill=(15, 23, 42, 220), outline=(255, 255, 255, 30), width=1)
    base = Image.alpha_composite(base, card_layer)
    
    # 3. Transparent badges and overlays
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    
    font_dir = "C:/Windows/Fonts"
    f_badge = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 16)
    f_title = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 64)
    f_role = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 30)
    f_desc = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 24)
    f_url = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 22)
    
    # Badge: DIAGNÓSTICO & SOLUCIÓN TI
    badge_text = "DIAGNÓSTICO & SOLUCIÓN TI"
    badge_x, badge_y = 120, 80
    bbox = f_badge.getbbox(badge_text)
    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    o_draw.rounded_rectangle([badge_x - 16, badge_y - 10, badge_x + bw + 16, badge_y + bh + 10], 
                             radius=8, fill=(56, 189, 248, 30), outline=(56, 189, 248, 90), width=1)
    
    # URL: sandrapuerto.com
    url_text = "sandrapuerto.com"
    u_bbox = f_url.getbbox(url_text)
    uw = u_bbox[2] - u_bbox[0]
    
    base = Image.alpha_composite(base, overlay)
    
    # 4. Text and opaque graphics
    draw = ImageDraw.Draw(base)
    draw.text((badge_x, badge_y), badge_text, font=f_badge, fill="#38bdf8")
    draw.text((W - 120 - uw, badge_y + 1), url_text, font=f_url, fill="#94a3b8")
    
    # Icon
    icon_img = create_base_icon(256)
    icon_resized = icon_img.resize((120, 120), Image.Resampling.LANCZOS)
    base.paste(icon_resized, (120, 150), icon_resized)
    
    # Title
    title_x = 270
    title_y = 150
    draw.text((title_x, title_y), "Sandra Puerto", font=f_title, fill="#f8fafc")
    sp_bbox = f_title.getbbox("Sandra Puerto")
    dot_x = title_x + (sp_bbox[2] - sp_bbox[0]) + 4
    draw.ellipse([dot_x, title_y + 42, dot_x + 14, title_y + 56], fill="#38bdf8")
    
    # Role
    draw.text((title_x, 235), "Desarrollo de Software & Dirección TI", font=f_role, fill="#38bdf8")
    
    # Description lines
    desc_y = 295
    draw.text((120, desc_y), "Desarrollo backend con conciencia de costo, riesgo y continuidad operativa.", font=f_desc, fill="#e2e8f0")
        
    out_dir = os.path.abspath(os.path.join(base_dir, ".."))
    out_path = os.path.join(out_dir, "linkedin-cover.png")
    base.save(out_path, format="PNG", optimize=True)
    print(f"Generated linkedin-cover.png (1584x396) in project root")

if __name__ == "__main__":
    generate_favicons()
    create_og_image()
    create_linkedin_cover()
