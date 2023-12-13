import pysrt
########################################################################
############   method to convert SubRipFile to list of dictionaries.

def convert_srt_to_list(file):
    subs = pysrt.open(file)
    subs_list = []

    for sub in subs:
        subs_list.append(
            {
                'start': sub.start.ordinal/1000,  # converting milliseconds to seconds
                'end': sub.end.ordinal/1000,  # converting milliseconds to seconds
                'text': sub.text
            }
        )

    return subs_list


# method to convert list of dictionaries to SubRipFile and save it.
def convert_list_to_srt(subs_list):

    subs = pysrt.SubRipFile()
    for index, sub_dict in enumerate(subs_list, start=1):

        # converting seconds to 'hours:minutes:seconds,milliseconds'
        start_time = convert_seconds_to_srttime(sub_dict['start'])
        end_time = convert_seconds_to_srttime(sub_dict['end'])

        sub = pysrt.SubRipItem(index, start_time, end_time, sub_dict['text'])
        subs.append(sub)

    return subs
    
# method to convert seconds to pysrt.SubRipTime format
def convert_seconds_to_srttime(seconds):
    msec = int((seconds % 1) * 1000)
    seconds = int(seconds)

    hrs, remainder = divmod(seconds, 3600)
    mins, secs = divmod(remainder, 60)

    return pysrt.SubRipTime(hours=hrs, minutes=mins, seconds=secs, milliseconds=msec)



