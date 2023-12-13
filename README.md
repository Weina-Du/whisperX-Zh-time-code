# whisperX-Zh-time-code
STEP 1. prepare all srt files
for each audio, there should be two files
1. whipserX merge srt file. All srt file paths shall form a list.
2. whisperX non-merge word level time stamp and speakers. Form a list as before(json but not srt format).

STEP 2. post process of srt + json file to generate the best time code srt.
```python main.py```
