from i2c_hmc5883l import HMC5883
from time import sleep


i2c_HMC5883l = HMC5883(gauss=8.1)

#Set declination according to your position
i2c_HMC5883l.set_declination(7, 55)

while True:
   print(i2c_HMC5883l.get_heading())
   sleep(0.1)
