# SGDK Palette Merger

![paletteMergerForSGDK_logo](https://github.com/bolon667/paletteMergerForSGDK/blob/main/gitImages/SGDK_paletteMerger_logo.jpg)

## About

This tool allows you easily change palette of each tile on the map by combining several images with different palettes.

## How to use

> Every **png** mast have "-" sign for **settings**, and have same **resolution**


- Put images in **png** format, next to **SGDK Palette Merger**
- Rename the images, according to this template
```
imageName-settings.png
```

Where **settings** can be:

- **pal0-pal3** - for palettes (myLevel-pa1.png, myLevel-pal2.png)
- **pal0_p-pal3_p** - for palettes with priority (myLevel-pa1_p.png, myLevel-pal2_p.png)
- **pal0_mask-pal3_mask** - when you want to use mask in merging alghorithm, by default, it's using 1st color of palette. And example: myLevel-pa1_mask.png, myLevel-pal2_mask.png

And run this tool, you will get file **result.png**

## License

MIT
