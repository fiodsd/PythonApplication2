import matplotlib.pyplot as plt
import numpy as np
import math
import random
import sympy as sp


"Набор, ведущий к самопересечению"
x=[-4,-8,-11,1,3,30,28,-6,19,24,-2,24]
y=[-3,-10,-1,-4,-5,20,14,5,18,20,2,16]

"Случайный набор"
nrandom=random.randint(3,20)
x=random.sample(range(0, 50), nrandom)
y=random.sample(range(0, 50), nrandom)

"Основной экспериментальный набор"
x=[38,24,2,20,26,30,22]
y=[20,29,4,18,22,32,8]

data=[x,y]
length=len(x)
data=np.transpose(data)

"Initial data demonstration"
plt.scatter(x,y)
plt.title("Набор исходных точек\nРис.1")
plt.show()


"Part 1 - Convex X"
full_data=[[],[],[],[]]
full_data[0]=x;full_data[1]=y
#print(full_data)
d=sorted(data,key=lambda data:data[1])
x0=d[0][0];y0=d[0][1]

data_sorted=[[],[]]
data_temp1=[[],[]]
data_temp_radius=[0]*length
data_temp_angle=[0]*length
data_temp1=[i-[x0,y0] for i in data]


for i in range(length):
   data_temp_radius[i]=np.sqrt(pow(data_temp1[i][0],2)+pow(data_temp1[i][1],2))
   if(data_temp1[i][1]!=0): data_temp_angle[i]=np.arctan(data_temp1[i][1]/data_temp1[i][0])
   if(data_temp1[i][1]==0):
       if(data_temp1[i][0]>=0):data_temp_angle[i]=0
       if(data_temp1[i][0]<0):data_temp_angle[i]=math.pi
   if(data_temp_angle[i]<0):data_temp_angle[i]=data_temp_angle[i]+2*math.pi



full_data[2]=data_temp_angle; full_data[3]=data_temp_radius

#print(np.transpose(full_data))
full_data=np.transpose(full_data)
full_data=sorted(full_data,key=lambda full_data:full_data[2])

ap=[[0 for _ in range(2)] for _ in range(len(full_data))]

for i in range(len(full_data)):
    ap[i][0]=full_data[i][0]
    ap[i][1]=full_data[i][1]
#print(ap)
goodline=[0]*2; goodline[0]=ap[0]; goodline[1]=ap[1];c=2
#print(goodline)

while(c<len(ap)):
    ux=goodline[c-1][0]-goodline[c-2][0]; uy=goodline[c-1][1]-goodline[c-2][1]
    vx=ap[c][0]-goodline[c-1][0]; vy=ap[c][1]-goodline[c-1][1];
    angle=ux*vy-uy*vx
    #print("Кандидат - ",ap[c-1])
    if(angle>=0): goodline.append(ap[c]); c=c+1; #print("Added")
    if(angle<0): del goodline[c-1]; del ap[c-1]; c=c-1; #print("Deleted")
    #print(np.transpose(goodline))
goodline_graph=np.transpose(goodline)

plt.scatter(x,y,color='black')
plt.scatter(goodline_graph[0],goodline_graph[1])
plt.title("Набор точек, образующих выпуклую оболочку\nРис.2")
plt.show()



"Part 2 - Initial data for splines"

"Расположение точек по мере возрастания абсциссы"
print("Точки до упорядочивания",goodline)
data_0=sorted(goodline,key=lambda goodline:goodline[0])
print("Точки после упорядочивания",data_0)

n=len(data_0)
print("Количество точек в множестве",n)

"Определение точки с крайней правой абсциссой"
x_rightest=data_0[n-1][0]
y_rightest=data_0[n-1][1]

print("Крайняя правая точка",[x_rightest,y_rightest])


#"Демонстрация множества и крайней правой точки"
#plt.scatter(goodline_graph[0],goodline_graph[1])
#plt.scatter(x_rightest,y_rightest,color='red')
#plt.title("Множество и крайняя правая точки")
#plt.show()


"Вычисление внутренней точки множества"
x0=sum(goodline_graph[0],0)/len(goodline_graph[0])
y0=sum(goodline_graph[1],0)/len(goodline_graph[1])

plt.scatter(goodline_graph[0],goodline_graph[1])
plt.scatter(x_rightest,y_rightest,color='red')
plt.scatter(x0,y0,color='red')
plt.title("Множество с внутренней и крайней точками\nРис.3")
plt.show()



"Сдвиг множества в начало координат относительно внутренней точки"
x_m=[0]*n;y_m=[0]*n
for i in range(n):
    x_m[i]=data_0[i][0]-x0
    y_m[i]=data_0[i][1]-y0


