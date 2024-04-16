class api_config:

    def __init__(self):
        self._config = dict()

        try:
            api = import_model
