from flask import Blueprint, request, jsonify 
from repository.mysql_external_server_repository import MySQLExternalServerRepository
from services.category_service import CategoryService
from routes.auth_routes import admin_required
category_service = CategoryService()

admin_bp = Blueprint('admin_bp', __name__)



@admin_bp.route('/external_servers', methods=['GET'])
@admin_required
def get_all_servers():
    
    mysql_external_server = MySQLExternalServerRepository()
    servers = mysql_external_server.get_all()
    filtered_servers = []
    for s in servers:
        filtered_servers.append({
            "name": s.name,
            "status": s.status,
            "last_accessed": s.last_accessed
        })

    return jsonify({
        "success": True,
        "servers": filtered_servers
    }), 200
    

@admin_bp.route('/categories', methods=['POST'])
@admin_required
def add_category():
    
    category = category_service.getCategories()
    data = request.get_json()
    category_name = data.get('name')
    
    if category_name in category:
        print(category_name)
        return jsonify({
                "success": True,
                "message": "Category Already exists."
        }),200
    
    
    response = CategoryService.createCategory(category_name)
    return jsonify({
        "success": True,
        "message": response.to_dict()
    }), 200
            

@admin_bp.route('/external_servers/<int:server_id>/status', methods=['PUT'])
@admin_required
def update_server_status(server_id):    
    data = request.get_json()
    new_status = data.get('status')
    new_api_key = data.get('api_key')
    
    if new_status not in ['active', 'inactive']:
        return jsonify({"success": False, "message": "Invalid status. Must be 'active' or 'inactive'."}), 400
    mysql_external_server = MySQLExternalServerRepository()
    server =  mysql_external_server.find_by_id(server_id) 
    if not server:
        return jsonify({"success": False, "message": "Server not found."}), 404

    if new_api_key:
        mysql_external_server.update_status(server_id, new_status, new_api_key)
        return jsonify({"success": True, "message": f"Server {server.name} status updated to {new_status} and spi_key updated to {new_api_key}."}), 200
    else:
        mysql_external_server.update_status(server_id, new_status)
        return jsonify({"success": True, "message": f"Server {server.name} status updated to {new_status}."}), 200


@admin_bp.route('/external_servers/details', methods=['GET'])
@admin_required
def get_external_server_details():
    try:
        mysql_external_server = MySQLExternalServerRepository()
        servers = mysql_external_server.get_all()
        filtered_servers = []
        for s in servers:
            filtered_servers.append({
                "name": s.name,
                "api_key": s.api_key,
            })

        return jsonify({
            "success": True,
            "servers": filtered_servers
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Error retrieving server details: {str(e)}"}), 500
