from tweepy import Stream
from tweepy.streaming import StreamListener
from googlemaps import GoogleMaps
import auth_elisa
import json


TOPIC = ''

class elisa_stream_listener(StreamListener):

    DEBUG = True
    gmaps = None
    countries_continent_json = None
    continents_counts = {'North America': 0,
                        'Asia': 0,
                        'Europe': 0,
                        'South America': 0,
                        'Australia': 0,
                        'Africa': 0,
                        }

    tweets_cnt = 0
    
    def trunc(self,f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        slen = len('%.*f' % (n, f))
        return str(f)[:slen]
    
    def update_stats(self, continent):
        #update stats
        self.tweets_cnt = self.tweets_cnt+1
        new_continent_count= self.continents_counts[continent]+1
        self.continents_counts[continent]=  new_continent_count
        
        #self.continents_ratio['North America']= self.trunc( round( float(self.continents_ratio['North America']) / self.tweets_cnt,5), 5)
        #self.continents_ratio['Asia']=  self.trunc( round( float(self.continents_ratio['Asia']) / self.tweets_cnt,5), 5)
        #self.continents_ratio['Europe']=  self.trunc( round( float(self.continents_ratio['Europe']) / self.tweets_cnt,5), 5)
        #self.continents_ratio['South America']=  self.trunc( round( float(self.continents_ratio['South America']) / self.tweets_cnt,5), 5)
        #self.continents_ratio['Africa']=  self.trunc( round( float(self.continents_ratio['Africa']) / self.tweets_cnt,5), 5)
        #self.continents_ratio[continent]=   self.trunc( round( ( float(tmp_continent_stat)+1) / self.tweets_cnt,5),5)
        return
        
    def auth_gmaps(self):
        self.gmaps = GoogleMaps('48e7668b14812c0bed47256d2234e7620e5d030e')

    def load_countries_continent_map(self):
        countries_continent_json_file = open('Countries-Continents.json')
        self.countries_continent_json = json.load(countries_continent_json_file)
        countries_continent_json_file.close()

    def get_complete_address(self,loc):
        try:
           
            #Fetching continent
            lat,lng = self.gmaps.address_to_latlng(loc)
            location = self.gmaps.latlng_to_address(lat,lng)
            start_index_country = location.rfind(',')
            country = location[start_index_country+1:]
            continent = self.countries_continent_json[country.strip()]
            self.update_stats(continent)
            return  continent
            
        except Exception as E:
            if self.DEBUG:
                print E
            return 'unknown'

    def on_error(self,status):
        print status
    
    def on_data(self,data):
        #print data

        
        tweet_dict = json.loads(data)
        
        try:
            location = tweet_dict['user']['location']
            continent = self.get_complete_address(location)
            if continent != 'unknown':
                print 'Topic: ', TOPIC
                print 'North America: ',  self.trunc( float(self.continents_counts['North America'])/self.tweets_cnt , 4 )
                print 'South America: ', self.trunc( float(self.continents_counts['South America'])/self.tweets_cnt, 4 )
                print 'Europa: ', self.trunc( float(self.continents_counts['Europe'])/self.tweets_cnt, 4)
                print 'Asia: ', self.trunc( float(self.continents_counts['Asia'])/self.tweets_cnt, 4)
                print 'Africa: ', self.trunc( float(self.continents_counts['Africa'])/self.tweets_cnt, 4)
                print 'Total Tweets: ', self.tweets_cnt
                print '\n'
                #print get_complete_address(long_address)
                
        except Exception as E:
            print E

        return True

        



if __name__ == '__main__':
    print "Elisa:: authentication"
    
    l = elisa_stream_listener()
    l.auth_gmaps()
    l.load_countries_continent_map()
    
    auth_cons_key = auth_elisa.set_consumer_key()
    auth = auth_elisa.set_access_token(auth_cons_key)
    api = auth_elisa.get_API(auth)
    
    auth_elisa.print_name(api)
    
    stream = Stream(auth, l)
    stream.filter(track=[TOPIC])
