from datetime import timedelta

def unit_split(asr_output):

    # Initialize an empty list that will hold the broken-down units
    units = []
    
    # Initialize a dictionary to hold the current unit's information
    current_unit = {
        'start': None,
        'end': None,
        'text': '',
        'words': [],
        'speaker': None
    }
    
    # Keep track of the last known start and end times
    last_start = None
    last_end = None
    
    # Iterate through each word in the ASR output
    for word_info in asr_output['words']:
        # Check if 'start' key exists and update last known start time
        if 'start' in word_info:
            last_start = word_info['start']
        
        # Check if 'end' key exists and update last known end time
        if 'end' in word_info:
            last_end = word_info['end']
    
        # If the word info represents a punctuation mark, we skip changing speaker or timestamps
        if 'start' not in word_info and 'end' not in word_info:
            # Just append the punctuation mark to the current text
            current_unit['text'] += word_info['word']
            continue
        
        # Check if a new unit should start (when there's a speaker change or if current_unit is empty)
        if current_unit['speaker'] != word_info.get('speaker', current_unit['speaker']) or not current_unit['words']:
            if current_unit['words']:
                # Append the previous unit to the list and start a new unit
                units.append(current_unit)
                current_unit = {'start': last_start, 'end': None, 'text': '', 'words': [], 'speaker': None}
        
            current_unit['start'] = last_start
            current_unit['speaker'] = word_info.get('speaker', current_unit['speaker'])
        
        # Populate the unit with data
        current_unit['text'] += word_info['word']
        current_unit['words'].append(word_info)
        # Use last known end time if 'end' is not present in word_info
        current_unit['end'] = last_end
        
    
    # Append the last unit if it contains any words
    if current_unit['words']:
        units.append(current_unit)
    
#     # Now `units` contains all the multiple units based on word-level timestamps and speaker changes
#     for i, unit in enumerate(units):
#         print(f"Unit {i+1}:")
#         print(f" Start: {unit['start']}")
#         print(f" End: {unit['end']}")
#         print(f" Text: {unit['text']}")
#         print(f" Speaker: {unit['speaker']}\n")
#     
    
    # The list `units` now holds all the broken-down units
    return units


def format_timestamp(ts):
    """Converts a float timestamp in seconds to SRT timestamp format"""
    srt_time = timedelta(seconds=ts)
    srt_str = str(srt_time)
    # Convert to HH:MM:SS,mmm format
    if '.' in srt_str:
        main, milli = srt_str.split('.')
        return f"{main},{milli[:3]}"
    else:
        return f"{srt_str},000"


def convert_to_srt(units):
    srt_output = ""
    
    for i, unit in enumerate(units):
        start_time = format_timestamp(unit['start'])
        end_time = format_timestamp(unit['end'])
        text = unit['text']

        # SRT entries are separated by a blank line
        srt_output += f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n"
    
    return srt_output    


def generate_new_splitUnit_srt(file_path):

    import ast
    
    # Open the file and read its contents
    with open(file_path, 'r') as file:
        # Convert single quotes to double quotes
        file_content = file.read().replace("'", '"')
        # Safely evaluate the modified string
        data = ast.literal_eval(file_content)
    
    data = data['segments']
    # Now 'data' should be a Python list of dictionaries
    units = []
    for item in data:
        #print(item)  # Prints each item in the list
        #print(unit_split(item))
        units.extend(unit_split(item))
        #print('\n\n')
        
        
    # Call the function with units data
    srt_data = convert_to_srt(units)
    
    # Output SRT data to a file
    srt_gen = '.'.join(file_path.split('.')[:-1])+'-split-units.srt'
    with open(srt_gen, 'w', encoding='utf-8') as f:
        f.write(srt_data)
    
    # Print the SRT formatted data
    #print(srt_data)
    return srt_gen
