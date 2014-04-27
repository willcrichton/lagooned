Lagooned
========

A game brought to you by CMU's [Game Creation Society](http://www.gamecreation.org/).

Setup
------
1. Install [pip](http://www.pip-installer.org/en/latest/), [npm](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager), [bower](http://bower.io/), and [sass](http://sass-lang.com/install).
2. Clone this repo: `git clone git@github.com:willcrichton/lagooned.git`
3. Run `cd lagooned`
4. Run `./setup.sh`
5. Run `./run.sh`
6. Visit [localhost:5000](http://localhost:5000).

Styling
------
To make changes to the stylesheet, you need to edit the style.scss file and convert it to a .css file by running `make` inside of the `static/css/` directory.

Code Goals
------
Current objectives:
- Have actions synced between SQLAlchemy and front-end (figure out REST architecture)
- Implement decision tree on the backend
- Implement a UI
