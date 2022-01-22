import cv2
import numpy as np
import logging

logger = logging.getLogger("analyse")

def smooth(y, N=10):
    box_pts = N
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def crop_image(image, minRadius=100, maxRadius=4000, dp=4, mindist=10000, param1=50, param2=50):
    logger.debug("crop_image")
    circles = cv2.HoughCircles(
        image, 
        cv2.HOUGH_GRADIENT, 
        dp, 
        mindist, 
        param1=param1, 
        param2=param2, 
        minRadius=minRadius, 
        maxRadius=maxRadius)
    if circles is None:
        raise Exception("no circle found")
    if len(circles) > 1:
        raise Exception("to many circles found") 
    circle = np.round(circles[0, :]).astype("int")[0]
    x = circle[0]
    y = circle[1]
    r = circle[2]
    y_start = y-r
    y_stop = y+r
    x_start = x-r
    x_stop = x+r
    output = image[y_start:y_stop, x_start:x_stop]
    return output, r


def find_greyscale(image, percent_of_circle_width=0.05, center_obstruction=0, smooth_factor=10):
    logger.debug("find_greyscale")
    r = int(len(image)/2)
    y_start = r-int(r*percent_of_circle_width/2)
    y_stop = r+int(r*percent_of_circle_width/2)
    x_start = 0
    x_stop = r*2
    output = image[y_start:y_stop, x_start:x_stop]
    greyscale = np.mean(output, axis=0)
    #generate grey deviation
    g2 = np.flip(greyscale[:r])
    g1 = greyscale[r:]
    #smooth
    g1 = smooth(g1, N=smooth_factor)
    g2 = smooth(g2, N=smooth_factor)
    #normalize
    mean = (np.mean(g1)+np.mean(g2))/2
    if mean != 0:
        g1 = g1/mean-0.5
        g2 = g2/mean-0.5
    if center_obstruction > 0:
        clear_length = int(len(g1)-center_obstruction*len(g1))
        g1[clear_length:] = 0
        g2[clear_length:] = 0
    return g1,g2

def find_zones(g1, g2):
    logger.debug("find_zones")
    idx = np.argwhere(np.diff(np.sign(g1 - g2))).flatten()/len(g1)
    return idx

def normalize_zones(h, l, zones=20):
    logger.debug("normalize_zones")
    H = list()
    L = list()
    for zone in range(zones):
        zone_start = zone/zones
        zone_end = (zone+1)/zones
        idx = np.argwhere((h > zone_start) & (h < zone_end))
        if len(idx) > 0:
            L += [np.mean(l[idx])]
        elif len(L) > 0:
            L += [L[-1]]
        else:
            L += [0]
        H += [zone_start + 0.5/zones]    
    H = np.array(H)
    L = np.array(L)
    return H,L

def calc_optimized_radius_offset(h, l):
    logger.debug("calc_optimized_radius_offset")
    prev_sum = np.inf
    prev_r = 0
    for r in np.linspace(-2,2,1000):
        sum = np.sum((h*(l+r))**2)
        if sum < prev_sum:
            prev_sum = sum
            prev_r = r
    return prev_r



def calculate_sphere_dev(h, l, mirror_roc, mirror_size, zones=12):
    z = mirror_size/(2*zones)
    l_mm = l*mirror_size/4
    mul = z*h*l_mm
    div = mirror_roc**2
    w = -np.cumsum(mul)/div
    return w, h

def run_analysis(foucault_test, image_radius_range=100):
    logger.debug("run_analysis")
    h = []
    l = []
    image_radius = None
    for image in foucault_test.image_list:
        if image_radius == None:
            croped_image, image_radius = crop_image(image.image)
        else:
            croped_image, image_radius = crop_image(
                image.image, 
                minRadius=image_radius-image_radius_range,
                maxRadius=image_radius+image_radius_range)
        image.crop_image = croped_image
        g1,g2 = find_greyscale(
            croped_image,
            percent_of_circle_width=foucault_test.greyscale_bar_width_percent/100,
            smooth_factor=foucault_test.image_smooth_factor)
        image.g1 = g1
        image.g2 = g2
        zones = find_zones(g1,g2)
        image.zones = zones
        h += zones.tolist()
        l += [image.position]*len(zones)
    h = np.array(h)
    l = np.array(l, dtype=np.float)
    l += calc_optimized_radius_offset(h, l)
    h,l = normalize_zones(h, l, zones=foucault_test.zone_count)
    w, h = calculate_sphere_dev(h, l, foucault_test.mirror_roc, foucault_test.mirror_diameter, zones=foucault_test.zone_count)
    foucault_test.w_nm = w*10**6
    foucault_test.h_mm = h*foucault_test.mirror_diameter/2

