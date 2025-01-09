# Jekyll Include Migration Tool

A Python script for managing Jekyll include files, allowing you to move files between directories and update all references automatically.

## Features

- Move include files between directories in Jekyll's `_includes` folder
- Rename specific files during migration
- Update all references in `.html`, `.md`, and `.markdown` files
- Support for both `{% include %}` and `{%- include -%}` syntax variations
- Dry run capability to preview changes
- Comprehensive logging to file and console

## Installation

1. Ensure you have Python 3.6 or later installed
2. Copy `migrate_includes.py` to your Jekyll project's scripts directory

## Usage

### Basic Usage

Move all files from one include directory to another:

```
python scripts/migrate_includes.py old-folder new-folder
```

### Advanced Options

```
python scripts/migrate_includes.py old-folder new-folder \
    --root /path/to/jekyll/site \
    --old-name header.html \
    --new-name new-header.html \
    --dry-run \
    --log-file migration.log
```

### Command Line Arguments

- `old_dir` (required): Current include directory name
- `new_dir` (required): New include directory name
- `--root`: Jekyll site root directory (default: current directory)
- `--old-name`: Original filename to change (optional)
- `--new-name`: New filename (required if --old-name is specified)
- `--dry-run`: Show what would be done without making changes
- `--log-file`: Specify a log file to record all operations

## Examples

1. Simple directory migration:
```
python scripts/migrate_includes.py components widgets
```

2. Preview changes with dry run:
```
python scripts/migrate_includes.py components widgets --dry-run
```

3. Move and rename a specific file:
```
python scripts/migrate_includes.py components widgets \
    --old-name header.html --new-name new-header.html
```

4. Full example with logging:
```
python scripts/migrate_includes.py components widgets \
    --root /path/to/site \
    --old-name header.html \
    --new-name new-header.html \
    --dry-run \
    --log-file migration.log
```

## Log File Format

The log file contains timestamped entries for all operations:

```
2024-01-20 10:15:30,123 - INFO - Starting include migration with parameters:
2024-01-20 10:15:30,124 - INFO -   Old directory: components
2024-01-20 10:15:30,124 - INFO -   New directory: widgets
```

## Error Handling

The script will:
- Validate that source directories exist
- Ensure both old and new filenames are provided if one is specified
- Log all errors and operations
- Preserve original files until successful migration

## Best Practices

1. Always run with `--dry-run` first to preview changes
2. Use `--log-file` to keep a record of all changes
3. Back up your Jekyll site before running migrations
4. Verify your site builds correctly after migration

## Troubleshooting

### Common Issues

1. **Files not moving**: Check directory permissions
2. **References not updating**: Ensure correct path to Jekyll root
3. **Log file errors**: Verify write permissions in log directory

### Debug Mode

For detailed debugging, you can set the Python logging level to DEBUG:

```
export PYTHONDEVMODE=1
```

## Contributing

Feel free to submit issues and enhancement requests on the project repository.

## License

This script is released under the MIT License. 