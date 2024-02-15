from pathlib import Path
import shutil
from datetime import date, datetime, timedelta


base_dir = Path(__file__).parent.parent

sh_path = Path(base_dir, 'media', 'screenshots')

mock_image = str(Path(sh_path, 'img.png'))

folder = Path(sh_path, date.today().strftime("%Y-%m-%d"))
if not folder.exists():
    folder.mkdir()

delta = timedelta(minutes=1)
cur_date = datetime(year=2024, month=2, day=12)
for i in range(0, 400):
    name = cur_date.strftime("%Y_%m_%dT%H_%M") + '.png'
    img_path = Path(folder, name)
    shutil.copyfile(mock_image, img_path)
    cur_date += delta


