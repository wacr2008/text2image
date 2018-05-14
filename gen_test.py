# coding=utf-8
import os
import pygame
import random
import h5py 
from PIL import Image

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


if __name__ == '__main__': 
    # path to the data-file, containing image, depth and segmentation:
    DB_FNAME = 'db/image_test.h5'

    #add more data into the dset
    more_img_file_path='gen_test/'

    add_image_data_into_dset(DB_FNAME,more_img_file_path)
