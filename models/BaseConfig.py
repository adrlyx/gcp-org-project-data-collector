from genericpath import exists
import configparser


class BaseConfig:
    CONFIG_FILE = '../gcp-org-project-data-collector/.env'

    def __init__(self):
        if not exists(BaseConfig.CONFIG_FILE):
            raise Exception(".env", "See README.md for instructions")

        self._config = configparser.ConfigParser()
        self._config.read(BaseConfig.CONFIG_FILE)

        self.organization = self._config["ENV"]["ORG_ID"]
