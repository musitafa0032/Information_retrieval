import subprocess
import sys
import gzip


def get_precision_at_k(result_file, qrels_directory, file_to_write, k=10):

    results_dict = {} # save information about retrieved documents
    precision_dict = {} # save the precision at k for each query
    with open(result_file, 'r') as f:
        for line in f:
            data = line.split()
            # data[0] is the topic and data[2] the retrieved document
            if data[0] not in results_dict:
                results_dict[data[0]] = [data[2]]
            else:
                results_dict[data[0]].append(data[2])
    
    # for each topic, open the qrel file and save information about assessed documents
    for key in results_dict:
        filepath = subprocess.check_output("find " + qrels_directory + "/N" + str(key) + ".txt.gz", shell=True)
        filepath = filepath.decode("utf-8")
        filepath = filepath.strip()
        a_file = gzip.open(filepath, "rb")
        contents = a_file.read().decode('utf-8')
        rel_info = contents.split('\n')[:-1] #Get rid of the empty string at the last position
        docs = [item.split('\t')[0] for item in rel_info]
        judgements = [int(item.split('\t')[1]) for item in rel_info]

        to_check = results_dict[key][:k]
        relevant_docs = 0
        for doc in to_check:
            if doc in docs and judgements[docs.index(doc)] > 0:
                relevant_docs += 1
        precision_dict[key] = relevant_docs/k

    with open(file_to_write, 'w', encoding='utf-8') as f:
        print('Topic', 'Precision at ' + str(k), file=f)
        for key, value in precision_dict.items():
            print(str(key) + '\t' + str(value), file=f)


if __name__ == "__main__":

    result_file = sys.argv[1]
    qrels_directory = sys.argv[2]
    file_to_write = sys.argv[3]
    
    if len(sys.argv) == 5:
        k = int(sys.argv[4])
        get_precision_at_k(result_file, qrels_directory, file_to_write, k=k)
    else:
        get_precision_at_k(result_file, qrels_directory, file_to_write)
    
