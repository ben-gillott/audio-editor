import scipy.fft
import numpy as np
import matplotlib.pyplot as plt

class Signal(object):
    def __init__(self, samples, sampling_rate):
        self.samples = samples;
        self.sampling_rate = sampling_rate;
    
    @property
    def n_samples(self):
        return len(self.samples);
    @property
    def sample_duration(self):
        return np.true_divide(1.0, self.sampling_rate);
    @property
    def duration(self):
        return self.n_samples*self.sample_duration;
    @property
    def times(self):
        return np.linspace(0,self.duration,int(self.n_samples), endpoint=False); # endpoint false since we are starting at t=0
    
    def plot(self, title=None):
        plt.plot(self.times, self.samples);
        plt.xlabel('Time (seconds)\n[Sampling Rate: {} Hz]'.format(self.sampling_rate));
        plt.ylabel('Value');
        if(not (title is None)):
            plt.title(title);
            
            
    def scatter(self, title=None):
        plt.scatter(self.times, self.samples, color='red');
        plt.xlabel('Time (seconds)\n[Sampling Rate: {} Hz]'.format(self.sampling_rate));
        plt.ylabel('Value');
        if(not (title is None)):
            plt.title(title);
        
    @property
    def fft_freqs(self):
        return scipy.fft.fftfreq(self.n_samples)*self.sampling_rate
        
    def plotFFT(self, title=None):
        fft_vals = scipy.fft.fft(self.samples);
        fft_freqs = self.fft_freqs;
        
        # you need to shift the fft to get the DC component in the middle of the array
        fft_vals = scipy.fft.fftshift(fft_vals);
        fft_freqs = scipy.fft.fftshift(fft_freqs);
        
        plt.plot(fft_freqs, np.abs(fft_vals))
        plt.xlabel('Frequency (Hz)\n[Sampling Rate: {} Hz]'.format(self.sampling_rate));
        plt.ylabel('Magnitude');
        if(not (title is None)):
            plt.title(title);


            
    def GetResampledToLength(self, new_length):
        # Resample by cropping or padding the fft with zeros         
        # Note: you will want to use the function scipy.fft.fftshift
        ###### To make life easier, we will only change by even amounts...
        n_pad=new_length-self.n_samples;
        

        
        assert(n_pad%2 == 0), "must resample by even number of samples. Requested {}".format(n_pad);
        ######

        # delete this error and implement resampling in the frequency domain

        
        
        # Your code here
        new_samples = scipy.fft.fft(self.samples);
        
        bpad = n_pad/2;
        print(bpad);
        print(-1*bpad);
        print(len(new_samples)+bpad);
        print(len(new_samples));
        
        if bpad < 0:
            #crop to a slice, shorter by bpda
            new_samples = new_samples[int(-1*bpad):int(len(new_samples)+bpad)];
        else:
            new_samples = np.pad(new_samples, n_pad);

        new_samples = scipy.fft.fftshift(new_samples);
        new_samples = scipy.fft.ifft(new_samples);
        
        new_sampling_rate = self.sampling_rate; #Unsure how the sampling rate should change here
        
        return Signal(samples=new_samples, sampling_rate = new_sampling_rate);
