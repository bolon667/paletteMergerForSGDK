# SGDK Palette Merger

![paletteMergerForSGDK_logo](https://github.com/bolon667/paletteMergerForSGDK/blob/main/gitImages/SGDK_paletteMerger_logo.jpg)

## About

This tool allows you easily change palette of each tile on the map by combining several images with different palettes.

## How to use

> Every **png** mast have "-" sign for **settings**, and have same **resolution**


- Put images in **png** format, next to **SGDK Palette Merger**
- Rename the images, according to this template
```
imageName-palType_layerNum.png
```

Where **palType** can be:

- **pal0-pal3** - for palettes (myLevel-pa1_0.png, myLevel-pal2_1.png)
- **pal0P-pal3P** - for palettes with priority (myLevel-pa1_p_3.png, myLevel-pal2_p_2.png)
- **pal0Mask-pal3Mask** - when you want to use mask in merging alghorithm, by default, it's using 1st color of palette. And example: myLevel-pa1_mask.png, myLevel-pal2_mask.png

**layerNum** - it's a number from **0** to **3**, where **0** is lowest layer, and **3** is highest. **layerNum** specifies the order in which the image is inserted.

And run this tool, you will get file **result.png**

## License

MIT
