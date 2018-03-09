from wave_reader import readWav
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import math

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

def qualify(wav_data, fr):
    nframe = len(wav_data)
    print wav_data
    time = np.arange(0, nframe) * (1.0 / fr)
    plt.plot(time, wav_data)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("Single channel wavedata")
    plt.grid('on')
    plt.show()

def recognize(wav_data, fs = 44100.0, tempo = 120):
    '''
    Usage: recognize notes of a banch of wave data in time zone
    Args:
        wav_data: a 1-d array that containing the time data
        fs: the sample frequency
        tempo: the tempo of the song, measured by crotchets per minute
    Returns:
        A list of note information. Each piece of information is a triple: (note_name, start_time(s), end_time(s))
    '''
#    print(len(wav_data))

    START_BLANK = 0.5
    WAVE_START_BIAS = 0.1
    NOTE_AMP_BIAS = 0.15

    r_t = 60.0 / tempo #resolution of STFT, 1/4 of a crotchet.

    start = 0
    for i, frame in enumerate(wav_data): #adjust the blank at the begining
        if abs(frame) > WAVE_START_BIAS:
            start = i
            break
    if start / fs > 60.0 / tempo:
        wav_data = wav_data[start - int(60.0/tempo * fs):]
    else:
        wav_data = [0 for _ in range(int(60.0/tempo * fs) - start)] + wav_data.tolist()


    f, t, Zxx = signal.stft(wav_data, fs, nperseg = int(r_t / 2 * fs)) #it should be adjusted by the resolution of the time zone
    Zxx = np.abs(Zxx)

    #print note_freq
    f_fil = []
    Zxx_fil = []

    for i, freq in enumerate(f):
        if freq > 50 and freq < 1000:
            f_fil.append(freq)
            Zxx_fil.append(Zxx[i][:])

    toRtn = []

    '''plt.pcolormesh(t, f_fil, np.abs(Zxx_fil), vmin=0, vmax=0.3)
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time[sec]')
    plt.show()'''

    Zxx_fil = np.transpose(Zxx_fil)
    last_note = None
    start_time = 0
    first_time = -1
    f = open("note.log", 'w')

    for i in range(len(t) / 4):
        #consider consecutive four time blocks
        time_part = t[i*4:min((i+1)*4, len(t))]
        Zxx_part = Zxx_fil[i*4:min((i+1)*4, len(t))]
        note_amp = [[0 for _ in range(88)] for __ in range(4)]
        note_freq_sort = []
        max_amp = []
        for j in range(4):
            for k in range(len(Zxx_part[j])):
                note_amp[j][note_name.index(freqToNote(f_fil[k]))] += Zxx_part[j][k]
            #for k in range(88):
            #    note_amp[j][k] /= math.sqrt(note_freq[k])
            note_freq_sort.append(np.argsort(np.array(note_amp[j])))
            max_amp.append(note_amp[j][note_freq_sort[j][87]])
        #print max_amp
        #print sum(max_amp)
        #assume it's a crotchet:
        #two ways to decide the note, calculate the sum of the amp, or major voting. here try to apply the second algorithm
        major_note = [0 for _ in range(88)]
        for j in range(4):
            for k in range(88):
                major_note[note_freq_sort[j][k]] += k
        major_notes = np.argsort(np.array(major_note)).tolist()
        #print major_notes
        for j in range(87, -1, -1):
            if last_note == None or abs(major_notes[j] - note_name.index(last_note)) <= 7:
                if last_note != None and major_notes[j] - note_name.index(last_note) == 1:
                    if major_notes.index(major_notes[j] + 1) > major_notes.index(major_notes[j] - 1):     #half-step notes are not allowed to avoid fluctuate
                        note = note_name[major_notes[j] + 1]
                    else:
                        note = last_note
                elif last_note != None and major_notes[j] - note_name.index(last_note) == -1:
                    if major_notes.index(major_notes[j] - 1) > major_notes.index(major_notes[j] + 1):
                        note = note_name[major_notes[j] - 1]
                    else:
                        note = last_note
                else:
                    note = note_name[major_notes[j]]
                break
        if sum(max_amp) > NOTE_AMP_BIAS:
            if first_time == -1:
                first_time = i * 4 * t[1]   #shift the output notes to shrink or amplify the possible blank
            last_note = note
            toRtn.append((note, i * 4 * t[1] - first_time + START_BLANK, (i + 1) * 4 * t[1] - first_time + START_BLANK))
    """for i, time in enumerate(t):
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
                f.write("%s %.4f\t\t" % (note_name[note_freq_sort[j]], note_amp[note_freq_sort[j]]))
                if note_amp[note_freq_sort[j]] < max_amp * 0.3:
                    break
                if note == None or note_name.index(note) > note_freq_sort[j]:
                    if last_note == None or abs(note_name.index(last_note) - note_freq_sort[j]) <= 7:
                        note = note_name[note_freq_sort[j]]
        f.write("%.4f\n"%np.sum(note_amp))
        if note != last_note:
            if last_note != None:
                toRtn.append((last_note, start_time, time))
            last_note = note
            start_time = time"""
    f.close()
#    if last_note != None:
#        toRtn.append((last_note, start_time, t[1]*len(t)))
    #print toRtn
    #print len(toRtn)

    return toRtn

if __name__ == "__main__":

#    f = open("note_freq.txt", 'w')
#    for i in range(len(note_name)):
#        f.write("%s: %.4f\n" % (note_name[i], note_freq[i]))
    _, _, fr, data = readWav("rec")
#    qualify(data, fr)
#    print("hello")
    recognize(data, fr, 195)
#    print(freqToNote(500))


