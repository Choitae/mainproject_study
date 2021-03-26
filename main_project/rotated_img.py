import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from copy import copy


class rotated_img : 

    def __init__(self, img):
        self.img_bf = img
        self.img = cv2.cvtColor(self.img_bf, cv2.COLOR_BGR2RGB)
        self.num = 0
        
    def kp_dist(self,a_list,b_list): 
        x_1, x_2 = a_list
        y_1, y_2 = b_list
        distance = (math.sqrt((x_1 - y_1)**2 +(x_2 - y_2)**2))
    
        return distance   
        
    def find_angle (self, list_1, list_2):
        x_1, y_1 = list_1 # 첫번 째 점
        x_2, y_2 = list_2 # 중앙에 있는 점
        
        # 마지막 점 생성하기
        x_3, y_3 = x_2, self.img.shape[1]
        
        line_1 = math.sqrt((x_2 - x_1)**2 +(y_2 - y_1)**2)
        line_2 = y_3 - y_2
        
        angle = float(np.rad2deg(np.arccos(line_2/line_1)))
        if (x_2 - x_1)> 0:
            angle = 180 - angle
        
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
            
        im_arr = cv2.arrowedLine(self.img, (y_1,x_1), (y_2, x_2), (255,0,0), 2)
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
        
        
        img_w, img_h =   self.img.shape[0], self.img.shape[1]
        
        rotated_im = cv2.warpAffine(self.img, rot_matrix, (img_w, img_h))
        cv2.imwrite(f'data_new/roted_img_{self.num}.jpg',rotated_im)
        num += 1
        plt.imshow(rotated_im)

if __name__ == "__main__":
    print("플레이 코드 입니다")