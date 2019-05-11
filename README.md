# Computer Vision Project

This is the repository holding the source code for Computer Vision project Spring 2019.

This Computer Vision project aimed to build a virtual Ping-pong game (called ‘pong’ for short) based on video motion detection using optical flow. We use the camera on a laptop for image capturing and the screenshot of color (blue and green) on a mobile device for input recognition and controlling the racquets.  Kalman filters are used for smooth and continuous motion of the racquets. Players can play it with their own with computers through the internet. The program was experimented under different conditions, including using different objects, speeds, and background. 

# Usage
```
git clone https://github.com/TerminalWitchcraft/cvproj
cd src
python3 main.py  --sender [name1] --receiver [name2]
```
naem1 and name2 should be the same for two players.

# Project Structure

All source code reside under `src` directory. 

All media assets reside under `assests` directory.

All build files should go under `build` directory.

Always run the project from the root directory, so that there in no conflict in imports

The `src` structure is shown below:

```bash
├── assets
│   └── DONOTOPEN
├── Makefile
├── README.md
├── run.py
└── src
    ├── motion
    │   └── __init__.py
    ├── physics
    │   └── __init__.py
    ├── server
    │   └── __init__.py
    ├── ui
    │   └── __init__.py
    └── utilities
        └── __init__.py
```

* `motion` module contains code related to optical flow
* `physics` module contains code related to game physics
* `server` module is responsible for communication between two instances of the game
* `ui` module contains all graphical components
* `utilities` contains _*functions*_ used by all modules 

# Notes

Please use _*spaces*_ instead of tabs, configure your editor accordingly

# Authors


[Aral](ahh335@nyu.edu)
[Kartikeya](kn1481@nyu.edu)
[Hitesh](hp1293@nyu.edu)
[Sherry](hrc304@nyu.edu)
