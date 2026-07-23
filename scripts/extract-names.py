import os
import yaml
import re
from pathlib import Path

def split_name(full_name):
    """Split a full name into given and family names"""
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], ""
    family_name = parts[-1]
    given_names = " ".join(parts[:-1])
    return given_names, family_name

def load_frontmatter(file_path):
    """Extract YAML frontmatter from markdown files"""
    content = file_path.read_text(encoding='utf-8')
    if content.startswith('---'):
        _, fm, _ = content.split('---', 2)
        return yaml.safe_load(fm)
    return None

def create_person_stub(name, output_dir):
    """Create a stub markdown file for a person"""
    # Split name into components
    given_name, family_name = split_name(name)
    
    # Convert name to filename format
    filename = name.lower().replace(' ', '-') + '.md'
    
    # Create stub frontmatter
    frontmatter = {
        'layout': 'person',
        'given': given_name,
        'family': family_name,
        'name': name,
        'biography': '',
        'image': '',
        'email': '',
        'url': '',
        'website': '',
        'twitter': '',
        'github': '',
        'linkedin': '',
        'scholar': '',
        'crsid': '',
        'orcid': '',
        'start': '',
        'end': '',
        'institution': '',
        'department': '',
        'position': '',
        'category': [],
        'supervisor': ''
    }
    
    # Convert frontmatter to YAML
    content = '---\n' + yaml.dump(frontmatter, sort_keys=False, allow_unicode=True) + '---\n'
    
    # Write the file
    output_path = output_dir / filename
    if not output_path.exists():
        output_path.write_text(content, encoding='utf-8')
        print(f"Created stub for {name} at {output_path}")
    else:
        print(f"Stub already exists for {name}")

def main():
    # Setup paths
    people_dir = Path('_people')
    people_dir.mkdir(exist_ok=True)
    
    # Get existing people files
    existing_people = {f.stem.lower() for f in people_dir.glob('*.md')}
    
    # Find all directories starting with _
    underscore_dirs = [d for d in Path('.').iterdir() if d.is_dir() and d.name.startswith('_')]
    
    # Process all files in underscore directories
    for dir_path in underscore_dirs:
        for file_path in dir_path.glob('*.md'):
            frontmatter = load_frontmatter(file_path)
            if frontmatter and 'people' in frontmatter:
                # Process each person listed in the frontmatter
                for name in frontmatter['people']:
                    name_slug = name.lower().replace(' ', '-')
                    
                    # If person doesn't exist in _people, create stub
                    if name_slug not in existing_people:
                        create_person_stub(name, people_dir)

if __name__ == '__main__':
    main()
