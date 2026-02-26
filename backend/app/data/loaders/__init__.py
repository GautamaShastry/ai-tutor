# Data loaders for different sources
from app.data.loaders.base import BaseLoader
from app.data.loaders.tatoeba import TatoebaLoader
from app.data.loaders.custom import CustomLoader
from app.data.loaders.samanantar import SamanantatLoader

__all__ = ["BaseLoader", "TatoebaLoader", "CustomLoader", "SamanantatLoader"]
