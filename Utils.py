'''
Created on Aug 1, 2016

@author: Matt
'''
import json

def pp_json(input_json):
    print ( json.dumps(input_json, indent=4) )