class Post:
    def __init__(self, dni_creator, caption, hashtag, date, kind, multimedia, like, comment):
        self.dni_creator = dni_creator
        self.caption = caption
        self.hashtag = hashtag
        self.date = date
        self.like = like
        self.comment = comment
        self.kind = kind
        self.multimedia = multimedia


    def show(self):
        return f'''
{self.dni_creator}

{self.kind}    


{self.multimedia}

❤️  {len(self.like)}    💬  {len(self.comment)}             {self.date}

{self.caption}
{self.comment}






'''