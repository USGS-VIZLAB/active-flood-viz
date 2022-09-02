# active-flood-viz
[![Build Status](https://travis-ci.org/USGS-VIZLAB/active-flood-viz.svg?branch=master)](https://travis-ci.org/USGS-VIZLAB/active-flood-viz)

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
1. Copy `DOIRootCA2.cer` into this directory.
1. Run `docker build --build-arg config=examples/iowa.py --build-arg ref=examples/reference.json --build-arg thumbnail=true  -t flood:latest -f Dockerfile-DOI .`. This will create the docker image and name it `flood`.
If you are building the image off of the DOI network, you will need to specify Dockerfile rather than Dockerfile-DOI in the above command

**To run a container based on the image:**
1. `docker run --rm -dp 80:80 -t flood:latest`. This will create a docker container from the `flood` image

Once this is done, [127.0.0.1](http://127.0.0.1) should take you to the example page.

## Disclaimer

This software is in the public domain because it contains materials that originally came from the U.S. Geological Survey, an agency of the United States Department of Interior. For more information, see the official USGS copyright policy at [http://www.usgs.gov/visual-id/credit_usgs.html#copyright](http://www.usgs.gov/visual-id/credit_usgs.html#copyright)

This information is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The information has not received final approval by the U.S. Geological Survey (USGS) and is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the information. Although this software program has been used by the USGS, no warranty, expressed or implied, is made by the USGS or the U.S. Government as to the accuracy and functioning of the program and related program material nor shall the fact of distribution constitute any such warranty, and no responsibility is assumed by the USGS in connection therewith.

This software is provided "AS IS."


[
  ![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png)
](http://creativecommons.org/publicdomain/zero/1.0/)
