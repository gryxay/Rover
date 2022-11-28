import qmc5883l


compass = qmc5883l.QMC5883L()

while True:
    print(compass.get_bearing())
