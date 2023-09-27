import json
import pandas as pd
import xmltodict as xmltd
from typing import Any, Union, List

class Response:
    def __init__(self, data: Any):
        self.data = data
        
    def __json__(self):
        return self.data

    def __str__(self) -> str:
        return json.dumps(self.__json__())

    def __repr__(self) -> str:
        return self.__str__()
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get an element from the serialized JSON data"""
        return self.data.get(key, default)

    def raw(self) -> Any:
        """Return the raw data"""
        return self.data

    def xml(self) -> str:
        try:
            return xmltd.unparse({'response': self.data})
        except ValueError as e:
            return str(e)

    def csv(self) -> Union[str, List[str]]:
        df2 = None
        if 'top_items' in self.data:
            df = pd.json_normalize(self.data['top_items'])
        elif 'logs' in self.data and 'aggregates' not in self.data:
            df = pd.json_normalize(self.data['logs'])
        elif 'reports' in self.data:
            df = pd.json_normalize(self.data['reports'])
        elif 'aggregates' in self.data and 'logs' in self.data:
            df = pd.json_normalize(self.data['aggregates'])
            df2 = pd.json_normalize(self.data['logs'])
        else:
            df = pd.json_normalize(self.data)
            
        if df2 is not None:
            return [df.to_csv(), df2.to_csv()]
        else:
            return df.to_csv()