

def get_pw_hashed(pw_plain: str):
    from passlib.context import CryptContext
    pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    pw_hashed = pw_context.hash(pw_plain)
    return pw_hashed
