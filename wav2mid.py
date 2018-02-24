from midi_writer import writeMid
from wave_reader import readWav
from note_recognize import recognize
import sys


def wav2mid(wav_file_name):
    print "readWav"
    _, _, fr, data = readWav(wav_file_name)
    print "recognize"
    note_time_list = recognize(data,fr)
    print "writeMid"
    writeMid(note_time_list)


if __name__ == "__main__":
    print sys.argv[1]
    wav2mid(sys.argv[1])