"Демонстрация множества после смещения"
plt.scatter(x_m,y_m)
plt.scatter(x_m[n-1],y_m[n-1],color='red')
plt.scatter(0,0,color='red')
plt.scatter(goodline_graph[0],goodline_graph[1],color='lightblue')
plt.scatter(x_rightest,y_rightest,color='lightcoral')
plt.scatter(x0,y0,color='lightcoral')
plt.title("Множество до и после смещения\nРис.4")
plt.show()

xmgraph=x_m[n-1]
ymgraph=y_m[n-1]


kangle=(y_m[n-1])/(x_m[n-1]); phi=math.atan(kangle)
x_r=[0]*(n-1); y_r=[0]*(n-1)
x_lost=x_m[n-1]*math.cos(phi)+y_m[n-1]*math.sin(phi)
del x_m[n-1]
del y_m[n-1]


for i in range(0,n-1):
    x_r[i]=x_m[i]*math.cos(phi)+y_m[i]*math.sin(phi)
    y_r[i]=-x_m[i]*math.sin(phi)+y_m[i]*math.cos(phi)

print(np.transpose([[x_r],[y_r]]))


plt.scatter(x_r,y_r)
plt.scatter(x_lost,0,color='red')
plt.scatter(x_m,y_m,color='lightblue')
plt.scatter(xmgraph,ymgraph,color='lightcoral')
plt.scatter(0,0,color='red')
plt.plot([xmgraph,0],[ymgraph,0],linestyle='dotted',color='lightcoral')
plt.title("Множество до и после поворота. Пунктир для\nдемонстрации угла поворота. Рис.5")
plt.show()

plt.scatter(x_r+[x_lost],y_r+[0])
plt.scatter(0,0,color='red')
plt.scatter(goodline_graph[0],goodline_graph[1],color='lightblue')
plt.scatter(x0,y0,color='lightcoral')
plt.title("Множество до и после преобразований\nРис.6")
plt.show()




r=[0]*len(x_r);theta=[0]*len(y_r)
r_lost=x_lost
theta_lost=0
for i in range(len(x_r)):
   r[i]=np.sqrt(pow(x_r[i],2)+pow(y_r[i],2))
   if(y_r[i]!=0): 
       if(x_r[i]>=0):theta[i]=np.arctan(y_r[i]/x_r[i])
       if(x_r[i]<0):theta[i]=np.arctan(y_r[i]/x_r[i])+math.pi
   if(y_r[i]==0):
       if(x_r[i]>=0):theta[i]=0
       if(x_r[i]<0):theta[i]=math.pi
   #if(theta[i]<0):theta[i]=theta[i]+2*math.pi

"(theta,r) - множество без крайних точек"

for i in range(len(theta)):
    if(theta[i]<0):theta[i]=theta[i]+2*math.pi


for_sort=np.transpose([theta,r])
data_polar=sorted(for_sort,key=lambda for_sort:for_sort[0])
print(data_polar)


data_polar.insert(0,[theta_lost,r_lost]); r.append(r_lost)
data_polar.append([2*math.pi,r_lost])


print(data_polar[0])
print(data_polar[1])
data_polar_transposed=np.transpose(data_polar)
print(data_polar_transposed)

print(data_polar_transposed[0])
print(data_polar_transposed[1])

plt.title("Развертка преобразованного множества\nРис.7")
plt.scatter(data_polar_transposed[0],data_polar_transposed[1])
plt.show()

"Part 3 - Splines"

x1=data_polar_transposed[0]
y1=data_polar_transposed[1]

count=len(x1)
coef_a=[[0 for _ in range(4*count-4)] for _ in range(4*count-4)]
coef_b=[0]*(4*count-4)
coef_h=[0]*(count-1)
for i in range(count-1): coef_h[i]=x1[i+1]-x1[i]
for i in range(count-2):
    coef_b[2*i+1]=y1[i+1]
    coef_b[2*i+2]=y1[i+1]
coef_b[0]=y1[0]
coef_b[2*count-3]=y1[0]


"Последние две строки, обеспечивающие гладкость в точке замыкания"
coef_a[4*count-6][1]=1; coef_a[4*count-6][2]=2*x1[0]; coef_a[4*count-6][3]=3*pow(x1[0],2)

coef_a[4*count-6][4*count-7]=-1; coef_a[4*count-6][4*count-6]=-2*x1[count-1]; coef_a[4*count-6][4*count-5]=-3*pow(x1[count-1],2)

coef_a[4*count-5][2]=2; coef_a[4*count-5][3]=6*x1[0]

coef_a[4*count-5][4*count-6]=-2; coef_a[4*count-5][4*count-5]=-6*x1[count-1]

