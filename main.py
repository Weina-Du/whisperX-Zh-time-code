import pysrt
from util_Zh import replace_punt
from text_split import adjust_text_len
from format_conv import convert_srt_to_list
from util_En import char_dur_avg, adjust_time_dur
from head_tail_adjust import merge_isolated_head_tail
from file_wordLevel2srt import generate_new_splitUnit_srt
from alignment import align_transcripts_sequence, combine_subs

######################################################################################################
############         main           ############
mainfolder = '/Users/weinadu/Sentient.io/Mediacorp/LLM_ASR-post-processing/asr_drama_Chinese/'
folder1 = mainfolder + 'test_dataset_v2_Oct3/merge_all_initialPrompt/'
srt1_lst = ['merge-ep1-v2.srt',
            'merge-ep2-v2.srt',
            'merge-ep3-v2.srt',
            'merge-episode6-v2.srt',
            'merge-episode7-v2.srt',
            'merge-episode8-v2.srt']
 
folder2 = mainfolder + 'test_dataset_v2_Oct3/non-merge-word-level-time-stamp/'
srt2_lst = ['Mystar_episode_1_nomerge_wordlevel.json',
            'Soul_episode_2_nomerge_world_level.json',
            'Mystar_episode_3_nomerge_wordlevel.json',
            'MyOne_episode_6_nomerge_wordlevel.json',
            'MyOne_episode_7_nomerge_wordlevel.json',
            'MyOne_episode_8_nomerge_wordlevel.json']
 
for i in range(len(srt1_lst)):
    # 1. 1st file, whisperX merge, this should contian most accurate text(missing spaces will borrow from 2nd file)
    file1 = folder1 + srt1_lst[i]
    print(file1)
    lst1 = convert_srt_to_list(folder1 + srt1_lst[i])
    
    # 2. this 2nd file is important, it should contain sufficient information on time stamping. 
    # initially uses './test_dataset_v2_Oct3/unmerge-all_initialPrompt/nomerge-ep2-v2.srt' 
    # but later improved to use
    # whisperX non-merge, word-level time stamps and speakers
    # The path to the JSON-like file with word-level time stamps and speakers
    file2_wl = folder2 + srt2_lst[i]
    print(file2_wl)
 
    new_fl = generate_new_splitUnit_srt(file2_wl)
    lst2 = convert_srt_to_list(new_fl)
    
    # Chinese average time per character,in second
    char_dur = char_dur_avg(file1, new_fl)
    print('avarage time duration per character:', char_dur)
    
    
    # # subs1 = convert_list_to_srt(lst1)
    # # subs2 = convert_list_to_srt(lst2)
    # # print(subs1)
    # # print(subs2)
    timecode_list, text_list = align_transcripts_sequence(lst1, lst2)
    #print(timecode_list)
    
    ### post process of one position punctuation(s) with a single space
    #print(text_list)
    for k, t in enumerate(text_list):
        t = replace_punt(t)
        t = ' '.join(t.split())
        text_list[k] = t
    #print('' in text_list)
    
    ### combine time code list and text list to srt format
    combined = combine_subs(timecode_list, text_list)
    time_length_fix = adjust_time_dur(combined, char_dur)
    text_chop = adjust_text_len(time_length_fix, cut_len=12)
    text_adjusted = merge_isolated_head_tail(input_subs=text_chop, Tavg=char_dur)
    
    ### write output to srt file ###
    
    output_srt = srt2_lst[i].split('_')
    print(output_srt)
    pysrt.SubRipFile(text_adjusted).save('_'.join(srt2_lst[i].split('_')[:3])+'.srt', encoding='utf-8')                                           


