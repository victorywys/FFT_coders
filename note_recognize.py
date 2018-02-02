from wave_reader import readWav
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

note_name=["A0", "Bb0", "B0",
        "C1", "C#1", "D1", "Eb1", "E1", "F1", "F#1", "G1", "G#1", "A1", "Bb1", "B1",
        "C2", "C#2", "D2", "Eb2", "E2", "F2", "F#2", "G2", "G#2", "A2", "Bb2", "B2",
        "C3", "C#3", "D3", "Eb3", "E3", "F3", "F#3", "G3", "G#3", "A3", "Bb3", "B3",
        "C4", "C#4", "D4", "Eb4", "E4", "F4", "F#4", "G4", "G#4", "A4", "Bb4", "B4",
        "C5", "C#5", "D5", "Eb5", "E5", "F5", "F#5", "G5", "G#5", "A5", "Bb5", "B5",
        "C6", "C#6", "D6", "Eb6", "E6", "F6", "F#6", "G6", "G#6", "A6", "Bb6","B6",
        "C7", "C#7", "D7", "Eb7", "E7", "F7", "F#7", "G7", "G#7", "A7", "Bb7","B7",
        "C8"  ]
note_freq=[27.5 * (2 ** (i/12.0)) for i in range(88)]

def freqToNote(freq):
    note_num = len(note_freq)
    log_note = np.log(list(map(lambda x: x[0]/x[1], zip(note_freq, [freq] * note_num))))
    return note_name[np.argmin(abs(log_note))]


def recognize(wav_data, fs = 1.0):
    '''
    Usage: recognize notes of a banch of wave data in time zone
    Args:
        wav_data: a 1-d array that containing the time data
    Returns:
        A list of note information. Each piece of information is a triple: (note_name, start_time(s), end_time(s))
    '''
#    print(len(wav_data))

    f, t, Zxx = signal.stft(wav_data, fs, nperseg = 10000) #it should be adjusted by the resolution of the time zone
    Zxx = np.abs(Zxx)

    #print note_freq
    f_fil = []
    Zxx_fil = []

    for i, freq in enumerate(f):
        if freq < 4500:
            f_fil.append(freq)
            Zxx_fil.append(Zxx[i][:])

    toRtn = []

    Zxx_fil = np.transpose(Zxx_fil)
    last_note = None
    start_time = 0
    for i, time in enumerate(t):
        max_freq = f_fil[np.argmax(Zxx_fil[i])]
        note = freqToNote(max_freq)
        if note != last_note:
            if last_note != None:
                toRtn.append((last_note,start_time,time))

            last_note = note
            start_time = time
    toRtn.append((last_note, start_time, t[1]*len(t)))
    print toRtn
    return toRtn

#
#    plt.pcolormesh(t, f_fil, np.abs(Zxx_fil), vmin=0, vmax=0.3)
#    plt.title('STFT Magnitude')
#    plt.ylabel('Frequency [Hz]')
#    plt.xlabel('Time[sec]')
#    plt.show()

if __name__ == "__main__":
#    print(len(note_name))
#    for i in range(len(note_name)):
#        print("%s: %.4f" % (note_name[i], note_freq[i]))
#    _, _, fr, data = readWav("night")
#    print("hello")
    recognize(data, fr)
#    print(freqToNote(500))

