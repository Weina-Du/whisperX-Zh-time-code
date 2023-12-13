import pysrt
from datetime import datetime, timedelta
### generac functions, not language specific ###


def str_idxing(input_list, input_string):
    # Dropped duplicates and preserve orders.
    numbers = list(dict.fromkeys(input_list))
    
    output = []
    start = 0
    for number in numbers:
        chunk_size = input_list.count(number)
        output.append((number, input_string[start:start + chunk_size]))
        start += chunk_size
        
    #for item in output:
    #    print(f"Number {item[0]} associates with string chunk '{item[1]}'")
        
    return output


    
def time_duration(startsub, endsub):

    start_time = timedelta(hours=startsub.hours, 
                           minutes=startsub.minutes, 
                           seconds=startsub.seconds, 
                           milliseconds=startsub.milliseconds)
    end_time = timedelta(hours=endsub.hours, 
                         minutes=endsub.minutes, 
                         seconds=endsub.seconds, 
                         milliseconds=endsub.milliseconds)

    duration = end_time - start_time
    total_duration = duration.total_seconds()
    #print(end_time, start_time, duration)
    
    return total_duration



def char_dur_avg(file1, file2):
    subs1 = pysrt.open(file1)
    subs2 = pysrt.open(file2)

    # Create combined texts
    combined_text1 = " ".join([s.text for s in subs1])
    combined_text2 = " ".join([s.text for s in subs2])

    time_dur1 = time_duration(subs1[0].start, subs1[-1].end)
    time_dur2 = time_duration(subs2[0].start, subs2[-1].end)
    #print('total time duration: ',time_dur1, '\ntotal text length: ', len(combined_text1))
    char_dur1 = time_dur1/len(combined_text1)
    char_dur2 = time_dur2/len(combined_text2)
    #print(char_dur1, char_dur2)
    
    return (char_dur1 + char_dur2)/2
    
    
    
def adjust_time_dur(subs, Tavg):
    
    for sub in subs:
        
        Tdur = time_duration(sub.start, sub.end)
        
        # time duration is more than 2 times of common sense
        if Tdur > 2*len(sub.text)*Tavg: 
            #print('\nOriginal', sub.index, sub.start, sub.end, sub.text)
            # sub.end and duration Tavg are known
            # Convert sub.end to standard datetime timedelta
            sub_end_timedelta = timedelta(hours=sub.end.hours, 
                                          minutes=sub.end.minutes, 
                                          seconds=sub.end.seconds, 
                                          milliseconds=sub.end.milliseconds)
            
            # Calculate sub.start
            # give 120% of the common sense length
            sub_start_timedelta = sub_end_timedelta - timedelta(seconds=len(sub.text)*Tavg*1.2) 
            #print(sub_start_timedelta, timedelta(seconds=Tdur), sub_end_timedelta)
            # Convert back to pysrt.SubRipTime format
            sub.start = pysrt.SubRipTime(hours=sub_start_timedelta.seconds // 3600, 
                                         minutes=(sub_start_timedelta.seconds // 60) % 60, 
                                         seconds=sub_start_timedelta.seconds % 60, 
                                         milliseconds=sub_start_timedelta.microseconds // 1000)
            #print('Revised:', sub.index, sub.start, sub.end, sub.text)
            
    return subs
    
    
def time_compute_with_format(subtime, Tdelta):
    sub_timedelta = timedelta(hours = subtime.hours, 
                                  minutes=subtime.minutes, 
                                  seconds=subtime.seconds, 
                                  milliseconds=subtime.milliseconds)
    new_subtime = sub_timedelta + timedelta(seconds=Tdelta)
    
    return pysrt.SubRipTime(hours=new_subtime.seconds // 3600, 
                            minutes=(new_subtime.seconds // 60) % 60, 
                            seconds=new_subtime.seconds % 60, 
                            milliseconds=new_subtime.microseconds // 1000)


