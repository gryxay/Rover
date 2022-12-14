# Author: peppe8o
# https://peppe8o.com


from i2c_hmc5883l import HMC5883
from time import sleep


i2c_HMC5883l = HMC5883(gauss=8.1)
# Set declination according to your position
i2c_HMC5883l.set_declination(7, 55)

Xmin=1000
Xmax=-1000
Ymin=1000
Ymax=-1000

while True:
    try:
     x, y, z = i2c_HMC5883l.get_axes()
     Xmin=min(x,Xmin)
     Xmax=max(x,Xmax)
     Ymin=min(y,Ymin)
     Ymax=max(y,Ymax)
     print(i2c_HMC5883l.get_axes())
     print("Xmin="+str(Xmin)+"; Xmax="+str(Xmax)+"; Ymin="+str(Ymin)+"; Ymax="+str(Ymax))
     sleep(0.01)

    except KeyboardInterrupt:
        print()
        print('Got ctrl-c')

        xs=1
        ys=(Xmax-Xmin)/(Ymax-Ymin)
        xb =xs*(1/2*(Xmax-Xmin)-Xmax)
        yb =xs*(1/2*(Ymax-Ymin)-Ymax)
        print("Calibration corrections:")
        print("xs="+str(xs))
        print("ys="+str(ys))
        print("xb="+str(xb))
        print("yb="+str(yb))
        break
        