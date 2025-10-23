from hashlib import sha256
print("Hash para admin123 →", sha256("admin123".encode()).hexdigest())
