from midi_writer import writeMid
from wave_reader import readWav
from note_recognize import recognize
import sys


def wav2mid(wav_file_name, tempo = 120):
    _, _, fr, data = readWav(wav_file_name)
    note_time_list = recognize(data,fr,tempo)
    outMidPath = writeMid(note_time_list,tempo)
    print outMidPath


# python wav2mid.py [wavFilePath] tempo
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        wav2mid(sys.argv[1], tempo = int(sys.argv[2]))
    else:
        wav2mid(sys.argv[1])



