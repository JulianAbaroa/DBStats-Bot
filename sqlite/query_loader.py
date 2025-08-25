# sqlite/query_loader.py
import difflib
import os
from pathlib import Path

class QueryLoader:
    def __init__(self, base_path: str | Path = None):
        """
        Por defecto busca en <this_file_folder>/player_queries.
        """
        if base_path is None:
            self.base_path = Path(__file__).resolve().parent / "player_queries"
        else:
            self.base_path = Path(base_path)
        self.queries: dict[str, str] = {}
        self._load_queries()

    def _load_queries(self):
        if not self.base_path.exists():
            raise FileNotFoundError(f"Queries folder no encontrada: {self.base_path.resolve()}")
        duplicates = []
        for filepath in self.base_path.rglob("*.sql"):
            content = filepath.read_text(encoding="utf-8").strip()
            stem_key = filepath.stem  # nombre del archivo sin extensión
            # clave basada en la ruta relativa, con separadores cambiados por underscore
            rel_key = str(filepath.relative_to(self.base_path).with_suffix(""))
            # Normalizar separadores independientemente de la plataforma:
            rel_key = rel_key.replace("/", "_").replace("\\", "_")

            # Si no existe la clave por stem, úsala.
            if stem_key not in self.queries:
                self.queries[stem_key] = content
            else:
                duplicates.append((stem_key, rel_key, filepath))
                if rel_key not in self.queries:
                    self.queries[rel_key] = content
                # No sobreescribimos la clave stem para mantener compatibilidad

        if duplicates:
            print("QueryLoader: archivos .sql con nombres duplicados (mismo stem).")
            for stem, rel, fp in duplicates:
                print(f"  - {fp} -> stem='{stem}' (ya existe), agregado rel_key='{rel}'")

    def list(self) -> list[str]:
        """Devuelve las claves disponibles (ordenadas)."""
        return sorted(self.queries.keys())

    def get(self, name: str) -> str:
        """Retorna la query o lanza KeyError con sugerencias."""
        if name in self.queries:
            return self.queries[name]
        close = difflib.get_close_matches(name, self.queries.keys(), n=5, cutoff=0.4)
        suggestion = f" Did you mean: {', '.join(close)}?" if close else ""
        raise KeyError(f"Query '{name}' no encontrada en {self.base_path.resolve()}.{suggestion}")
