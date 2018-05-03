# coding=utf-8
import os
import pygame
import random
import h5py 
from PIL import Image
import io 

def read_image_data_from_dset(DB_FNAME,more_img_file_path):
  db=h5py.File(DB_FNAME,'r') 
  
  for key in db.keys():
    print(key) #Names of the groups in HDF5 file.
    #Get the HDF5 group
    group = db[key]
    #Checkout what keys are inside that group.
    for key in group.keys():
        print(key) 
        print(group[key].name) 
        print(group[key].size) 

        rawData = group[key].value
        img=Image.fromarray(rawData,'RGB')
        img.save(more_img_file_path+key) 
  db.close()


  

if __name__ == '__main__':
    # path to the data-file, containing image, depth and segmentation:
    DB_FNAME = 'db/image_test.h5'

    #add more data into the dset
    more_img_file_path='gen_img_out/'

    read_image_data_from_dset(DB_FNAME,more_img_file_path)
