import requests
import json
from Student import Student
from Professor import Professor
from Post import Post
from Comment import Comment
import uuid
import datetime

class Metrogram:
    def __init__(self):
        self.users = []
        self.posts = []
        self.majors = []
        self.departments = []
        self.comments = []
        self.deleted_users =[]
        self.deleted_posts = []
        self.deleted_comments = []

    def get_api_info(self):
        # Función para extraer los datos y crear objetos de los usuarios y los posts de la api

        # Dichos objetos se agregan en la lista de usuarios o posts
        url_users = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json"
        url_posts = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json"
        res_users= requests.get(url_users).json()
        res_posts = requests.get(url_posts).json()
        for y in res_posts:
            creator = y["publisher"]
            kind_post = y["type"]
            cap =  y["caption"]
            date = y["date"]
            tag = y["tags"]
            multi= y["multimedia"]['url']
            post = Post(creator, cap, tag, date, kind_post, multi, like = [], comment = [])
            self.posts.append(post)

        for x in res_users:
            dni = x["id"]
            first_name = x["firstName"]
            last_name = x["lastName"]
            email = x["email"]
            username = x["username"].lower()
            kind_user = x["type"]
            following = x["following"]
            posts = []
            for p in self.posts:
              if dni == p.dni_creator:
                  posts.append(p)
            if kind_user == "student":
                career = x["major"]
                if career not in self.majors:
                    self.majors.append(career)
                student = Student(dni, first_name, last_name, email, username, posts, following, kind_user, career)
                self.users.append(student)
                
            else: 
                department = x["department"]
                if department not in self.departments:
                    self.departments.append(department)
                professor = Professor(dni, first_name, last_name, email, username, posts, following, kind_user, department)
                self.users.append(professor)
        print('Usuarios registrados')

    def all_majors(self):

        # Función para separar las carreras universitarias de la lista de usuarios
        
        # Muestra enumeradamente las carreras universitarias

        for i,m in enumerate(self.majors):
            print(f'{i+1} / {m}')

    def all_departments(self):

        # Función para separar los departamentos universitarios de la lista de usuarios
        
        # Muestra enumeradamente los departamentos universitarios

        for i, m in enumerate(self.departments):
            print(f'{i+1} / {m}')

    def login(self):

        # Función para verificar y logear un perfil

        # Returns: 
        # profile
        username = input('Ingrese su usuario:  ')
        f = False
        for x in self.users:
            if x.username == username:
                profile = x
                f = True
                return profile
        
        if f == False:
            self.reg_new_users()    

    def usuario_dispo(self,x):

        # Función para verificar si el nombre de usuario está disponible

        # Args:
        # x
        
        # Returns:
        # Bool
        for j in self.users:
            if x == j.username:
                return True
            return False

    def random_dni(self):

        # Función para generar un id

        # Returns:
        # str: Id generado
        sms = uuid.uuid4()
        return sms   
    
    def reg_new_users(self):

        # Función para registrar nuevos usuarios, estos se agregan a la lista de usuarios
        # junto con los usuarios extraidos de la api

        followings = []
        wall = []

        dni = self.random_dni()
        name = input('Ingrese su nombre:  ')
        lastname = input('Ingrese su apellido:  ')
        correo = input('Ingrese su correo electrónico:  ')
        username_new = input('Ingrese su nombre de usuario:  ').lower()
        valid_username = self.usuario_dispo(username_new)
        while valid_username == True:
            username_new = input('Nombre de usuario no disponble, intenta uno nuevo:  ')
        type_user = input('Estudiante o Profesor (E/P):  ').upper()
        if type_user != 'E' and type_user != 'P':
            type_user = input('Ingrese una opción válida (E/P):  ').upper()
        if type_user == 'E':
            type_user = 'Estudiante'
            print(self.all_majors())
            op = input('Ingrese el número de la carrera que cursa:  ')
            major = self.majors[int(op)-1]
            for v in self.users:
                if hasattr(v, 'major'):
                    if major == v.major:
                        followings.append(v.dni)
            nuevo_usuario = Student(dni, name, lastname, correo, username_new, wall, followings, type_user, major)
            self.users.append(nuevo_usuario)
        elif type_user == 'P':
            type_user = 'Profesor'
            print(self.all_departments())
            op = input('Ingrese el número de la carrera que dicta:  ')
            department = self.departments[int(op)-1]
            for v in self.users:
                if hasattr(v, 'department'):
                    if department == v.department:
                        followings.append(v.dni)
            nuevo_usuario = Professor(dni, name, lastname, correo, username_new, wall, followings, type_user, department)
            self.users.append(nuevo_usuario)
        print('Su usuario ha sido creado exitósamente!')

    def search_profile(self, profile):
        
        # Función para buscar perfiles y poder interactuar con ellos y con sus posts
        
        # Args:
        # Profile

        # Esta función en mi proyecto es de las más importante, porque utilizándola, se puede acceder a muchas otras funciones
        while True:
            print('''
            Buscar...
            1. Usuario
            2. Carrera o Departamento
            3. Salir
            ''')
            op = input('Ingrese el método que desea utilizar para buscar el usuario')
            while not op.isnumeric() or int(op) not in range(1,4):
                op = input('Ingrese una opción válida')
            if op == '1':
                for x in self.users:
                    print(f'@{x.username}')
                usuarios_encontrados = []
                search = input('Ingrese el nombre de usuario que quiere buscar...  ').lower()
                for y in self.users:
                    if search in y.username.lower():
                        usuarios_encontrados.append(y)
                count = 1
                for u in usuarios_encontrados:
                    print(f'{count}) {u.username}')
                    count += 1
                opt = input('Elija el usuario con el que desea interactuar... ')
                while not opt.isnumeric() or int(opt) not in range(1, len(usuarios_encontrados)+1):
                    opt = input('Ingrese una opcion valida: ')
                obj = usuarios_encontrados
                print(obj[int(opt) -1].show())
                while True:
                    print('''
                    1. Seguir
                    2. Dejar de seguir
                    3. Elegir post
                    4. Salir
                    ''')
                    fig = input('Ingrese la opción que desea realizar:  ')
                    while not fig.isnumeric() or int(fig) not in range(1,5):
                        fig = input('Error! Ingrese la opción que desea realizar:  ')
                    if fig == '1':
                        self.follow(profile, obj[int(opt) -1])
                    elif fig == '2':
                        self.unfollow(profile, obj[int(opt) -1])
                    elif fig == '3':
                        while True:
                            inte = input('Elija el post con el que desea interactuar (Para salir, escriba 100):')
                            if inte == '100':
                                break
                            var = profile.posts[int(inte)-1]
                            print('''
                            1. Dar like
                            2. Ver likes
                            3. Comentar
                            4. Ver comentarios
                            5. Salir
                            ''')
                            opc = input('Elija la opción que desee realizar:  ')
                            while not opc.isnumeric() or int(opc) not in range(1,6):
                                opc = input('Error! Ingrese una opción válida:  ')
                            if opc == '1':
                                var = self.likear_post(var, profile)
                            elif opc == '2':
                                pass
                            elif opc == '3':
                                self.comment_post(profile)
                            elif opc == '4':
                                pass
                            else:
                                break

                    else:
                        break

            elif op == '2':
                while True:
                    print('''
                    1. Carrera
                    2. Departamento
                    3. Salir
                    ''')
                    kind = input('Elija la opción:  ')
                    while not kind.isnumeric() or int(kind) not in range(1,4):
                        kind = input('Ingrese una opción válida:  ')
                    if kind == '1':
                        self.all_majors()
                        found = input('Ingresar carrera: ')
                        if (int(found)-1) in range(len(self.majors)):
                            u = 1
                            print(self.majors[int(found)-1])
                            lis = []
                            for x in self.users:
                                if isinstance(x, Student):
                                    if x.major == self.majors[int(found)-1]:
                                        print(f'{u}/ "@{x.username}"')
                                        lis.append(x)
                                        u += 1
                            
                            ok = input('Elija el usuario con el que desea interactuar:  ')
                            while not ok.isnumeric() or int(ok) not in range(1, len(lis) +1):
                                ok = input('Error! Elija el usuario con el que desea interactuar:  ')
                            
                            print((lis[int(ok)-1]).show())
                            while True:
                                print('''
                                1. Seguir
                                2. Dejar de seguir
                                3. Elegir post
                                4. Salir
                                ''')
                                fig = input('Ingrese la opción que desea realizar:  ')
                                while not fig.isnumeric() or int(fig) not in range(1,5):
                                    fig = input('Error! Ingrese la opción que desea realizar:  ')
                                if fig == '1':
                                    self.follow(profile, lis[int(ok)-1])
                                elif fig == '2':
                                    self.unfollow(profile, lis[int(ok)-1] )
                                elif fig == '3':
                                    while True:
                                        inte = input('Elija el post con el que desea interactuar(Para salir, escriba 100):')
                                        if inte == '100':
                                            break
                                        var = profile.posts[int(inte)-1]
                                        print('''
                                        1. Dar like
                                        2. Ver likes
                                        3. Comentar
                                        4. Ver comentarios
                                        5. Salir
                                        ''')
                                        opc = input('Elija la opción que desee realizar:  ')
                                        while not opc.isnumeric() or int(opc) not in range(1,6):
                                            opc = input('Error! Ingrese una opción válida:  ')
                                        if opc == '1':
                                            var = self.likear_post(var, profile)
                                        elif opc == '2':
                                            pass
                                        elif opc == '3':
                                            self.comment_post(profile)
                                        elif opc == '4':
                                            pass
                                        else:
                                            break
                                else:
                                    break

                    elif kind == '2':
                        self.all_departments()
                        found = input('Ingresar departamento:  ')
                        if (int(found)-1) in range(len(self.departments)):
                            y = 1
                            print(self.departments[int(found)-1])
                            lsi = []
                            for y in self.users:
                                if isinstance(y, Professor):
                                    if y.department == self.departments[int(found)-1]:
                                        print(f'{y}, "@{y.username}"')
                                        lsi.append(y)
                                        y += 1

                            ok = input('Elija el usuario con el que desea interactuar:  ')
                            while not ok.isnumeric() or int(ok) not in range(1, len(lis) +1):
                                ok = input('Error! Elija el usuario con el que desea interactuar:  ')
                            
                            print((lis[int(ok)-1]).show())
                            while True:
                                print('''
                                1. Seguir
                                2. Dejar de seguir 
                                3. Elegir post
                                4. Salir
                                ''')
                                fig = input('Ingrese la opción que desea realizar:  ')
                                while not fig.isnumeric() or int(fig) not in range(1,5):
                                    fig = input('Error! Ingrese la opción que desea realizar:  ')
                                if fig == '1':
                                    self.follow(profile, lis[int(ok)-1])
                                elif fig == '2':
                                    self.unfollow(profile, lis[int(ok)-1])
                                elif fig == '3':
                                    while True:
                                        inte = input('Elija el post con el que desea interactuar(Para salir, escriba 100):')
                                        if inte == '100':
                                            break
                                        var = profile.posts[int(inte)-1]
                                        print('''
                                        1. Dar like
                                        2. Ver likes
                                        3. Comentar
                                        4. Ver comentarios
                                        5. Salir
                                        ''')
                                        opc = input('Elija la opción que desee realizar:  ')
                                        while not opc.isnumeric() or int(opc) not in range(1,6):
                                            opc = input('Error! Ingrese una opción válida:  ')
                                        if opc == '1':
                                            var = self.likear_post(var, profile)
                                        elif opc == '2':
                                            pass
                                        elif opc == '3':
                                            self.comment_post(profile)
                                        elif opc == '4':
                                            pass
                                        else:
                                            break
                                else:
                                    break
                    else:
                        break
            else:
                break
                    
    def change_info_users(self, profile):

        # Función para cambiar información de los usuarios

        # Args:
        # Profile

        # Actualiza cualquier dato del usuario

        count = 0
        for s in self.users:
            if s.username == profile:
                break
            count += 1
        clap = input('Estudiante o Profesor (E/P):  ').upper()
        if clap != 'E' and clap != 'P':
            clap = input('Ingrese una opción válida (E/P): ')
        if clap == 'E':
            while True:
                print('''Escoja la opción que desee modificar
                1. Nombre
                2. Apellido
                3. Correo electrónico
                4. Username
                5. Carrera
                6. Salir
                ''')
                op = input('Ingrese la opción deseada:  ')
                while not op.isnumeric or int(op) not in range(1,7):
                    op = input('Por favor, ingrese una opción válida:  ')
                if op == '1':
                    new_name = input('Ingrese el nuevo nombre: ')
                    self.users[count].name = new_name
                elif op == '2':
                    new_lastName = input('Ingrese el nuevo apellido:  ')
                    self.users[count].last_name = new_lastName
                elif op == '3':
                    new_email = input('Ingrese el nuevo correo electrónico:  ')
                    self.users[count].email = new_email
                elif op =='4':
                    new_username = input('Ingrese el nuevo nombre de usuario:  ')
                    self.users[count].username = new_username
                elif op =='5':
                    print(self.all_majors)
                    fig = input('Ingrese el número de la carrera que va a cursar:  ')
                    new_major = self.majors[int(fig)-1]
                    self.users[count].major = new_major
                else:
                    break
        else:
            while True:
                print('''Escoja la opción que desee modificar
                1. Nombre
                2. Apellido
                3. Correo electrónico
                4. Username
                5. Departamento
                6. Salir
                ''')
                op = input('Ingrese la opción deseada:  ')
                while not op.isnumeric or int(op) not in range(1,7):
                    op = input('Por favor, ingrese una opción válida:  ')
                if op == '1':
                    new_name = input('Ingrese el nuevo nombre: ')
                    self.users[count].name = new_name
                elif op == '2':
                    new_lastName = input('Ingrese el nuevo apellido:  ')
                    self.users[count].last_name = new_lastName
                elif op == '3':
                    new_email = input('Ingrese el nuevo correo electrónico:  ')
                    self.users[count].email = new_email
                elif op =='4':
                    new_username = input('Ingrese el nuevo nombre de usuario:  ')
                    self.users[count].username = new_username
                elif op =='5':
                    print(self.all_majors)
                    fig = input('Ingrese el número de la carrera que va a cursar:  ')
                    new_department = self.departments[int(fig)-1]
                    self.users[count].department = new_department
                else:
                    break
             
    def delete_data_account(self, profile):

        # Función para eliminar la cuenta

        # Args:
        # Profile
        count = 0
        for s in self.users:
            if s.username == profile.username:
                break
            count += 1
        self.users.pop(count)
        print('Su usuario ha sido eliminado')

    def comment_post(self, profile):

        # Función para comentar cualquier post

        # Args:
        # Profile

        while True:
            try:
                username = input('Ingrese el nombre de usuario: ').lower()
                for i in range(0, len(self.users)):
                    if self.users[i].username == username:
                        for n in range(0, len(self.posts)):
                            if self.users[i].dni == self.posts[n].dni_creator:
                                print(n)
                                self.posts[n].show()
                        opt = int(input('Ingrese el post que desea comentar:  '))
                        comment = input('Comentar...  ')
                        date = datetime.date.today()
                        new_comment = Comment(profile, comment, date)
                        self.comments.append(new_comment)
                        print('Comentario agregado!')
                        self.posts[opt].show()
                        self.posts[opt].comment.append(new_comment.show_comment())
                break
            except:
                print('Usuario no encontrado')
                break

    def likear_post(self, post, profile):

        # Función para dar like a los posts

        # Args:
        # post y profile

        # Returns:
        # post

        if len(post.like) == 0:
            post.like.append(profile.username)
            print(len(post.like))
            print(post.show())
            print('Me gusta')
            return(post)
        else:
            if profile.username in post.like:
                post.like.remove(profile.username)
                print('No me gusta')
                return(post)
            else:
                post.like.append(profile.username)
                print('Me gusta')
                return(post)

    def reg_post(self,profile):

        # Función para registrar un nuevo post

        # Args:
        # Profile

        # Agrega los nuevos posts a la lista de posts general y los posts personales de cada usuario

        while True:
            try:
                username = input('Ingrese el nombre de usuario del usuario que va a publicar:  ')
                for u in range(0, len(self.users)):
                    if username == self.users[u].username:
                        dni = self.users[u].dni
                break
            except:
                print('Usuario no encontrado...')
        while True:
            print(''' Que tipo de multimedia desea registrar
            1. Foto
            2. Video
            3. Salir
            ''')
            op = input('Ingrese la opción que desea realizar:  ')
            while not op.isnumeric() or int(op) not in range(1,4):
                op = input('Error! Ingrese la opción que desea realizar:  ')
            if op == '1':
                kind = 'foto'
            elif op == '2':
                kind == 'video'
            else:
                break
            caption =input('''Ingrese el pie de foto
                            
                    ''')
            tags = []
            hashtags = input('''Ingrese los hashtagas de la foto o video
                            
                        ''')
            tags.append(hashtags)
            while True:
                print('''1. Desea agregar otro hashtag?
                    2. Continuar
                        ''')
                op = input('Ingrese la opción deseada:  ')
                while not op.isnumeric() or int(op) not in range(1,3):
                    op = input('Ingrese una opción válida:  ') 
                if op == '1':
                    hashtags = input('''Ingrese los hashtagas de la foto o video
                            
                        ''')
                    tags.append(hashtags)
                else :
                    break
                   
            date = datetime.date.today()
            multimedia = input('Ingrese el URL de la foto o el video que desear registrar: ')
            likes = []
            comments = []
            
            post = Post(dni, caption, hashtags, date, kind, multimedia, likes, comments)
            self.posts.append(post)
            profile.append(post)
            print('Su post ha sido registrado exitósamente!')

    def search_post(self):

        # Función para buscar posts, mediante usuario o mediante los hashtags

        while True:
            print('''
            Buscar...
            1. Usuario
            2. Hashtag
            3. Salir
            ''')
            op = input('Ingrese el método que desea utilizar para buscar el usuario')
            while not op.isnumeric() or int(op) not in range(1,4):
                op = input('Ingrese una opción válida')
            if op == '1':
                print(self.users[0].username)
                for x in self.users:
                    print(f'@{x.username}')
                usuarios_encontrados = []
                search = input('Ingrese el nombre de usuario que quiere buscar...  ').lower()
                for x in self.users:
                    if search in x.username.lower():
                        usuarios_encontrados.append(x)
                count = 1
                for u in usuarios_encontrados:
                    print(f'{count}) {u.username}')
                    count += 1
                opt = input('Elija la cuenta con la que desee interactuar:  ')
                while not opt.isnumeric() or int(opt) not in range(0, len(usuarios_encontrados) + 1):
                    opt = input('Elija una opción válida: ')
                print((usuarios_encontrados[int(opt) - 1].posts))
            elif op == '2':
                print(self.posts[0].hashtag)
                for x in self.posts:
                    print(f'#{x.hashtag}')
                hashtags_encontrados = []
                find = input('Ingrese el hashtag que desea buscar...  ').lower()
                for x in self.posts:
                    if find in x.hashtag.lower():
                        hashtags_encontrados.append(x)
                coun = 1
                for h in hashtags_encontrados:
                    print(f'{coun}) {h.hashtag}')
                    coun += 1
                optc = input('Ingrese el hashtag con el que desea interactuar:  ')
                while not optc.isnumeric() or int(optc) not in range(0, len(hashtags_encontrados) + 1):
                    optc = input('Error! Ingrese una opción válida: ')
                print((hashtags_encontrados[int(opt) - 1].posts))
            else:
                break

    def follow(self, profile, seguir):

        # Función para seguir un perfil

        # Args:
        # profile y seguir

        if profile in seguir.following:
            seguir.following.remove(profile)
            print('Se ha dejado de seguir')
        count = 0
        for i in self.users:
            if i.username == seguir.username:
                break
            count += 1
        self.users[count].following.append(profile.username)
        print('Ahora lo sigues')

    def unfollow(self, profile, dejardeseguir):

        # Función para dejar de seguir un perfil, el contrario de la función anterior

        # Args:
        # profile, dejardeseguir

        count = 0
        for i in self.users:
            if i.username == dejardeseguir.username:
                break
            count += 1
        self.users[count].following.remove(profile.username)
        print('Ya no sigues a este usuario')

    def delete_comment(self, profile):

        # Función para que los dueños de los posts puedan borrar un comentario que no les guste

        # Args:
        # profile

        while True:
            try:
                for i in range(0, len(self.users)):
                    if self.users[i].username == profile:
                        for n in range(0, len(self.posts)):
                            if self.users[i].dni == self.posts[n].dni_creator:
                                print(n)
                                self.posts[n].show()

                        opt = int(input('Ingrese el post que desea interactuar:  '))
                        for x, com in enumerate(self.posts[opt].comment, 1):
                            print(x, com)
                        op = int(input('Ingrese el comentario que dsea eliminar:  '))
                        self.posts[opt].comment.pop(op)
                        print('Comentario eliminado con éxito')
                break
            except:
                print('Usuario no encontrado')
                break

    def delete_post_admin(self):

        # Función para el admin, permite eliminar cualquier post del sistema

        while True:
            try:
                username = input('Ingrese el nombre de usuario:').lower()
                for i in range(0, len(self.users)):
                    if self.users[i].username == username:
                        for n in range(0, len(self.posts)):
                            if self.users[i].dni == self.posts[n].dni_creator:
                                print(n)
                                self.posts[n].show()
                        opt = int(input('Ingrese el post que desea eliminar:  '))
                        self.posts[n].pop(opt)
                        print('Post eliminado con éxito')
                        self.deleted_posts.append(username)
                break
            except:
                print('Usuario no encontrado')
                break

    def delete_comment_admin(self):

        # Función para el admin, permite eliminar cualquier comentario del sistema

        while True:
            try:
                username = input('Ingrese el nombre de usuario').lower()
                for i in range(0, len(self.users)):
                    if self.users[i].username == username:
                        for n in range(0, len(self.posts)):
                            if self.users[i].dni == self.posts[n].dni_creator:
                                print(n)
                                self.posts[n].show()
                        opt = input('Ingrese el post con el que desea interactuar:  ')
                        for x, com in enumerate(self.posts[opt].comment, 1):
                            print(x, com)
                            op = int(input('Ingrese el comentario que desea eliminar:  '))
                            self.posts[opt].comment.pop(op)
                            self.deleted_comments.append(username)
                            print('Comentario eliminado con éxito')
                break
            except:
                print('Usuario no encontrado')
                break

    def delete_account_admin(self):

        # Función para el admin, permite eliminar cualquier cuenta del sistema

        while True:
            try:
                username = input('Ingrese el nombre de usuario:  ')
                for i in range(0, len(self.users)):
                    if self.users[i].username == username:
                        self.users.pop(i)
                        self.deleted_users.append(username)
                        print('Usuario eliminado con éxito')
                break
            except:
                print('Usuario no encontrado')
                break

    def admin(self):

        # Función de administrador (admin)
        # Le permite borrar cuentas, comentario y posts de cualquier usuario

        while True:
            print('''
            1. Eliminar post
            2. Eliminar comentario
            3. Eliminar usuario
            4. Salir
            ''')
            opt = input('Ingrese la opción que desea realizar:  ')
            while not opt.isnumeric() or int(opt) not in range(0,5):
                opt = input('Error! Ingrese una opción válida')
            if opt == '1':
                self.delete_post_admin()
            elif opt == '2':
                self.delete_comment_admin()
            elif opt == '3':
                self.delete_account_admin()
            else:
                break
        
    def user_more_posts(self):

        # Función de estadísticas, muestra los usuarios con mas posts

        pass

    def majors_more_posts(self):

        # Función de estadísticas, muestra las carreras universitarias con mas posts

        pass

    def posts_more_inter(self):

        # Función de estadísticas, muestra los posts con mas interacciones (likes y comentarios)

        pass

    def users_more_inter(self):

        # Función de estadísticas, muestra los usuarios con mas interacciones (likes y comentarios)

        pass

    def users_more_del_posts(self):

        # Función de estadística, muestra los usuarios que tengan posts eliminados por el admin

        for u in self.deleted_posts:
            print(u)

    def majors_more_incomm(self):

        # Función de estadísticas, muestra los usuarios que tengan comentarios eliminados por el admin

        pass

    def del_users(self):

        # Función de estadísticas, muestra los nombres de usuario de las cuentas que fueron eliminadas por el admin

        for u in self.deleted_users:
            print(u)

    def menu(self):

        # Función principal, el menú de la app
        # Es la función que dentro de ella, tiene todas las funciones del programa, es la que hace funcionar al código

        self.get_api_info()

        while True:
            print('''
            1. Registrarse
            2. Iniciar sesión
            3. Salir
            ''')
            op = input('Ingrese la opción que desea hacer:   ')
            while not op.isnumeric() or int(op) not in range(0, 5):
                op = input('Error! Ingrese una opción válida:  ')
            if op == '1':
                self.reg_new_users()

            elif op == '2':
                profile = self.login()
                print(profile)
                while True:
                    print('''
                    1. Subir publicación
                    2. Buscar perfil
                    3. Buscar publicación
                    4. Acceder a otra cuenta
                    5. Configuración de la cuenta
                    6. Estadísticas
                    7. Salir     
                    ''')
                    opt = input('Ingrese la acción que desea hacer:  ')
                    while not opt.isnumeric() or int(opt) not in range(1, 8):
                        opt = input('Error! Ingrese una opción válida:  ')
                    if opt == '1':
                        self.reg_post(profile)
                        
                    elif opt == '2':
                        self.search_profile(profile)

                    elif opt == '3':
                        self.search_post()

                    elif opt=='4':
                        profile = self.login()

                    elif opt == '5':
                        while True:
                            print('''
                            1. Cambiar información de la cuenta
                            2. Borrar comentario
                            3. Borrar información de la cuenta
                            4. Salir
                            ''')
                            option = input('Ingrese la opción que desea realizar":  ')
                            while not option.isnumeric() or int(option) not in range(1,5):
                                option = input('Error! Ingrese la opción que desea realizar":  ')
                            if option == '1':
                                self.change_info_users()
                            elif option == '2':
                                self.delete_comment(profile)
                            elif option == '3':
                                self.delete_data_account(profile)
                                self.reg_new_users()
                            else:
                                break
                    elif opt == '6':
                        while True:
                            print('''
                            Menú de estadísticas
                                  
                            1. Informe de Publicaciones
                            2. Informes de Interacción
                            3. Informes de Moderación
                            4. Salir''')
                            opc = input('Qué estadística desea revisar?: ')
                            while not opc.isnumeric() or int(opc) not in range(1,5):
                               opc = input('Error! Ingrese una opción válida: ')
                            if opc == '1':
                                while True:
                                    print('''
                                    Menú de Informe de Publicaciones
                                    1. Usuarios con mayor cantidad de publicaciones
                                    2. Carreras con mayor cantidad de publicaciones
                                    3. Salir
                                    ''')
                                    s = input('Ingrese el número de la estadística que desea ver:  ')
                                    while not s.isnumeric() or int(s) not in range(1,4):
                                        s = input('Error! Ingrese una opción válida:  ')
                                    if s == '1':
                                        self.user_more_posts()
                                    elif s =='2':
                                        self.majors_more_posts()
                                    else:
                                        break
                            elif opc == '2':
                                while True:
                                    print('''
                                    Menú de Informes de Interacción
                                        
                                    1. Post con más interacciones
                                    2. Usuarios con mayor interacciones
                                    3. Salir
                                    ''')
                                    w = input('Ingrese el número de la estadística que desea ver:  ')
                                    while not w.isnumeric() or int(w) not in range(1,4):
                                        w = input('Error! Ingrese una opción válida:  ')
                                    if w == '1':
                                        self.posts_more_inter()
                                    elif w =='2':
                                        self.users_more_inter()
                                    else:
                                        break
                            elif opc == '3':
                                while True:
                                    print('''
                                    Menú de Informes de Moderación
                                    1. Usuarios con más posts tumbados
                                    2. Carreras con más comentarios inadecuados
                                    3. Usuarios eliminados por infracciones
                                    4. Salir
                                    ''')
                                    f = input('Ingrese el número de la estadística que desea ver:  ')
                                    while not f.isnumeric() or int(f) not in range(1,5):
                                        f = input('Error! Ingrese una opción válida:  ')
                                    if f == '1':
                                        self.users_more_del_posts()
                                    elif f =='2':
                                        self.majors_more_incomm()
                                    elif f == '3':
                                        self.del_users()
                                    else:
                                        break
                            else:
                                break
                    else:
                        break
            elif op == '0':
                self.admin()
            else: 
                break
