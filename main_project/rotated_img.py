# 이미지 돌리기 전 까지의 코드
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from copy import copy

class rotated_img : 

    def __init__(self, path):
        self.path = path
        self.file_name = path.split('/')[-1]
        self.img = cv2.imread(path, cv2.IMREAD_COLOR)
        print(self.img.shape)
                
        
    def kp_dist(self,a_list,b_list): 
        x_1, x_2 = a_list
        y_1, y_2 = b_list
        distance = (math.sqrt((x_1 - y_1)**2 +(x_2 - y_2)**2))
    
        return distance   
    
    # 이미지 배열 찾는 함수
    def make_img_list(self, image) : 
        # 비어있지 않은 최소 x값 찾기 (이미지를 위로 올리기 위해서)
        # 비어있지 않는 최소 y값 찾기 (이미지를 위로 왼쪽으로 정렬하기 위해서)
        find_x_list = []
        find_y_list = []
        for i in range(image.shape[0]) :
            for j in range(image.shape[1]) :
                    if np.all(image[i][j] != 0) :
                        find_x_list.append(i)
                        find_y_list.append(j)
                        
        return find_x_list, find_y_list
        
    def find_angle (self, list_1, list_2):
        x_1, y_1 = list_1 # 첫번 째 점
        x_2, y_2 = list_2 # 중앙에 있는 점
        
        # 마지막 점 생성하기
        x_3, y_3 = x_2, self.img.shape[1]
        
        # 일반적으로 cv2.imshow 실행시, 세로축이 x, 가로축이 y의 값을 갖는다.
        # line_1, line_2의 값은 양수이므로 line_2/line_1의 값이 양수일 때에,
        # arccos가 항상 90이하의 값을 추출한다. 때문에, 첫번 째 점과 두번째 점이 이루는 각도가 90를 넘는 경우를 고려해, line_1에
        # -1의 값을 곱해준다,

        if y_2 > y_1 : 
            line_1 = (-1) * math.sqrt((x_2 - x_1)**2 +(y_2 - y_1)**2)
            line_2 = y_3 - y_2
        else : 
            line_1 = math.sqrt((x_2 - x_1)**2 +(y_2 - y_1)**2)
            line_2 = y_3 - y_2
        
        angle = float(np.rad2deg(np.arccos(line_2/line_1)))

        return angle
        
    def find_want_arr(self):
    
        ## GaussianBlur를 통한 이미지 노이즈 제거
        img_gaus = cv2.GaussianBlur(self.img, (13,13),0)

        ## Canny를 통한 테두리 찾기
        img_canny = cv2.Canny(img_gaus,50, 120)
        
        # 값이 255인, canny를 통해 출력된 테두리 값을 저장하기
        kp_list = []
        for i in range(img_canny.shape[0]):
            for j in range(img_canny.shape[1]):
                  if img_canny[i][j]== 255:
                        kp_list.append([i, j])
        max_dist = 0
        max_pt = []
        
        ilist = copy(kp_list)
        for i,kp in enumerate(kp_list) : 
            for j in range(i, len(ilist)) : 
                dist = self.kp_dist(kp, ilist[j])
          
                if dist > max_dist : 
                    max_dist = dist
                    max_pt = []
                    max_pt.append(kp)
                    max_pt.append(kp_list[j])
                    
        x_1, y_1 = max_pt[0]
        x_2, y_2 = max_pt[1]
        x_3, y_3 = x_2, self.img.shape[1]
            
        copy_img = self.img
        im_arr = cv2.arrowedLine(copy_img, (y_1,x_1), (y_2, x_2), (255,0,0), 2)
        im_arr = cv2.arrowedLine(im_arr, (y_2, x_2), (y_3, x_3),(255,0,0), 2)
        print(max_pt[0], max_pt[1])

        plt.imshow(im_arr)
    
    def rotated (self) :
    
        ## GaussianBlur를 통한 이미지 노이즈 제거
        img_gaus = cv2.GaussianBlur(self.img, (13,13),0)

        ## Canny를 통한 테두리 찾기
        img_canny = cv2.Canny(img_gaus,50, 120)
        
        # 값이 255인, canny를 통해 출력된 테두리 값을 저장하기
        kp_list = []
        for i in range(img_canny.shape[0]):
            for j in range(img_canny.shape[1]):
                  if img_canny[i][j]== 255:
                        kp_list.append([i, j])
        max_dist = 0
        max_pt = []
        
        for i,kp in enumerate(kp_list) : 
            for j in range(i, len(kp_list)) : 
                dist = self.kp_dist(kp, kp_list[j])
                if dist > max_dist : 
                    max_dist = dist
                    max_pt = []
                    max_pt.append(kp)
                    max_pt.append(kp_list[j])
                    
        x_1, y_1 = max_pt[0]
        x_2, y_2 = max_pt[1]
        
        list_x = [y_1, x_1]
        list_y = [y_2, x_2]
        img_angle = self.find_angle(list_x, list_y)
        
        half_x = int((x_2 + x_1)/2)
        half_y = int((y_2 + y_1)/2)
        rot_matrix= cv2.getRotationMatrix2D((half_x,half_y), img_angle, 0.7)
        # 이미지 회전
        img_w, img_h =   int(1.5 *self.img.shape[0]), int(1.5*self.img.shape[1])
        rotated_im = cv2.warpAffine(self.img, rot_matrix, (img_w, img_h))
        
        # 이동할 이미지 틀 만들기
        move_img = np.zeros((self.img.shape[1],self.img.shape[0], 3), dtype = np.uint8)
        
        
        find_rotated_x, find_rotated_y =self.make_img_list(rotated_im)
        # 비어있지 않은 최소 x값 찾기 (이미지를 위로 올리기 위해서)

        find_x = min(find_rotated_x)
        find_y = min(find_rotated_y)
        
        # rotated_im를 x축,y축 만큼 옮겨주기
        for i in range(move_img.shape[0]):
            for j in range(move_img.shape[1]):
                move_img[i][j] = rotated_im[i+find_x][j+find_y]
        
        
        # 불필요한 이미지 내용 제거하기불필요한 이미지 내용 제거하기
        # 지금까지 이미지는 x축, y축으로 최대한 옮겨진 상태로 저장되었다. 이제 불필요한 x, y 값을 제거해보자
        # 비어있지 않은 이미지 찾기
        find_move_x, find_move_y = self.make_img_list(move_img)
        
        # x축 제거하기
        find_x_max = max(find_move_x)
        for i in range(find_x_max+1,move_img.shape[0]):
            move_img = np.delete(move_img,find_x_max+1, axis = 0)        

        #y축 제거하기

        find_y_max = max(find_move_y)
        for i in range(find_y_max+1,move_img.shape[1]):
             move_img = np.delete(move_img,find_y_max+1, axis = 1)

        
        cv2.imwrite(f'data_new/rotated_{self.file_name}.jpg',move_img)
        print("Image Saving is Complete")
        print("***"*7)