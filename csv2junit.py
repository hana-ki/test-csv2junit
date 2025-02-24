import argparse
import csv
import glob
import xml.etree.ElementTree as ET
from pprint import pprint


def read_csv(files):    
    names = ['name', 'subname', 'foo', 'bar', 'sub-name', 'result', 'date']
    data = []
    for file in files:
        pprint(f"{file}----------------")
        with open(file) as f:
            reader = csv.DictReader(f, names)
            data.append([row for row in reader])
    return data
        
def csv2junit(dataset):
    for data in dataset:
        
        root = ET.Element('testsuites')    
        for d in data:
            if (d['name'] != ''):
                major = d['name']
                suite = ET.SubElement(root, 'testsuite')
                
            if (d['subname'] != ''):
                minor = d['subname']
                subsuite = ET.SubElement(suite, 'testsuite')
                subsuite.set('classname', f'{major}.{minor}')
                
            case = ET.SubElement(subsuite, 'testcase')
            kind = d['foo']
            case.set('name', d['bar'])
            case.set('classname', f'{major}.{minor}.{kind}')
            
            if (d['result'] == 'NG'):
                ET.SubElement(case, 'failure', type='AssertionError')
        
        print('+'*20)
        ET.indent(root)
        ET.dump(root)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CSV to JUnit XML format')
    parser.add_argument('csv_path', type=str, nargs='+', help='Path to the input CSV file')
    args = parser.parse_args()
    
    pprint(args)

    data = read_csv(args.csv_path)
    csv2junit(data)

