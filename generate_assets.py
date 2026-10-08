"""Generate the site's original, locally stored vintage-car illustrations."""

import random
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
SCALE = 2


def point(x, y):
    return round(x * SCALE), round(y * SCALE)


def polygon(draw, points, fill, outline=None, width=1):
    draw.polygon([point(x, y) for x, y in points], fill=fill)
    if outline:
        line(draw, points + [points[0]], outline, width)


def line(draw, points, fill, width=1):
    draw.line([point(x, y) for x, y in points], fill=fill, width=max(1, round(width * SCALE)), joint="curve")


def ellipse(draw, bounds, fill, outline=None, width=1):
    scaled = tuple(round(value * SCALE) for value in bounds)
    draw.ellipse(scaled, fill=fill, outline=outline, width=max(1, round(width * SCALE)))


def bezier_polygon(draw, start, segments, fill):
    path = [start]
    current = start
    for control_a, control_b, end in segments:
        for step in range(1, 25):
            t = step / 24
            inverse = 1 - t
            path.append((
                inverse ** 3 * current[0] + 3 * inverse ** 2 * t * control_a[0]
                + 3 * inverse * t ** 2 * control_b[0] + t ** 3 * end[0],
                inverse ** 3 * current[1] + 3 * inverse ** 2 * t * control_a[1]
                + 3 * inverse * t ** 2 * control_b[1] + t ** 3 * end[1],
            ))
        current = end
    draw.polygon([point(x, y) for x, y in path], fill=fill)


def rounded(draw, bounds, radius, fill, outline=None, width=1):
    scaled = tuple(round(value * SCALE) for value in bounds)
    draw.rounded_rectangle(scaled, radius=round(radius * SCALE), fill=fill, outline=outline,
                           width=max(1, round(width * SCALE)))


def canvas(width, height, sky, horizon):
    image = Image.new("RGB", (width * SCALE, height * SCALE))
    pixels = image.load()
    for y in range(height * SCALE):
        t = y / max(1, height * SCALE - 1)
        eased = t * t * (3 - 2 * t)
        color = tuple(round(a * (1 - eased) + b * eased) for a, b in zip(sky, horizon))
        for x in range(width * SCALE):
            pixels[x, y] = color
    return image


def draw_alfa(draw, x, y, scale=1, color=(132, 48, 42)):
    x0, y0 = x, y
    p = lambda a, b: (x0 + a * scale, y0 + b * scale)
    # A long bonnet and fastback cabin give the Sprint its poised coupé profile.
    bezier_polygon(draw, p(10, 176), [
        (p(22, 148), p(63, 141), p(147, 129)), (p(195, 124), p(220, 102), p(269, 72)),
        (p(315, 48), p(371, 51), p(410, 55)), (p(457, 64), p(489, 106), p(535, 116)),
        (p(610, 123), p(699, 131), p(744, 164)), (p(759, 175), p(756, 193), p(748, 203)),
        (p(735, 220), p(706, 220), p(680, 218)), (p(507, 222), p(251, 222), p(76, 218)),
        (p(39, 215), p(17, 205), p(10, 190)), (p(6, 184), p(8, 179), p(10, 176)),
    ], color)
    polygon(draw, [p(228, 119), p(276, 82), p(403, 67), p(508, 121)], (42, 54, 51))
    polygon(draw, [p(290, 111), p(315, 83), p(397, 73), p(407, 111)], (163, 183, 174))
    polygon(draw, [p(418, 73), p(496, 119), p(469, 119), p(424, 111)], (130, 154, 148))
    for cx in (170, 590):
        ellipse(draw, (x0 + (cx - 67) * scale, y0 + 150 * scale,
                       x0 + (cx + 67) * scale, y0 + 284 * scale), (28, 31, 30))
        ellipse(draw, (x0 + (cx - 42) * scale, y0 + 176 * scale,
                       x0 + (cx + 42) * scale, y0 + 258 * scale), (187, 177, 151),
                outline=(219, 205, 176), width=5 * scale)
        ellipse(draw, (x0 + (cx - 11) * scale, y0 + 207 * scale,
                       x0 + (cx + 11) * scale, y0 + 229 * scale), (92, 89, 77))
    ellipse(draw, (x0 + 709 * scale, y0 + 155 * scale, x0 + 745 * scale, y0 + 184 * scale),
            (239, 214, 160))
    ellipse(draw, (x0 + 40 * scale, y0 + 154 * scale, x0 + 71 * scale, y0 + 178 * scale),
            (242, 203, 133))
    line(draw, [p(34, 191), p(95, 184), p(141, 186), p(687, 186)], (225, 188, 115), 4 * scale)
    line(draw, [p(555, 142), p(655, 148), p(701, 160)], (177, 91, 69), 3 * scale)
    ellipse(draw, (x0 + 698 * scale, y0 + 164 * scale, x0 + 719 * scale, y0 + 177 * scale),
            (43, 52, 48), outline=(226, 203, 164), width=3 * scale)
    polygon(draw, [p(716, 168), p(733, 173), p(731, 192), p(716, 196), p(710, 183)], (42, 49, 45),
            outline=(222, 205, 169), width=2 * scale)


