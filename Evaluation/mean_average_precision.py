import subprocess
import gzip
import numpy as np
import sys

def get_average_precision(relevant_documents, retrieved_documents):
    precisions = []
    nr_relevant_retrieved = 0
    nr_nonrelevant_retrieved = 0
    for item in retrieved_documents:
        if item not in relevant_documents:
            nr_nonrelevant_retrieved += 1
        else:
            nr_relevant_retrieved += 1
            precisions.append(nr_relevant_retrieved/(nr_relevant_retrieved + nr_nonrelevant_retrieved))
    #add a 0 for each relevant document that was not retrieved
    for i in range(len(relevant_documents)-nr_relevant_retrieved):
        precisions.append(0)
        
    return np.round(np.array(precisions).mean(), 2)

def get_mean_average_precision(result_file, qrels_directory):

    results_dict = {}
    all_average_precisions = []
    # get all retrieved documents for each query
    with open(result_file, 'r') as f:
        for line in f:
            data = line.split()
            if data[0] not in results_dict:
                results_dict[data[0]] = [data[2]]
            else:
                results_dict[data[0]].append(data[2])

    for key in results_dict:
        filepath = subprocess.check_output("find " + qrels_directory + "/N" + str(key) + ".txt.gz", shell=True)
        filepath = filepath.decode("utf-8")
        filepath = filepath.strip()
        a_file = gzip.open(filepath, "rb")
        contents = a_file.read().decode('utf-8')
        rel_info = contents.split('\n')[:-1] #Get rid of the empty string at the last position
        docs = [item.split('\t')[0] for item in rel_info]
        judgements = [int(item.split('\t')[1]) for item in rel_info]
        relevant_documents = [doc for i, doc in enumerate(docs) if judgements[i] > 0]
        all_average_precisions.append(get_average_precision(relevant_documents, results_dict[key]))

    mean_avg_precision = np.round(np.array(all_average_precisions).mean(),2)
    print(mean_avg_precision)
    return mean_avg_precision


if __name__ == "__main__":

    result_file = sys.argv[1]
    qrels_directory = sys.argv[2]

    get_mean_average_precision(result_file, qrels_directory)

