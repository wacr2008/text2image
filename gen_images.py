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
    txt_mode = 'rw' if not continue_gen else 'ra'
    image_counter = 1000000 if not continue_gen else 1000000 + len(os.listdir(save_path))

    image_number =0
    image_class =0
    if not os.path.exists(save_path+str(image_class)):
        os.mkdir(save_path+str(image_class))

    with open('simple.txt', txt_mode) as f:
        for color in color_list:
            count = 0
            while count < per_class: 
                image_number +=1
                if(image_number>2499):
                    image_number =0
                    image_class +=1
                    if not os.path.exists(save_path+str(image_class)):
                        os.mkdir(save_path+str(image_class))

                label_line = save_path+str(image_class)+"/"+str(image_counter) + ".jpg"
                
                text_length = 15
                text = ' '
                for i in range(text_length):
                    ch = characters[random.randint(0, len(characters) - 1)]
                    text += ch 
    
                text += ' '     

                ftext = font.render(text, True, (255, 255, 255)) #, color[0])
                
                label_line +=  ' '
                label_line +=  text
                label_line +=  '\n'
                
                f.write(label_line.encode("utf-8"))
 
                # 载入背景图
                bk_img = 'background/'+str(random.randint(1,5))+'.bmp' 

                background = pygame.image.load(bk_img)
                screen.fill(0) # 因为默认背景白 
                screen.blit(background, (0, 0)) 
                screen.blit(ftext, (0, 0))  
                pygame.display.update()
 
                        
                pygame.image.save(screen, save_path+str(image_class)+"/" + str(image_counter) + ".jpg")
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
    txt_mode = 'bw' if not continue_gen else 'ba'
    
    image_number=0
    image_class=0
    image_counter = 1000000 if not continue_gen else 1000000 + len(os.listdir(save_path))

    if not os.path.exists(save_path+str(image_class)):
        os.mkdir(save_path+str(image_class))

    with open('hz_simple.txt', txt_mode) as f:
        for color in color_list:
            for _ in range(per_class):
                count = 0
                random.shuffle(characters)
                text_length = 10
                for i in range((len(characters))//text_length): 
                    image_number +=1
                    if(image_number>2500):
                        image_number =0
                        image_class +=1
                        if not os.path.exists(save_path+str(image_class)):
                            os.mkdir(save_path+str(image_class))

                    text = ' '
                    label_line = save_path+str(image_class)+"/"+str(image_counter) + ".jpg"
                    for ch in characters[count:count+text_length]:
                        text += ch
                    
                    text += ' '
                    label_line +=  ' '
                    label_line +=  text
                    label_line +=  '\n'

                    ftext = font.render(text, True, (255,255,255)) #color[1], color[0])
                    f.write(label_line.encode("utf-8"))

                    # 载入背景图
                    bk_img = 'background/'+str(random.randint(1,5))+'.bmp' 

                    background = pygame.image.load(bk_img)
                    screen.fill(0) # 因为默认背景白 
                    screen.blit(background, (0, 0)) 
                    screen.blit(ftext, (0, 0))  
                    pygame.display.update()
                     
                     
                    pygame.image.save(screen, save_path+str(image_class)+"/" + str(image_counter) + ".jpg")
                    image_counter += 1 
                    
                    count += 10
        f.close()


if __name__ == '__main__':
    genearte_hanzi_mages(per_class=120, continue_gen=True,save_path="gen_img_hz/") 
    genearte_images(per_class=10000, continue_gen=False,save_path="gen_img/")