def draw_peugeot(draw, x, y, scale=1, color=(101, 121, 99)):
    x0, y0 = x, y
    p = lambda a, b: (x0 + a * scale, y0 + b * scale)
    # The open cabin and upright screen keep the 403's cabriolet distinct.
    bezier_polygon(draw, p(12, 172), [
        (p(22, 152), p(46, 142), p(90, 136)), (p(143, 128), p(193, 130), p(226, 119)),
        (p(263, 108), p(277, 91), p(311, 91)), (p(383, 91), p(474, 100), p(523, 122)),
        (p(586, 132), p(680, 137), p(728, 162)), (p(746, 171), p(747, 191), p(738, 202)),
        (p(727, 216), p(693, 220), p(665, 218)), (p(475, 222), p(221, 220), p(72, 218)),
        (p(31, 216), p(13, 203), p(10, 190)), (p(8, 182), p(9, 176), p(12, 172)),
    ], color)
    polygon(draw, [p(246, 122), p(284, 76), p(300, 68), p(315, 73), p(293, 121)], (43, 55, 51))
    polygon(draw, [p(306, 82), p(321, 80), p(353, 116), p(318, 116)], (161, 180, 169))
    polygon(draw, [p(365, 113), p(390, 116), p(408, 151), p(356, 151)], (35, 47, 44))
    line(draw, [p(52, 154), p(190, 146), p(231, 150), p(258, 138)], (205, 192, 158), 3 * scale)
    for cx in (158, 589):
        ellipse(draw, (x0 + (cx - 62) * scale, y0 + 156 * scale,
                       x0 + (cx + 62) * scale, y0 + 279 * scale), (30, 33, 31))
        ellipse(draw, (x0 + (cx - 37) * scale, y0 + 181 * scale,
                       x0 + (cx + 37) * scale, y0 + 254 * scale), (189, 178, 151),
                outline=(222, 211, 184), width=5 * scale)
        ellipse(draw, (x0 + (cx - 10) * scale, y0 + 207 * scale,
                       x0 + (cx + 10) * scale, y0 + 227 * scale), (92, 90, 79))
    ellipse(draw, (x0 + 701 * scale, y0 + 158 * scale, x0 + 733 * scale, y0 + 183 * scale),
            (239, 222, 174))
    ellipse(draw, (x0 + 30 * scale, y0 + 159 * scale, x0 + 62 * scale, y0 + 184 * scale),
            (237, 196, 127))
    line(draw, [p(41, 191), p(119, 185), p(183, 189), p(696, 189)], (214, 197, 151), 4 * scale)
    line(draw, [p(490, 146), p(615, 151), p(694, 160)], (160, 159, 133), 3 * scale)
    rounded(draw, (x0 + 700 * scale, y0 + 166 * scale, x0 + 734 * scale, y0 + 195 * scale),
            8 * scale, (40, 50, 47), outline=(217, 199, 163), width=2 * scale)
    line(draw, [p(708, 170), p(708, 191)], (213, 198, 166), 2 * scale)


