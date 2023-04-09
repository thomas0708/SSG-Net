import numpy as np
#import matplotlib.pyplot as plt
import cv2
import ast
import pydegensac

def read_npy(name):
    dataset = np.load(name,allow_pickle=True)
    #print(dataset.files)
    #['keypoints0', 'keypoints1', 'matches', 'match_confidence']
    #print('kp',dataset['keypoints0'].shape)
   # print(dataset['matches'])
    a= dataset['keypoints0']
    c= dataset['keypoints1']
    b= dataset['match_confidence']
    e =dataset['matches']
    #print('con',dataset['matches'].shape)
    #plt.imshow(b)
    #print(dataset['match_confidence'])
    with open('matched_conf.txt','w') as f:
        for i in range(len(b)):
            f.write(str(b[i])+'\n')
    with open('matched_kp1.txt','w') as s:
        for j in range(len(a)):
            s.write(str(a[j])+'\n')
    with open('matched_kp2.txt', 'w') as t:
        for k in range(len(c)):
            t.write(str(c[k]) + '\n')
    with open('matched.txt', 'w') as fi:
        for m in range(len(e)):
            fi.write(str(e[m]) + '\n')

def resize(a,b):
    #默认修改大小
    size = (640, 480)
    a= cv2.imread(a,flags=1)
    b = cv2.imread(b, flags=1)
    resize_a = cv2.resize(a, size,interpolation = cv2.INTER_AREA)
    resize_b = cv2.resize(b, size, interpolation=cv2.INTER_AREA)
    cv2.imwrite('img1.jpg',resize_a)
    cv2.imwrite('img2.jpg',resize_b)


