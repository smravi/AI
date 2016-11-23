import sys

import Assignment_3.inference.parse as parse
import Assignment_3.inference.fol_resolution as resolution
import Assignment_3.inference.cnf as cnf

def write_file(data, fileName):
    with open(fileName, 'w') as fw:
        for val in data:
            fw.write(str(val))
            fw.write('\n')
        fw.truncate(fw.tell() - 1)


def main(input, output):
    inputSpec = []
    with open(input, 'r') as file:
        for line in file:
            inputSpec.append(line)
    if len(inputSpec) > 0:
        queryCount = int(inputSpec[0])
        queries = []
        for i in range(1, queryCount + 1):
            queries.append(inputSpec[i])
        kbCount = int(inputSpec[queryCount + 1])
        kbStart = queryCount + 1
        kb = []
        for i in range(kbStart + 1, kbStart + 1 + kbCount):
            kb.append(inputSpec[i])
    if len(kb) > 0 and len(queries) > 0:
        resolve_result = process_clauses(kb, queries)
        print((resolve_result))
        write_file(resolve_result, output)


def process_clauses(kb, queries):
    resolve_result = []
    # convert the Kb to cnf
    cnf_list = []
    for item in kb:
        cnf_list.extend(cnf.convert_with_and(cnf.get_cnf_sentence(item)))
    for q in queries:
        resolve_result.append(resolution.fol_resolution_corrected(cnf_list, parse.parse_sentence(q)))
    return resolve_result


if __name__ == '__main__':
    print(sys.getrecursionlimit())
    main('input/input0.txt', 'output/output0.txt')
