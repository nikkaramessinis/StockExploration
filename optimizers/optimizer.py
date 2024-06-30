from abc import ABC, abstractmethod
from typing import Dict, Any

class Optimizer:
    def __init__(self, strategy, stocks_list):
        self.strategy = strategy
        self.stocks_list = stocks_list

    @abstractmethod
    def optimize(self) -> Dict[str, Any]:
        pass