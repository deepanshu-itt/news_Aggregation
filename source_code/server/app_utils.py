from models.external_server import ExternalServer

def load_external_server_keys_into_app_config(flask_app_config):
    try:
        external_servers = ExternalServer.get_all()
        if not external_servers:
            return

        api_keys_from_db = {server.name.lower(): server.api_key for server in external_servers if hasattr(server, 'name') and hasattr(server, 'api_key')}

        if 'newsapi.org' in api_keys_from_db:
            flask_app_config['NEWSAPI_ORG_API_KEY'] = api_keys_from_db['newsapi.org']
        if 'thenewsapi.com' in api_keys_from_db:
            flask_app_config['THENEWSAPI_COM_API_KEY'] = api_keys_from_db['thenewsapi.com']
        print("loaded")
    except Exception as e:
        pass