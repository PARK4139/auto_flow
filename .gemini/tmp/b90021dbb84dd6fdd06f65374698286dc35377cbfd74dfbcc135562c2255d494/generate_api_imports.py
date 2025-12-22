import os

from pk_internal_tools.pk_functions.get_pk_root import get_pk_root

package_root = get_pk_root()
import_prefix = "pk_system"
import_statements = ["# This file is auto-generated to re-export all modules from pk_system.",
                     "# It provides a simplified public API for the pk_memo project."]

for root, dirs, files in os.walk(package_root):
    # Exclude __pycache__ directories
    if '__pycache__' in dirs:
        dirs.remove('__pycache__')

    for file in files:
        if file.endswith(".py") and not file.startswith("__init__"):
            # Construct module path
            relative_path = os.path.relpath(os.path.join(root, file), package_root)
            module_path_with_ext = relative_path.replace(os.sep, '.')
            module_path = os.path.splitext(module_path_with_ext)[0]

            # Create the import statement
            # Using 'from ... import *' as requested for "brief" calls
            import_statements.append(f"from {import_prefix}.{module_path} import *")

# Print all statements to be written to the file
for stmt in import_statements:
    print(stmt)
