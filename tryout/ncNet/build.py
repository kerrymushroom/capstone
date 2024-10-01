from bs4 import BeautifulSoup
import os
import json
import ast # tranform string to dict

def read_with_soup(file_path):
    # Read HTML file
    with open(file_path, 'r',encoding='utf-8') as f:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(f, 'html.parser')
    return soup


# Get NL query questions 
def get_query(file_path):
    list = html_read.find_all('tr')[1].find_all('td')[1].ol.find_all('p') 
    for i in range(len(list)):
        list[i] = list[i].get_text()
    return list

# Build an informative dict, output as a tuple for json
def build_dict(file_path):
    temp = {}
    global html_read 
    html_read = read_with_soup(file_path)
    html_id = html_read.find_all('tr')[1].find_all('td')[0].get_text() 
    temp.update({"html_name":os.path.basename(file_path)})  
    temp.update({"description_id":html_read.find_all('tr')[1].find_all('td')[3].find_all('p')[0].find('b').next_sibling.strip()})  
    temp.update({"hardness":html_read.find_all('tr')[1].find_all('td')[3].find_all('p')[1].find('b').next_sibling.strip()})  
    temp.update({"chart_type":html_read.find_all('tr')[1].find_all('td')[3].find_all('p')[2].find('b').next_sibling.strip()})  
    temp.update({"db_id":html_read.find_all('tr')[1].find_all('td')[3].find_all('p')[3].find('b').next_sibling.strip()})  
    temp.update({"table_name":html_read.find_all('h4',style='margin-left:5%')[0].get_text().split(':')[2].strip()}) 
    temp.update({"query_list":get_query(file_path)})
    temp.update({"vega_obj":ast.literal_eval(html_read.find_all('script')[3].get_text().split(';')[0].replace("var vlSpec1  =", "").strip())}) 
    return (html_id,temp)

