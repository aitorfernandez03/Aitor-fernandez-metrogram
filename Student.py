from User import User

class Student(User):
    def __init__(self,dni , name, last_name, email, username, posts, following, kind, major):
        super().__init__(dni, name, last_name, email, username, posts, following)
        self.kind = kind
        self.major = major

    
    def show(self):
        return f'''
        {self.username}
        {self.name}  {self.last_name}
        
        {self.kind}               Publicaciones                Seguidores
        {self.major} ...............{len(self.posts)}...........{len(self.following)}
        
        
        {print(self.show_posts())}
        
        
        '''
        
    def show_posts(self):
        count = 1
        for post in self.posts:
            print(f'{count}. {post.show()}')
            count += 1
        return "------------------------"