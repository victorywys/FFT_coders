import wave
import numpy as np

allowModes = ["average", "split", "first"]

def readWav(filename, mode = "first"):
    '''
    Usage: read from a .wav file and return the infos and contents of the file
    Args:
        filename: filename of the .wav file
        mode: specify how multi-channel .wav files are processed
    Returns:
        nchannels: the number of chennels of the .wav file
        sampwidth: the sample width(byte) of the .wav file
        framerate: the frame rate of the .wav file
        wavedata: the content list of the .wav file
    '''

    #avoid invalid mode
    if not mode in allowModes:
        print("mode \"%s\" is not available in this version!\n" % mode)
        print("usage:")
        print("\taverage: return a 1-d list containing the average frame data of all channels.")
        print("\tsplit: return a 2-d list containing the frame data of every channels respectively.")
        print("\tfirst: return a 1-d list containing the frame data of the first channel.")
        return

    #add suffix if suffix is not explicitly given
    if len(filename) < 4:
        filename = filename + ".wav"
    elif not filename[-4:].lower() in ".wav":
        filename = filename + ".wav"

    #avoid FileIO exceptions
    try:
        f = wave.open(filename, "rb")
    except Exception, e:
        print("%s open with an exception!" % filename)
        print("\t%s" % str(e))
        return None

    #process wave file
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)
    waveData = np.fromstring(strData, dtype = np.int16)
    if max(abs(waveData)) > 0:
        waveData = waveData * 1.0 / max(abs(waveData))
    f.close()
    if mode == "average":
        waveData = np.mean(np.reshape(waveData, [nframes, -1]), axis = 1)
    elif mode == "split":
        waveData = np.reshape(waveData, [nframes, -1])
    elif mode == "first":
        waveData = np.reshape(waveData, [nframes, -1])[:, 0]
    return nchannels, sampwidth, framerate, waveData

if __name__ == '__main__':
    a, b, c, d = readWav("9157", "first")
    print(a)
    print(b)
    print(c)
    print(d)
