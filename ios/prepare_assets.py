#!/usr/bin/env python3
"""Copy the same 22 Android tarot images into iOS asset catalogs."""
import json
from pathlib import Path
source = Path("android/app/src/main/res/drawable")
target = Path("ios/MoonArcana/Assets.xcassets")
target.mkdir(parents=True, exist_ok=True)
for png in sorted(source.glob("*.png")):
    name = png.stem
    if name == "moon_arcana_icon_512":
        continue
    folder = target / (name + ".imageset")
    folder.mkdir(exist_ok=True)
    (folder / png.name).write_bytes(png.read_bytes())
    (folder / "Contents.json").write_text(json.dumps({"images":[{"filename":png.name,"idiom":"universal"}],"info":{"author":"xcode","version":1}}),encoding="utf-8")
icon = source / "moon_arcana_icon_512.png"
if icon.exists():
    folder = target / "AppIcon.appiconset"
    folder.mkdir(exist_ok=True)
    (folder / icon.name).write_bytes(icon.read_bytes())
    (folder / "Contents.json").write_text(json.dumps({"images":[{"filename":icon.name,"idiom":"universal","platform":"ios","size":"1024x1024"}],"info":{"author":"xcode","version":1}}),encoding="utf-8")
print("iOS card and icon assets prepared")
