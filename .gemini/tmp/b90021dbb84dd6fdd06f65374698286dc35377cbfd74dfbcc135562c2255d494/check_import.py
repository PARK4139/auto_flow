import sys
import os

try:
    # Attempt the desired import path
    from pk_system.pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    print(f"get_caller_name found at: {get_caller_name.__file__}")
except ImportError as e:
    print(f"Could not import from pk_system.pk_internal_tools: {e}")
    # If the above failed, let's try a common alternative structure for pk_system
    # such as if pk_internal_tools itself is directly under pk_system
    try:
        from pk_system.pk_functions.get_caller_name import get_caller_name
        print(f"get_caller_name found at: {get_caller_name.__file__}")
    except ImportError as e_alt:
        print(f"Could not import from pk_system.pk_functions either: {e_alt}")
        # Finally, try the deprecated pk_sources path, to see if it still exists somehow
        try:
            from pk_sources.pk_functions.get_caller_name import get_caller_name
            print(f"get_caller_name found at: {get_caller_name.__file__}")
        except ImportError as e_deprecated:
            print(f"Could not import from pk_sources either (as deprecated): {e_deprecated}")
            print("\n--- sys.path ---")
            for p in sys.path:
                print(p)
            print("--- /sys.path ---")
            print("No working import path found for get_caller_name.")
