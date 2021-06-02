
Running the code (preferably from your home folder):
$ python lab2_wrapper.py path_to_data_tar_file corpus_class field_to_use path_to_assessment_file

You will be asked to enter the number of your task and your query, separated by a comma, for example: 304,unesco
The evaluation table is then printed out after which you can enter a new task + query combination if you wish.
If you are done, type 'exit' after which all created files and folders will be deleted.


Example with the GH95 data:
$ python lab2_wrapper.py /local/course/ir/data/adhoc-news/data/collections/English_data/GlasgowHerald95.tgz trectext p /local/course/ir/data/adhoc-news/assessments/assessments2006/AH-ENGLISH-CLEF2006.txt