"""Product Agent.

Handles product-related questions and knowledge base searches.

TODO: Complete the MCP integration for knowledge base.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any, List, Optional
import json


# Simulated knowledge base (replace with MCP connection in production)
PRODUCTS = [
    {
        "id": "LAPTOP-001",
        "name": "ProBook 15",
        "category": "Laptops",
        "price": 1299.99,
        "description": "Professional laptop with Intel i7, 16GB RAM, 512GB SSD",
        "specs": {"processor": "Intel i7-12700H", "ram": "16GB DDR5", "storage": "512GB NVMe SSD"}
    },
    {
        "id": "LAPTOP-002",
        "name": "UltraBook Air",
        "category": "Laptops",
        "price": 999.99,
        "description": "Lightweight ultrabook for everyday use",
        "specs": {"processor": "Intel i5-1235U", "ram": "8GB DDR4", "storage": "256GB SSD"}
    },
    {
        "id": "PHONE-001",
        "name": "SmartPhone Pro",
        "category": "Phones",
        "price": 899.99,
        "description": "Flagship smartphone with advanced camera",
        "specs": {"display": "6.7 inch OLED", "camera": "108MP", "battery": "5000mAh"}
    },
]

FAQ = [
    {"question": "What is your return policy?", "answer": "We offer a 30-day return policy for all unused items in original packaging. Defective items can be returned within 90 days.", "category": "returns"},
    {"question": "How long does shipping take?", "answer": "Standard shipping takes 5-7 business days. Express shipping (2-3 days) is available for $9.99.", "category": "shipping"},
    {"question": "Do you offer warranty?", "answer": "All products come with a 1-year manufacturer warranty. Extended warranty options are available at checkout.", "category": "warranty"},
    {"question": "How do I track my order?", "answer": "You can track your order using the tracking number sent to your email, or by logging into your account.", "category": "orders"},
]


def search_products(
    query: str,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search the product catalog.
    
    Args:
        query: Search terms
        category: Filter by category (Laptops, Phones, etc.)
    
    Returns:
        Matching products
    """
    results = []
    query_lower = query.lower()
    
    for product in PRODUCTS:
        if category and product["category"].lower() != category.lower():
            continue
        
        if (query_lower in product["name"].lower() or 
            query_lower in product["description"].lower() or
            query_lower in product["category"].lower()):
            results.append(product)
    
    return {
        "status": "success",
        "count": len(results),
        "products": results
    }


def get_product_details(product_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific product.
    
    Args:
        product_id: The product ID
    
    Returns:
        Product details
    """
    for product in PRODUCTS:
        if product["id"] == product_id:
            return {
                "status": "success",
                "product": product
            }
    
    return {
        "status": "error",
        "message": f"Product {product_id} not found"
    }


def search_faq(query: str) -> Dict[str, Any]:
    """
    Search the FAQ database.
    
    Args:
        query: Search terms
    
    Returns:
        Relevant FAQ entries
    """
    results = []
    query_lower = query.lower()
    
    for faq in FAQ:
        if (query_lower in faq["question"].lower() or 
            query_lower in faq["answer"].lower() or
            query_lower in faq["category"].lower()):
            results.append(faq)
    
    return {
        "status": "success",
        "count": len(results),
        "faqs": results
    }


def create_product_agent() -> Agent:
    """Create the Product Agent."""
    
    return Agent(
        name="product_agent",
        model="gemini-2.0-flash",
        description="""
        Product specialist agent. Handles questions about products, specifications,
        pricing, and general FAQ. Delegate product and information queries here.
        """,
        instruction="""
        You are a product specialist. Help customers learn about products and
        find answers to common questions.
        
        ## Your Capabilities
        - Search products by name, description, or category
        - Provide detailed product specifications
        - Answer frequently asked questions
        - Compare products when asked
        
        ## Guidelines
        1. Always search the product catalog for accurate information
        2. Search FAQ for policy-related questions
        3. Be honest if a product isn't available
        4. Provide helpful comparisons when relevant
        5. Include prices when discussing products
        """,
        tools=[
            FunctionTool(search_products),
            FunctionTool(get_product_details),
            FunctionTool(search_faq),
        ]
    )
