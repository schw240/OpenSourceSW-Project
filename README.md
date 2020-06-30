# OpenSourceSW

오픈소스SW 기여
딥러닝 기반 얼굴변환 프로젝트

조원: 김한주 , 김성민 , 전현진

## Application with Face Conversion Project with CycleGAN


딥러닝 알고리즘인 CycleGAN을 이용하여 만약 흡연 , 음주 , 마약등에 중독된다면
얼굴이 어떻게 변화하는지 사용자에게 이미지를 받아서 어플리케이션을 통해
변형된 얼굴 이미지를 보여주는 프로젝트입니다.

###  Unpaired Image to Image Transition

Source: Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks
https://junyanz.github.io/CycleGAN/

The previous image-to-image translation such as Pix2Pix learns the mapping between an input image and an output image with a set of aligned image pairs. However, for many tasks, paired training dataset is unavailable. CycleGAN solves this issue by learning to translate an image from a source domain X to a target domain Y in the absence of paired examples.

## Dataset

Source: UTKFace - Large Scale Face Dataset + drugIdentification(https://github.com/JoinGitHubing/drugIdentification) + etc(Google , SHERIFF)

## Test Result

![3000장 이미지 변환 결과(before, after) (2)](https://user-images.githubusercontent.com/54871612/86091095-4456b900-bae6-11ea-94a8-6f3a08756ef5.jpg)
![3000장 이미지 변환 결과(before, after) (3)](https://user-images.githubusercontent.com/54871612/86091096-44ef4f80-bae6-11ea-9fc9-9459f6d04f06.jpg)
![500장 이미지 변환 결과(before , after) (1)](https://user-images.githubusercontent.com/54871612/86091098-44ef4f80-bae6-11ea-94ad-5abc20538f5c.jpg)
![500장 이미지 변환 결과(before , after) (2)](https://user-images.githubusercontent.com/54871612/86091099-4587e600-bae6-11ea-99ce-2b578f20e40a.jpg)

문제점: CycleGan은 이미지 데이터가 많이 필요한 Unsupervised 알고리즘인데
비지도학습의 경우 컴퓨터가 스스로 학습할 수 있도록 목표가 명확한 깔끔한 이미지 데이터셋이 필요합니다.
음주 , 흡연, 마약등의 중독증상에 의하여 변화하는 가장 큰 특징들은 3가지가 있습니다.
# 1. 피부의 붉은 반점
# 2. 노화(주름)
# 3. 피부톤(down)

이 3가지 문제점들을 전부 가지고 있거나 아니면 각각의 문제점들을 가진 고해상도의 이미지가 필요한데
저희가 자료수집에 많은 시간을 투자하였지만 결국 충분한 자료를 찾지 못하였습니다. 

학습 이미지가 모자란 관계로 결과 이미지가 많이 깨져있습니다. 

### CNN이용한 고해상도로 이미지 변환

![CNN 이용 고해상도 변환 3000장](https://user-images.githubusercontent.com/54871612/86091455-ea0a2800-bae6-11ea-8a6c-a1731c84f828.png)
![CNN이용 고해상도 변환 500장](https://user-images.githubusercontent.com/54871612/86091456-eb3b5500-bae6-11ea-86d9-1587bf46e2b8.png)

### 샤프닝 + 필터


