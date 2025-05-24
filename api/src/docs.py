from flask import Blueprint, render_template, jsonify, Response
from datetime import datetime
import json
from typing import Dict, List, Any, Optional
from collections import defaultdict
from pathlib import Path
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

docs_bp = Blueprint('docs', __name__, template_folder='../templates')

class PostmanEndpoint:
    def __init__(self, data: Dict[str, Any]):
        self.name = data.get('name', 'Unnamed Endpoint')
        self.description = data.get('description', 'No description available')
        self.request = data.get('request', {})
        self.responses = data.get('response', [])
        
    def get_path(self) -> str:
        url = self.request.get('url', {})
        if isinstance(url, str):
            # Clean up the URL path
            path = url.split('{{API}}')[-1] if '{{API}}' in url else url
            return path.replace('{{BASEURL}}', '')
        elif isinstance(url, dict):
            return '/' + '/'.join(url.get('path', []))
        return ''
    
    def get_method(self) -> str:
        return self.request.get('method', 'GET').upper()
    
    def get_request_body(self) -> Optional[Dict]:
        if not self.request.get('body'):
            return None
        
        try:
            body = self.request['body']
            if body.get('mode') == 'raw' and body.get('raw'):
                return json.loads(body['raw'])
            return None
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse request body for endpoint {self.name}: {str(e)}")
            return None
    
    def get_headers(self) -> List[Dict[str, str]]:
        return self.request.get('header', [])
    
    def get_query_params(self) -> List[Dict[str, str]]:
        url = self.request.get('url', {})
        if isinstance(url, dict) and 'query' in url:
            return [{q['key']: q.get('value', '')} for q in url['query']]
        return []
    
    def get_responses(self) -> List[Dict[str, Any]]:
        formatted_responses = []
        for response in self.responses:
            try:
                response_body = json.loads(response.get('body', '{}')) if response.get('body') else None
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse response body for endpoint {self.name}: {str(e)}")
                response_body = response.get('body')
                
            headers = {h['key']: h['value'] for h in response.get('header', [])}
            
            formatted_responses.append({
                "code": response.get('code', 200),
                "status": response.get('status', 'OK'),
                "description": response.get('name', ''),
                "content_type": headers.get('Content-Type', 'application/json'),
                "body": response_body,
                "headers": headers
            })
        return formatted_responses

class APIDocumentation:
    def __init__(self, postman_file: str = 'postman_collection.json'):
        self.postman_file = Path(postman_file)
        self.postman_data = self._load_postman_file()
        self.docs = self._organize_endpoints()
    
    def _load_postman_file(self) -> Dict[str, Any]:
        """Load and validate Postman collection file"""
        if not self.postman_file.exists():
            raise FileNotFoundError(f"Postman collection file not found: {self.postman_file}")
        
        try:
            with open(self.postman_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Basic validation
            if not isinstance(data, dict) or 'item' not in data:
                raise ValueError("Invalid Postman collection format")
                
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in Postman collection: {str(e)}")
    
    def _organize_endpoints(self) -> Dict[str, Any]:
        """Organize endpoints from Postman collection"""
        docs = {
            "info": {
                "title": self.postman_data.get('info', {}).get('name', 'API Documentation'),
                "description": self.postman_data.get('info', {}).get('description', ''),
                "version": "1.0.0",
                "contact": {
                    "email": "support@diskominfo.api",
                    "name": self.postman_data.get('info', {}).get('name', 'Diskominfo Team')
                },
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "basePath": "/api",
            "tags": [],
            "endpoints": defaultdict(list)
        }

        for item in self.postman_data.get('item', []):
            self._process_item(item, docs)
            
        return docs
    
    def _process_item(self, item: Dict[str, Any], docs: Dict[str, Any]) -> None:
        """Process an item which could be a category or endpoint"""
        if 'item' in item:
            # This is a category with nested endpoints
            self._process_category(item, docs)
        else:
            # This is a standalone endpoint
            self._process_endpoint(item, "General", docs)
    
    def _process_category(self, category: Dict[str, Any], docs: Dict[str, Any]) -> None:
        """Process a category and its endpoints"""
        category_name = category.get('name', 'Uncategorized')
        docs['tags'].append({
            "name": category_name,
            "description": category.get('description', f"{category_name} related endpoints")
        })

        for endpoint_data in category.get('item', []):
            self._process_endpoint(endpoint_data, category_name, docs)
    
    def _process_endpoint(self, endpoint_data: Dict[str, Any], category_name: str, docs: Dict[str, Any]) -> None:
        """Process individual endpoint and add to documentation"""
        try:
            endpoint = PostmanEndpoint(endpoint_data)
            
            endpoint_info = {
                "path": endpoint.get_path(),
                "method": endpoint.get_method(),
                "name": endpoint.name,
                "description": endpoint.description,
                "category": category_name,
                "request": {
                    "headers": endpoint.get_headers(),
                    "content_type": next(
                        (h['value'] for h in endpoint.get_headers() 
                         if h.get('key', '').lower() == 'content-type'),
                        'application/json'
                    ),
                    "body": endpoint.get_request_body(),
                    "query_params": endpoint.get_query_params()
                },
                "responses": endpoint.get_responses()
            }

            docs['endpoints'][category_name].append(endpoint_info)
        except Exception as e:
            logger.error(f"Failed to process endpoint {endpoint_data.get('name')}: {str(e)}")

# Initialize API documentation by loading from Postman file
try:
    # Assuming the Postman file is in the same directory as this script
    postman_file = os.path.join(os.path.dirname(__file__), 'postman_collection.json')
    api_docs = APIDocumentation(postman_file)
except Exception as e:
    logger.error(f"Failed to initialize API documentation: {str(e)}")
    # Fallback to empty docs if loading fails
    api_docs = APIDocumentation({
        "info": {"name": "API Documentation", "description": "Failed to load Postman collection"},
        "item": []
    })

@docs_bp.route('/docs')
def documentation() -> str:
    """Render API documentation page"""
    return render_template('api_docs.html', docs=api_docs.docs)

@docs_bp.route('/docs/json')
def documentation_json() -> Response:
    """Return API documentation as JSON"""
    return jsonify(api_docs.docs)

@docs_bp.route('/docs/categories')
def list_categories() -> Response:
    """List all available API categories"""
    return jsonify({
        "categories": api_docs.docs['tags'],
        "count": len(api_docs.docs['tags'])
    })

@docs_bp.route('/docs/category/<category>')
def category_endpoints(category: str) -> Response:
    """Get all endpoints for a specific category"""
    endpoints = []
    for cat in api_docs.docs['tags']:
        if cat['name'].lower() == category.lower():
            endpoints = api_docs.docs['endpoints'].get(cat['name'], [])
            break
            
    if not endpoints:
        return jsonify({"error": "Category not found"}), 404
    
    return jsonify({
        "category": category,
        "endpoints": endpoints,
        "count": len(endpoints)
    })