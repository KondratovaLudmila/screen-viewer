import os
import django
from pathlib import Path
from datetime import date, datetime
from PIL import Image

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screen_viewer.settings")
django.setup()

from viewer.models import Location, Screenshot
from users.models import User
#from screen_viewer.screen_viewer import settings

BASE_DIR = Path(__file__).parent.parent.joinpath('media')

class ScrrenshotHandler:

    def __init__(self):
        self.user = User.objects.get(pk=1)
        self.locations = Location.objects.all()
        


if __name__ == "__main__":
    locations = Location.objects.all()
    user = User.objects.get(pk=1)
    for location in locations:
        screen_date = date.today()
        folder_path = Path(BASE_DIR, 
                            location.path, 
                            screen_date.strftime("%Y-%m-%d"))
        if not folder_path.exists():
            continue
        
        for file in folder_path.iterdir():
            if not file.is_file():
                continue
            if "_thmb" in file.stem:
                continue
            path = Path(location.path, screen_date.strftime("%Y-%m-%d"), file.name)
            img_created_at = datetime.strptime(file.stem, "%Y_%m_%dT%H_%M")
            thmb_path = Path(file.parent, file.stem + "_thmb.png")
            thmb = Image.open(file).copy()
            thmb.thumbnail((800, 800))
            thmb.save(thmb_path)
            try:
                Screenshot.objects.create(screen_date=screen_date, 
                                            path=path.as_posix(), 
                                            location=location, 
                                            img_created_at=img_created_at,
                                            thmb_path=thmb_path,
                                            user=user)
            except Exception as err:
                print(err)

            
                
