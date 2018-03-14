from matplotlib import pyplot as plt 
from matplotlib.widgets import Button
import copy
from math import sqrt
import numpy as np
from scipy.misc import comb


input_points = []
lamda = []
bezeir_ci02 = []


def bernstein_poly(i, n, t):
	return comb(n, i) * ( t**(n-i) ) * (1 - t)**i


def bezier_curve(points, nTimes=1000):
	nPoints = len(points)
	xPoints = np.array([p[0] for p in points])
	yPoints = np.array([p[1] for p in points])

	t = np.linspace(0.0, 1.0, nTimes)

	polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

	xvals = np.dot(xPoints, polynomial_array)
	yvals = np.dot(yPoints, polynomial_array)

	return xvals, yvals


#get the point by pressing
def on_press(event):
	if event.inaxes == None:
		print("none")
		return 
	ax1.scatter(event.xdata,event.ydata)
	point = []
	point.append(event.xdata)
	point.append(event.ydata)
	input_points.append(point)
	fig.canvas.draw()

#calculation for the point
def point_mul_const(const_num,point):
	new_point = []
	new_point.append(const_num * point[0])
	new_point.append(const_num * point[1])
	return new_point

def point_div_const(const_num,point):
	new_point = []
	new_point.append(point[0] / const_num)
	new_point.append(point[1] / const_num)
	return new_point

def point_mul_point(point_1,point_2):
	val = 0
	val = point_1[0] * point_2[0] + point_1[1] * point_2[1]
	return val

def point_add(point_1,point_2):
	new_point = []
	new_point.append(point_1[0] + point_2[0])
	new_point.append(point_1[1] + point_2[1])
	return new_point

def point_sub(point_1,point_2):
	new_point = []
	new_point.append(point_1[0] - point_2[0])
	new_point.append(point_1[1] - point_2[1])
	return new_point

def cal_fun(arg_vec,t):
	res = arg_vec[0] * t ** 3 + arg_vec[1] * t ** 2 + arg_vec[2] * t + arg_vec[3]  
	return res

def cal_ci02(lamda,ci1,c_i1_1):
	new_point = point_add(point_mul_const(1 - lamda,ci1),point_mul_const(lamda,c_i1_1))
	return new_point
	

#generate the curve
def cal_curve(event):
	plt.subplot(212)
	plt.xlim(0,1000)
	plt.ylim(0,1000)
	point_num = len(input_points) - 1
	for i in range(point_num):
		lamda.append(0.5)

	bezeir_ci1 = copy.deepcopy(input_points[:-1])
	#init ci,2
	for i in range(point_num):
		ci1 = bezeir_ci1[i]
		c_i1_1 = bezeir_ci1[(i + 1) % point_num]
		tmp_lamda = lamda[i]
		point_ci02 =  cal_ci02(tmp_lamda,ci1,c_i1_1)
		bezeir_ci02.append(point_ci02)

	for i in range(15):
		#calculate ci1
		for i in range(point_num):
			ci2 = bezeir_ci02[i]
			ci0 = bezeir_ci02[(i + point_num - 1) % point_num]
			pi = input_points[i]
			t = cal_root_t(ci2,ci0,pi)
			point_ci1 = cal_new_ci1(pi,t,ci0,ci2)
			bezeir_ci1[i] = point_ci1

		#calculate lamda
		for i in range(point_num):
			ci0 = bezeir_ci02[(i + point_num - 1) % point_num]
			ci1 = bezeir_ci1[i]
			c_i1_1 = bezeir_ci1[(i + 1) % point_num]
			c_i1_2 = bezeir_ci02[(i + 1) % point_num]
			lamda[(i + 1) % point_num] = cal_lamda(ci0,ci1,c_i1_1,c_i1_2)

		#calculate ci02
		# cal_ci02(lamda,bezeir_ci1,bezeir_ci02):
		for i in range(point_num):
			ci1 = bezeir_ci1[i]
			c_i1_1 = bezeir_ci1[(i + 1) % point_num]
			tmp_lamda = lamda[i]
			point_ci02 =  cal_ci02(tmp_lamda,ci1,c_i1_1)
			bezeir_ci02[i] = point_ci02

