import json
import random
from config.config import cfg


class JSON_Mngr:

    # class members
    json_data = None
    categories = []
    json_data_categorized = {}

    ## load json file
    def load_data( self ):
        file_path = cfg['JSON_FILE_PATH']
        try:
            with open(file_path) as json_file:
                self.json_data = json.load(json_file)
        except FileNotFoundError:
            print ('json file not found : "%s"' % file_path)
            exit(1)
        except Exception:
            print ('can\'t open json file : "%s"' % file_path)
            exit(1)
        self._categorizing()

    ## sort data with categories
    def _categorizing( self ):
        print('> loading JSON file... ', end='')
        for e in self.json_data:
            if e['type'] not in self.categories:
                self.categories.append(e['type'])
                self.json_data_categorized[e['type']] = []
            self.json_data_categorized[e['type']].append(e)
        print('done')

    ## return random joke from json
    def get_random_joke( self ):
        nb_jokes = len(self.json_data)
        random_number = random.randrange(0, nb_jokes)
        return self.json_data[random_number]

    ## return random joke with specific type, from json
    def get_random_joke_with_type( self, joke_type ):
        if joke_type not in self.categories:
            return None
        nb_jokes = len(self.json_data_categorized[joke_type])
        random_number = random.randrange(0, nb_jokes)
        return self.json_data_categorized[joke_type][random_number]

    ## return categories
    def get_categories( self ):
        return { 'categories': sorted(self.categories) }