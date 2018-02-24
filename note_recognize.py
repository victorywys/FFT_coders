from wave_reader import readWav
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

note_name=["A_0", "As_0", "B_0",
        "C_1", "Cs_1", "D_1", "Ds_1", "E_1", "F_1", "Fs_1", "G_1", "Gs_1", "A_1", "As_1", "B_1",
        "C_2", "Cs_2", "D_2", "Ds_2", "E_2", "F_2", "Fs_2", "G_2", "Gs_2", "A_2", "As_2", "B_2",
        "C_3", "Cs_3", "D_3", "Ds_3", "E_3", "F_3", "Fs_3", "G_3", "Gs_3", "A_3", "As_3", "B_3",
        "C_4", "Cs_4", "D_4", "Ds_4", "E_4", "F_4", "Fs_4", "G_4", "Gs_4", "A_4", "As_4", "B_4",
        "C_5", "Cs_5", "D_5", "Ds_5", "E_5", "F_5", "Fs_5", "G_5", "Gs_5", "A_5", "As_5", "B_5",
        "C_6", "Cs_6", "D_6", "Ds_6", "E_6", "F_6", "Fs_6", "G_6", "Gs_6", "A_6", "As_6", "B_6",
        "C_7", "Cs_7", "D_7", "Ds_7", "E_7", "F_7", "Fs_7", "G_7", "Gs_7", "A_7", "As_7", "B_7",
        "C_8"]
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

#    plt.pcolormesh(t, f_fil, np.abs(Zxx_fil), vmin=0, vmax=0.3)
#    plt.title('STFT Magnitude')
#    plt.ylabel('Frequency [Hz]')
#    plt.xlabel('Time[sec]')
#    plt.show()

    Zxx_fil = np.transpose(Zxx_fil)
    last_note = None
    start_time = 0
    for i, time in enumerate(t):
        '''    max_freq = f_fil[np.argmax(Zxx_fil[i])]
        note = freqToNote(max_freq)
        fout.write("%s, %.4f, %.4f\n" % (note, max(Zxx_fil[i]), np.sum(Zxx_fil[i])))
        if note != last_note:
            if last_note != None:
                toRtn.append((last_note,start_time,time))

            last_note = note
            start_time = time
        '''
        note_amp = [0 for _ in range(88)]
        for j in range(len(Zxx_fil[i])):
            note_amp[note_name.index(freqToNote(f_fil[j]))] += Zxx_fil[i][j]
        note_freq_sort = np.argsort(np.array(note_amp))
        max_amp = note_amp[note_freq_sort[87]]
        note = None
        if max_amp > 0.1:
            for j in range(87, -1, -1):
                if note_amp[note_freq_sort[j]] < max_amp * 0.7:
                    break
                if note == None:
                    note = note_name[note_freq_sort[j]]
                elif note_name.index(note) > note_freq_sort[j]:
                    note = note_name[note_freq_sort[j]]
        if note != last_note:
            if last_note != None:
                toRtn.append((last_note, start_time, time))
            last_note = note
            start_time = time
    if last_note != None:
        toRtn.append((last_note, start_time, t[1]*len(t)))
    print toRtn
    print len(toRtn)

    return toRtn

if __name__ == "__main__":
#    print(len(note_name))
#    for i in range(len(note_name)):
#        print("%s: %.4f" % (note_name[i], note_freq[i]))
    _, _, fr, data = readWav("fft_coder")
#    print("hello")
    recognize(data, fr)
#    print(freqToNote(500))

