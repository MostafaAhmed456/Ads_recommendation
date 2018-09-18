# this file is written using snake_case
import sys
sys.path.append('../')
import falcon
import json
import redis

app = falcon.API()  # falcon instance

# this class is written based on parent pattern
class parent:

    class __child:

        def __init__(self):
            #self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
            self.env = json.load(open('../env.json'))
            self.redis_connection = redis.StrictRedis(
                                                    host=str(self.env['redis_host']),
                                                    port=6379,
                                                    db=1,password = self.env['redis_pass'])


        def get_from_redis(self, user_id,campaigns):
            """ link_recommendation gets current link recommendation from redis"""
            
            general_campaign  = 1  # targets all users
            mutual_campaign   = 2  # targets users that clicked more than once 
            targeted_campaign = 3  # targets user that clicked once 

            passed_campaigns =[]


            if general_campaign in  campaigns:
                passed_campaigns.append(general_campaign)
            
            if targeted_campaign in campaigns:
                user = self.redis_connection.get(user_id)
                if user :
                    passed_campaigns.append(targeted_campaign)
                else:
                    pass
            
            if  mutual_campaign in  campaigns:
                user = self.redis_connection.hget("mutual_users",user_id)
                if user :
                    passed_campaigns.append(mutual_campaign)
                else:
                    pass
            if len(passed_campaigns)>0:
                return passed_campaigns
            else:
                return campaigns

                

    # storage for the instance reference
    __instance = None

    def __init__(self):
        if not parent.__instance:
            self.__instance = parent.__child()

    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = ('This is me, Falcon, serving a resource!')

    def on_post(self, req, resp):
            #resp.status = falcon.HTTP_200
        
            paramters = json.loads(req.stream.read())

            user_id =paramters['user_id']
            campaigns=paramters['campaigns']
            passed_campaigns = self.__instance.get_from_redis(user_id,campaigns)
            
            if passed_campaigns:
                resp.data = json.dumps({"result":passed_campaigns})
            else:
                resp.data = json.dumps({"result":passed_campaigns}) 
        
            #except:
            #resp.data = json.dumps({"result":[]})


                

Api_obj = parent()
print Api_obj
#recomm_innner = recomm.__child()
app.add_route('/targeting', Api_obj)