def draw_mercedes(draw, x, y, scale=1, color=(45, 62, 58), gullwing=False):
    p = lambda a, b: (x + a * scale, y + b * scale)
    bezier_polygon(draw, p(8, 179), [
        (p(23, 151), p(54, 144), p(139, 130)), (p(184, 124), p(211, 99), p(248, 80)),
        (p(294, 56), p(358, 58), p(385, 62)), (p(434, 68), p(472, 105), p(513, 119)),
        (p(588, 125), p(685, 135), p(734, 163)), (p(754, 174), p(759, 192), p(748, 203)),
        (p(733, 219), p(705, 222), p(674, 218)), (p(483, 221), p(222, 222), p(72, 219)),
        (p(29, 216), p(13, 205), p(9, 191)), (p(5, 185), p(6, 181), p(8, 179)),
    ], color)
    polygon(draw, [p(214, 128), p(254, 86), p(372, 72), p(467, 119)], (35, 49, 47))
    polygon(draw, [p(267, 119), p(288, 93), p(368, 82), p(376, 119)], (143, 164, 156))
    polygon(draw, [p(386, 84), p(451, 118), p(416, 118), p(381, 113)], (111, 137, 130))
    if gullwing:
        polygon(draw, [p(279, 92), p(326, 14), p(442, 56), p(470, 116), p(437, 115), p(405, 77)],
                (177, 159, 128), outline=(230, 214, 176), width=4 * scale)
        polygon(draw, [p(327, 26), p(424, 61), p(440, 101), p(376, 79)], (43, 57, 54))
        line(draw, [p(287, 103), p(326, 14), p(442, 56)], (237, 220, 181), 5 * scale)
    for cx in (163, 592):
        ellipse(draw, (x + (cx - 67) * scale, y + 150 * scale,
                       x + (cx + 67) * scale, y + 284 * scale), (23, 26, 25))
        ellipse(draw, (x + (cx - 41) * scale, y + 176 * scale,
                       x + (cx + 41) * scale, y + 258 * scale), (184, 175, 150),
                outline=(223, 208, 175), width=5 * scale)
        ellipse(draw, (x + (cx - 10) * scale, y + 207 * scale,
                       x + (cx + 10) * scale, y + 227 * scale), (92, 88, 78))
    ellipse(draw, (x + 709 * scale, y + 157 * scale, x + 748 * scale, y + 186 * scale),
            (240, 218, 164))
    ellipse(draw, (x + 31 * scale, y + 155 * scale, x + 66 * scale, y + 184 * scale),
            (245, 190, 118))
    ellipse(draw, (x + 686 * scale, y + 163 * scale, x + 718 * scale, y + 182 * scale),
            (38, 51, 48), outline=(218, 198, 161), width=3 * scale)
    line(draw, [p(27, 192), p(93, 185), p(151, 187), p(692, 187)], (208, 184, 132), 4 * scale)
    line(draw, [p(543, 143), p(644, 151), p(691, 164)], (109, 127, 116), 3 * scale)
    ellipse(draw, (x + 711 * scale, y + 164 * scale, x + 741 * scale, y + 195 * scale),
            (42, 52, 49), outline=(220, 205, 174), width=3 * scale)
    for offset in (0, 7, 14):
        line(draw, [p(716 + offset, 171), p(736, 171 + offset)], (175, 175, 152), 2 * scale)


