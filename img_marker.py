import cv2
import glob
import os

circle_radius = 20
circle_color = (150,150,150)
flag = ''

def mouse_click_event(event,x,y,flags,param):
	(img,txt_name) = param
	if event==cv2.EVENT_FLAG_LBUTTON: #点击鼠标左键，标记眼睛
		file = open(txt_name,'a')
		file.write(str(x)+' '+str(y)+' ') #追加内容
		file.close()
		print('(',x,',',y,')')
		cv2.circle(img,(x,y),circle_radius,circle_color,1) #画一个圆，作为标记
	elif event==cv2.EVENT_FLAG_RBUTTON: #点击鼠标右键，清空内容
		file = open(txt_name,'w') #清空文档内容
		file.close
		global flag 
		flag = 'clear'
		print('cancle')

#寻找当前目录中的图片文件（后缀名是大写字母也能被找到）
pics = glob.glob(r'.\\*.jpg')
pics += glob.glob(r'.\\*.jpeg')
pics += glob.glob(r'.\\*.png')
pics += glob.glob(r'.\\*.bmp')
pics += glob.glob(r'.\\*.pgm')

i = 0
while flag!='exit':
	if flag=='next':
		if i<len(pics)-1:
			i += 1
		else:
			break
	elif flag=='last' and i>0:
		i -= 1
	pic_name = pics[i].split('\\')[-1] #适用于Windows系统
	txt_name = pic_name.split('.')[0]+'.txt'
	cv2.namedWindow(pic_name)
	image = cv2.imread(pic_name, cv2.IMREAD_GRAYSCALE)
	print(pic_name)
	if os.path.exists(txt_name):
		file = open(txt_name,'r')
		sp = file.readline().split(' ')
		file.close
		end = len(sp)-1
		j = 0
		while(j<end):
			x = int(sp[j])
			y = int(sp[j+1])
			print('(',x,',',y,')')
			cv2.circle(image,(x,y),circle_radius,circle_color,1) #根据文本文件的原有内容画圆
			j += 2
	cv2.setMouseCallback(pic_name,mouse_click_event,(image,txt_name)) #将窗口与鼠标回调函数绑定
	while(True):
		cv2.imshow(pic_name,image)
		if(flag=='clear'):
			flag=''
			break
		key = cv2.waitKey(20)&0xFF
		if key==ord('z'): #按z键前往下一张图片
			cv2.destroyWindow(pic_name)
			flag = 'next'
			break
		elif key==ord('x'): #按x键返回上一张图片
			cv2.destroyWindow(pic_name)
			flag = 'last'
			break
		elif key==27: #按esc键可以退出
			cv2.destroyWindow(pic_name)
			flag = 'exit'
			break
cv2.destroyAllWindows()