Running the code:


1) Creating the query parameter file:

$ python create_50_queries.py <topics_path> <mapping_file> <index_folder> <file_to_write>

For example:

$ python create_50_queries.py /local/course/ir/data/MedEvalTK/Topics/MedTopics.txt /local/course/ir/lab3/mapping_qrels_topics.txt /tmp/my_index_folder my_50_queries.xml

2) Precision at k

$ python precision_at_k.py <result_file> <qrels_folder> <file_to_write> (<k>)

If no k is specified, k defaults to 10.

For example:

$ python precision_at_k.py my_results_with_index1.txt /local/course/ir/data/MedEvalTK/None precision_at_k_results.txt

3) MAP

$ python mean_average_precision.py <result_file> <qrels_folder>

For example:

$ python mean_average_precision.py my_results_with_index1.txt /local/course/ir/data/MedEvalTK/None