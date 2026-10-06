import json

from repository.cache_repository import snapshot


class CacheExporter:
    def __init__(self, entries: dict):
        self.entries = entries

    @classmethod
    def from_cache(cls) -> "CacheExporter":
        return cls(snapshot())

    def save_to_file(self, fp, sep=b'\n'):
        n = 0
        for text, result in self.entries.items():
            fp.write(json.dumps({"text": text, **result}).encode("utf-8"))
            fp.write(sep)
            n += 1
        return n

    def save_to_filename(self, file_name, sep=b'\n'):
        """
        Write all cached results to a local file.
        Results are written to the file and the 'sep' string is written
        in between results.
        Returns the number of results saved.
        """
        fp = open(file_name, 'wb')
        n = self.save_to_file(fp, sep)
        fp.close()
        return n
