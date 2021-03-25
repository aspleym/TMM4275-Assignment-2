import os
import requests
import json


def generateTrajectory(tName):
    headers = {
        'Accept': 'application/sparql-results+json,*/*;q=0.9',
    }

    prefix = 'PREFIX kbe:<http://www.my-kbe.com/shapes.owl#>\n  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n  PREFIX owl: <http://www.w3.org/2002/07/owl#>\n  SELECT *\n  WHERE\n  {\n  ?trajectory a kbe:Trajectory.\n  ?trajectory kbe:Points ?point.\n  ?point kbe:index ?index.\n    ?point kbe:x ?x.\n    ?point kbe:y ?y.   \n    FILTER(?trajectory = kbe:'
    postfix = ').\n}'
    data = {
    'query': prefix + tName + postfix
    }

    response = requests.post('http://127.0.0.1:3030/kbe', headers=headers, data=data)
    data = response.json()

    points = ""

    for point in data['results']['bindings']:
        x = int(point['x']['value'])
        y = int(point['y']['value'])
        index = int(point['index']['value'])

        points = points + f'Point({x}, {y}, 0),\n'

    points = points.removesuffix(",\n")

    print(points)
    
    script_dir = os.path.dirname(__file__)
    rel_path_template = "DFA/TrajectoryTemplate.dfa"
    abs_file_path_template = os.path.join(
        script_dir[:len(script_dir) - 6], rel_path_template)

    f = open(abs_file_path_template, "r")
    txt = f.read()

    # Replacement section for parameters in the template file
    txt = txt.replace("<T_NAME>", tName)

    txt = txt.replace("<POINTS>", points)

    rel_path_product = f'DFA/products/{tName}.dfa'
    abs_file_path_product = os.path.join(
        script_dir[:len(script_dir) - 6], rel_path_product)

    f = open(abs_file_path_product, "w")
    f.write(txt)
    f.close()