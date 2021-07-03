from pathlib import Path
import re
import shutil

pycache_pattern = r'__pycache__$'
mgrtions_pattern = r'00\d.+_\w.*\.py$'
sqlitedb_pattern = r'.sqlite3$'


dirs = [str(i) for i in Path.cwd().glob('**')]

for item in dirs:
    if re.search(pycache_pattern, item) and Path(item).is_dir():
        shutil.rmtree(Path(item))
        print('__pycaches__\t', item)

    if Path(item).exists():
        for child in Path(item).iterdir():
            if re.search(mgrtions_pattern, str(child)):
                Path(child).unlink(missing_ok=True)
                print('migrations files\t', child)



for file in Path.cwd().iterdir():
    if re.search(sqlitedb_pattern, str(file)):
        Path(file).unlink(missing_ok=True)
        print('sqlite3 db\t', file)