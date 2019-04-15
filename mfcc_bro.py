import numpy
from scipy.fftpack import dct

def do_mfcc(spectrogram, upper_frequency_limit=4000, lower_frequency_limit=0, dct_coefficient_count=12):

    mfcc = dct(spectrogram, type=2, axis=1, norm='ortho')[:, 1: (dct_coefficient_count + 1)]  # Keep 2-13

    mfcc -= (numpy.mean(mfcc, axis=0) + 1e-8)  # Mean normalization of mfcc

    return mfcc

    #(nframes, ncoeff) = mfcc.shape
    #n = numpy.arange(ncoeff)
    #lift = 1 + (cep_lifter / 2) * numpy.sin(numpy.pi * n / cep_lifter)
    #mfcc *= lift