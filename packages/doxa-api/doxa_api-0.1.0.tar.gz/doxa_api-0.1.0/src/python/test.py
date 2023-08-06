import doxa_api

doxa_api.gen_keys()
api = doxa_api.Connection()

print(api.get_ip())

api.register("Feluk6174", doxa_api.get_pub_key(), "A"*64, "Your mom is a pinneapple")