from passlib.context import CryptContext
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str): 
    return pwdContext.hash(password)