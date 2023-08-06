from __future__ import annotations

import time
from typing import List, Tuple

import cv2
import imutils
import numpy as np
import uiautomator2 as u2
from numpy.random import uniform


def pause(low, high):
    time.sleep(np.random.uniform(low, high))


def findHomography(template, image, ratio_thresh=0.75):
    img1 = cv2.imread(template, 0) if type(template) == str else cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    img2 = cv2.imread(image, 0) if type(image) == str else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # find feature matches-----------
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    if des2 is None:
        print("Cannot detect features in image")
        return None
    # Match descriptors.
    matches = cv2.BFMatcher(cv2.NORM_L2).knnMatch(des1, des2, k=2)
    good_matches = []
    try:
        for m, n in matches:
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)
    except Exception as e:
        print(e)
        return None
    if len(good_matches) >= 4:
        print("Number of good matches:", len(good_matches))
    else:
        return None
    # find homography --------------------
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 0)
    if mask.sum() == 0:
        print("Empty mask")
        return None
    # find matches pixel coordinates-------------
    list_kp2 = [kp2[match.trainIdx].pt for match in good_matches]
    center_x, center_y = np.array(list_kp2)[mask.ravel().astype(bool), :].mean(axis=0)
    print("x, y=", center_x, center_y)
    return center_x, center_y


class AndroidBot:
    def __init__(self, adb_addr="127.0.0.1", adb_device_port=5555):
        self.d = u2.connect(f"{adb_addr}:{adb_device_port}")
        screen_size = self.d.window_size()
        self.screen_width, self.screen_height = screen_size[0], screen_size[1]

    def run_adb_command(self, command):
        self.d.shell(command)

    def save_screenshots(self, n=1, file_name="screenshot"):
        for i in range(n):
            self.d.screenshot(filename=f"{file_name}_{i}.png")

    def get_screenshot(self) -> np.ndarray:
        """
        get screenshot as numpy array
        """
        return self.d.screenshot(format="opencv")

    def match_image(
        self, template: str | np.ndarray = None, image=None, scales: List[int] = [1]
    ) -> Tuple[float, int, int]:
        """
        match image template in image
        Args:
            template:  the template to be matched with the image
            image:  the image to be matched with the templated
            scales:  the scales of the template to be used for matching

        Returns: the max value of the match, the x and y coordinates of the center of the matched template

        """
        img = image or self.get_screenshot()

        if type(template) == str:
            template = cv2.imread(template)
        elif type(template) == np.ndarray:
            template = template

        if len(template.shape) == 3:
            h, w, _ = template.shape
        elif len(template.shape) == 2:
            h, w = template.shape
        else:
            raise ValueError("Template shape not supported")

        if img.shape[0] <= h or img.shape[1] <= w:
            print("template larger than image. restart")
            raise ValueError("Template larger than image")

        max_max_val = 0
        for scale in scales:
            template = imutils.resize(template, width=int(w * scale), inter=cv2.INTER_LINEAR)
            res = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val >= max_max_val:
                max_max_val, top_left = max_val, max_loc
        center_x = top_left[0] + w / 2
        center_y = top_left[1] + h / 2
        return max_max_val, int(center_x), int(center_y)

    def tap_location(
        self,
        x: float,
        y: float,
        pause_l=1,
        pause_h=1,
        msg=None,
    ) -> None:
        """
        tap location at x and y
        Args:
            x: the x location of the tap, in percentage of screen width
            y: the y location of the tap, in percentage of screen height
            pause_l: the lower bound of the pause time
            pause_h: the upper bound of the pause time
            msg: message to be printed

        Returns: None

        """
        if msg is not None:
            print(msg)
        self.d.click(x * self.screen_width, y * self.screen_height)
        pause(pause_l, max(pause_l, pause_h))

    def tap_image(
        self,
        image: str | np.ndarray,
        max_wait_before_tap: float = 2,
        pause_after_tap_l: float = 0,
        pause_after_tap_h: float = 0,
        x_shift: int = 0,
        y_shift: int = 0,
        msg: str = None,
        use_homography: bool = False,
    ) -> bool:
        """
        tap image template in image
        Args:
            image: the image template to be tapped
            max_wait_before_tap: the maximum time to wait before tapping
            pause_after_tap_l: the lower bound of the pause time after tapping
            pause_after_tap_h: the upper bound of the pause time after tapping
            x_shift: the x shift of the tap location in pixels
            y_shift: the y shift of the tap location in pixels
            msg: message to be printed
            use_homography: whether to use homography to find the tap location

        Returns: True if the image was found and tapped, False otherwise

        """
        if msg is not None:
            print(msg)

        start_time = time.time()
        if use_homography is False:
            val = 0
            while val <= 0.99 and time.time() - start_time <= max_wait_before_tap:
                val, x, y = self.match_image(image)
            if val <= 0.99:
                return False
        else:
            res = None
            while res is None and time.time() - start_time <= max_wait_before_tap:
                res = findHomography(image, image=self.get_screenshot())
            if res is None:
                return False
            else:
                x, y = res
        self.d.click(x * self.screen_width + x_shift, y * self.screen_height + y_shift)
        pause(pause_after_tap_l, max(pause_after_tap_l, pause_after_tap_h))
        return True

    def swipe(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        duration_s: float = 0.3,
        pause_l: float = 0,
        pause_h: float = 0,
        msg: str = None,
    ) -> None:
        """
        Swipe from (x1, y1) to (x2, y2) in duration_s seconds
        Args:
            x1: x coordinate of start point, in percentage of screen width
            y1: y coordinate of start point, in percentage of screen height
            x2: x coordinate of end point, in percentage of screen width
            y2: y coordinate of end point, in percentage of screen height
            duration_s: duration of swipe in seconds
            pause_l: lower bound of pause time after swipe
            pause_h: upper bound of pause time after swipe
            msg: message to print before swipe

        Returns: None

        """
        if msg is not None:
            print(msg)
        self.d.swipe(
            x1 * self.screen_width,
            y1 * self.screen_height,
            x2 * self.screen_width,
            y2 * self.screen_height,
            duration_s,
        )

        pause(pause_l, pause_h)
