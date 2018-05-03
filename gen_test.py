# coding=utf-8
import os
import pygame
import random
import h5py 
from PIL import Image

# background and font
color_list = [[(255, 255, 255), (0, 0, 0)],
              [(255, 255, 0), (0, 0, 0)],
              [(255, 0, 255), (0, 0, 0)],
              [(0, 255, 255), (0, 0, 0)],
              [(255, 0, 0), (0, 0, 0)],
              [(0, 0, 255), (0, 0, 0)],
              [(0, 255, 0), (0, 0, 0)],
              [(0, 0, 0), (255, 255, 255)],
              [(255, 255, 0), (255, 255, 255)],
              [(255, 0, 255), (255, 255, 255)],
              [(0, 255, 255), (255, 255, 255)],
              [(255, 0, 0), (255, 255, 255)],
              [(0, 0, 255), (255, 255, 255)],
              [(0, 255, 0), (255, 255, 255)]
              ]


def add_image_data_into_dset(DB_FNAME,more_img_file_path):
  db=h5py.File(DB_FNAME,'w')
  db.create_group('image')
  for imname in os.listdir(more_img_file_path):
    if imname.endswith('.jpg'):
      full_path=more_img_file_path+imname
      print(full_path,imname)
      
      j=Image.open(full_path)
      imgSize=j.size
      rawData=j.tobytes()
      img=Image.frombytes('RGB',imgSize,rawData)
      #img = img.astype('uint16')
      db['image'].create_dataset(imname,data=img)
  db.close()



# 生成数字与字母的组合
def genearte_images(per_class=10000, continue_gen=False, save_path='/home/dl1/datasets/ocr/gen_img/'):
    """
    :param per_class: 每种色彩配置下生成的图片数量
    :param continue_gen:  是否接着上一次继续生成，若是则改为True
    :param save_path: 图片保存的路径
    :return: None
    """
    characters = '0123456789-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    if not os.path.exists(save_path):
        os.mkdir(save_path)
    pygame.init()
    screen = pygame.display.set_mode((272, 32))
    font = pygame.font.SysFont('SimHei', 31)
    f = open('char_std_5990.txt', 'r', encoding='gb18030')
    label_txt = f.readlines()
    f.close()
    label_index = [label.strip() for label in label_txt]
    txt_mode = 'w' if not continue_gen else 'a'
    image_counter = 1000000 if not continue_gen else 1000000 + len(os.listdir(save_path))
    with open('train.txt', txt_mode) as f:
        for color in color_list:
            count = 0
            while count < per_class:
                label_line = str(image_counter) + '.jpg'
                text_length = 15
                text = ' '
                for i in range(text_length):
                    ch = characters[random.randint(0, len(characters) - 1)]
                    text += ch
                    label_line += ' ' + str(label_index.index(ch))
                text += ' '

                ftext = font.render(text, True, (255, 255, 255)) #, color[0])
                f.write(label_line + '\n')
 
                # 载入背景图
                bk_img = 'background/'+str(random.randint(1,5))+'.bmp' 

                background = pygame.image.load(bk_img)
                screen.fill(0) # 因为默认背景白 
                screen.blit(background, (0, 0)) 
                screen.blit(ftext, (0, 0))  
                pygame.display.update()

                pygame.image.save(screen, save_path + str(image_counter) + ".jpg")
                image_counter += 1
                count += 1
        f.close()


# 生成汉字、字母、数字的组合
def genearte_hanzi_mages(per_class=300, continue_gen=False, save_path='/home/dl1/datasets/ocr/gen_img/'):
    """
    :param per_class: 每种色彩配置下生成的图片数量 = per_class * 598
    :param continue_gen:  是否接着上一次继续生成，若是则改为True
    :param save_path: 图片保存的路径
    :return: None
    """
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    pygame.init()
    screen = pygame.display.set_mode((272, 32))
    font = pygame.font.SysFont('SimHei', 31)
    f = open('char_std_5990.txt', 'r', encoding='gb18030')
    label_txt = f.readlines()
    f.close()
    label_index = [label.strip() for label in label_txt]
    characters = label_index[1:]
    txt_mode = 'w' if not continue_gen else 'a'
    image_counter = 1000000 if not continue_gen else 1000000 + len(os.listdir(save_path))
    with open('train.txt', txt_mode) as f:
        for color in color_list:
            for _ in range(per_class):
                count = 0
                random.shuffle(characters)
                text_length = 10
                for i in range((len(characters))//text_length):
                    text = ' '
                    label_line = str(image_counter) + '.jpg'
                    for ch in characters[count:count+text_length]:
                        text += ch
                        label_line += ' ' + str(label_index.index(ch))
                    text += ' '
                    ftext = font.render(text, True, (255,255,255)) #color[1], color[0])
                    f.write(label_line + '\n')

                    # 载入背景图
                    bk_img = 'background/'+str(random.randint(1,5))+'.bmp' 

                    background = pygame.image.load(bk_img)
                    screen.fill(0) # 因为默认背景白 
                    screen.blit(background, (0, 0)) 
                    screen.blit(ftext, (0, 0))  
                    pygame.display.update()
                    
                    pygame.image.save(screen, save_path + str(image_counter) + ".jpg")
                    image_counter += 1
                    count += 10
        f.close()


if __name__ == '__main__':
    #genearte_images(per_class=10000, continue_gen=False,save_path="gen_img/")
    #genearte_hanzi_mages(per_class=120, continue_gen=True,save_path="gen_img_hz/")

    # path to the data-file, containing image, depth and segmentation:
    DB_FNAME = 'db/image_test.h5'

    #add more data into the dset
    more_img_file_path='gen_test/'

    add_image_data_into_dset(DB_FNAME,more_img_file_path)
