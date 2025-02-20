import csv
import xml.etree.ElementTree as ET
from pprint import pprint

def read_csv():
    names = ['name', 'subname', 'foo', 'bar', 'sub-name', 'result', 'date']
    with open('./sample.csv') as f:
        reader = csv.DictReader(f, names)
        data = [row for row in reader]
    return data
        
def csv2junit(data):
    root = ET.Element('testsuits')
    
    for d in data:
        if (d['name'] != ''):
            major = d['name']
            suite = ET.SubElement(root, 'testsuit')
            suite.set('name', major)
            
        
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
    
    ET.indent(root)
    ET.dump(root)



csv2junit(read_csv())
