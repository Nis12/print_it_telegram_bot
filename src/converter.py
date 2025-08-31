import subprocess
import os
from abc import ABC, abstractmethod

class IFileConverter(ABC):
    @abstractmethod
    def convert_to_pdf(self, file_path: str) -> str | None:
        pass

class LibreOfficeConverter(IFileConverter):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def convert_to_pdf(self, file_path: str) -> str | None:
        try:
            pdf_name = os.path.splitext(os.path.basename(file_path))[0] + '.pdf'
            pdf_path = os.path.join(self.output_dir, pdf_name)
            cmd = [
                'libreoffice', '--headless', '--convert-to', 'pdf',
                '--outdir', self.output_dir, file_path
            ]
            subprocess.run(cmd, check=True, timeout=60)
            return pdf_path if os.path.exists(pdf_path) else None
        except Exception as e:
            print(f"Conversion error: {e}")
            return None
