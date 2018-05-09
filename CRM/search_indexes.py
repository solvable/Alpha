import datetime
from haystack import indexes
from .models import Customer, Jobsite, Ticket


class CustomerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    fullName = indexes.CharField(model_attr='fullName')
    lastName = indexes.CharField(model_attr='lastName')
    firstName = indexes.CharField(model_attr='firstName')
    billStreet = indexes.CharField(model_attr='billStreet')
    billCity = indexes.CharField(model_attr='billCity')
    billState = indexes.CharField(model_attr='billState')
    billZip = indexes.CharField(model_attr='billZip')
    phone1 = indexes.CharField(model_attr='phone1')
    email = indexes.CharField(model_attr='email')
    source = indexes.CharField(model_attr='source')

    def get_model(self):
        return Customer

    # def index_queryset(self, using=None):
    #     """Used when the entire index for model is updated."""
    #     return self.get_model().objects.filter(created=datetime.datetime.now())
    def index_queryset(self, using=None):
        return self.get_model().objects.all()