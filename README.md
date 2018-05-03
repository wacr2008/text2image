# text2image
pygame text to image

基于 https://github.com/TianzhongSong/text2image.git 代码,
考虑到要自己生成CRNN的训练数据集,所以做了以下改动:
1.因为我这这的CRNN训练需要背景图,所以在生成的图片的时候加入了背景图
2.在它的基础上加入了将图片存储为hdf5格式的功能,并提供了读测试