#Равенство на внутренних точках
for i in range(count-2+1):
    coef_a[2*i][4*i]=1
    coef_a[2*i][4*i+1]=x1[i]
    coef_a[2*i][4*i+2]=pow(x1[i],2)
    coef_a[2*i][4*i+3]=pow(x1[i],3)
    coef_a[2*i+1][4*i]=1
    coef_a[2*i+1][4*i+1]=x1[i+1]
    coef_a[2*i+1][4*i+2]=pow(x1[i+1],2)
    coef_a[2*i+1][4*i+3]=pow(x1[i+1],3)

#Равенство первых производных
for i in range(count-3+1):
    coef_a[2*count-2+i][4*i]=0
    coef_a[2*count-2+i][4*i+1]=1
    coef_a[2*count-2+i][4*i+2]=2*x1[i+1]
    coef_a[2*count-2+i][4*i+3]=3*pow(x1[i+1],2)
    coef_a[2*count-2+i][4*i+4]=0
    coef_a[2*count-2+i][4*i+5]=-1
    coef_a[2*count-2+i][4*i+6]=-2*x1[i+1]
    coef_a[2*count-2+i][4*i+7]=-3*pow(x1[i+1],2)

#Равенство вторых производных    
for i in range(count-3+1):
    coef_a[3*count-4+i][4*i]=0
    coef_a[3*count-4+i][4*i+1]=0
    coef_a[3*count-4+i][4*i+2]=2
    coef_a[3*count-4+i][4*i+3]=6*x1[i+1]
    coef_a[3*count-4+i][4*i+4]=0
    coef_a[3*count-4+i][4*i+5]=0
    coef_a[3*count-4+i][4*i+6]=-2
    coef_a[3*count-4+i][4*i+7]=-6*x1[i+1]

print("Матрица A")
for i in range(4*count-4):
    print([round(j,3) for j in coef_a[i]])

print("Матрица B")
print(coef_b)

m=np.linalg.solve(coef_a,coef_b)
print("Коэффициенты M")
print(m)


"Реализация кусочной функции"

def piecewise_splines(u):
    conditions = [(x1[i]<=u)&(u<=x1[i+1]) for i in range(count-1)]
    functions = [lambda u, n=i: m[4*n]+m[4*n+1]*u+m[4*n+2]*pow(u,2)+m[4*n+3]*pow(u,3) for i in range(count-1)]
    return np.piecewise(u, conditions, functions)


u_array = np.linspace(0,x1[count-1],100*(count-1))
plt.plot(u_array,piecewise_splines(u_array),color='orange')
plt.scatter(x1,y1)
plt.title("Сплайн как кусочная функция\nРис.8")
plt.show()


doptheta=[0]*(4*count-4)
dopord=[0]*(4*count-4)
for i in range(count-1):
    doptheta[4*i]=x1[i]+(coef_h[i])/5
    doptheta[4*i+1]=x1[i]+(2*coef_h[i])/5
    doptheta[4*i+2]=x1[i]+(3*coef_h[i])/5
    doptheta[4*i+3]=x1[i]+(4*coef_h[i])/5

for i in range(count-1):
    dopord[4*i]=piecewise_splines(doptheta[4*i])
    dopord[4*i+1]=piecewise_splines(doptheta[4*i+1])
    dopord[4*i+2]=piecewise_splines(doptheta[4*i+2])
    dopord[4*i+3]=piecewise_splines(doptheta[4*i+3])


plt.plot(u_array,piecewise_splines(u_array),color='orange')
plt.scatter(x1,y1)
plt.scatter(doptheta,dopord)
plt.title("Сплайн как кусочная функция с дополнительными точками\nрис.9")
plt.show()


"Part 4 - Return to original coordinate"
"Возвращение в исходную систему координат путем параметризации сплайнов"\

def Sfinal_x(u):
    return piecewise_splines(u)*(np.cos(u)*math.cos(phi)-np.sin(u)*math.sin(phi))+x0

def Sfinal_y(u):
    return piecewise_splines(u)*(np.cos(u)*math.sin(phi)+np.sin(u)*math.cos(phi))+y0

dopx=[0]*(4*count-4)
dopy=[0]*(4*count-4)
for i in range(4*count-4):
    dopx[i]=dopord[i]*(np.cos(doptheta[i])*np.cos(phi)-np.sin(doptheta[i])*np.sin(phi))+x0
    dopy[i]=dopord[i]*(np.cos(doptheta[i])*np.sin(phi)+np.sin(doptheta[i])*np.cos(phi))+y0



