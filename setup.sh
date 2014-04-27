bower install
sudo pip install -r requirements.txt
cd static/css
make
cd ../../
python -c 'from server import db; db.create_all()'
