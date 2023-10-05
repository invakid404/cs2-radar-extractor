import os
import re
import glob
import pathlib
import vpk
import vdf
import json
import subprocess
from sortedcollections import SortedDict
from PIL import Image


RADAR_IMAGES_PATTERN = re.compile(
    "^panorama/images/overheadmaps/(.*?)_radar_psd.vtex_c$"
)
OVERVIEWS_PATTERN = re.compile("^resource/overviews/(.*?).txt$")


def extract_from_vpk(target, output_dir):
    images = {}
    overviews = {}

    def process_file(filepath, pattern, out):
        match = pattern.match(filepath)
        if not match:
            return

        (map,) = match.groups()
        out[map] = filepath

    for filepath in target:
        process_file(filepath, RADAR_IMAGES_PATTERN, images)
        process_file(filepath, OVERVIEWS_PATTERN, overviews)

    maps = set(images.keys()).intersection(overviews.keys())

    metadata = SortedDict()   
    for map in maps:
        image_path = images[map]
        image_input = target[image_path]

        image_output = pathlib.Path(output_dir, pathlib.Path(image_path).name)
        image_output.write_bytes(image_input.read())

        decompiled_output = pathlib.Path(output_dir, f"{map}.png")

        subprocess.run(
            ["Decompiler", "-i", image_output, "-o", decompiled_output],
            env={"PATH": os.getenv("PATH"), "COMPlus_EnableDiagnostics": "0"},
        )

        image_output.unlink()

        image = Image.open(decompiled_output)
        (image_x, image_y) = image.size

        overview_path = overviews[map]
        overview_input = target[overview_path]
        overview_data = overview_input.read().decode("utf-8")

        parsed_overview = vdf.loads(overview_data)[map]

        top_left_x = float(parsed_overview["pos_x"])
        top_left_y = float(parsed_overview["pos_y"])
        scale = float(parsed_overview["scale"])

        bottom_left_x = top_left_x + image_x * scale
        bottom_left_y = top_left_y - image_y * scale

        range = [top_left_x, top_left_y, bottom_left_x, bottom_left_y]
        metadata[map] = [round(coord) for coord in range]

    metadata_output = pathlib.Path(output_dir, "metadata.json")
    metadata_output.write_text(json.dumps(metadata))


def main():
    path_to_cs2 = os.getenv("CS2_PATH")
    if not path_to_cs2:
        raise RuntimeError("the CS2_PATH env variable must be set")

    output_dir = os.getenv("OUTPUT_DIR")
    if not output_dir:
        output_dir = "output"

    output_path = pathlib.Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    path_to_vpk = pathlib.Path(path_to_cs2, "game", "csgo", "pak01_dir.vpk")
    target = vpk.open(str(path_to_vpk.resolve()))

    extract_from_vpk(target, output_path.resolve())


if __name__ == "__main__":
    main()
