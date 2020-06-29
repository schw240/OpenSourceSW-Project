import os, glob, time, warnings
import os.path
import keras.backend as K
import tensorflow as tf
from PIL import Image 
from random import randint, shuffle, uniform
warnings.simplefilter('error', Image.DecompressionBombWarning)
from keras.optimizers import RMSprop, SGD, Adam
from keras.models import Sequential, Model
from keras.layers import Conv2D, ZeroPadding2D, BatchNormalization, Input, Dropout
from keras.layers import Conv2DTranspose, UpSampling2D, Activation, Add, Lambda
from keras.layers.advanced_activations import LeakyReLU
from keras.activations import relu
from keras.initializers import RandomNormal
from keras_contrib.layers.normalization.instancenormalization import InstanceNormalization
import socketserver
import datetime
import base64
import numpy as np
import cv2
import socket
import sys
import inference2 as inf

# for convolution kernel
conv_init = RandomNormal(0, 0.02)
# for batch normalization
gamma_init = RandomNormal(1., 0.02)

# gloabal variables
image_size = 128
image_jitter_range = 30
load_size = image_size + image_jitter_range
batch_size = 16
input_nc = 3
path = './man/'
dpath = path + 'weights-cyclelossweight10-batchsize{}-imagesize{}/'.format(batch_size, image_size)
dpath_result = dpath + 'results'
now = datetime.datetime.now().strftime("%H-%M")
train_A = inf.load_data('./data/trainA/*')
train_B = inf.load_data('./data/trainB/*')
print(len(train_A))
print(len(train_B))

val_A = inf.load_data('./data/trainA/*')
val_B = inf.load_data('./data/trainB/*')

netD_A = inf.n_layer_discriminator(image_size)
netD_B = inf.n_layer_discriminator(image_size)
netG_A, real_A, fake_B = inf.resnet_generator(image_size, use_conv_transpose=True)
netG_B, real_B, fake_A = inf.resnet_generator(image_size, use_conv_transpose=True)
netD_B_predict_fake = netD_B(fake_B)
rec_A= netG_B(fake_B)
netD_A_predict_fake = netD_A(fake_A)
rec_B = netG_A(fake_A)
lambda_layer_inputs = [netD_B_predict_fake, rec_A, real_A, netD_A_predict_fake, rec_B, real_B]
for l in netG_A.layers: 
    l.trainable=True
for l in netG_B.layers: 
    l.trainable=True
for l in netD_A.layers: 
    l.trainable=False
for l in netD_B.layers: 
    l.trainable=False
netG_train_function = Model([real_A, real_B],Lambda(inf.netG_loss)(lambda_layer_inputs))
Adam(lr=2e-4, beta_1=0.5, beta_2=0.999, epsilon=None, decay=0.0)
netG_train_function.compile('adam', 'mae')
netD_A_predict_real = netD_A(real_A)

_fake_A = Input(shape=(image_size, image_size, input_nc))
_netD_A_predict_fake = netD_A(_fake_A)
for l in netG_A.layers: 
    l.trainable=False
for l in netG_B.layers: 
    l.trainable=False
for l in netD_A.layers: 
    l.trainable=True      
for l in netD_B.layers: 
    l.trainable=False

netD_A_train_function = Model([real_A, _fake_A], Lambda(inf.netD_loss)([netD_A_predict_real, _netD_A_predict_fake]))
netD_A_train_function.compile('adam', 'mae')
netD_B_predict_real = netD_B(real_B)

_fake_B = Input(shape=(image_size, image_size, input_nc))
_netD_B_predict_fake = netD_B(_fake_B)

for l in netG_A.layers: 
    l.trainable=False
for l in netG_B.layers: 
    l.trainable=False
for l in netD_B.layers: 
     l.trainable=True  
for l in netD_A.layers: 
    l.trainable=False 

netD_B_train_function= Model([real_B, _fake_B], Lambda(inf.netD_loss)([netD_B_predict_real, _netD_B_predict_fake]))
netD_B_train_function.compile('adam', 'mae')

netG_A_function = inf.get_generater_function(netG_A)
netG_B_function = inf.get_generater_function(netG_B)
load_name = dpath + '{}' + '10.h5'
netG_A.load_weights(load_name.format('tf_GA_weights'))
netG_B.load_weights(load_name.format('tf_GB_weights'))
netD_A.load_weights(load_name.format('tf_DA_weights'))
netD_B.load_weights(load_name.format('tf_DB_weights'))
netG_train_function.load_weights(load_name.format('tf_G_train_weights'))
netD_A_train_function.load_weights(load_name.format('tf_D_A_train_weights'))
netD_B_train_function.load_weights(load_name.format('tf_D_B_train_weights'))

while True:

    host = "192.168.0.2"
    port = 9955
    server_sock = socket.socket(socket.AF_INET)
    server_sock.bind((host, port))
    server_sock.listen(5)
    print("get....")
    client_sock, addr = server_sock.accept()
    print("connected : ", addr)


    image1 = []
    #image1 = open("now.jpg", 'wb')

    try:
    
        while True:
            data1=client_sock.recv(1024)
            print("data1 = ")
            print(data1)
            print("length = ")
            print(len(data1))
            image1.extend(data1)
            if len(data1) < 1024:
                break
            #while True:
                #image1.write(data1)
                #data1 = client_sock.recv(1024)
                #if bytes("DONE", 'utf-8') in data1:
                    #break
        print("get over")

        image = np.asarray(bytearray(image1), dtype="uint8")
        print("point1")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        print("point2")
        dir = os.path.dirname(os.path.abspath(__file__))
        client_dir = dir + "\\client\\" + str(now) + ".jpg"
        cv2.imwrite(client_dir, image)
               
        ## 이미지 받아와서 저장
        print("point3")
        
    except Exception:
        print(addr,"exception")
        shutdown(client_sock, SHUT_RD)
        
    #받아온 이미지 다시 읽어오기
    filename = client_dir
    print("1point")
    #이미지 변환하기
    	
    pred_A = inf.load_data(filename)
    val_pred = inf.load_data(filename)
    val_batch = inf.minibatchAB(pred_A, val_B, batch_size=1)
    _,A, B = next(val_batch)
    inf.show_generator_image(A,B, netG_A, netG_B)
    print("2point_fin_conv")
    #변환된 이미지 불러오고 jpg로 변경
    #img = inf.load_data('./conv/after' + str(now) + '.jpg')

    
    ### 가우시안 필터 적용 bmp파일로 저장됨
    #filename = ('./conv/after' + str(now) + '.jpg')
    im = Image.open('./conv/after' + str(now) + '.jpg')
    print("gaus point") 
    im_array = np.asarray(im) 
    kernel1d = cv2.getGaussianKernel(5, 3) 
    kernel2d = np.outer(kernel1d, kernel1d.transpose()) 
    low_im_array = cv2.filter2D(im_array, -1, kernel2d) 
    low_im = Image.fromarray(low_im_array) 
    low_im.save('./conv/' + 'new_res.bmp','BMP')
    print("3pointgaus fin")
    
   #변환된 이미지 다시 불러오기
    #filename = ('./conv/after' + str(now) + '.jpg')
    filename2 = ('./conv/new_res.bmp')
    print('4point')
    f=open(filename2 ,'rb')
    data2=f.read()
    ####여기서 이미지 전송
    exx=client_sock.sendall(data2)
    print("send????")
    f.flush()
    f.close()