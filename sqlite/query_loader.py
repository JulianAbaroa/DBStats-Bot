from pathlib import Path
import difflib

class QueryLoader:
    def __init__(self, base_paths: str | Path | list[str | Path] = None):
        """
        If not specified, searches in <this_file_folder>/player_queries.
        You can also pass a list of paths to search for queries in multiple directories.
        """
        if base_paths is None:
            self.base_paths = [Path(__file__).resolve().parent / "player_queries"]
        elif isinstance(base_paths, (str, Path)):
            self.base_paths = [Path(base_paths)]
        else:
            self.base_paths = [Path(p) for p in base_paths]

        self.queries: dict[str, str] = {}
        self._load_queries()

    def _load_queries(self):
        duplicates = []
        for base_path in self.base_paths:
            if not base_path.exists():
                print(f"QueryLoader: directory not found: {base_path.resolve()}")
                continue

            for filepath in base_path.rglob("*.sql"):
                content = filepath.read_text(encoding="utf-8").strip()
                stem_key = filepath.stem
                rel_key = str(filepath.relative_to(base_path).with_suffix(""))
                rel_key = rel_key.replace("/", "_").replace("\\", "_")

                if stem_key not in self.queries:
                    self.queries[stem_key] = content
                else:
                    duplicates.append((stem_key, rel_key, filepath))
                    if rel_key not in self.queries:
                        self.queries[rel_key] = content

        if duplicates:
            print("QueryLoader: files .sql with duplicated names (same stem).")
            for stem, rel, fp in duplicates:
                print(f"  - {fp} -> stem='{stem}' (already exists), added rel_key='{rel}'")

    def list(self) -> list[str]:
        """Returns the available keys (ordered)."""
        return sorted(self.queries.keys())

    def get(self, name: str) -> str:
        """Returns the query or throws KeyError with suggestions."""
        if name in self.queries:
            return self.queries[name]
        close = difflib.get_close_matches(name, self.queries.keys(), n=5, cutoff=0.4)
        suggestion = f" Did you mean: {', '.join(close)}?" if close else ""
        raise KeyError(f"Query '{name}' not found. {suggestion}")