def select_point(kp1,kp2,conf,mat,conf_yz):
    data_last=[]
    with open(conf, 'r') as conf:

        data_conf = conf.readlines()
        for row in data_conf:
            tmp = row.replace('\n','')

            data_last.append(tmp)
        data_show = map(eval,data_last)
        data_show = list(data_show)

    kp1_last = []
    kp2_last = []
    with open (kp1, 'r') as kp1:
        kp1 = kp1.readlines()
        for row in kp1:
            tmp = row.replace('\n', '')
            tmp = tmp.replace('.', '')
            tmp = tmp.replace('  ', ', ')
            tmp = tmp.replace('[', ' ')
            tmp = tmp.replace(']', ' ')
            tmp = tmp.split()

            #print(tmp)
            #mp1= eval(tmp)
            kp1_last.append(tmp)
        #data_show2 = map(eval, kp1_last)
        #data_show2 = list(data_show2)
    with open(kp2, 'r') as kp2:
        kp2 = kp2.readlines()
        for row in kp2:
            tmp = row.replace('\n', '')
            tmp = tmp.replace('.', '')
            tmp = tmp.replace('  ', ', ')
            tmp = tmp.replace('[', ' ')
            tmp = tmp.replace(']', ' ')
            tmp = tmp.split()
            kp2_last.append(tmp)
        #data_show3 = map(eval, kp2_last)
        #data_show3 = list(data_show3)

    kp1_good = []
    kp2_good = []

    matches = []
    matches_num = []
    with open(mat, 'r') as mat:
        for i,item in enumerate(mat):
            matches_num.append(int(item))
            if int(item)>-1:
                matches.append(i)

    #print('match',matches_num)

    good_matches = []
    for i, conf in enumerate(data_show):
        if conf > conf_yz:
            good_matches.append(i + 1)
    print(good_matches)  # 123

    for num in good_matches:
        if num in matches:
            kp1_good.append(kp1_last[num-1])
            kp2_num= matches_num[num-1]
            kp2_good.append(kp2_last[kp2_num])
    #print('kp0', kp1_good)
    #print('kp0',kp2_good)



    y = len(kp1_good)
    list1 = []
    list1_fine = []
    list2 = []
    list2_fine = []
    for i in range(y):
        #print(kp1_good)
        if kp1_good[i][0].rstrip(',')=='':
            list1.append(int(kp1_good[i][1].rstrip(',')))
            list2.append(int(kp1_good[i][2]))
        else:#i =i+1
            list1.append(int(kp1_good[i][0].rstrip(',')))
            list2.append(int(kp1_good[i][1]))
        list1_fine.append([list1[i],list2[i]])
    #print('list',list1_fine)
    list3 = []
    list4 = []
    for i in range(y):
        # print(i)
        #i =i+1
        #print('kp',kp2_good[i])
        if kp2_good[i][0].rstrip(',')=='':
            list3.append(int(kp2_good[i][1].rstrip(',')))
            list4.append(int(kp2_good[i][2]))
        else:
            list3.append(int(kp2_good[i][0].rstrip(',')))
            list4.append(int(kp2_good[i][1]))
        list2_fine.append([list3[i], list4[i]])
    #list2_fine和list1_fine是找到的坐标系
    #print(list1)
    #print(list2)
    #print(list3)
    #print(list4)


    # = cv2.imread('img1.jpg')


    # color = (0,0,255)
    # cv2.circle(img1,(429,8),5,color,3)
    # cv2.circle(img1, (387,9), 5, color, 3)
    # cv2.circle(img1, (348, 11), 5, color, 3)
    # cv2.circle(img1, (398, 12), 5, color, 3)
    # # cv2.circle(img1, (331, 14), 5, color, 3)
    # # cv2.circle(img1, (396, 28), 5, color, 3)
    # cv2.imwrite('test.jpg',img1)


    # img2 = cv2.imread('img2.jpg')
    #
    #
    # color = (0,0,255)
    # cv2.circle(img2,(384,60),5,color,3)
    # cv2.circle(img2, (349,63), 5, color, 3)
    # cv2.circle(img2, (318, 62), 5, color, 3)
    # cv2.circle(img2, (358, 66), 5, color, 3)
    # cv2.circle(img2, (303,65), 5, color, 3)
    # cv2.circle(img2, (357, 81), 5, color, 3)
    #cv2.imwrite('test1.jpg',img2)



    # a=list1[0]
    # b=list2[0]
    # c=list1[1]
    # d=list2[1]
    # e=list1[2]
    # f=list2[2]
    # g=list3[0]
    # h=list4[0]
    # i=list3[1]
    # j=list4[1]
    # l=list3[2]
    # m=list4[2]
    # #
    # n=list1[3]
    # q=list2[3]
    # o=list3[3]
    # p=list4[3]

    post1 = np.float32(list1_fine)
    post2 = np.float32(list2_fine)

    # post1 = np.float32([[a,b],[c,d],[e,f]])
    #     # post2 = np.float32([[g,h],[i,j],[l,m]])
    #print('pos',post2)
    #post2 = np.float32([])
    #H,status = pydegensac.findHomography(post1,post2,4 ,0.99,2000,laf_consistensy_coef=3,error_type='symm_sq_max',symmetric_error_check=False)
    H, status = pydegensac.findHomography(post1, post2, 4, 0.99, 2000, error_type='symm_sq_max',
                                          symmetric_error_check=False)
    print('H',H)
    img_input = cv2.imread('img1.jpg')
    row, col = img_input.shape[: 2]
    result = cv2.warpPerspective(img_input, H,(col,row))
    cv2.imwrite("result.jpg",result)
    #cv2.waitKey(0)
def show_pair(img1,img2):
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)
    imadd = cv2.addWeighted(img1,0.7,img2,0.3,0)
    cv2.imwrite('show_pair.jpg',imadd)
#以后边数字为基础，配准前一项数字
name = '001_002_matches.npz'
read_npy(name)
resize('test_1/test11/001.jpg','test_1/test11/002.jpg')
select_point('matched_kp1.txt','matched_kp2.txt','matched_conf.txt','matched.txt',0.2)
show_pair('result.jpg','img2.jpg')