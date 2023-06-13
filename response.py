import pandas as pd
import csv
import io
import json

class Response:
    def __init__(self, data):
        self.data = data
        
    def __str__(self):
        return json.dumps(self.data)
        
    def __repr__(self):
        return json.dumps(self.data)

    def _json_to_xml(self, json_obj, line_padding=""):
        json_obj_type = type(json_obj)
        result = ""

        if json_obj_type is list:
            for sub_elem in json_obj:
                result += self._json_to_xml(sub_elem, line_padding)

        elif json_obj_type is dict:
            for tag_name in json_obj:
                sub_obj = json_obj[tag_name]
                if tag_name.isidentifier(): # Check if valid XML tag name
                    result += f"\n{line_padding}<{tag_name}>"
                    result += self._json_to_xml(sub_obj, "\t" + line_padding)
                    result += f"\n{line_padding}</{tag_name}>"
                else:
                    raise ValueError(f"Invalid XML tag name: {tag_name}")

        else:
            result += escape(str(json_obj)) # Escape special XML characters

        return result

    def xml(self):
        try:
            return self._json_to_xml(self.data)
        except ValueError as e:
            return str(e)
        
    def csv(self):
        df2 = None
        if 'top_items' in self.data:
            df = pd.json_normalize(self.data['top_items'])
        elif 'logs' in self.data and 'aggregates' not in self.data:
            df = pd.json_normalize(self.data['logs'])
        elif 'reports' in self.data:
            df = pd.json_normalize(self.data['reports'])
        elif 'aggregates' and 'logs' in self.data:
            df = pd.json_normalize(self.data['aggregates'])
            df2 = pd.json_normalize(self.data['logs'])
        else:
            df = pd.read_json(self.data)
            
        if df2 is not None:
            return [df.to_csv(), df2.to_csv()]
        else:
            return df.to_csv()