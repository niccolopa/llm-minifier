import json
import re

def minify_key(key):
    if not isinstance(key, str) or len(key) <= 2:
        return key
    first_char = key[0]
    rest_of_word = key[1:]
    minified_rest = re.sub(r'[aeiouAEIOU_]', '', rest_of_word)
    return first_char + minified_rest

def compress_payload(data, key_map=None):
    if key_map is None:
        key_map = {}

    if isinstance(data, dict):
        minified_dict = {}
        for k, v in data.items():
            mk = minify_key(k)
            while mk in minified_dict and key_map.get(mk) != k:
                mk += "x"
            key_map[mk] = k

            valore_compresso, key_map = compress_payload(v, key_map)
            minified_dict[mk] = valore_compresso
            
        return minified_dict, key_map

    if isinstance(data, list):
        processed_list = []
        for item in data:
            item_compresso, key_map = compress_payload(item, key_map)
            processed_list.append(item_compresso)
            
        return processed_list, key_map

    return data, key_map

def decompress_payload(minified_data, key_map):
    if isinstance(minified_data, dict):
        restored_dict = {}
        for mk, v in minified_data.items():
            original_key = key_map.get(mk, mk)
            restored_dict[original_key] = decompress_payload(v, key_map)
        return restored_dict
        
    if isinstance(minified_data, list):
         return [decompress_payload(item, key_map) for item in minified_data]
         
    return minified_data