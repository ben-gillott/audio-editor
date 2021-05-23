import os;
def _getModulePath():
    return os.path.abspath(os.path.dirname(__file__));


from apy.amedia.examplefiles import *
import apy.utils as utils
import numpy as np
import matplotlib.pyplot as plt

from apy.amedia.Video import *
from apy.amedia.Image import *
from a3py.Audio import Audio
from a3py.STFT import *
Video.AudioClass = Audio;
from a3py import pointline

from a3py.MySignal import *