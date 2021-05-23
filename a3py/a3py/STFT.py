import apy.asigpy.maths.NDArray as NDArray
from apy.aobject import *
import scipy as sp
import librosa
import matplotlib.pyplot as plt
import numpy as np
from a3py import Audio

class STFT(NDArray):
    # STFT class
    def __init__(self, values, window_size=None, hop_size=None, name=None, sampling_rate = None, nfft=None, **kwargs):
        '''

        :param values: the actual stft coefficients
        :type values:
        :param window_size: the window size used to compute the stft
        :type window_size:
        :param hop_size: the hop size used to compute the stft
        :type hop_size:
        :param name: optional name for displaying in plots
        :type name:
        :param sampling_rate: sampling rate of underlying signal
        :type sampling_rate:
        :param nfft: optional number of samples used to compute each fft. By default, this will be equal to window_size
        :type nfft:
        :param kwargs:
        :type kwargs:
        '''
        super(STFT, self).__init__(data=values, copy_data=False);
        self.window_size = window_size;
        self.hop_size = hop_size;
        self.name = name;
        self._nfft=nfft;
        self.sampling_rate = sampling_rate;
        
    def clone(self):
        '''
        Create and return a copy of the stft object
        :return:
        :rtype:
        '''
        thisclass = type(self);
        return thisclass(values=self.values.copy(),
                         window_size=self.window_size,
                         hop_size=self.hop_size,
                         name=self.name,
                         sampling_rate=self.sampling_rate,
                         nfft=self._nfft);

    @property
    def mag(self):
        '''
        Get the magnitudes of the stft coefficients
        :return:
        :rtype:
        '''
        return np.abs(self.values);

    @property
    def phase(self):
        '''
        get the phases of the stft coefficients
        :return:
        :rtype:
        '''
        return np.angle(self.values);

    def setPhaseMag(self, phase, mag):
        '''
        Set stft coefficients according to provided phases and magnitudes
        :param phase: phases for each coefficient
        :type phase:
        :param mag: magnitudes for each coefficient
        :type mag:
        :return:
        :rtype:
        '''
        self.values=mag*np.exp(1j*phase);

    def GetPhaseMagCopy(self, phase, mag):
        '''
        returns a copy of the STFT with coefficients set according to provided phases and magnitudes
        :param phase:
        :type phase:
        :param mag:
        :type mag:
        :return:
        :rtype:
        '''
        rval = self.clone();
        rval.setPhaseMag(phase=phase, mag=mag);
        return rval;

    @property
    def freqs(self):
        '''
        Get the frequencies represented by the rows of the stft.
        :return:
        :rtype: array of frequencies in Hz
        '''
        return librosa.fft_frequencies(self.sampling_rate, self.nfft);

    @property
    def times(self):
        '''
        Get the times represented by the columns of the stft
        :return:
        :rtype:
        '''
        return librosa.frames_to_time(np.arange(self.values.shape[1]), sr=self.sampling_rate, hop_length=self.hop_size),

    @property
    def values(self):
        '''
        get the stft coefficients
        :return:
        :rtype:
        '''
        if(not isinstance(self._ndarray, np.ndarray)):
            return np.array(self._ndarray);
        else:
            return self._ndarray;

    @values.setter
    def values(self, value):
        '''
        set the stft coefficients
        :param value:
        :type value:
        :return:
        :rtype:
        '''
        self._ndarray = value;

    @property
    def nfft(self):
        '''
        :return: if nfft is not specified, default to window size.
        :rtype:
        '''
        if(self._nfft is None):
            return self.window_size;
        else:
            return self._nfft;

    @nfft.setter
    def nfft(self, value):
        self._nfft = value;

    @property
    def is_onesided(self):
        '''
        returns true if only the positive coefficients are stored. This will generally be true in this implementation.
        :return:
        :rtype:
        '''
        return len(self.freqs)<self.nfft;
    # </editor-fold>
    ##################\\--props--//##################

    @classmethod
    def FromSignal(cls, samples, sampling_rate=None, window_size=None, hop_size=None, nfft=None, **kwargs):
        '''
        Get STFT object from signal
        :param samples:
        :type samples:
        :param sampling_rate:
        :type sampling_rate:
        :param window_size:
        :type window_size:
        :param hop_size:
        :type hop_size:
        :param nfft:
        :type nfft:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        '''
        if(window_size is None):
            window_size=2048;
        if(hop_size is None):
            hop_size = int(np.round(window_size*0.5));
        if(sampling_rate is None):
            sampling_rate=1;
        if(nfft is None):
            nfft = window_size;
        lrargs = dict(
            y=samples,
            n_fft=nfft,
            hop_length=int(hop_size),
            win_length=int(window_size),
            **kwargs);
        lrstft = librosa.stft(**lrargs);
        rval = cls(values=lrstft,
                   sampling_rate=sampling_rate,
                   window_size=int(window_size),
                   hop_size = int(hop_size),
                   nfft=nfft,
                   **kwargs);
        return rval;

    @classmethod
    def FromAudio(cls, audio, window_size=None, hop_size=None, nfft=None, **kwargs):
        '''
        Helper function to create STFT object from Audio object
        :param audio:
        :type audio:
        :param window_size:
        :type window_size:
        :param hop_size:
        :type hop_size:
        :param nfft:
        :type nfft:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        '''
        return cls.FromSignal(samples=audio.samples,
                              sampling_rate=audio.sampling_rate,
                              window_size=window_size,
                              hop_size=hop_size,
                              nfft=nfft,
                              **kwargs);

    def GetISTFTAudio(self, window_size=None, hop_size=None, sampling_rate = None, name=None, **kwargs):
        '''
        Get the Audio object corresponding the the istft of an STFT. Samples will be the real part of the istft.
        :param window_size:
        :type window_size:
        :param hop_size:
        :type hop_size:
        :param sampling_rate:
        :type sampling_rate:
        :param name:
        :type name:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        '''
        if(sampling_rate is None):
            sampling_rate = self.sampling_rate;
        istft = self.istft(window_size=window_size, hop_size=hop_size, **kwargs);
        return Audio(samples=np.real(istft), sampling_rate=sampling_rate, name=name);

    def istft(self, window_size=None, hop_size=None, **kwargs):
        '''
        get the istft signal. samples will be the real part of the istft result.
        :param window_size:
        :type window_size:
        :param hop_size:
        :type hop_size:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        '''
        if(window_size is None):
            window_size=self.window_size;
        if(hop_size is None):
            hop_size=self.hop_size;
        lrargs = dict(stft_matrix=self.values, hop_length=int(hop_size), win_length=int(window_size), window='hann', **kwargs);
        return librosa.istft(**lrargs);

    def getPositiveFrequencyCoefficients(self):
        '''
        helper function that gets just the positive part of the stft, regardless of whether the underlying representation is one- or two-sided.
        Not super necessary in librosa-based implementation, but was in scipy-based one.
        :return:
        :rtype:
        '''
        if(self.is_onesided):
            return self.values;
        else:
            lastfindex = int(self.values.shape[0]/2)-1;
            return self[:lastfindex,:];

    def showPower(self, time_range=None, frequency_range=None, fig = None, linear_frequency=False, **kwargs):
        '''
        Show the power spectrogram
        :param time_range:
        :type time_range:
        :param frequency_range:
        :type frequency_range:
        :param fig:
        :type fig:
        :param linear_frequency:
        :type linear_frequency:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        '''
        if(fig is None):
            fig = plt.figure();
        S = self.getPositiveFrequencyCoefficients();
        if(linear_frequency):
            librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), sr=self.sampling_rate, hop_length=self.hop_size,
                                     y_axis='linear', x_axis='time',
                                     **kwargs)
        else:
            librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), sr=self.sampling_rate, hop_length=self.hop_size,
                                     y_axis='log', x_axis='time',
                                     **kwargs)
        plt.title('Power spectrogram')
        if (frequency_range is not None):
            plt.ylim(frequency_range);
        plt.xlabel('Time (s)')
        if (time_range is not None):
            plt.xlim(time_range);
        plt.tight_layout()
        return fig;

    def showPhase(self, time_range=None, frequency_range=None, fig = None, **kwargs):
        '''
        Show the phases of the stft
        :param time_range:
        :type time_range:
        :param frequency_range:
        :type frequency_range:
        :param fig:
        :type fig:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        '''
        if(fig is None):
            fig = plt.figure();
        S = self.getPositiveFrequencyCoefficients();
        librosa.display.specshow(np.angle(S),
                                 sr=self.sampling_rate,
                                 hop_length=self.hop_size,
                                 y_axis='linear',
                                 x_axis='time',
                                 cmap='gray_r',
                                 **kwargs);
        plt.title('Phase')
        if (frequency_range is not None):
            plt.ylim(frequency_range);
        plt.xlabel('Time (s)')
        if (time_range is not None):
            plt.xlim(time_range);
        plt.tight_layout()
        return fig;

    def show(self, title=None, time_range=None, frequency_range=None, **kwargs):
        fig, axs = plt.subplots(nrows=1,ncols=2,figsize=[10,4]);
        self.showPower(fig = fig, ax=axs[0], time_range=time_range, frequency_range=frequency_range, **kwargs);
        self.showPhase(fig = fig, ax=axs[1], time_range=time_range, frequency_range=frequency_range, **kwargs);
        axs[0].set(title='Power')
        axs[1].set(title='Phase')

        if (frequency_range is not None):
            axs[0].set_ylim(frequency_range);
            axs[1].set_ylim(frequency_range);
        if (time_range is not None):
            axs[0].set_xlim(time_range);
            axs[1].set_xlim(time_range);
        plt.tight_layout()
        if(title is not None):
            fig.suptitle(title, weight='bold', size=16, va='baseline');

