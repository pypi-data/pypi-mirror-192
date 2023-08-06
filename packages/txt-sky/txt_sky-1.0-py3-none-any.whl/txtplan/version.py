def get_version():
    import os
    from pathlib import Path
    txt="version.mx"
    extension = Path(txt).suffix
    filename=os.path.split(txt)
    fiesion=os.path.splitext(extension)
    newname="version.txt"
    os.rename(txt,newname)
    with open(newname,"r") as r:
        version=r.read()
    txt="version.txt"
    extension = Path(txt).suffix
    filename=os.path.split(txt)
    fiesion=os.path.splitext(extension)
    newname="version.mx"
    os.rename(txt,newname)
    return version
