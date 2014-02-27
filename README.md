Lagooned
========

A game brought to you by CMU's [Game Creation Society](http://www.gamecreation.org/).

Setup
------
1. Install [pip](http://www.pip-installer.org/en/latest/), [npm](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager), [bower](http://bower.io/), and [sass](http://sass-lang.com/install).
2. Clone this repository: `git clone git@github.com:willcrichton/lagooned.git`
3. Run `cd lagooned`
4. Run `bower install` and `pip install -r requirements.txt`.
5. Run `python server.py`
6. In your browser, go to [localhost:5000](http://localhost:5000).

Styling
------
To make changes to the stylesheet, you need to edit the style.scss file and convert it to a .css file by running `sass style.scss > style.css` inside of the `static/css/` directory.

Code Goals
------
Current objectives:
- Have actions synced between SQLAlchemy and front-end (figure out REST architecture)
- Implement decision tree on the backend
- Implement a UI
