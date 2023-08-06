class Universal:
    attributes = []
    def get_property(self):
        print(self.__class__.__name__)
        for e in self.attributes:
            print(e)
   

class Article(Universal):
    attributes = ["title", "author", "content"]

univer = Article()
univer.get_property()