Before you can run this script at all, you'll need to download python from here https://www.python.org/downloads/
I have version 3.9.0, so get that version just in case, should be the latest.

Rules:
- Spreadsheet csv files must be the name you want shown in the results and can only be one word.
- Overall or N/A must be the last song for each artist (to handle the overall scores and comments, or N/A if not needed)

To use the script. You will need to download Overall, Comments, Averages, and Compatibility sheets as CSV files.
In google sheets, just go to File -> Download As -> Comma-seperated values (.csv)
You have to do this individually for each sheet.
Make sure each file is named accordingly (Overall.csv, Comments.csv, Averages.csv, Compatibility.csv)

Then put these 4 files in the same folder as the python script (and this README)

Commands to run program:
- cd "LOCATION_OF_SCRIPT" (this will take you to the script location in command line)
- python Song_Rating_Parser.py

After hitting enter, there should be a "Results.txt" file that contains everything you need!