
from interfaces.external_server import IExternalServer
from models.external_server import ExternalServer
from database.database import db
from dto.cursor_dto import CursorDto 
from repository.mysql_queries.external_server_queries import (
    create_external_server_query,
    get_all_external_servers,
    get_external_server_by_id_query,
    get_external_server_by_name_query,
    update_external_server_last_accessed_query,
    update_external_server_query,
    update_external_server_status_query
)


class MySQLExternalServerRepository(IExternalServer):

    def create(self, name, api_key, base_url, status='active'):
        query = create_external_server_query
        cursor_params = CursorDto(query=query, params=(name, api_key, base_url, status),commit=True)
        server_id = db.execute_query(cursor_params)

        if server_id:
            return ExternalServer(server_id, name, api_key, base_url, status)

        return self.find_by_name(name)


    def find_by_id(self, server_id):
        query = get_external_server_by_id_query
        cursor_params = CursorDto(query=query, params=(server_id,), fetch_one=True)
        row = db.execute_query(cursor_params)
        return ExternalServer(**row) if row else None


    def find_by_name(self, name):
        query = get_external_server_by_name_query
        cursor_params = CursorDto(query=query, params=(name,), fetch_one=True)
        row = db.execute_query(cursor_params)
        return ExternalServer(**row) if row else None


    def get_all(self):
        query = get_all_external_servers
        cursor_params = CursorDto(query=query, fetch_all=True)
        rows = db.execute_query(cursor_params)
        return [ExternalServer(**row) for row in rows] if rows else []


    def update_status(self, server_id, status, new_api_key=None):
        cursor_params = CursorDto(query="", commit=True)
        if new_api_key:
            query = update_external_server_query
            cursor_params.query = query
            cursor_params.params = (status, new_api_key, server_id)
        else:
            query = update_external_server_status_query
            cursor_params.query = query
            cursor_params.params = (status, server_id)
            
        db.execute_query(cursor_params)


    def update_last_accessed(self, server_id):
        query = update_external_server_last_accessed_query
        cursor_params = CursorDto(query=query, params=(server_id,),commit=True)
        db.execute_query(cursor_params)
