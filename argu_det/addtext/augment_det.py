from PIL import Image, ImageDraw, ImageFont
import os 
import argparse
import numpy as np
import cv2

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_bg_image", required=True)
    parser.add_argument("--output_data_folder", required=True)
    parser.add_argument("--file_language", required=True)
    parser.add_argument("--foder_fonts", required=True)
    parser.add_argument("--random_seed",required=True)
    return parser.parse_args()
    
def get_font(foder_fonts):
    list_font = os.listdir(foder_fonts)
    return np.random.choice(list_font)

def read_language(path_foder_language):
    all_data = []
    for file in os.listdir(path_foder_language):
        path_language = os.path.join(path_foder_language, file)
        with open(path_language,'r',encoding='utf8') as f:
            data = f.read()
        data = data.split("\n")[:-1]
        all_data = all_data + data
    return all_data
def get_lines():
    list_lines = [1,2,3,4]
    return np.random.choice(list_lines)

def get_possions(image, num_poss):
    width, height = image.size
    range_width = range(width-200)
    range_height = range(height-200)
    list_possions = []
    for i in range(num_poss):
        possions = [np.random.choice(range_width,replace = False),np.random.choice(range_height,replace = False)]
        list_possions.append(possions)
    return list_possions

def get_num_text():
    mintext = 1
    maxtext = 10
    list_text = range(mintext,maxtext+1)
    return np.random.choice(list_text)
def get_poss():
    mintext = 1
    maxtext = 5
    list_text = range(mintext,maxtext+1)
    return np.random.choice(list_text)

def get_color(list_color):
    return np.random.choice(list_color)

def get_iou(ground_truth, pred):
    # coordinates of the area of intersection.
    ix1 = np.maximum(ground_truth[0], pred[0])
    iy1 = np.maximum(ground_truth[1], pred[1])
    ix2 = np.minimum(ground_truth[2], pred[2])
    iy2 = np.minimum(ground_truth[3], pred[3])
     
    # Intersection height and width.
    i_height = np.maximum(iy2 - iy1 + 1, np.array(0.))
    i_width = np.maximum(ix2 - ix1 + 1, np.array(0.))
     
    area_of_intersection = i_height * i_width
     
    # Ground Truth dimensions.
    gt_height = ground_truth[3] - ground_truth[1] + 1
    gt_width = ground_truth[2] - ground_truth[0] + 1
     
    # Prediction dimensions.
    pd_height = pred[3] - pred[1] + 1
    pd_width = pred[2] - pred[0] + 1
     
    area_of_union = gt_height * gt_width + pd_height * pd_width - area_of_intersection
     
    iou = area_of_intersection / area_of_union
     
    return iou
def draw_box(list_box,image,idx):
    if len(list_box)<=0:
        return
    save_path = './draw_box'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for box in list_box:
        # print(box)
        start = (int(box[0]),int(box[1]))
        end = (int(box[2]),int(box[3]))
        print(start, end)
        color = (255, 255, 0)
        image = cv2.rectangle(image,start,end,color,2)
    path_save = os.path.join(save_path,f'{idx}.jpg')
    cv2.imwrite(path_save, image)

def check_over(possion,image,w,h):
    x_min = possion[0]
    x_max = possion[0] + w
    y_min = possion[1]
    y_max = possion[1] + h
    width, height = image.size
    if x_min<0 or x_max >width or y_min<0 or y_max > height:
        return True
    return False
def check_over_lab(possion,image,w,h, hist_box):
    x_min = possion[0]
    x_max = possion[0] + w
    y_min = possion[1]
    y_max = possion[1] + h
    pre = [x_min, y_min, x_max, y_max]
    for box in hist_box:
        if get_iou(pre,box)!=0:
            return True
    return False
def get_possion(image,w,h, hist_box):
    width, height = image.size
    range_width = range(width)
    range_height = range(height)
    flag = 0
    while flag <= 1000:
        flag +=1
        possions = [np.random.choice(range_width),np.random.choice(range_height)]
        if not(check_over(possions,image,w,h)) and not(check_over_lab(possions,image,w,h, hist_box)):
            break
    if flag > 1000:
        return -1
    return possions
def draw_image(path_image,path_folder_out,list_language,foder_fonts,output_data_folder_labels,idx):
    image = Image.open(path_image)
    draw = ImageDraw.Draw(image)
    num_poss = get_poss()
    list_possion = get_possions(image, num_poss)
    MIN_FONT = 30
    MAX_FONT = 200
    colors = ["green", "blue", "red", "yellow", "purple","black","white"]
    path_label = os.path.join(output_data_folder_labels,f"{idx}.txt")
    hist_box = []
    # history_position = []
    f = open(path_label,'w')
    for possion in list_possion:
        font_size = get_font_size(MIN_FONT,MAX_FONT)
        num_text = get_num_text()
        color = get_color(colors)
        # print(color)
        font_name = get_font(foder_fonts)
        path_font = os.path.join(foder_fonts,font_name)
        for _ in range(num_text):
            text = np.random.choice(list_language)
            font = ImageFont.truetype(path_font, size=font_size)
            w,h = draw.textsize(text, font)
            # possion = get_possion(hist_box,image,w,h)
            if check_over(possion,image,w,h) or check_over_lab(possion,image,w,h, hist_box):
                possion = get_possion(image,w,h, hist_box)
                if possion == -1:
                    break
            x_min = possion[0]
            x_max = possion[0] + w
            y_min = possion[1]
            y_max = possion[1] + h
            draw.text((possion[0],possion[1]),text,font=font, fill=color)
            hist_box.append([x_min, y_min, x_max, y_max])
            f.write(f"{x_min},{y_min},{x_max},{y_max},{text}\n")
            possion[0] += w + 10
    f.close()
    path_save = os.path.join(path_folder_out,f"{idx}.jpg")
    # print(path_image.split('\\')[-1])
    # print(path_save)
    image.save(path_save)
    # image_true = cv2.imread(path_save)
    # # print(image_true)
    # draw_box(hist_box,image_true,idx)

def get_font_size(min_size, max_size):
    list_font = range(min_size, max_size+1)
    return np.random.choice(list_font)

def main(input_bg_image,output_data_folder,file_language,random_seed,foder_fonts):
    if not(os.path.exists(output_data_folder)):
        os.mkdir(output_data_folder)
    output_data_folder_image = os.path.join(output_data_folder,"images")
    output_data_folder_labels = os.path.join(output_data_folder,"labels")

    if not(os.path.exists(output_data_folder_image)):
        os.mkdir(output_data_folder_image)

    if not(os.path.exists(output_data_folder_labels)):
        os.mkdir(output_data_folder_labels)
    # path_immiage = os.path.join(input_bg_image,"im0001.jpg")
    list_language = read_language(file_language)
    for i in range(5500):
        file_image = np.random.choice(os.listdir(input_bg_image))
        path_image = os.path.join(input_bg_image,file_image)
        print(i)
        # if i == 10:
        #     break
        try:
            draw_image(path_image,output_data_folder_image,list_language,foder_fonts,output_data_folder_labels,i)
        except:
            print("Error")
        # draw_image(path_image,output_data_folder_image,list_language,foder_fonts,output_data_folder_labels,i)
if __name__ == "__main__":
    args = get_parser()
    main(args.input_bg_image, args.output_data_folder, args.file_language, args.random_seed,args.foder_fonts)
    # main(args.i)
    # print(args.input_data_folder_image)
