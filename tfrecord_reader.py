#导入相应的模块
import tensorflow as tf
import os
import random
import math
import sys
from PIL import Image 
import io

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
 
 
def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(
    serialized_example,
    features={
        'image_raw': tf.FixedLenFeature([], tf.string),
        'file_name': tf.FixedLenFeature([], tf.string),
        'class_id':tf.FixedLenFeature([],tf.int64),
        'height':tf.FixedLenFeature([],tf.int64),
        'width':tf.FixedLenFeature([],tf.int64),
        'img_mode':tf.FixedLenFeature([], tf.string),
    })

    image_raw = tf.decode_raw(features['image_raw'], tf.uint8) 
    class_id = tf.cast(features['class_id'],tf.int32)
    height = tf.cast(features['height'],tf.int32)
    width = tf.cast(features['width'],tf.int32)
    img_mode = tf.cast(features['img_mode'], tf.string)
    file_name = tf.cast(features['file_name'], tf.string)
    return image_raw,file_name,class_id,height,width,img_mode


def get_all_records(split_name,tf_dataset_dir):
 assert split_name in ['train','test'] 
 for shard_id in range(_NUM_SHARDS):
    #定义tfrecord的路径名字
    tfrecord_filename = _get_dataset_filename(tf_dataset_dir,split_name,shard_id)
    print(tfrecord_filename)
    with tf.Session() as sess:
        filename_queue = tf.train.string_input_producer([tfrecord_filename], num_epochs=1)
        image_raw,file_name,_,_,_,_ = read_and_decode(filename_queue)
        image_raw = tf.reshape(image_raw, [32,272, 3])
        
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())#就是这一行

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        try:
            while True:
                _,label = sess.run([image_raw,file_name])
                #imaged_data_array,label = sess.run([image_raw,file_name])
                print(label)
                #在这里为所欲为即可...
                # img=Image.fromarray(imaged_data_array, 'RGB')
                # img.save("test.jpg")
                # img.show()
                # img.close()
        except tf.errors.OutOfRangeError as e:
                coord.request_stop(e)
        finally:
            coord.request_stop()
            coord.join(threads) 

if __name__ == '__main__':
    #判断tfrecord文件是否存在
    if _dataset_exists(TF_DATASET_DIR):
        #读取图片数据
        get_all_records('train',TF_DATASET_DIR) 
        get_all_records('test',TF_DATASET_DIR) 
        print('all OK')
    else:
        print ('tfrecord not exists')
        
        