def draw_porsche(draw, x, y, scale=1, color=(76, 95, 105)):
    p = lambda a, b: (x + a * scale, y + b * scale)
    # Short tail, sloping roof and separate round lamps suggest the first 911.
    bezier_polygon(draw, p(9, 183), [
        (p(22, 155), p(49, 146), p(88, 140)), (p(127, 134), p(169, 132), p(198, 119)),
        (p(231, 99), p(255, 79), p(304, 75)), (p(372, 68), p(419, 90), p(454, 120)),
        (p(507, 131), p(597, 135), p(667, 146)), (p(720, 153), p(746, 168), p(751, 188)),
        (p(757, 207), p(727, 218), p(699, 219)), (p(500, 222), p(206, 221), p(66, 219)),
        (p(28, 216), p(11, 205), p(9, 190)), (p(8, 187), p(8, 185), p(9, 183)),
    ], color)
    polygon(draw, [p(240, 135), p(269, 98), p(388, 88), p(470, 132), p(430, 133)],
            (43, 56, 55))
    polygon(draw, [p(285, 128), p(305, 105), p(376, 97), p(389, 128)], (158, 176, 169))
    polygon(draw, [p(399, 99), p(455, 130), p(427, 130), p(390, 124)], (119, 144, 137))
    for cx in (159, 597):
        ellipse(draw, (x + (cx - 67) * scale, y + 151 * scale,
                       x + (cx + 67) * scale, y + 284 * scale), (25, 28, 27))
        ellipse(draw, (x + (cx - 41) * scale, y + 176 * scale,
                       x + (cx + 41) * scale, y + 258 * scale), (188, 179, 155),
                outline=(223, 210, 184), width=5 * scale)
        ellipse(draw, (x + (cx - 11) * scale, y + 207 * scale,
                       x + (cx + 11) * scale, y + 229 * scale), (87, 87, 79))
    ellipse(draw, (x + 700 * scale, y + 157 * scale, x + 744 * scale, y + 193 * scale),
            (238, 218, 170), outline=(230, 205, 154), width=3 * scale)
    ellipse(draw, (x + 30 * scale, y + 158 * scale, x + 65 * scale, y + 184 * scale),
            (236, 194, 126))
    line(draw, [p(32, 193), p(104, 186), p(162, 188), p(690, 187)], (215, 193, 150), 4 * scale)
    line(draw, [p(68, 155), p(130, 149), p(189, 151)], (115, 131, 137), 3 * scale)
    line(draw, [p(517, 151), p(644, 158), p(695, 169)], (125, 142, 144), 3 * scale)


def landscape_car(size, palette, composition):
    width, height = size
    image = canvas(width, height, palette["sky"], palette["haze"])
    draw = ImageDraw.Draw(image)
    if composition == "alfa":
        polygon(draw, [(0, 490), (165, 355), (315, 428), (490, 318), (710, 430),
                       (940, 340), (1200, 450), (1200, 800), (0, 800)], palette["hill"])
        polygon(draw, [(0, 585), (235, 463), (422, 529), (668, 405), (900, 523),
                       (1200, 448), (1200, 800), (0, 800)], palette["hill_far"])
        polygon(draw, [(0, 700), (1200, 636), (1200, 800), (0, 800)], palette["ground"])
        line(draw, [(0, 711), (330, 675), (650, 665), (1200, 682)], palette["road"], 4)
        draw_alfa(draw, 186, 398, 1.13, (132, 48, 42))
        ellipse(draw, (955, 188, 1080, 313), (227, 173, 119))
    elif composition == "peugeot":
        polygon(draw, [(0, 250), (0, 125), (1200, 125), (1200, 285)], palette["stone"])
        for xx in range(40, 1200, 210):
            rounded(draw, (xx, 186, xx + 142, 448), 68, palette["shadow_stone"])
            rounded(draw, (xx + 10, 196, xx + 132, 444), 60, palette["glass"])
        polygon(draw, [(0, 450), (1200, 418), (1200, 800), (0, 800)], palette["ground"])
        ellipse(draw, (930, 70, 1120, 260), (228, 189, 145))
        draw_peugeot(draw, 174, 445, 1.18, (99, 119, 96))
        line(draw, [(0, 729), (1200, 706)], palette["road"], 3)
    elif composition == "mercedes":
        rounded(draw, (80, 60, 1120, 636), 26, palette["wall"])
        for xx in (150, 405, 660, 915):
            rounded(draw, (xx, 95, xx + 170, 489), 80, palette["arch"])
            rounded(draw, (xx + 17, 112, xx + 153, 482), 68, palette["glass"])
            line(draw, [(xx + 85, 118), (xx + 85, 465)], palette["mullion"], 3)
        ellipse(draw, (330, 115, 870, 650), palette["light"])
        polygon(draw, [(0, 602), (1200, 602), (1200, 800), (0, 800)], palette["ground"])
        rounded(draw, (128, 687, 1090, 743), 20, palette["plinth"])
        draw_mercedes(draw, 212, 433, 1.02, (48, 66, 62), gullwing=True)
        line(draw, [(40, 780), (1160, 780)], palette["floor_line"], 2)
    else:
        polygon(draw, [(0, 360), (180, 145), (355, 357), (560, 115), (795, 366),
                       (1010, 173), (1200, 344), (1200, 800), (0, 800)], palette["mountain"]
                )
        polygon(draw, [(0, 448), (190, 269), (354, 441), (558, 237), (790, 448),
                       (1008, 291), (1200, 438), (1200, 800), (0, 800)], palette["snow"]
                )
        polygon(draw, [(0, 650), (1200, 607), (1200, 800), (0, 800)], palette["ground"])
        line(draw, [(0, 714), (350, 680), (720, 692), (1200, 653)], palette["road"], 5)
        draw_porsche(draw, 197, 435, 1.08, (74, 92, 104))
    return image


