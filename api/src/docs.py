from flask import Blueprint, render_template
from datetime import datetime
import json

docs_bp = Blueprint('docs', __name__, template_folder='../templates')

with open('src/postman_collection.json') as f:
    postman_data = json.load(f)

API_DOCS = {
    "info": {
        "title": postman_data['info']['name'],
        "description": "Comprehensive API for Diskominfo Services",
        "version": "1.0.0",
        "contact": {
            "email": "support@diskominfo.api"
        },
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    "basePath": "/api",
    "endpoints": []
}

# Transform Postman collection to our format
for item in postman_data['item']:
    category = {
        "name": item['name'],
        "description": f"{item['name']} endpoints",
        "endpoints": []
    }
    
    for endpoint in item.get('item', []):
        request = endpoint['request']
        responses = endpoint.get('response', [])
        
        endpoint_data = {
            "path": request['url'].split('{{API}}')[-1] if isinstance(request['url'], str) else request['url']['raw'].split('{{API}}')[-1],
            "method": request['method'],
            "tag": item['name'],
            "name": endpoint['name'],
            "description": f"{request['method']} operation for {endpoint['name']}",
            "request": {
                "content-type": next((h['value'] for h in request.get('header', []) 
                                   if h.get('key', '').lower() == 'content-type'), "application/json"),
                "body": json.loads(request['body']['raw']) if request.get('body') and request['body'].get('raw') else None
            },
            "responses": []
        }
        
        for response in responses:
            endpoint_data['responses'].append({
                "code": response.get('code', 200),
                "description": response.get('status', 'OK'),
                "body": json.loads(response['body']) if response.get('body') else None
            })
        
        category['endpoints'].append(endpoint_data)
    
    API_DOCS['endpoints'].append(category)

@docs_bp.route('/docs')
def api_docs():
    return render_template('api_docs.html', docs=API_DOCS)