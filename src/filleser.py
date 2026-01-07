
import json

class Filleser:

    @staticmethod
    def json(filnavn):
        streng = ""
        with open(filnavn + '.json', encoding='utf-8') as fil:
            for linje in fil:
                streng += linje.strip()
        return json.loads(streng)
