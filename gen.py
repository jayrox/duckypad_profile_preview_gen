import os
import re
import sys


def get_btn_value(buttons, id):
    button_value = None
    if not id.endswith(" "):
        id = id + " "

    for button in buttons:
        if button.startswith(id):
            button_value = button

    if not button_value:
        return None

    button_value = button_value[len(id) :]
    button_value = button_value.strip()

    return button_value


def clamp(x):
    if isinstance(x, str):
        x = int(x.strip())
    return max(0, min(x, 255))


profiles_path = None
try:
    profiles_path = sys.argv[1]
except IndexError:
    print("Profiles path is required")
    exit(1)

if not profiles_path:
    print("Profiles path is required")
    exit(1)

print("Parsing: ", profiles_path)

profiles = []

for root, dirs, files in os.walk(profiles_path, topdown=False):
    print("".join("*" * 25))
    for name in files:
        if name != "config.txt":
            continue
        config_name = os.path.join(root, name)
        print("Parsing: ", config_name)

        with open(config_name, "r", encoding="utf8") as fp:
            lines = fp.readlines()

        cells = []
        for i in range(1, 16):
            z1_text = get_btn_value(lines, f"z{i}")
            z1_color = get_btn_value(lines, f"SWCOLOR_{i}")

            if not z1_text:
                cells.append("&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;")
                continue

            r, g, b, color_hex = None, None, None, None

            if z1_color:
                r, g, b = z1_color.split(" ")

                color_hex = "#{0:02x}{1:02x}{2:02x}".format(
                    clamp(r), clamp(g), clamp(b)
                )

            z1_text_len = len(z1_text)

            z1_text = z1_text.replace("|", "\|").replace("_", "\_")
            if z1_text_len < 7:
                padding = int((7 - z1_text_len) / 2)
                z1_text = ("&nbsp;" * padding) + z1_text + ("&nbsp;" * padding)

            cell = z1_text

            if color_hex and "_" not in z1_text:
                cell = r"$${\textsf{\color{" + color_hex + r"} " + z1_text + r" }}$$"

            cells.append(cell)

        table = f"\n|       |       |       |\n| :----------: | :----------: | :----------: |\n| {cells[0]} | {cells[1]} | {cells[2]} |\n| {cells[3]} | {cells[4]} | {cells[5]} |\n| {cells[6]} | {cells[7]} | {cells[8]} |\n| {cells[9]} | {cells[10]} | {cells[11]} |\n| {cells[12]} | {cells[13]} | {cells[14]} |\n\n"

        profile_name = root.split("_")[-1]
        profile_index = re.search(r"profile(\d+)_", root)
        index = None
        if profile_index.group(1):
            index = int(profile_index.group(1))
        profiles.append({"name": profile_name, "index": index, "table": table})

profiles = sorted(profiles, key=lambda d: d["index"])

with open("tables.md", "w", encoding="utf8") as fp:
    fp.write("\n")
    for profile in profiles:
        fp.write(f'# Profile {profile["index"]}: {profile["name"]}')
        fp.write("\n")
        fp.write(profile["table"])
        fp.write("\n")
