from abc import ABC, abstractmethod


class AbstractQuerySetBuilder(ABC):
    def __init__(self, queryset):
        self.queryset = queryset

    @classmethod
    @abstractmethod
    def from_model(cls, model):
        pass

    @abstractmethod
    def create_model_instance(self, model, **kwargs):
        pass

    @abstractmethod
    def save_model_instance(self, model, instance):
        pass

    @abstractmethod
    def filter(self, **kwargs):
        pass

    @abstractmethod
    def filter_in(self, **kwargs):
        pass

    @abstractmethod
    def exists(self, *args, **kwargs):
        pass

    @abstractmethod
    def count(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass
