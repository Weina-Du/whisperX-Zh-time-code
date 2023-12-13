import re
import pysrt
import difflib
from util_En import str_idxing
from util_Zh import replace_space
from format_conv import convert_list_to_srt

def is_punctuation(ch):
    return bool(re.match(r'[^\w\s]', ch, re.UNICODE))

def update_sequence_text_pos(sequence1,sequence2,seq1_positions,seq2_positions,sdiff):
    # Updated sequence and position list
    updated_sequence1 = ""
    updated_seq1_positions = []
    
    
    # Process the diff output and update sequence 1 and its position list
    for df in sdiff.get_opcodes():
        action, start1, end1, start2, end2 = df
        
        #print(f"{action} a[{start1}:{end1}] ('{sequence1[start1:end1]}')"
        #      f" b[{start2}:{end2}] ('{sequence2[start2:end2]}')")
        
        if action == 'equal':
            updated_sequence1 += sequence1[start1:end1]
            updated_seq1_positions.extend(seq2_positions[start2:end2])
            #print(sequence1[start1:end1], seq2_positions[start2:end2])
    
        elif action == 'replace':
            updated_seq1_text = sequence1[start1:end1]
            updated_seq1_post = (seq2_positions[start2:start2+1])*(end1-start1)
            # Include punctuation from sequence 2
            if is_punctuation(sequence2[start2:start2+1]):
                
                if not is_punctuation(sequence1[start1:start1+1]):
                    updated_seq1_text = sequence2[start2:start2+1] + updated_seq1_text
                    
                updated_seq1_post = seq2_positions[start2:start2+1]+\
                                    seq2_positions[end2-1:end2]*(len(updated_seq1_text)-1)
                    
            if is_punctuation(sequence2[end2-1:end2]):
                
                if not is_punctuation(sequence1[end1-1:end1]):
                    updated_seq1_text = updated_seq1_text + sequence2[end2-1:end2]
                
                updated_seq1_post = updated_seq1_post+\
                                    seq2_positions[end2-1:end2]*(len(updated_seq1_text)-len(updated_seq1_post))
            
            #print(updated_seq1_text, updated_seq1_post)
            # Update the sequence 1 text
            updated_sequence1 += updated_seq1_text
    
            # Update the positions for the replaced text
            updated_seq1_positions.extend(updated_seq1_post)
    
    
        elif action == 'insert':
            insert_text = sequence2[start2:end2]
    
            # Include punctuation from sequence 2
            updated_sequence1 += insert_text
            updated_seq1_positions.extend(seq2_positions[start2:end2])
            #print(insert_text, seq2_positions[start2:end2])
    # Output the resulting text and position list for sequence 1
    #print("Updated Sequence 1:", updated_sequence1)
    #print("Updated Positions:", updated_seq1_positions)
    
    return updated_sequence1, updated_seq1_positions


def align_transcripts_sequence(lst1, lst2):
    
    subs1 = convert_list_to_srt(lst1)
    subs2 = convert_list_to_srt(lst2)
    
    # Create a list of tuples for the 1st text
    s1_index = []
    combined_text1 = ''
    for i, s in enumerate(subs1):
        subs1[i].text = replace_space(s.text)
        combined_text1 += subs1[i].text + '。'
        s1_index.extend([i]*(len(subs1[i].text)+1))
    s1_index = s1_index[:-1]
    combined_text1 = combined_text1[:-1]
    assert len(s1_index) == len(combined_text1)
    
    # Create a list of tuples for the 2nd text
    s2_index = []
    combined_text2 = ''
    for i, s in enumerate(subs2):
        subs2[i].text = replace_space(s.text)
        combined_text2 += subs2[i].text + '。'
        s2_index.extend([i]*(len(subs2[i].text)+1))
    s2_index = s2_index[:-1]
    combined_text2 = combined_text2[:-1]
    assert len(s2_index) == len(combined_text2)
    
    s = difflib.SequenceMatcher(None, combined_text1, combined_text2)
    
    # To see the ratio of similarities, use ratio()
    similarity_ratio = s.ratio()
    print(f"Similarity Ratio: {similarity_ratio:.2f}")

    seq, pos = update_sequence_text_pos(combined_text1, combined_text2, s1_index, s2_index, s)
            
    out_list = str_idxing(pos, seq)
    
    # Create an empty subtitle variable
    aligned_subs = pysrt.SubRipFile()
    
    timecode_lst = []
    text_lst = []
    for i, out in enumerate(out_list):

        if out[0] >= 0:
            aligned_sub = subs2[out[0]]
        else:
            aligned_sub = subs1[abs(out[0])]
        text_lst.append(out[1])
        timecode_lst.append((aligned_sub.start, aligned_sub.end))
        # Create a new aligned subtitle item
        cnt = len(aligned_subs)
        item = pysrt.SubRipItem(index=cnt+1,
                                start=aligned_sub.start,
                                end=aligned_sub.end,
                                text=out[1])
       
        #print(f'final chunk {item.index} :', out[0], item.start, item.end, item.text)
        aligned_subs.append(item)

    return timecode_lst, text_lst

def combine_subs(timecode_list, text_list):
    
    # Create subtitle units from timecodes and texts
    subs = [pysrt.SubRipItem(index=index, 
                             start=timecode[0], 
                             end=timecode[1], 
                             text=text) for index, (timecode, text) in enumerate(zip(timecode_list, text_list), 
                                                                                 start=1)]
    

    return subs


