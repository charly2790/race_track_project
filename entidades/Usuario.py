from werkzeug.security import check_password_hash,generate_password_hash

class Usuario():
    
    def __init__(self, id,email,password,nombre,apellido,foto):
        self.id = id
        self.email = email
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
        self.foto = foto

    @classmethod
    def comprobar_password(self, hashed_password,password):
        return check_password_hash(hashed_password,password)
    
    print(generate_password_hash("morgangato"))
