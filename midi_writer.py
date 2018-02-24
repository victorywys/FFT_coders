import midi


def writeMid(note_time_list):
    '''
        Usage: write the infomation got from wav transfer to a .mid file
        Args:
            note_time_list: the info from the note tranfer
        Returns:
    '''
    print("write midi")
    # create a new midi.pattern, and add a track to it
    pattern = midi.Pattern()
    track = midi.Track()
    pattern.append(track)

    # transfer the note name in note_time_list to int value in midi format
    note_num_list = note_name2note_num(note_time_list)

    # transfer the note start_time and end_time to tick number in midi format
    start_end_tick_list = time2tick(note_time_list)

    #change the absolute tick to delta tick
    event_list = order_ticks(note_num_list,start_end_tick_list)

    # write the transformed list to noteOnEvents,add to the track
    for event in event_list:
        if event[2]==1:
            on = midi.NoteOnEvent(tick=event[1],velocity=50,pitch=event[0])
            track.append(on)
        else:
            off = midi.NoteOffEvent(tick=event[1],pitch=event[0])
            track.append(off)

    # add endTrackEvent on the track
    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)

    # Print out the pattern
    print pattern
    # Save the pattern to "out.mid" file
    midi.write_midifile("out.mid", pattern)


def note_name2note_num(note_name_list):
    '''
        Usage: transfer the note name in note_time_list to int value in midi format
        Args:
            note_time_list: the original info got from wav_reader
        Returns:
            note_num_list: the list of note number in the order of input list
    '''
    NOTE_NAME_DICT = {}
    NOTE_NAMES = ['C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B']
    NOTE_PER_OCTAVE = len(NOTE_NAMES)

    for value in range(128):
        noteidx = value % NOTE_PER_OCTAVE
        octidx = value / NOTE_PER_OCTAVE
        octidx -= 2
        name = NOTE_NAMES[noteidx]
        if len(name) == 2:
            # sharp note
            flat = NOTE_NAMES[noteidx + 1] + 'b'
            NOTE_NAME_DICT['%s_%d' % (flat, octidx)] = value
            NOTE_NAME_DICT['%s_%d' % (name, octidx)] = value
        else:
            NOTE_NAME_DICT['%s_%d' % (name, octidx)] = value
            NOTE_NAME_DICT['%s_%d' % (name, octidx)] = value

    note_num_list = []

    for note_tuple in note_name_list:
        note_num_list.append(NOTE_NAME_DICT[note_tuple[0]])

    return note_num_list


def time2tick(time_list):
    '''
        Usage: transfer the note start_time and end_time to tick number(absolute) in midi format
        Args:
            time_list: the original info got from wav_reader
        Returns:
            tick_list: the list of start_end_tick_num tuples
    '''
    BPM = 120
    RESOLUTION = 220
    tick_list = []
    for time_tuple in time_list:
        start_tick = int(round(time_tuple[1]*RESOLUTION*2))
        end_tick = int(round(time_tuple[2]*RESOLUTION*2))
        temp = (start_tick,end_tick)
        tick_list.append(temp)

    return tick_list


def order_ticks(note_num_list,start_end_tick_list):
    '''
        Usage: reorder the tick number from absolute to relative(midi format)
        Args:
            note_num_list: note num's list
            start_end_tick_list: the list of tuples of start and end tick(absolute)
        Returns:
            event_list: the list of tuple (note_num, relative_tick_num, on/off), 1/0 represent on/off
    '''
    event_list = []

    for i in range(len(note_num_list)):
        note_num = note_num_list[i]
        start_tick  = start_end_tick_list[i][0]
        end_tick = start_end_tick_list[i][1]
        start = [note_num, start_tick, 1]
        end = [note_num, end_tick, 0]
        event_list.append(start)
        event_list.append(end)

    event_list = sorted(event_list, key=lambda event: event[1])

    current_tick = 0
    for event in event_list:
        delta = event[1]-current_tick
        current_tick = event[1]
        event[1] = delta

    return event_list


