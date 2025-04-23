# Satellite to Pixel Map Converter

This tool helps convert satellite images of real-world places into pixel-aligned, grid-ready maps. It's approximate but useful for creating a quick and dirty reference image when using tools such as [Tiled Map Editor](https://www.mapeditor.org/)

## Usage

1. Run the program and pass it a filepath to your satellite image: 
```bash
python3 main.py ./images/test_image.png
```
2. Click two points to mark the ends of flat plane that you want to be horizontally aligned.
3. Click two opposite corners to crop the image
4. Enter real-world width & height in meters (you can use google maps to measure distances), use whole numbers.
5. Tool scales and overlays a grid.
6. Final image is saved to the directory it was read from, with `_grid` appended to the name.

## Dependencies

- Python 3
- OpenCV (`cv2`)
- Numpy

Install dependencies:

```bash
pip3 install -r requirements.txt
```

## Notes

By default, the scale is 16 pixels per metre and the grid uses red (minor) and yellow (major every 10 units) lines. You can customize this by modifying the following lines in main.py:
```python
resized = scale_image_to_metres(cropped, real_width_m, real_height_m, pixels_per_m=16)
# draw grid
grid_img = draw_grid(resized, tile_size_px=16, colour=(0, 0, 255), major_colour=(0, 255, 255))
```

## License

This project is released into the public domain under [The Unlicense](https://unlicense.org/). You are free to use, modify, and distribute it without restriction.

## Satellite Imagery Source

Satellite imagery used in this project is based on orthophotography captured on 11 February 2021 over the Canterbury Region (Christchurch CBD), New Zealand.  
Captured by **Landpro Ltd** for **Environment Canterbury**.  
Available via [Land Information New Zealand (LINZ)](https://data.linz.govt.nz/layer/106915-christchurch-005m-urban-aerial-photos-2021/) under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
