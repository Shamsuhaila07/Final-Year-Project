# Real time thermal camera using OpenCV and Python 2.7
# Thermomin. Rodo Lillo 2017 

import time
import timeit
import cv2
from scipy import ndimage
import numpy as np
from skimage import exposure, img_as_ubyte

fifo = open('/var/run/mlx9062x.sock', 'rb')  # Open FIFO in binary mode
irbase = np.zeros((4, 16))
step = 0.5

def get_overlay():
    ir_raw = fifo.read()
    if len(ir_raw) < 256:
        print("Error: Insufficient data read from FIFO")
        return None, None
    
    ir_trimmed = ir_raw[0:256]
    ir = np.frombuffer(ir_trimmed, dtype=np.float32)
    ir2 = ir.reshape(16, 4)[::, ::]
    irt = ir2.transpose()
    
    # Morph the image allowing only to increase or decrease at $step increment
    for x in range(0, 4):
        for y in range(0, 16):
            if irbase[x, y] == 0: 
                irbase[x, y] = irt[x, y]
            elif irt[x, y] < irbase[x, y] - step: 
                irbase[x, y] -= step    
            elif irt[x, y] > irbase[x, y] + step:
                irbase[x, y] += step
            else:
                irbase[x, y] = irt[x, y]

    ir3 = exposure.rescale_intensity(irbase, in_range=(20, 40))  # Adjust temperature range for more color diversity
    ir5 = img_as_ubyte(ir3)
    
    return ir5, np.max(irbase)

time.sleep(0.01)
cv2.namedWindow("VIDEO", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("VIDEO", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

delay = 0.0666666  # 15fps

while True:
    startTime = timeit.default_timer()
    fifoir, max_temp = get_overlay()
    if fifoir is None:
        continue
    
    # Debugging statements to check type and shape
    print(f"fifoir type: {type(fifoir)}")
    print(f"fifoir shape: {fifoir.shape if isinstance(fifoir, np.ndarray) else 'N/A'}")

    # Apply filters to create the image
    fifores = cv2.blur(fifoir, (2, 2))
    fifores2 = cv2.resize(fifores, (256, 16), interpolation=cv2.INTER_CUBIC)
    img_fifo = cv2.resize(fifores2, (800, 480), interpolation=cv2.INTER_CUBIC)
    # Apply the colormap. cv2.COLORMAP_JET is also nice
    fifo_color = cv2.applyColorMap(img_fifo, cv2.COLORMAP_JET)
    
    # Display the highest temperature
    cv2.putText(fifo_color, f"Max Temp: {max_temp:.2f} C", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('VIDEO', fifo_color)
    waitTime = (delay - (timeit.default_timer() - startTime)) * 1000  # avoid flickering
    if waitTime < 1:  # minimum value to keep the flow
        waitTime = 1
    key = cv2.waitKey(int(waitTime)) & 0xFF
    # if the q key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
fifo.close()
