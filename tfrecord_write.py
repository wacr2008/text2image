#导入相应的模块
import tensorflow as tf
import os
import random
import math
import sys
from PIL import Image 

#划分验证集训练集
_NUM_TEST = 40
#random seed
_RANDOM_SEED = 0
#数据块
_NUM_SHARDS = 2
#tfrecords数据集路径
TF_DATASET_DIR = 'gen_tf/'
#数据集路径
DATASET_DIR = 'images/'
#标签文件
LABELS_FILENAME = 'labels.txt'
#定义tfrecord 的路径和名称
def _get_dataset_filename(dataset_dir,split_name,shard_id):
    output_filename = 'image_%s_%05d-of-%05d.tfrecord' % (split_name,shard_id,_NUM_SHARDS)
    return os.path.join(dataset_dir,output_filename)

#判断tfrecord文件是否存在
def _dataset_exists(dataset_dir):
    for split_name in ['train','test']:
        for shard_id in range(_NUM_SHARDS):
            #定义tfrecord的路径名字
            output_filename = _get_dataset_filename(dataset_dir,split_name,shard_id)
        if not tf.gfile.Exists(output_filename):
            return False
    return True

#获取图片以及分类
def _get_filenames_and_classes(dataset_dir):
    #数据目录
    directories = []
    #分类名称
    class_names = []
    for filename in os.listdir(dataset_dir):
        #合并文件路径
        path = os.path.join(dataset_dir,filename)
        #判断路径是否是目录
        if os.path.isdir(path):
            #加入数据目录
            directories.append(path)
            #加入类别名称
            class_names.append(filename)
    photo_filenames = []
    #循环分类的文件夹
    for directory in directories:
        for filename in os.listdir(directory):
            path = os.path.join(directory,filename)
            #将图片加入图片列表中
            photo_filenames.append(path)
    #返回结果
    return photo_filenames ,class_names

def int64_feature(values):
    if not isinstance(values,(tuple,list)):
        values = [values]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

def bytes_feature(values):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))

#图片转换城tfexample函数
def image_to_tfexample(image_raw,file_name,width,height,img_mode,class_id):
    return tf.train.Example(features=tf.train.Features(feature={
        'image_raw': bytes_feature(image_raw),
        'file_name': bytes_feature(file_name),
        'class_id': int64_feature(class_id),
        'height': int64_feature(height),  
        'width': int64_feature(width),  
        'img_mode': bytes_feature(img_mode),  
    }))

def write_label_file(labels_to_class_names,tf_dataset_dir,filename=LABELS_FILENAME):
    label_filename = os.path.join(tf_dataset_dir,filename)
    with tf.gfile.Open(label_filename,'w') as f:
        for label in labels_to_class_names:
            class_name = labels_to_class_names[label]
            f.write('%d:%s\n' % (label, class_name))

#数据转换城tfrecorad格式
def _convert_dataset(split_name,filenames,class_names_to_ids,tf_dataset_dir):
    assert split_name in ['train','test']
    #计算每个数据块的大小
    num_per_shard = int(len(filenames) / _NUM_SHARDS)
    with tf.Graph().as_default():
        with tf.Session() as sess:
            for shard_id in range(_NUM_SHARDS):
            #定义tfrecord的路径名字
                output_filename = _get_dataset_filename(tf_dataset_dir,split_name,shard_id)
                print(output_filename)
                with tf.python_io.TFRecordWriter(output_filename) as tfrecord_writer:
                    #每个数据块开始的位置
                    start_ndx = shard_id * num_per_shard
                    #每个数据块结束的位置
                    end_ndx = min((shard_id+1) * num_per_shard,len(filenames))
                    for i in range(start_ndx,end_ndx):
                        try:
                            #sys.stdout.write('\r>> Converting image %d/%d shard %d '% (i+1,len(filenames),shard_id))
                            #sys.stdout.flush()
                            #读取图片
                            img=Image.open(filenames[i])
                            width, height = img.size
                            img_mode = img.mode
                            img_raw=img.tobytes() 
                            #获取图片的类别名称
                            #basename获取图片路径最后一个字符串
                            #dirname是除了basename之外的前面的字符串路径
                            file_name = os.path.basename(filenames[i])
                            class_name = os.path.basename(os.path.dirname(filenames[i]))
                            #获取图片的id 
                            class_id = class_names_to_ids[class_name] 
                            

                            #生成tfrecord文件
                            example = image_to_tfexample(img_raw,file_name.encode("utf-8"),height,width,img_mode.encode("utf-8"),class_id)
                            #写入数据
                            tfrecord_writer.write(example.SerializeToString())
                            img.close()
                        except IOError  as e:
                            print ('could not read:',filenames[i])
                            print ('error:' , e)
                            print ('skip it \n') 

if __name__ == '__main__':
    #判断tfrecord文件是否存在
    if _dataset_exists(TF_DATASET_DIR):
        print ('tfrecord exists')
    else:
        #获取图片以及分类
        photo_filenames,class_names = _get_filenames_and_classes(DATASET_DIR)
        #将分类的list转换成dictionary{‘house':3,'flowers:2'}
        class_names_to_ids = dict(zip(class_names,range(len(class_names))))
        #切分数据为测试训练集
        random.seed(_RANDOM_SEED)
        random.shuffle(photo_filenames)
        training_filenames = photo_filenames[_NUM_TEST:]
        testing_filenames = photo_filenames[:_NUM_TEST]
        #数据转换
        _convert_dataset('train',training_filenames,class_names_to_ids,TF_DATASET_DIR)
        _convert_dataset('test',testing_filenames,class_names_to_ids,TF_DATASET_DIR)
        #输出lables文件
        #与前面的 class_names_to_ids中的元素位置相反{1:'people,2:'flowers'}
        labels_to_class_names = dict(zip(range(len(class_names)),class_names))
        write_label_file(labels_to_class_names,TF_DATASET_DIR)
        