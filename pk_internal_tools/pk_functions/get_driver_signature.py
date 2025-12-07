from seleniumbase import Driver
import inspect

print("--- DOCSTRING ---")
print(Driver.__doc__)
print("\n--- ARG SPEC ---")
try:
    print(inspect.getfullargspec(Driver))
except TypeError:
    print("Could not get arg spec for Driver. It might be a class, not a function.")

# Let's try to inspect the __init__ method of the class that might be returned
# I'll assume Driver is a factory function returning a class instance
# This is a bit of a guess.
try:
    # This is a guess, as I don't know what Driver returns.
    # I'll try to instantiate it with a basic argument to see if I can inspect it.
    # This might fail.
    # driver_instance = Driver(browser="chrome")
    # print(inspect.getfullargspec(driver_instance.__init__))
    pass
except Exception as e:
    print(f"Could not inspect __init__: {e}")
