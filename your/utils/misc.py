import logging

import numpy as np

from your.utils.math import closest_number

logger = logging.getLogger(__name__)
from skimage.transform import resize

import json
import matplotlib

matplotlib.use('Agg')


def save_bandpass(your_object, bandpass, chan_nos=None, mask=[], outdir=None, outname=None):
    """
    Plots and saves the bandpass
    :param your_object: Your object
    :param bandpass: Bandpass of data
    :param chan_nos: array of channel numbers
    :param mask: boolean array of channel mask 
    :param outdir: output directory to save the plot
    :return: 

    """
    
    freqs = your_object.chan_freqs
    foff = your_object.your_header.foff
        
    if not outdir:
        outdir = './'

    if chan_nos is None:
        chan_nos=np.arange(0,bandpass.shape[0])
        
    if not outname:
        bp_plot=outdir+ your_object.your_header.basename + '_bandpass.png'
    else:
        bp_plot = outname

    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax11 = fig.add_subplot(111)
    if foff < 0:
        ax11.invert_xaxis()

    ax11.plot(freqs, bandpass,'k-',label="Bandpass")
    if mask is not None:
        if mask.sum():
            logging.info('Flagged %d channels',mask.sum())
            ax11.plot(freqs[mask],bandpass[mask],'ro',label="Flagged Channels")
    ax11.set_xlabel("Frequency (MHz)")
    ax11.set_ylabel("Arb. Units")
    ax11.legend()

    ax21 = ax11.twiny()
    ax21.plot(chan_nos, bandpass,alpha=0)
    ax21.set_xlabel("Channel Numbers")
    
    return plt.savefig(bp_plot,bbox_inches='tight')


def _decimate(data, decimate_factor, axis, pad=False, **kwargs):
    """

    :param data: data array to decimate
    :param decimate_factor: number of samples to combine
    :param axis: axis along which decimation is to be done
    :param pad: Whether to apply padding if the data axis length is not a multiple of decimation factor
    :param args: arguments of padding
    :return:
    """
    if data.shape[axis] % decimate_factor and pad is True:
        logger.info(f'padding along axis {axis}')
        pad_width = closest_number(data.shape[axis], decimate_factor)
        data = pad_along_axis(data, data.shape[axis] + pad_width, axis=axis, **kwargs)
    elif data.shape[axis] % decimate_factor and pad is False:
        raise AttributeError('Axis length should be a multiple of decimate_factor. Use pad=True to force decimation')

    if axis:
        return data.reshape(int(data.shape[0]), int(data.shape[1] // decimate_factor), int(decimate_factor)).mean(2)
    else:
        return data.reshape(int(data.shape[0] // decimate_factor), int(decimate_factor), int(data.shape[1])).mean(1)


def _resize(data, size, axis, **kwargs):
    """

    :param data: data array to resize
    :param size: required size of the axis
    :param axis: axis long which resizing is to be done
    :param args: arguments for skimage.transform resize function
    :return:
    """
    if axis:
        return resize(data, (data.shape[0], size), **kwargs)
    else:
        return resize(data, (size, data.shape[1]), **kwargs)


def crop(data, start_sample, length, axis):
    """

    :param data: Data array to crop
    :param start_sample: Sample to start the output cropped array
    :param length: Final Length along the axis of the output
    :param axis: Axis to crop
    :return:
    """
    if data.shape[axis] > start_sample + length:
        if axis:
            return data[:, start_sample:start_sample + length]
        else:
            return data[start_sample:start_sample + length, :]
    elif data.shape[axis] == length:
        return data
    else:
        raise OverflowError('Specified length exceeds the size of data')


def pad_along_axis(array: np.ndarray, target_length, loc='end', axis=0, **kwargs):
    """

    :param array: Input array to pad
    :param target_length: Required length of the axis
    :param loc: Location to pad: start: pad in beginning, end: pad in end, else: pad equally on both sides
    :param axis: Axis to pad along
    :return:
    """
    pad_size = target_length - array.shape[axis]
    axis_nb = len(array.shape)

    if pad_size < 0:
        return array
        # return a

    npad = [(0, 0) for x in range(axis_nb)]

    if loc == 'start':
        npad[axis] = (int(pad_size), 0)
    elif loc == 'end':
        npad[axis] = (0, int(pad_size))
    else:
        npad[axis] = (int(pad_size // 2), int(pad_size // 2))

    return np.pad(array, pad_width=npad, **kwargs)


class MyEncoder(json.JSONEncoder):
    """
    Custom Encoder Class to convert any class to a JSON serializable object
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)
