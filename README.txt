Before you can run this script at all, you'll need to download python from here https://www.python.org/downloads/
I have version 3.9.0, so get that version just in case, should be the latest.

To use the script. You will need to download each raters rating sheet as CSV files.
In google sheets, just go to File -> Download As -> Comma-seperated values (.csv)
Make sure each file is named the name of the rater and is only one word (for example, my score sheet should be named "Nate.csv"
Then put these files in a folder named "Rating" that must be in the same folder as the python script (and this README)

Rules:
- Spreadsheet csv files must be the name you want shown in the results and can only be one word.
- Overall or N/A must be the last song for each artist (to handle the overall artist scores and comments, or N/A if not needed)
- Column order must be Artist Name, Song Name, Score, Comment
- Script must be in the same folder as a folder named "Rating" containing all of the different raters sheets

Commands to run program:
- cd "LOCATION_OF_SCRIPT" (this will take you to the script location in command line)
- python Song_Rating_Parser.py

After hitting enter, there should be a "Results.txt" file that contains everything you need!