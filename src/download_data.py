"""Optional source refresh. Verify bytes before replacing bundled raw files."""
import hashlib
import io
import json
import urllib.request
import zipfile
from .pipeline import ROOT

URL='https://archive.ics.uci.edu/static/public/198/steel+plates+faults.zip'
def main():
    manifest=json.loads((ROOT/'data/source_manifest.json').read_text())
    with urllib.request.urlopen(URL,timeout=60) as response:
        archive=zipfile.ZipFile(io.BytesIO(response.read()))
    verified={}
    for name, expected in manifest['sha256'].items():
        content=archive.read(name)
        if hashlib.sha256(content).hexdigest()!=expected:
            raise ValueError(f'Source changed: {name}. Review it before updating the manifest.')
        verified[name]=content
    for name,content in verified.items():(ROOT/'data/raw'/name).write_bytes(content)
    print('Source downloaded and verified.')
if __name__=='__main__':main()
