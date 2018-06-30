import urllib2
import json

class OKBQA(object):

    #extracts the corresponding value "o", and display it as output as flows
    def extract(self):
        
        data = '{"string": "Which river flows through Seoul?" ,"language": "en"}'        
        
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

        #iterating the output json to extract required ans. i.e. flows
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
        
    # Runs After the Wrapped class is called.    
    def post(self):
        #Uncomment below for testing.
        #print "<< post"
        return    

#Execution begins from here
if __name__ == '__main__':
    
    query = Wrapper(OKBQA)
    query.extract()
