# Utility Repo for Showing ply Point Clouds in Viser

# Installation

I like to use `uv` to manage python environments and packages. However, if you prefer using normal `pip`, that should work too.

## Installation using uv

Navigate to the cloned repo and type

```bash
uv sync
```
It creates a venv and downloads the dependencies

## Installation using pip

Create and activate a venv
```bash
python3 -m venv .venv
. .venv/bin/activate
```
Install the project and the dependencies
```bash
pip install -e .
```

# Usage

If not done already, activate the venv
```bash
. .venv/bin/activate
```
Run the visualisation script and pass the path of the file you would like to visualise.
```bash
python show.py point_clouds/engine_room_01.ply
```
This opens a local server that you can connect to through your browser by simply clicking on the link (likely http://localhost:8080)
You can navigate using the left, right, and centre mouse buttons or using the arrow keys and A, S, D, W keys on your keyboard.

Enjoy :)
