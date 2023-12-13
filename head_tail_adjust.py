import pysrt
import jieba
from util_En import time_compute_with_format
# This cell perfects the text by:  
# Handle isolated last character from the previous unit
# and
# Handle isolated first character for the next unit

def head_should_merge_with_previous(sub1_text, sub2_text):
    combined_text = sub1_text + sub2_text
    cut_list = list(jieba.cut(combined_text, cut_all=False))
    # Return True if the first character of sub2 should merge with sub1
    return cut_list[-1] != sub2_text

def tail_should_merge_with_next(sub1_text, sub2_text):
    combined_text = sub1_text + sub2_text
    cut_list = list(jieba.cut(combined_text, cut_all=False))
    return cut_list[0] != sub1_text[-1]

def merge_isolated_head_tail(input_subs, Tavg):
    # Assuming timecode_list and text_list are defined:
    raw_timecode_list = [(s.start, s.end) for s in input_subs]
    raw_text_list = [s.text for s in input_subs]
    
    # Remove empty strings from text_list and their corresponding timecodes from timecode_list
    filtered_pairs = [(timecode, text) for timecode, text in zip(raw_timecode_list, raw_text_list) if text]
    timecode_list, text_list = zip(*filtered_pairs)  # Unzip pairs into filtered lists
    timecode_list = list([list(t) for t in timecode_list])
    text_list = list(text_list)
    
    
    subs = []
    cnt = 0 
    
    for index in range(len(text_list)):
        
        current_text = text_list[index]
        #print(current_text, len(current_text))
        
        if len(current_text)>0:
            
            this_start_time = timecode_list[index][0]
            this_end_time = timecode_list[index][1]
            
            # Handle isolated last character from the previous unit
            if (index > 0 and subs and timecode_list[index][0] == timecode_list[index - 1][1] and
                    not current_text[0].isspace() and (subs[-1].text[-2].isspace() if 
                                                       len(subs[-1].text)>=2 else True) and
                    tail_should_merge_with_next(subs[-1].text[-1], current_text)):
                
                #print('adjust: ', subs[-1].text, ',', current_text)
                current_text = subs[-1].text[-1] + current_text
                subs[-1].text = subs[-1].text[:-2] # -2 is space, -1 is the character merged with next text unit
                
                #print('start time accordingly: ')
                #print(this_start_time)
                this_start_time = time_compute_with_format(timecode_list[index][0], -Tavg)
                subs[-1].end = this_start_time
                #print(this_start_time, '\n')
                
            # Handle isolated first character for the next unit
            if (index < len(text_list) - 1 and timecode_list[index][1] == timecode_list[index + 1][0] and
                    not current_text[-1].isspace() and (text_list[index + 1][1].isspace() if 
                                                        len(text_list[index + 1])>=2 else True) and
                    head_should_merge_with_previous(current_text, text_list[index + 1][:1])):
                
                #print('adjust: ', current_text, ',', text_list[index + 1])
                current_text = current_text + text_list[index + 1][0]
                text_list[index + 1] = text_list[index + 1][2:] # 0  is merged with last unit, 1 is space
                
                #print('end time accordingly: ')
                #print(this_end_time)
                this_end_time = time_compute_with_format(timecode_list[index][1], Tavg)
                timecode_list[index + 1][0] = this_end_time
                #print(this_end_time, '\n')
            
            subs.append(pysrt.SubRipItem(
            index=cnt + 1,
            start=this_start_time,
            end=this_end_time,
            text=current_text
            ))
            
            cnt += 1
    
    return subs


