import json
import yaml

from pydantic import ValidationError

from .exceptions.authenticator_exc import ConfigLoadException, ConfigLoadValidationException
from .login_provider import LoginProvider
from .models.config import ConfigData

DEFAULT_CONFIG_FNAME = 'data/config.json'

class Config:
    fname: str
    data: ConfigData
    
    def __init__(self, fname = DEFAULT_CONFIG_FNAME):
        self.fname = fname
        self.load()

    def load(self):
        try:
            with open(self.fname, 'r') as out:
                config = json.loads(out.read())
            
            self.data = ConfigData(**config)

        except ValidationError:
            raise ConfigLoadValidationException(self.fname)

        except Exception:
            raise ConfigLoadException(self.fname)
        
        
class ConfigYaml(Config):
    def load(self):
        try:
            with open(self.fname, 'rb') as out:
                config = yaml.safe_load(out)
            
            self.data = ConfigData(**config)

        except ValidationError:
            raise ConfigLoadValidationException(self.fname)

        except Exception as e:
            raise ConfigLoadException(self.fname)
    

class Authenticator:
    config: Config
    config_fname = DEFAULT_CONFIG_FNAME
    provider: LoginProvider

    def __init__(self, config_fname=DEFAULT_CONFIG_FNAME, provider=LoginProvider()):
        
        self.config_fname = config_fname
        
        if self.config_fname.find('.yml') != -1 or self.config_fname.find('.yaml') != -1:
            self.config = ConfigYaml(config_fname)
        else:
            self.config = Config(config_fname)
        
        self.provider = provider
    
    def login(self):
        email = self.config.data.lisensi.email
        password = self.config.data.lisensi.pwd
        return self.provider.login(email, password)