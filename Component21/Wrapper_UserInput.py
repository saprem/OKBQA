import urllib2
import json
import sys

'''
first_arg is the question
second_arg is the language of question
'''

first_arg = sys.argv[1]
second_arg = sys.argv[2]

class OKBQA(object):

    '''
    extracts the corresponding value "o", and display it as output
    For eg:
    (1)
    first_arg: "Which river flows through India?"
    second_arg: "en"
    OUTPUT: flows
    (2)
    first_arg: "Who is dancing in the hall?"
    second_arg: "en"
    NOTE: change x['s'] =="v1" (in this case)
    OUTPUT: dancing 
    '''
    def extract(self):
        
        data = {}
        data["string"] = first_arg
        data["language"] = second_arg

        #Return a String representing JSON object-Here Dict 
        #ENCODING 
        data = json.dumps(data)

        #http url
        url = 'http://ws.okbqa.org:1515/templategeneration/rocknrole'

        #POST request 
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        
        #fetching URL
        f = urllib2.urlopen(req)
        jsonX = f.read()

        #Uncomment below for testing purpose
        #print jsonX  
        
        #return a JSON object from string representing JSON object 
        #DECODING
        json_object = json.loads(jsonX)

        '''
        iterating the output json to extract required ans.
        It is hard-coded. Change x['s'] below accordingly for different
        input query questions(i.e. first_arg)  
        '''
        for item in json_object:
            for x in item['slots']:
                if x['p']=="verbalization" and x['s']=="v9":
                    print x['o']
        
        f.close()    

'''
Wrapper class that wraps another class 
so that when a function is run through the wrapper class.
A pre and post function is run as well.(For Testing or any other purpose)
'''
class Wrapper(object):
    def __init__(self,wrapped_class):
        self.wrapped_class = wrapped_class()

    def __getattr__(self,attr):
        orig_attr = self.wrapped_class.__getattribute__(attr)
        #print orig_attr
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                self.pre()
                result = orig_attr(*args, **kwargs)
                # prevent wrapped_class from becoming unwrapped
                if result == self.wrapped_class:
                    return self
                self.post()
                return result
            return hooked
        else:
            return orig_attr

    # Runs Before the Wrapped class is called.        
    def pre(self):
        #Uncomment below for testing. 
        #print ">> pre"  
        return

    #Runs After the Wrapped class is called.    
    def post(self):
        #Uncomment below for testing
        #print "<< post"
        return

#Execution begins from here
if __name__ == '__main__':
    
    query = Wrapper(OKBQA)
    query.extract()
    