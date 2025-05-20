from flask import Blueprint, render_template, jsonify, Response
from datetime import datetime
import json
from typing import Dict, List, Any, Optional
from collections import defaultdict
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

docs_bp = Blueprint('docs', __name__, template_folder='../templates')

class PostmanEndpoint:
    def __init__(self, data: Dict[str, Any]):
        self.name = data.get('name', 'Unnamed Endpoint')
        self.description = data.get('description', '')
        self.request = data.get('request', {})
        self.response = data.get('response', [])

    def get_path(self) -> str:
        url = self.request.get('url', {})
        if isinstance(url, str):
            return url.split('{{API}}')[-1]
        return '/' + '/'.join(url.get('path', [])) if isinstance(url, dict) else ''

    def get_request_body(self) -> Optional[Dict]:
        if not self.request.get('body'):
            return None
        
        try:
            return json.loads(self.request['body'].get('raw', '{}'))
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse request body for endpoint: {self.name}")
            return None

    def get_responses(self) -> List[Dict[str, Any]]:
        responses = []
        for response in self.response:
            try:
                response_body = json.loads(response.get('body', '{}')) if response.get('body') else None
            except json.JSONDecodeError:
                response_body = response.get('body')
                
            responses.append({
                "code": response.get('code', 200),
                "description": response.get('status', 'OK'),
                "content_type": next(
                    (h['value'] for h in response.get('header', []) 
                    if h.get('key', '').lower() == 'content-type'),
                    'application/json'
                ),
                "body": response_body
            })
        return responses

class APIDocumentation:
    def __init__(self, collection_path: str = 'src/postman_collection.json'):
        self.collection_path = Path(collection_path)
        self.postman_data: Dict[str, Any] = {}
        self.docs: Dict[str, Any] = {}
        self.load_postman_collection()
        self.organize_endpoints()

    def load_postman_collection(self) -> None:
        """Load and parse the Postman collection JSON file"""
        try:
            with open(self.collection_path) as f:
                self.postman_data = json.load(f)
        except FileNotFoundError:
            logger.error(f"Postman collection file not found: {self.collection_path}")
            self.postman_data = {'item': []}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in Postman collection file: {self.collection_path}")
            self.postman_data = {'item': []}

    def organize_endpoints(self) -> None:
        """Organize endpoints into a structured format for documentation"""
        self.docs = {
            "info": {
                "title": self.postman_data.get('info', {}).get('name', 'API Documentation'),
                "description": "Comprehensive API for Diskominfo Services",
                "version": "1.0.0",
                "contact": {"email": "support@diskominfo.api"},
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "basePath": "/api",
            "tags": [],
            "endpoints": defaultdict(list)
        }

        for item in self.postman_data.get('item', []):
            self._process_category(item)

    def _process_category(self, item: Dict[str, Any]) -> None:
        """Process a category and its endpoints"""
        category_name = item.get('name', 'Uncategorized')
        self.docs['tags'].append({
            "name": category_name,
            "description": f"{category_name} related endpoints"
        })

        for endpoint_data in item.get('item', []):
            self._process_endpoint(endpoint_data, category_name)

    def _process_endpoint(self, endpoint_data: Dict[str, Any], category_name: str) -> None:
        """Process individual endpoint and add to documentation"""
        endpoint = PostmanEndpoint(endpoint_data)
        request = endpoint.request

        endpoint_data = {
            "path": endpoint.get_path(),
            "method": request.get('method', 'GET'),
            "name": endpoint.name,
            "description": endpoint.description,
            "category": category_name,
            "request": {
                "headers": [
                    {h['key']: h['value']} 
                    for h in request.get('header', [])
                ],
                "content_type": next(
                    (h['value'] for h in request.get('header', []) 
                    if h.get('key', '').lower() == 'content-type'),
                    'application/json'
                ),
                "body": endpoint.get_request_body(),
                "query_params": self._get_query_params(request.get('url', {}))
            },
            "responses": endpoint.get_responses()
        }

        self.docs['endpoints'][category_name].append(endpoint_data)

    @staticmethod
    def _get_query_params(url: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract query parameters from URL"""
        if not isinstance(url, dict):
            return []
        return [{q['key']: q.get('value', '')} for q in url.get('query', [])]

    def get_endpoints_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all endpoints for a specific category"""
        return self.docs['endpoints'].get(category, [])

    def get_all_endpoints(self) -> Dict[str, Any]:
        """Get all endpoints organized by category"""
        return self.docs

# Initialize API documentation
api_docs = APIDocumentation()

@docs_bp.route('/docs')
def documentation() -> str:
    """Render API documentation page"""
    return render_template('api_docs.html', docs=api_docs.get_all_endpoints())

@docs_bp.route('/docs/json')
def documentation_json() -> Response:
    """Return API documentation as JSON"""
    return jsonify(api_docs.get_all_endpoints())

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
    endpoints = api_docs.get_endpoints_by_category(category)
    if not endpoints:
        return jsonify({"error": "Category not found"}), 404
    
    return jsonify({
        "category": category,
        "endpoints": endpoints,
        "count": len(endpoints)
    })