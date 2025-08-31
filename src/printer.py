import subprocess
from abc import ABC, abstractmethod

class IPrinter(ABC):
    @abstractmethod
    def print_file(self, file_path: str):
        pass

class CupsPrinter(IPrinter):
    def __init__(self, printer_name: str = ""):
        self.printer_name = printer_name

    def print_file(self, file_path: str):
        if self.printer_name:
            subprocess.run(['lp', '-P', self.printer_name, file_path], check=True)
        else:
            subprocess.run(['lp', file_path], check=True)