from .estimator_2d import Estimator2D

import sys
import os
from sys import platform

dir_path = 'D:/Softwares/openpose/build/examples/tutorial_api_python'

try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

class OpenPoseEstimator(Estimator2D):

    def __init__(self, model_folder):
        """
        OpenPose 2D pose estimator. See [https://github.com/
        CMU-Perceptual-Computing-Lab/openpose/tree/ master/examples/
        tutorial_api_python] for help.
        Args: 
        """
        super().__init__()
        params = {'model_folder': model_folder, 'render_pose': 0}
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()

    def estimate(self, img_list, bbox_list=None):
        """See base class."""
        keypoints_list = []
        for i, img in enumerate(img_list):
            if bbox_list:
                x, y, w, h = bbox_list[i]
                img = img[y:y+h, x:x+w]
            datum = op.Datum()
            datum.cvInputData = img
            self.opWrapper.emplaceAndPop([datum])
            keypoints = datum.poseKeypoints
            if bbox_list:
                # TODO: restore coordinate
                pass
            keypoints_list.append(datum.poseKeypoints)

        return keypoints_list