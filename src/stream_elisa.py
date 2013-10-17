from tweepy import Stream
from tweepy.streaming import StreamListener
import auth_elisa
import json
import threading
import time
import re

TOPIC = ''

    
class elisa_stream_listener(StreamListener):

    DEBUG = True
    miss = 0
    hit = 0
    tweets_cnt = 0
    countries_continent = {}
    
    continents_counts = {'North America': 0,
                        'Asia': 0,
                        'Europe': 0,
                        'South America': 0,
                        'Australia': 0,
                        'Africa': 0,
                        }

   
    


    def get_continent_from_city(self, city):
        try:
            result = self.countries_continent[city.lower()]
            return result
        except Exception as E:
            return 'unknown'
      
    
    def get_location(self, loc):
        #candidates = re.split('; | , | - | \/ | ) | ( |   ', loc)
        candidates = re.split('[\W]+',loc)
        for candidate in candidates:
            continent = self.get_continent_from_city(candidate.lower())
            if continent != 'unknown':
                self.hit +=1
                return continent
      
        self.miss +=1
        return 'unknown'




    
    def load_cities(self):
        cities_fp = open("../resources/city_continent_map","r")
        cities  = cities_fp.readlines()

        for city in cities:
            self.countries_continent.update({city.split("\t")[0].lower().strip() : city.split("\t")[2].strip()})
           # print {city.split("\t")[0].strip().lower() : city.split("\t")[2].strip()}
        cities_fp.close()
        
            
    def start_thread_print_stats(self):
        t_print_stats = threading.Thread(target=self.timeout_print_stats)
        t_print_stats.start()

    def get_continent_stat(self, continent):
        tot_hit_count= self.hit
        if tot_hit_count == 0 :
            return 0
        else:
            count = self.continents_counts[continent]
            return self.trunc( float(count) / tot_hit_count, 4)
        
    def timeout_print_stats(self):
        while True:
            try:
                time.sleep(2)
                print '\n\nTopic: ', TOPIC
                print 'North America(',self.continents_counts['North America'],'): ',  self.get_continent_stat('North America')
                print 'South America(',self.continents_counts['South America'],'): ', self.get_continent_stat('South America')
                print 'Europe(',self.continents_counts['Europe'],'): ',self.get_continent_stat('Europe')
                print 'Asia(',self.continents_counts['Asia'],'): ', self.get_continent_stat('Asia')
                print 'Africa(',self.continents_counts['Africa'],'): ',self.get_continent_stat('Africa')
                print 'Total Tweets: ', self.tweets_cnt
                print 'Miss: ', self.miss
                print 'Hit: ', self.hit
                if self.tweets_cnt != 0 :
                    print 'Hit ratio: ', self.trunc( float(self.hit) / self.tweets_cnt, 4)
                print '\n'
            except Exception as E:
                if self.DEBUG:
                    print 'timeout_print_stats: ',E
            
        
    
    def trunc(self,f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        slen = len('%.*f' % (n, f))
        return str(f)[:slen]
    
    def update_stats(self, continent):
        #update stats
        
        new_continent_count= self.continents_counts[continent]+1
        self.continents_counts[continent]=  new_continent_count
        
      
        return
        
        

    def on_error(self,status):
        print status
    
    def on_data(self,data):
        
        self.tweets_cnt = self.tweets_cnt+1
        tweet_dict = json.loads(data)
        
        try:
            #print tweet_dict['user']['location']
            continent = self.get_location(tweet_dict['user']['location'])
            
            if continent != 'unknown':
                self.update_stats(continent)
                
                
        except Exception as E:
            if self.DEBUG:
                print 'on_data-city: ',tweet_dict['user']['location']
                print 'on_data-exception(): ', E

        return True

        



if __name__ == '__main__':
    print "Elisa:: authentication"
    
    l = elisa_stream_listener()
    l.load_cities()
    l.start_thread_print_stats()
    auth_cons_key = auth_elisa.set_consumer_key()
    auth = auth_elisa.set_access_token(auth_cons_key)
    api = auth_elisa.get_API(auth)
    
    auth_elisa.print_name(api)

    
   
    stream = Stream(auth, l)
    stream.filter(track=[TOPIC])
