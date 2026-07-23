import os
import yaml
import re

def load_frontmatter(file_path):
    """Load YAML frontmatter from markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1]), parts[2]
    return None, None

def save_frontmatter(file_path, frontmatter, content):
    """Save updated frontmatter back to file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(yaml.dump(frontmatter, allow_unicode=True, sort_keys=False))
        f.write('---')
        f.write(content)

def generate_name(data):
    """Generate full name from components."""
    components = []
    
    # Use preferred name if it exists, otherwise given name
    if 'preferred' in data:
        components.append(data['preferred'])
    elif 'given' in data:
        components.append(data['given'])
    
    # Add prefix if it exists (e.g., 'van', 'de')
    if 'prefix' in data:
        components.append(data['prefix'])
    
    # Add family name
    if 'family' in data:
        components.append(data['family'])
    
    # Add suffix if it exists
    if 'suffix' in data:
        components.append(data['suffix'])
    
    return ' '.join(filter(None, components))  # filter(None) removes empty strings

def generate_filename(data):
    """Generate filename from name components."""
    # Use preferred name if available, otherwise given name
    first = data.get('preferred', data.get('given', ''))
    family = data.get('family', '')
    
    name = f"{first} {family}".lower()
    # Only replace spaces with hyphens, keeping other Unicode characters
    filename = name.replace(' ', '-')
    # Remove only problematic filesystem characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return f"{filename}.md"

def process_directory(directory):
    """Process all markdown files in directory."""
    for filename in os.listdir(directory):
        if not filename.endswith('.md'):
            continue
            
        file_path = os.path.join(directory, filename)
        frontmatter, content = load_frontmatter(file_path)
        
        if not frontmatter:
            continue
            
        changes_needed = False
        
        # Check if name field needs to be added
        if 'name' not in frontmatter:
            new_name = generate_name(frontmatter)
            print(f"\nFile: {filename}")
            print(f"Planning to add name: {new_name}")
            changes_needed = True
        
        # Check if filename matches the expected format
        expected_filename = generate_filename(frontmatter)
        if filename != expected_filename:
            print(f"Current filename: {filename}")
            print(f"Expected filename: {expected_filename}")
            changes_needed = True
        
        if changes_needed:
            response = input("Apply these changes? (y/n): ")
            if response.lower() == 'y':
                if 'name' not in frontmatter:
                    frontmatter['name'] = new_name
                    save_frontmatter(file_path, frontmatter, content)
                
                if filename != expected_filename:
                    new_path = os.path.join(directory, expected_filename)
                    os.rename(file_path, new_path)
                print("Changes applied.")
            else:
                print("Changes skipped.")

if __name__ == "__main__":
    process_directory("_people")
