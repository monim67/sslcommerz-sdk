from .base import AbstractQuerySetBuilder


class DjangoQuerySetBuilder(AbstractQuerySetBuilder):
    @classmethod
    def from_model(cls, model):
        return cls(model.objects.all())

    def create_model_instance(self, model, **kwargs):
        return model(**kwargs)

    def save_model_instance(self, model, instance):
        instance.save()

    def filter(self, **kwargs):
        return DjangoQuerySetBuilder(self.queryset.filter(**kwargs))

    def filter_in(self, **kwargs):
        in_kwargs = {f"{key}__in": value for key, value in kwargs.items()}
        return DjangoQuerySetBuilder(self.queryset.filter(**in_kwargs))

    def exists(self, *args, **kwargs):
        return self.queryset.count(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self.queryset.count(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.queryset.get(*args, **kwargs)

    def first(self, *args, **kwargs):
        return self.queryset.first(*args, **kwargs)

    def all(self):
        return self.queryset.all()

    def __iter__(self):
        return iter(self.queryset.all())
