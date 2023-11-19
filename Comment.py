class Comment():
    def __init__(self, user, comment, date):
        self.user = user
        self.comment = comment
        self.date = date

    def show_comment(self):
        f'''
{self.user}
{self.comment}                  {self.date}
'''
        


        