exp_u=np.linspace(x1[0],x1[count-1],400*(count-1))
plt.plot(Sfinal_x(exp_u),Sfinal_y(exp_u))
plt.title("Непрерывная замкнутая кривая - результат после\nвозвращения в исходную систему координат. Рис.10")
plt.show()


plt.plot(Sfinal_x(exp_u),Sfinal_y(exp_u))
plt.scatter(x,y,color='black')
plt.scatter(goodline_graph[0],goodline_graph[1])
plt.scatter(dopx,dopy)
plt.title("Результат интерполяции выпуклой оболочки непрерывной\nкривой с дополнительными точками. Рис.11")
plt.show()


print("\n//////////////////////////////////////\n")
"Part 5 - grid for solve, distance to curve. No longer actual"

bool_conditions=[0]*(count-1)
for i in range(count-1):
    if (m[4*i+3]*((-m[4*i+2])/(3*m[4*i+3]))**3+m[4*i+2]*((-m[4*i+2])/(3*m[4*i+3]))**2+m[4*i+1]*((-m[4*i+2])/(3*m[4*i+3]))+m[4*i]<=0):
        if (m[4*i+3]>0): bool_conditions[i]=1
    if (m[4*i+3]*((-m[4*i+2])/(3*m[4*i+3]))**3+m[4*i+2]*((-m[4*i+2])/(3*m[4*i+3]))**2+m[4*i+1]*((-m[4*i+2])/(3*m[4*i+3]))+m[4*i]>0):
        if (m[4*i+3]<0): bool_conditions[i]=1


potential_extr=[0]*(2*count-2)
for i in range(count-1):
    if (bool_conditions[i]!=0):
        potential_extr[2*i]=(-m[4*i+2]-np.sqrt(m[4*i+2]**2-3*m[4*i+3]*m[4*i+1]))/(3*m[4*i+3])
        potential_extr[2*i+1]=(-m[4*i+2]+np.sqrt(m[4*i+2]**2-3*m[4*i+3]*m[4*i+1]))/(3*m[4*i+3])

extr=[0]*(2*count-2)
for i in range(count-1):
    if ((x1[i]<=potential_extr[2*i])&(potential_extr[2*i]<=x1[i+1])):
        extr[2*i]=potential_extr[2*i]
    if ((x1[i]<=potential_extr[2*i+1])&(potential_extr[2*i+1]<=x1[i+1])):
        extr[2*i+1]=potential_extr[2*i+1]

good_extr= list(filter(None, extr))
good_extr.extend(x1)
good_extr_result=piecewise_splines(good_extr)


temporary_data=[good_extr,good_extr_result]
temporary_data=np.transpose(temporary_data)
temporary=sorted(temporary_data,key=lambda temporary_data:temporary_data[1])

global_extr=temporary[len(temporary)-1][0]
global_extr_result=temporary[len(temporary)-1][1]

"Угол дальнейшего поворота"
kpsi=(y0-Sfinal_y(global_extr))/(x0-Sfinal_x(global_extr))
psi=math.atan(kpsi)


def S_x(u):
    return (Sfinal_x(u)-x0)*math.cos(psi)+(Sfinal_y(u)-y0)*math.sin(psi)

def S_y(u):
    return -(Sfinal_x(u)-x0)*math.sin(psi)+(Sfinal_y(u)-y0)*math.cos(psi)

distance=S_x(global_extr)

half=1.05*abs(distance)
left_side=-half; right_side=half; up_side=half; down_side=-half


plt.plot(Sfinal_x(exp_u),Sfinal_y(exp_u),color='blue')
plt.scatter(goodline_graph[0],goodline_graph[1],color='blue')
plt.scatter(x0,y0,color='red')
plt.scatter(Sfinal_x(global_extr),Sfinal_y(global_extr),color='red')
plt.plot([Sfinal_x(global_extr),x0],[Sfinal_y(global_extr),y0],linestyle='dotted',color='red')
plt.plot(S_x(exp_u),S_y(exp_u),color='lightblue')
plt.scatter(S_x(x1),S_y(x1),color='lightblue')
plt.scatter(0,0,color='lightcoral')
plt.scatter(distance,0,color='lightcoral')
plt.plot([distance,0],[0,0],linestyle='dotted',color='lightcoral')
plt.plot([right_side,down_side],[right_side,up_side],linestyle='dotted',color='lightcoral')
plt.plot([right_side,up_side],[left_side,up_side],linestyle='dotted',color='lightcoral')
plt.plot([left_side,up_side],[left_side,down_side],linestyle='dotted',color='lightcoral')
plt.plot([left_side,down_side],[right_side,down_side],linestyle='dotted',color='lightcoral')
plt.show()
