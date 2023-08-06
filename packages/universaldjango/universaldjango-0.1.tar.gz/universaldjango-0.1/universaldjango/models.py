from django.db import models

# Create your models here.
class Donnee(models.Model):
    colonne_id = models.IntegerField()
    value = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)

class Colonne(models.Model):
    table = models.ForeignKey(Donnee, on_delete=models.CASCADE)
    value = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)

class Enregistrement(models.Model):
    table = models.ForeignKey(Donnee, on_delete=models.CASCADE)

class Relation(models.Model):
    origine = models.ForeignKey(Enregistrement, on_delete=models.CASCADE)
    destination = models.ForeignKey(Donnee, on_delete=models.CASCADE)

class Universal:
    attributes = []
    compteur = 0
    def get_property(self):
        return self.attributes
    
    def migrate(self):
        self.compteur = 0
        props = self.get_property()
        donnees = Donnee.objects.filter(value=self.__class__.__name__, colonne_id=-1)
        
        if not donnees.exists():
            data = Donnee(colonne_id=-1, value=self.__class__.__name__)
            data.save()
            donnees = Donnee.objects.filter(value=self.__class__.__name__, colonne_id=-1).first()
            for element in self.attributes:
                col = Colonne(table=donnees, value=element)
                col.save()
            return donnees
        return donnees.first()
    
    def create(self, dict_data):
        table = self.migrate()
        record = Enregistrement(table=table)
        record.save()
        for key, val in dict_data.items():
            donnee = Donnee(colonne_id=Colonne.objects.filter(value=key, table=table).first().id, value=val)
            donnee.save()
            relation = Relation(origine=record, destination=donnee)
            relation.save()
        return record
    def format(self, record):
        data = {}
        count = self.compteur
        self.compteur = count+1
        data['id']=count
        relations = Relation.objects.filter(origine=record).all()
        for element in relations:
            data[Colonne.objects.filter(id=element.destination.colonne_id).first().value] = element.destination.value
        return data
    
    def all(self):
        table = self.migrate()
        record = Enregistrement.objects.filter(table=table).all()
        record = [self.format(el)  for el in record]
        

        return record
    def get(self, id):
        table = self.migrate()
        if Enregistrement.objects.filter(table=table).count()<=id:
            return []
        record = Enregistrement.objects.filter(table=table).all()
        i = 0
        for el in record:
            if(id==i):
                element = self.format(el)
                element['id'] = id
                return element
            i = i+1
        return []
    
    def update(self, data_dict, id):
        table = self.migrate()
        record = Enregistrement.objects.filter(table=table).all()
        i=0
        for el in record:
            if(i==id):
                target_record = el
                relations = Relation.objects.filter(origine=target_record).all()
                for element in relations:
                    element.destination.value = data_dict[Colonne.objects.filter(id=element.destination.colonne_id).first().value]
                    element.destination.save()
            i = i+1

    def delete(self, id):
        table = self.migrate()
        record = Enregistrement.objects.filter(table=table).all()
        i=0
        for el in record:
            if(i==id):
                target_record = el
                relations = Relation.objects.filter(origine=target_record).all()
                for element in relations:
                    element.destination.delete()
                    element.delete()
            i = i+1
            el.delete()
            return ''
        

            



class Article(Universal):
    attributes = ["auteur", "title", "content"]
   
    


