import apy
from apy.aobject.SavesFeatures import FeatureFunction
import scipy as sp
import numpy as np


class Audio(apy.amedia.Audio):
    def __init__(self, path=None, sampling_rate=None, samples=None, name=None,**kwargs):
        super(Audio, self).__init__(path=path, sampling_rate=sampling_rate, samples=samples, name=name, **kwargs);
    def GetResampledToLength(self, new_length):
        from a3py.MySignal import Signal
        s = Signal(self.samples, self.sampling_rate);
        new_signal = s.GetResampledToLength(new_length);
        return Audio(samples=new_signal.samples, sampling_rate=new_signal.sampling_rate);