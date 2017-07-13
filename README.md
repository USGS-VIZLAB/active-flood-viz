# active-flood-viz

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
1. `docker run -p 5055:5050 -t --name floodviz flood`. This will create a docker container from the `flood` image and name it `floodviz`.


Once this is done, [127.0.0.1:5055](http://127.0.0.1:5055) should take you to the example page.

