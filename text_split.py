import pysrt
from datetime import timedelta
from util_En import time_duration

####################################################################################
############ split text, 3 functions ################################################


def split_subtitle(text, limit=10):
    
    chunks = text.split()
    lines = []
    current_line = []
    current_length = 0

    for chunk in chunks:
        #print(chunk)
        if len(chunk) + current_length <= limit:
            #print('if', current_length, current_line)
            current_length += len(chunk) + 1  # Spaces count as a character
            current_line.append(chunk)
            #print('if', current_length, current_line)
        else:
            #print('else', current_length, current_line)
            lines.append(' '.join(current_line))
            current_line = [chunk]
            current_length = len(chunk)
            #print('else', current_length, current_line)

    #print('lines:', lines)
    lines.append(' '.join(current_line))  # Append the last line
    #print('lines:', lines)
    
    lines = [t for t in lines if len(t)>0]
    midpoint = len(lines) // 2
    #print('midpoint:', midpoint)
    
    return lines[:midpoint], lines[midpoint:]


def split_timecode(start_time, end_time, proportion):

    duration = time_duration(start_time, end_time)
    
    start_time_delta = timedelta(hours=start_time.hours, 
                                  minutes=start_time.minutes, 
                                  seconds=start_time.seconds, 
                                  milliseconds=start_time.milliseconds)
    
    middle_time = start_time_delta + timedelta(seconds=duration * proportion) 
    
    middle_srt = pysrt.SubRipTime(hours=middle_time.seconds // 3600, 
                                  minutes=(middle_time.seconds // 60) % 60, 
                                  seconds=middle_time.seconds % 60, 
                                  milliseconds=middle_time.microseconds // 1000)

    return middle_srt


def adjust_text_len(subs, cut_len=10):
    new_subs = []
    cnt=0
    for sub in subs:
        if len(sub.text) > cut_len:
            #print("adjusting text len: ", sub.text)
            upper_half, lower_half = split_subtitle(sub.text, cut_len)
            #print(' '.join(upper_half))
            #print('---')
            #print(' '.join(lower_half))
            
            upper_half = ' '.join(upper_half)
            lower_half = ' '.join(lower_half)
            
            prop = len(upper_half) / len(sub.text)
            mid_time = split_timecode(sub.start, sub.end, prop)
            cnt += 1
            item = pysrt.SubRipItem(index=cnt,
                                    start=sub.start,
                                    end=mid_time,
                                    text=upper_half)
            new_subs.append(item)
            cnt += 1
            item = pysrt.SubRipItem(index=cnt,
                                    start=mid_time,
                                    end=sub.end,
                                    text=lower_half)
            new_subs.append(item)
        else:
            cnt += 1
            new_subs.append(sub)
    
    return new_subs


