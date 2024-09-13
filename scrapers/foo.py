import os
from cfbd import ApiClient, Configuration, CoachesApi
from dotenv import load_dotenv

load_dotenv()

# Configure API key authorization: ApiKeyAuth
configuration = Configuration()
configuration.api_key['Authorization'] = os.getenv('CFBD_API_KEY')
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_instance = CoachesApi(ApiClient(configuration))

try:
    # Betting lines
    api_response = api_instance.get_coaches(first_name="Nick", last_name="Saban")
    print(api_response)
except Exception as e:
    print("Exception when calling BettingApi->get_lines: %s\n" % e)