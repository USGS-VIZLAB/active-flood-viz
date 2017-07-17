# active-flood-viz

### Configuration Files

Settings specific to a single event are stored in an `instance/` directory which is not tracked by git.
Create this directory in the root project directory and then create the file `instance/config.py`.
This will store any event-specific settings.
The `examples/` directory contains files for example event settings.
Copy and paste the contents of one of these files into `instance/config.py` to use these settings.

### Docker Instructions

Currently, our dockerfile creates an image for a container that freezes the basic flask app and then runs a server using
the frozen files. 

**To build the image:**
1. Navigate to your project directory.
1. Put your configuration parameters in 'instance_config.py' and copy into this directory.
1. Put the rivers.json file in `floodviz/static/geojson/rivers.json` (temporary step)
1. Copy `DOIRootCA2.cer` into this directory.
1. Run `docker build --rm -t flood .`. This will create the docker image and name it `flood`.

**To run a container based on the image:**
1. `docker run -p 80:80 -t --name floodviz flood`. This will create a docker container from the `flood` image and name it `floodviz`.


Once this is done, [127.0.0.1](http://127.0.0.1) should take you to the example page.