#	for i in range(point_num):
#		ci2 = bezeir_ci02[i]
#		ci0 = bezeir_ci02[(i + point_num - 1) % point_num]
#		pi = input_points[i]
#		t = cal_root_t(ci2,ci0,pi)
#		point_ci1 = cal_new_ci1(pi,t,ci0,ci2)
#		bezeir_ci1[i] = point_ci1

	for i in range(point_num):
		nPoints = 3
		points = []
		points.append(bezeir_ci02[(i - 1 + point_num) % point_num])
		points.append(bezeir_ci1[i])
		points.append(bezeir_ci02[i])
		xpoints = [p[0] for p in points]
		ypoints = [p[1] for p in points]
		x_input = input_points[i][0]
		y_input = input_points[i][1]
		xvals, yvals = bezier_curve(points, nTimes=1000)
		plt.plot(xvals, yvals)
		plt.plot(xpoints, ypoints, "ro")
		plt.plot(x_input,y_input,"bs")
		for nr in range(len(points)):
			if nr == 1:
				plt.text(points[nr][0], points[nr][1], str(i))

	plt.show()

	

def cal_root_t(ci2,ci0,pi):
	delta =  0.1

	c20 = point_sub(ci2,ci0)
	tri_arg = c20[0] ** 2 + c20[1] ** 2
	
	c0_pi = point_sub(ci0,pi)
	quadr_arg = 3 * point_mul_point(c0_pi,c20)
	
	p11 = point_mul_const(3,ci0)
	p12 = point_mul_const(2,pi)
	p1 = point_sub(point_sub(p11,p12),ci2)
	p2 = point_sub(ci0,pi)
	linear_arg = point_mul_point(p1,p2)
	
	p0 = point_sub(ci0,pi)
	const_arg = - (p0[0] ** 2 + p0[1] ** 2)

	arg_vec = []
	arg_vec.append(tri_arg)
	arg_vec.append(quadr_arg)
	arg_vec.append(linear_arg)
	arg_vec.append(const_arg)

	t_up = 1
	t_bottom = 0
	t = (t_up + t_bottom) / 2

	deviation = 1
	choose_direc = 1 #choose the upper as the kept number 
	while(True):
		#calculate the cubic function
		func_t = cal_fun(arg_vec,t)
		upper_val = cal_fun(arg_vec,t_up)
		bottom_val = cal_fun(arg_vec,t_bottom)

		deviation = abs(func_t)
		sign_t = (1 if func_t > 0 else -1) #func_t > 0 ? 1 : -1
		sign_up = (1 if upper_val > 0 else -1)#upper_val > 0 ? 1 : -1
		sign_bottom = (1 if bottom_val > 0 else -1)#bottom_val > 0 ? 1 : -1
		if deviation < delta:
			break	
		elif sign_t * sign_bottom < 0:
			t_up = t
		else:
			t_bottom = t

		t = (t_up + t_bottom) / 2

	return t

def cal_new_ci1(pi,t,ci0,ci2):
	p1 = point_mul_const((1 - t) ** 2,ci0)
	p2 = point_sub(pi,p1)
	p3 = point_mul_const(t ** 2, ci2) 
	div1_p = point_sub(p2,p3)
	div2 = 2 * t * (1 - t)
	ci1 = point_div_const(div2,div1_p)
	return ci1

def cal_lamda(ci0,ci1,c_i1_1,c_i1_2):
	area1 = cal_area(ci0,ci1,c_i1_1)
	area2 = cal_area(ci0,ci1,c_i1_1)
	area3 = cal_area(ci1,c_i1_1,c_i1_2)
	a1 = sqrt(area1)
	a2 = sqrt(area2)
	a3 = sqrt(area3)
	lamda = a1 / (a2 + a3)
	return lamda 

def cal_area(p1,p2,p3):
	e1 = cal_edge(p1,p2)
	e2 = cal_edge(p2,p3)
	e3 = cal_edge(p3,p1)
	s = 0.5 * (e1 + e2 + e3)
	area = sqrt(s * (s - e1) * (s - e2) * (s - e3))
	return area


def cal_edge(point_1,point_2):
	tmp_p = point_sub(point_1,point_2)
	edge = sqrt(point_mul_point(tmp_p,tmp_p))
	return edge

if __name__ == "__main__":
	#img = Image.open("./test.bmp")
	fig = plt.figure()
	fig.canvas.mpl_connect("button_press_event",on_press)
	ax1 = fig.add_subplot(211)
	plt.axis("on")
	plt.xlim(0,1000)
	plt.ylim(0,1000)
	
	ax_ok = plt.axes([0.5,0.05,0.18,0.075]) #x_start,y_start,height,width
	button_ok = Button(ax_ok,'Generate curve')
	button_ok.on_clicked(cal_curve)
	plt.show()
	



