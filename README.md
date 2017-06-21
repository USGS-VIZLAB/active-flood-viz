# active-flood-viz

### Docker Instructions

Currently, our dockerfile creates an image for a container that runs the basic flask app. 

**To build the image:**
1. Navigate to your project directory.
1. Copy `DOIRootCA2.cer` into this directory.
1. Run `docker build -t flood .`. This will create the docker image and name it `flood`.

**To run a container based on the image:**
1. 