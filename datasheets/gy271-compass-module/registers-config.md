### REGISTER CONFIGURATION FOR QMC5883L

#### THIS WAS THE FIRST I'VE TRIED BUT THE OSR SPEND MORE ENERGY THAN THE LAST ONE
0x1D - OSR 512, RNG 8G, ODR 200Hz, Mode Continuous
SAMPLE_15 = [261, 258, 258, 257, 257, 257, 267, 267, 267, 267, 261, 261, 264, 264, 265]
0X1C - OSR 512, RNG 8G, ODR 200Hz, Mode Stand By

#### THIS IS A BAD CHOICE TOO INACCURATE
0x0D - OSR 512, RNG 2G, ODR 200Hz, Mode Continuous
SAMPLE_15 = [270, 270, 270, 258, 258, 254, 254, 185, 185, 123, 123, 123, 123, 123, 123]
0X0C - OSR 512, RNG 2G, ODR 200Hz, Mode Stand By

#### THIS IS ALSO A BAD CHOICE, VARIES TOO MUCH AND THE READING FREQUENCY IS NOT ENOUGH
0x01 - OSR 512, RNG 2G, ODR 10Hz, Mode Continuous
SAMPLE_15 = [110, 113, 113, 109, 109, 106, 106, 107, 106, 106, 109, 109, 109, 109, 110]
0X00 - OSR 512, RNG 2G, ODR 10Hz, Mode Stand By

#### THIS IS ALSO A BAD CHOICE, VARIES TOO MUCH AND THE READING FREQUENCY IS NOT ENOUGH
0x11 - OSR 512, RNG 8G, ODR 10Hz, Mode Continuous
SAMPLE_15 = [247, 247, 247, 247, 247, 247, 247, 247, 110, 110, 110, 110, 110, 110]
0x10 - OSR 512, RNG 8G, ODR 10Hz, Mode Stand By

#### LESS VARIATION IN COMPARATION WITH OTHERS
0x5D - OSR 256, RNG 8G, ODR 200Hz, Mode Continuous
SAMPLE_15 = [337, 337, 337, 337, 325, 325, 338, 338, 330, 330, 330, 330, 330, 332, 332]
0x5C - OSR 256, RNG 8G, ODR 200Hz, Mode Stand By

### SOME ALTERNATIVE DOCUMENTATION
https://esphome.io/components/sensor/qmc5883l.html
