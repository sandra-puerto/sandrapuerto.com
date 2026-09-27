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

def draw_rounded_bar(draw, x, y, w, h, radius, fill_color, bg_color=(30, 41, 59, 180)):
    """Draw a rounded progress bar."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg_color)
    
def draw_filled_bar(draw, x, y, total_w, h, radius, fill_pct, fill_color, bg_color=(30, 41, 59, 180)):
    """Draw a rounded progress bar with a fill percentage."""
    draw.rounded_rectangle([x, y, x + total_w, y + h], radius=radius, fill=bg_color)
    fill_w = max(int(total_w * fill_pct), h)
    draw.rounded_rectangle([x, y, x + fill_w, y + h], radius=radius, fill=fill_color)

def create_linkedin_cover():
    W, H = 1200, 1200
    base = Image.new("RGBA", (W, H), (3, 7, 18, 255))
    
    # ── 1. Rich multi-layered background ──
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([-200, -200, 700, 500], fill=(56, 189, 248, 65))
    g_draw.ellipse([600, 700, 1500, 1500], fill=(16, 185, 129, 55))
    g_draw.ellipse([300, 300, 900, 900], fill=(139, 92, 246, 25))
    g_draw.ellipse([800, -100, 1400, 400], fill=(245, 158, 11, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    base = Image.alpha_composite(base, glow)
    
    # ── 2. Geometric grid pattern ──
    grid_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_layer)
    grid_spacing = 60
    for gx in range(0, W, grid_spacing):
        grid_draw.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 8), width=1)
    for gy in range(0, H, grid_spacing):
        grid_draw.line([(0, gy), (W, gy)], fill=(255, 255, 255, 8), width=1)
    import random
    random.seed(42)
    for _ in range(25):
        ix = random.randint(0, W // grid_spacing) * grid_spacing
        iy = random.randint(0, H // grid_spacing) * grid_spacing
        grid_draw.ellipse([ix - 3, iy - 3, ix + 3, iy + 3], fill=(56, 189, 248, 40))
    base = Image.alpha_composite(base, grid_layer)
    
    # ── 3. Main content card ──
    card_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(card_layer)
    margin = 60
    c_draw.rounded_rectangle([margin, margin, W - margin, H - margin], 
                             radius=32, fill=(15, 23, 42, 200), 
                             outline=(255, 255, 255, 25), width=2)
    base = Image.alpha_composite(base, card_layer)
    
    # ── 4. Accent stripe at top ──
    stripe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stripe)
    stripe_y = margin
    stripe_h = 5
    for sx in range(margin, W - margin):
        ratio = (sx - margin) / (W - 2 * margin)
        r = int(56 + (16 - 56) * ratio)
        g = int(189 + (185 - 189) * ratio)
        b = int(248 + (129 - 248) * ratio)
        s_draw.line([(sx, stripe_y), (sx, stripe_y + stripe_h)], fill=(r, g, b, 220))
    base = Image.alpha_composite(base, stripe)
    
    # ── 5. Fonts ──
    font_dir = "C:/Windows/Fonts"
    f_tag = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 16)
    f_name = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 62)
    f_role = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 28)
    f_headline = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 34)
    f_metric_val = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 72)
    f_metric_label = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 19)
    f_desc = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 24)
    f_tech = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 17)
    f_url = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 20)
    f_cta = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 26)
    f_bottom = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 18)
    
    # ── 6. Build overlays ──
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    
    pad = 80  # inner padding from card edge
    lx = margin + pad
    rx_end = W - margin - pad
    content_w = rx_end - lx
    
    # --- Top badge ---
    badge_text = "SOFTWARE & INFRAESTRUCTURA TI"
    badge_y = margin + 40
    bb = f_tag.getbbox(badge_text)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    o_draw.rounded_rectangle([lx - 14, badge_y - 8, lx + bw + 14, badge_y + bh + 10], 
                             radius=10, fill=(56, 189, 248, 35), outline=(56, 189, 248, 100), width=1)
    
    # --- URL badge right ---
    url_text = "sandrapuerto.com"
    ub = f_url.getbbox(url_text)
    uw = ub[2] - ub[0]
    o_draw.rounded_rectangle([rx_end - uw - 14, badge_y - 8, rx_end + 14, badge_y + bh + 10], 
                             radius=10, fill=(16, 185, 129, 25), outline=(16, 185, 129, 80), width=1)
    
    # --- Metric cards ---
    metrics_y = 440
    gap = 24
    card_w = (content_w - gap * 2) // 3
    card_h = 190
    metric_colors = [
        (56, 189, 248),   # cyan
        (16, 185, 129),   # emerald
        (139, 92, 246),   # violet
    ]
    for i in range(3):
        cx = lx + i * (card_w + gap)
        mc = metric_colors[i]
        o_draw.rounded_rectangle([cx, metrics_y, cx + card_w, metrics_y + card_h],
                                 radius=18, fill=(15, 23, 42, 240),
                                 outline=(mc[0], mc[1], mc[2], 70), width=2)
        for px in range(cx + 18, cx + card_w - 18):
            o_draw.point((px, metrics_y + 1), fill=(mc[0], mc[1], mc[2], 150))
            o_draw.point((px, metrics_y + 2), fill=(mc[0], mc[1], mc[2], 80))
    
    # --- Tech badges ---
    tech_y = 690
    techs = [
        ("PHP / Laravel", (255, 45, 32)),
        ("Proxmox & Linux", (229, 112, 0)),
        ("On-Premise", (56, 189, 248)),
        ("Zero Trust", (139, 92, 246)),
        ("Docker", (36, 150, 237)),
    ]
    # Calculate total width to center the row
    total_pills_w = 0
    pill_sizes = []
    for t_text, t_color in techs:
        tb = f_tech.getbbox(t_text)
        tw = tb[2] - tb[0]
        th = tb[3] - tb[1]
        pw = tw + 40
        ph = th + 22
        pill_sizes.append((pw, ph, tw, th))
        total_pills_w += pw
    pill_gap = 12
    total_pills_w += pill_gap * (len(techs) - 1)
    tx_start = lx + (content_w - total_pills_w) // 2
    tx = tx_start
    for idx, (t_text, t_color) in enumerate(techs):
        pw, ph, tw, th = pill_sizes[idx]
        o_draw.rounded_rectangle([tx, tech_y, tx + pw, tech_y + ph],
                                 radius=ph // 2, fill=(t_color[0], t_color[1], t_color[2], 25),
                                 outline=(t_color[0], t_color[1], t_color[2], 120), width=2)
        tx += pw + pill_gap
    
    # --- Divider ---
    div_y = 770
    o_draw.line([(lx, div_y), (rx_end, div_y)], fill=(255, 255, 255, 15), width=1)
    
    # --- CTA button ---
    cta_y = 1030
    cta_text = "sandrapuerto.com"
    ctb = f_cta.getbbox(cta_text)
    ctw = ctb[2] - ctb[0]
    cth = ctb[3] - ctb[1]
    cta_btn_w = ctw + 80
    cta_btn_h = cth + 32
    cta_x = (W - cta_btn_w) // 2
    for bx in range(cta_x, cta_x + cta_btn_w):
        ratio = (bx - cta_x) / cta_btn_w
        r = int(56 + (16 - 56) * ratio)
        g = int(189 + (185 - 189) * ratio)
        b = int(248 + (129 - 248) * ratio)
        o_draw.line([(bx, cta_y), (bx, cta_y + cta_btn_h)], fill=(r, g, b, 200))
    o_draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_btn_w, cta_y + cta_btn_h],
                             radius=cta_btn_h // 2, outline=(255, 255, 255, 60), width=2)
    
    base = Image.alpha_composite(base, overlay)
    
    # ── 7. CTA button mask ──
    btn_mask = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bm_draw = ImageDraw.Draw(btn_mask)
    for bx in range(cta_x, cta_x + cta_btn_w):
        ratio = (bx - cta_x) / cta_btn_w
        r = int(56 + (16 - 56) * ratio)
        g = int(189 + (185 - 189) * ratio)
        b = int(248 + (129 - 248) * ratio)
        bm_draw.line([(bx, cta_y), (bx, cta_y + cta_btn_h)], fill=(r, g, b, 230))
    mask_img = Image.new("L", (W, H), 0)
    mask_draw = ImageDraw.Draw(mask_img)
    mask_draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_btn_w, cta_y + cta_btn_h],
                                radius=cta_btn_h // 2, fill=255)
    base = Image.composite(Image.alpha_composite(base, btn_mask), base, mask_img)
    
    # ── 8. Draw all text ──
    draw = ImageDraw.Draw(base)
    
    # Badge text
    draw.text((lx, badge_y), badge_text, font=f_tag, fill="#38bdf8")
    draw.text((rx_end - uw, badge_y), url_text, font=f_url, fill="#10b981")
    
    # Icon
    icon_img = create_base_icon(256)
    icon_resized = icon_img.resize((115, 115), Image.Resampling.LANCZOS)
    icon_y = margin + 95
    base.paste(icon_resized, (lx, icon_y), icon_resized)
    
    # Name
    name_x = lx + 140
    name_y = icon_y + 8
    draw.text((name_x, name_y), "Sandra Puerto", font=f_name, fill="#f8fafc")
    sp_bbox = f_name.getbbox("Sandra Puerto")
    dot_x = name_x + (sp_bbox[2] - sp_bbox[0]) + 5
    draw.ellipse([dot_x, name_y + 40, dot_x + 14, name_y + 54], fill="#38bdf8")
    
    # Role
    draw.text((name_x, name_y + 78), "Desarrollo de Software & Dirección TI", font=f_role, fill="#38bdf8")
    
    # Headline — professional, direct, no drama
    headline_y = 330
    draw.text((lx, headline_y), "Backend, infraestructura y control de costos TI.", font=f_headline, fill="#e2e8f0")
    draw.text((lx, headline_y + 48), "Resultados medibles en entornos productivos reales.", font=f_headline, fill="#94a3b8")
    
    # ── Metrics ──
    metric_data = [
        ("-60%", "OPEX tecnológico\ntras rediseño", (56, 189, 248), 0.60),
        ("-50%", "Errores en\nproducción", (16, 185, 129), 0.50),
        ("-70%", "Tamaño de nuevas\nimplementaciones", (139, 92, 246), 0.70),
    ]
    
    for i, (val, label, color, pct) in enumerate(metric_data):
        cx = lx + i * (card_w + gap)
        draw.text((cx + 24, metrics_y + 18), val, font=f_metric_val, fill=color)
        bar_y = metrics_y + 118
        bar_w = card_w - 48
        draw_filled_bar(draw, cx + 24, bar_y, bar_w, 10, 5, pct, 
                       color + (200,), (30, 41, 59, 180))
        draw.text((cx + 24, bar_y + 20), label, font=f_metric_label, fill="#94a3b8")
    
    # ── Tech badges text ──
    tx = tx_start
    for idx, (t_text, t_color) in enumerate(techs):
        pw, ph, tw, th = pill_sizes[idx]
        dot_cy = tech_y + ph // 2
        draw.ellipse([tx + 14, dot_cy - 4, tx + 22, dot_cy + 4], fill=t_color)
        draw.text((tx + 28, tech_y + 10), t_text, font=f_tech, fill="#f1f5f9")
        tx += pw + pill_gap
    
    # ── Description — short, factual, no self-praise ──
    desc_y = 810
    draw.text((lx, desc_y), 
              "Desarrollo backend con experiencia en operación real de", 
              font=f_desc, fill="#cbd5e1")
    draw.text((lx, desc_y + 36), 
              "infraestructura. Decisiones técnicas con criterio financiero",
              font=f_desc, fill="#cbd5e1")
    draw.text((lx, desc_y + 72),
              "y enfoque en continuidad operativa.",
              font=f_desc, fill="#e2e8f0")
    
    # ── CTA button text ──
    draw.text((cta_x + 40, cta_y + 12), cta_text, font=f_cta, fill="#030712")
    
    # ── Bottom bar ──
    bottom_y = H - margin - 38
    draw.text((lx, bottom_y), "PHP · Laravel · Proxmox · Linux · Docker · Ciberseguridad", 
              font=f_bottom, fill=(148, 163, 184, 120))
    
    # ── Save ──
    out_dir = os.path.abspath(os.path.join(base_dir, ".."))
    out_path = os.path.join(out_dir, "linkedin-cover.png")
    final = base.convert("RGB")
    final.save(out_path, format="PNG", optimize=True)
    print(f"Generated linkedin-cover.png (1200x1200) in project root")

if __name__ == "__main__":
    generate_favicons()
    create_og_image()
    create_linkedin_cover()
