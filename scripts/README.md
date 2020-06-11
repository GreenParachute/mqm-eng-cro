### Instructions on how to use the scripts to extract annotations and calculate Inter-Annotator Agreement

These scripts conduct the statistical analysis on the MQM output.

Note: This is the original code that was written back in 2017 in Python 2.7. 
If you'd prefer to work with a more streamlined and up-to-date version of the code, Yuying Ye has been kind enough to do some refactoring. I wholeheartedly recommend checking out [this GitHub repository](https://github.com/yy-ye/mqm-analysis) for scripts that work with Python 3.* and make it easier to run. (Plus, it also contains annotation data for English-Chinese!)

## Running the code:

1. For starters you need the annotated .csv file exported from translate5 (e.g. "m3-fm.en-hr.translate5_rnd_wquote.csv")

2. Add the path to this file to the script prepare_MQM_output.py (line 13) and run it. The script essentially just gives it additional tags to make it a proper .xml file. (Make sure to also change the path in line 51, to wherever you want to output the new .xml file.)

3. Then parse the output of that script - i.e. the new .xml file - with the script parse_MQM_system.py (use the .data output from step 2. as standard input).

4. Finally, feed the parsed output to the script extract_MQM_stats.py, and voila, you know how many tokens you have, and how many tokens have which error on them. 
Note that this script uses a Croatian tokeniser which is not included in this repo. If you require tokenisation for Croatian, we suggest the [ReLDI](https://github.com/clarinsi/reldi-tokeniser) tokenizer. In case you are using a different language, consider using an appropriate tokeniser, just in case.

5. For IAA (Inter Annotator Agreement), after parsing everything following the above steps,
run  extract_MQM_sent_IAA_stats.py. This script requires as input two \*.parsed files (output fo step 3.) - define their paths within the script (line 73-74).
(Also note that MQM error categories have been hard-coded here, so make sure to double check that all the MQM error categories you're using are actually in the script (e.g. lines 80-83, and then everything from 121-143))