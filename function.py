import sys
import requests
from bs4 import BeautifulSoup, Tag

def html_to_text_tree(html_content):
    """Convert HTML content to a text tree representation."""
    soup = BeautifulSoup(html_content, 'html.parser')
    root = soup.html
    
    if root:
        _print_tree(root)

def _format_attributes(attrs):
    """Format HTML attributes into a string."""
    if not attrs:
        return ""
    attributes = []
    for key, value in attrs.items():
        if isinstance(value, list):
            value = " ".join(value)
        attributes.append(f'{key}="{value}"')
    return f' ({", ".join(attributes)})'

def _print_tree(node, prefix="", is_last=False, is_root=True):
    """Recursively print the HTML tree structure."""
    tag_name = node.name
    attrs_str = _format_attributes(node.attrs)
    full_name = f"{tag_name}{attrs_str}"
    if is_root:
        print(full_name)
    else:
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{full_name}")
    new_prefix = prefix
    if not is_root:
        new_prefix += "    " if is_last else "│   "
    children = [child for child in node.contents if isinstance(child, Tag)]
    for i, child in enumerate(children):
        is_last_child = i == len(children) - 1
        _print_tree(child, new_prefix, is_last_child, is_root=False)

def process_url_or_file(input_source):
    """Process either a URL or file path and return HTML content."""
    if input_source.startswith('http'):

        try:
            response = requests.get(input_source)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None
    else:
        try:
            with open(input_source, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python html2txttree.py [input.html|URL]")
        sys.exit(1)
    
    html_content = process_url_or_file(sys.argv[1])
    if html_content:
        html_to_text_tree(html_content)
def show_tree_from_url(url):
    """Display HTML tree from URL in Jupyter/IPython."""
    html_content = process_url_or_file(url)
    if html_content:
        html_to_text_tree(html_content)

def show_tree_from_file(filepath):
    """Display HTML tree from file in Jupyter/IPython."""
    html_content = process_url_or_file(filepath)
    if html_content:
        html_to_text_tree(html_content)
