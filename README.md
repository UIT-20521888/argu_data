## That is project argument data

### 1. How to argument data detect?
#### The first you need install the following required libraries:

* PIL
* cv2
* numpy
* argparse
* os

 After having installed the above library packages, you need to prepare fonts, backround images and necessary characters. In it the backround images we put [here](https://drive.google.com/drive/folders/1CcgheeiRWSgsMTt6A5CJauvroazXHFsr?usp=share_link). These backgrounds are part of the 8000 background images set from the repo [SynthText](https://github.com/ankush-me/SynthText.git)

```
python3 argu_det\addtext\augment_det.py --input_bg_image <path foder background images> --file_language <path foder file language> --foder_fonts <path foder fonts> --output_data_folder <path foder data>
```
For exmple:
```
python3 argu_det/addtext/augment_det.py --input_bg_image ./images_1/bg_img --file_language argu_det/campos --foder_fonts argu_det/fonts --output_data_folder data_5500
```