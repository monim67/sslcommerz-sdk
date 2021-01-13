from abc import ABC, abstractmethod


class AbstractORMAdapter(ABC):
    def create_session_instance(self, model, **kwargs):
        return model(**kwargs)

    @abstractmethod
    def get_session_instance_by_pk(self, model, pk):
        pass

    @abstractmethod
    def get_session_instance_iterator(self, model, tran_id, status_list):
        pass

    def save_session_instance(self, model, instance, **kwargs):
        instance.save()