def draw_hero_mercedes(draw):
    p = lambda a, b: (a, b)
    body = (49, 65, 61)
    chrome = (213, 194, 155)
    # A front-facing study with both famous doors raised, unlike the side-view card art.
    polygon(draw, [p(320, 846), p(253, 673), p(368, 720), p(425, 826), p(395, 868)],
            (77, 91, 80), outline=chrome, width=5)
    polygon(draw, [p(680, 846), p(747, 673), p(632, 720), p(575, 826), p(605, 868)],
            (77, 91, 80), outline=chrome, width=5)
    polygon(draw, [p(292, 699), p(360, 727), p(409, 818), p(357, 811)],
            (40, 56, 53), outline=(127, 137, 115), width=3)
    polygon(draw, [p(708, 699), p(640, 727), p(591, 818), p(643, 811)],
            (40, 56, 53), outline=(127, 137, 115), width=3)
    polygon(draw, [p(385, 793), p(615, 793), p(678, 872), p(322, 872)], (36, 51, 49),
            outline=(170, 173, 144), width=4)
    polygon(draw, [p(411, 807), p(589, 807), p(635, 858), p(365, 858)], (113, 139, 132))
    bezier_polygon(draw, p(191, 924), [
        (p(207, 884), p(247, 864), p(298, 860)), (p(356, 846), p(409, 862), p(500, 862)),
        (p(591, 862), p(644, 846), p(702, 860)), (p(753, 864), p(793, 884), p(809, 924)),
        (p(827, 957), p(823, 1000), p(800, 1034)), (p(777, 1071), p(715, 1091), p(660, 1090)),
        (p(557, 1096), p(443, 1096), p(340, 1090)), (p(285, 1091), p(223, 1071), p(200, 1034)),
        (p(177, 1000), p(173, 957), p(191, 924)),
    ], body)
    ellipse(draw, (226, 941, 330, 1058), (25, 29, 28))
    ellipse(draw, (670, 941, 774, 1058), (25, 29, 28))
    ellipse(draw, (242, 957, 314, 1040), (185, 176, 151), outline=chrome, width=5)
    ellipse(draw, (686, 957, 758, 1040), (185, 176, 151), outline=chrome, width=5)
    polygon(draw, [p(299, 878), p(701, 878), p(752, 949), p(248, 949)], (58, 74, 68))
    line(draw, [p(329, 891), p(671, 891)], (129, 143, 125), 3)
    ellipse(draw, (281, 898, 362, 942), (243, 215, 164), outline=chrome, width=3)
    ellipse(draw, (638, 898, 719, 942), (243, 215, 164), outline=chrome, width=3)
    ellipse(draw, (423, 906, 577, 1007), (34, 46, 43), outline=chrome, width=5)
    for yy in (924, 941, 958, 975, 992):
        line(draw, [p(442, yy), p(558, yy)], (145, 151, 128), 3)
    line(draw, [p(236, 1022), p(764, 1022)], chrome, 7)
    line(draw, [p(272, 1040), p(728, 1040)], (101, 111, 93), 3)
    line(draw, [p(383, 865), p(310, 716)], (237, 217, 177), 5)
    line(draw, [p(617, 865), p(690, 716)], (237, 217, 177), 5)


def hero_image():
    width, height = 1000, 1300
    image = canvas(width, height, (65, 79, 73), (29, 39, 36))
    draw = ImageDraw.Draw(image)
    rounded(draw, (74, 64, 926, 874), 24, (48, 63, 58))
    for xx in (118, 393, 668):
        rounded(draw, (xx, 104, xx + 206, 635), 100, (115, 128, 116))
        rounded(draw, (xx + 16, 122, xx + 190, 622), 86, (53, 72, 67))
        line(draw, [(xx + 103, 126), (xx + 103, 610)], (103, 117, 106), 3)
    ellipse(draw, (278, 208, 722, 660), (69, 82, 71))
    polygon(draw, [(0, 816), (1000, 816), (1000, 1300), (0, 1300)], (34, 45, 42))
    rounded(draw, (108, 1093, 892, 1145), 18, (62, 77, 68))
    draw_hero_mercedes(draw)
    line(draw, [(91, 1074), (913, 1074)], (116, 111, 88), 3)
    line(draw, [(146, 1193), (854, 1193)], (76, 86, 76), 2)
    return image


def add_paper_grain(image, seed):
    randomizer = random.Random(seed)
    image = image.resize((image.width // SCALE, image.height // SCALE), Image.Resampling.LANCZOS)
    pixels = image.load()
    for _ in range(image.width * image.height // 90):
        x = randomizer.randrange(image.width)
        y = randomizer.randrange(image.height)
        shift = randomizer.choice((-4, -3, -2, 2, 3, 4))
        r, g, b = pixels[x, y]
        pixels[x, y] = (max(0, min(255, r + shift)), max(0, min(255, g + shift)),
                        max(0, min(255, b + shift)))
    return image


def save_illustration(name, image, seed):
    add_paper_grain(image, seed).save(ASSETS / name, "JPEG", quality=93, subsampling=0, optimize=True)


def save_brand_mark():
    mark = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(mark)
    draw.rounded_rectangle((26, 28, 228, 228), radius=40, fill=(122, 95, 63, 255))
    draw.polygon([(76, 100), (180, 100), (128, 176)], fill=(246, 240, 224, 255))
    draw.rectangle((108, 102, 148, 170), fill=(246, 240, 224, 255))
    mark.save(ASSETS / "brand-mark.png")


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    save_brand_mark()
    save_illustration("hero-classic.jpg", hero_image(), 300)
    scenes = (
        ("car-alfa.jpg", "alfa", (1200, 900), {
            "sky": (227, 203, 175), "haze": (170, 145, 118), "hill": (133, 125, 101),
            "hill_far": (82, 94, 78), "ground": (64, 71, 59), "road": (203, 174, 132),
        }),
        ("car-peugeot.jpg", "peugeot", (1200, 900), {
            "sky": (221, 209, 190), "haze": (190, 174, 151), "stone": (174, 158, 137),
            "shadow_stone": (117, 113, 98), "glass": (65, 79, 72), "ground": (72, 75, 63),
            "road": (192, 174, 143),
        }),
        ("car-mercedes.jpg", "mercedes", (1200, 900), {
            "sky": (38, 52, 48), "haze": (27, 39, 36), "wall": (34, 48, 44),
            "arch": (99, 109, 93), "glass": (41, 57, 53), "mullion": (111, 119, 98),
            "light": (139, 125, 93), "ground": (34, 45, 42), "plinth": (77, 89, 77),
            "floor_line": (65, 78, 68),
        }),
        ("car-porsche.jpg", "porsche", (1200, 900), {
            "sky": (191, 205, 207), "haze": (156, 175, 179), "mountain": (88, 110, 116),
            "snow": (177, 189, 177), "ground": (65, 74, 66), "road": (196, 184, 159),
        }),
    )
    for seed, (filename, model, size, palette) in enumerate(scenes, start=301):
        save_illustration(filename, landscape_car(size, palette, model), seed)


if __name__ == "__main__":
    main()
