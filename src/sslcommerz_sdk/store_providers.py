class SingleStoreProvider:
    def __init__(self, store):
        self._store = store

    def get_store_by_id(self, store_id):
        if store_id != self._store.id:
            raise Exception(f"Invalid store id: {store_id}")
        return self._store

    def validate_store(self, store):
        if store.id != self._store.id:
            raise Exception(f"Invalid store id: {store.id}")


class MultpleStoreProvider:
    def __init__(self, get_store_by_id, validate_store=None, **kwargs):
        if not callable(get_store_by_id):
            raise Exception(f"Invalid callable get_store_by_id: {get_store_by_id}")
        if validate_store and not callable(validate_store):
            raise Exception(f"Invalid callable validate_store: {validate_store}")
        self._callables = {
            "get_store_by_id": get_store_by_id,
            "validate_store": validate_store,
        }

    def get_store_by_id(self, store_id):
        return self._callables["get_store_by_id"](store_id)

    def validate_store(self, store):
        if self._callables["validate_store"] is not None:
            self._callables["validate_store"](store)
