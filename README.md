# cs2-radar-extractor

A simple script that extracts CS2 radar images and metadata from the game.
Requires a local CS2 installation.

Depends on
[ValveResourceFormat](https://github.com/ValveResourceFormat/ValveResourceFormat)
to extract the images from the proprietary compiled Valve formats used by the
game.

## Quick Start

### Manual

1. Install Python dependencies:

```shell
$ pip install vpk vdf pillow sortedcollections
```

2. Install `ValveResourceFormat`:

Refer to the
[releases](https://github.com/ValveResourceFormat/ValveResourceFormat/releases)
for precompiled binaries. In particular, you need the `Decompiler` executable.
It must be present in `$PATH` for the script to work.

3. Set the path to your CS2 install:

```shell
$ export CS2_PATH="/path/to/cs2"
```

The path could be retrieved from Steam if you don't know it.

4. Run the script

```shell
$ python extract.py
```

### Docker

To run this project via Docker, you can use the
[prebuilt Docker image](https://github.com/invakid404/cs2-radar-extractor/pkgs/container/cs2-radar-extractor)
like so:

```shell
$ docker run \
    -v "${CS2_PATH}:/cs2:ro" \
    -v ./output:/data/output \
    ghcr.io/invakid404/cs2-radar-extractor
```

### Nix

Nix users can directly skip to step 3 when using the provided `shell.nix` file.
