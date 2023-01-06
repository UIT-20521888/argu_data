python3 tools/extract_font_charset.py -w 8 resources/fonts_1/fonts/
python3 tools/create_colormap.py --max_k 3 -w 8 resources/images_1/bg_img/ resources/colormap/colormap_1.txt
synthtiger -o results_5500 -w 8 -c 5500 -v examples/synthtiger/template.py SynthTiger examples/synthtiger/config_horizontal.yaml
