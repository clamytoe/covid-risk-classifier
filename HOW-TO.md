# Covid Risk Classifier

```bash
 ▄████████  ▄█          ▄████████   ▄▄▄▄███▄▄▄▄   ▄██   ▄       ███      ▄██████▄     ▄████████ 
███    ███ ███         ███    ███ ▄██▀▀▀███▀▀▀██▄ ███   ██▄ ▀█████████▄ ███    ███   ███    ███ 
███    █▀  ███         ███    ███ ███   ███   ███ ███▄▄▄███    ▀███▀▀██ ███    ███   ███    █▀  
███        ███         ███    ███ ███   ███   ███ ▀▀▀▀▀▀███     ███   ▀ ███    ███  ▄███▄▄▄     
███        ███       ▀███████████ ███   ███   ███ ▄██   ███     ███     ███    ███ ▀▀███▀▀▀     
███    █▄  ███         ███    ███ ███   ███   ███ ███   ███     ███     ███    ███   ███    █▄  
███    ███ ███▌    ▄   ███    ███ ███   ███   ███ ███   ███     ███     ███    ███   ███    ███ 
████████▀  █████▄▄██   ███    █▀   ▀█   ███   █▀   ▀█████▀     ▄████▀    ▀██████▀    ██████████ 
           ▀                                                                                    
```

## Setting up environment

The first thing to do is to replicate the virtual environment.
The project uses Python 3.10.6.
In order to get things to work correctly, I recommend that you duplicate it as best as possible.

### Anaconda workflow

If you are using Anaconda, I got you fam.
Just run the following commands:

```bash
conda env create .
```

Then activate the environment and install the rest of the required packages:

```bash
conda activate py310
pipenv install --dev
```

### Different workflow

If you're working in this field then you should be able to figure out how to get Python 3.10.6 installed.
Once you have the right verion of Python, you can either install the dependencies with the `requirements.txt` file or install pipenv and do the same as above for the conda install.

> **NOTE:** I recommend that you use a virtual environment.

```bash
pip install -r requirements.txt
```

## Scripts provided

I have included some scripts to be used alongside the service:

* `train.py` - Generates a pickled version of the model.
* `create_bento_model.py` - Generates bentoml model from the pickled model.
* `service.py` - Runs the service.
* `predict.py` - Tests the service by generating some predictions.
* `locustfile.py` - For load testing the service.
* `Makefile` - Used to run all of the above and more.

### Makefile

The Makefie will simplify the use of this project:

```make
make help
Makefile for generating and deploying the covid risk classifier model

Usage:
   make help                           prints this message
   make all                            runs through the whole process
   make classifier                     creates a new bentoml classifier
   make clean                          remove the generated files
   make debug                          prints all of the variables used
   make docker                         creates a new docker image
   make model                          creates a new bentoml model
   make predict                        tests some sample predictions
   make push                           pushes docker image to docker hub
   make serve                          start the server for development
   make serve-docker                   start the server from docker image
   make shell                          open a shell in running container
   make tag                            tags the new docker image
   make train                          (re)trains the model
   make -n                             prints the commands without
                                       executing them

Example:
   make -n train                       would display the command for
                                       training a new model
```

If you want to go from nothing to running the service locally, just use the `make` command by itself:

```text
make
Training and saving the model...
Generating bentoml model from xgboost_eta=0.3_max_depth=5_min_child_weight=1.bin...
Generating classifier from latest covid_risk_model\:k5afpns3gogiq567...
Starting classifier service for development...
```

> **NOTE:** When running the commands `make docker` and `make tag`, make sure that you expand your terminal window!

While testing, I noticed that if my terminal window isn't expanded, that the bentoml classifier name will get truncated and the end will be replaced with three periods:

```bash
bentoml list
 Tag                               Size        Creation Time        Path
 covid_risk_classifier:pjzbhhs4t…  434.57 KiB  2022-11-04 18:29:19  ~/bentoml/bentos/covid_risk_cla…
 covid_risk_classifier:o5dyi3c3g…  431.65 KiB  2022-11-02 23:53:45  ~/bentoml/bentos/covid_risk_cla…
 ```

 Once expanded, I get this:

 ```bash
 bentoml list
 Tag                                     Size        Creation Time        Path
 covid_risk_classifier:pjzbhhs4tcmkax6a  434.57 KiB  2022-11-04 18:29:19  ~/bentoml/bentos/covid_risk_classifier/pjzbhhs4tcmkax6a
 covid_risk_classifier:o5dyi3c3gotjoliq  431.65 KiB  2022-11-02 23:53:45  ~/bentoml/bentos/covid_risk_classifier/o5dyi3c3gotjoliq
 ```

 You can verify that your names aren't being truncated by running `make debug`:

 ```bash
make debug
Rule -> debug
              USER: clamytoe
           PROJECT: covid_risk
     BENTOML_MODEL: covid_risk_model\:pezox2c4tchdcgky
BENTOML_CLASSIFIER: covid_risk_classifier\:pjzbhhs4tcmkax6a
      DOCKER_IMAGE: covid_risk_classifier\:pjzbhhs4tcmkax6a_docker
         CONTAINER:
          MY_IMAGE: clamytoe/covid_risk_classifier\:latest
            PICKLE: xgboost_eta=0.3_max_depth=5_min_child_weight=1.bin
```

### train.py

This script will train and save the model as a pickle file.

```bash
python train.py
saved: xgboost_eta=0.3_max_depth=5_min_child_weight=1.bin
```

> It can also generate 10 randomly selected patients along with their predictions and actual values.
This is useful for testing and can be enabled by uncommenting that portion of the code.
*Line 863.*

### create_bento_model.py

This script will create a local bentoml model from the exported pickle file.

```bash
python create_bento_model.py
Model(tag="covid_risk_model:djsbjtk2jcaladg5")
```

> If you have more than one pickled model saved, it will use the most recent one.

#### Confirm that your model has been created

You can confirm that your model has been created with this command:

```bash
bentoml models list
 Tag                                   Module           Size        Creation Time
 covid_risk_model:djsbjtk2jcaladg5     bentoml.xgboost  742.06 KiB  2022-11-01 19:48:44
 ```

To get more information on your model:

```yaml
bentoml models get covid_risk_model:djsbjtk2jcaladg5
name: covid_risk_model
version: rgvdhgs2noldydg5
module: bentoml.xgboost
labels:
  owner: Martin Uribe
  email: clamytoe@gmail.com
  stage: dev
options:
  model_class: Booster
metadata: {}
context:
  framework_name: xgboost
  framework_versions:
    xgboost: 1.6.2
  bentoml_version: 1.0.7
  python_version: 3.10.6
signatures:
  predict:
    batchable: false
api_version: v2
creation_time: '2022-11-02T05:02:23.599680+00:00'
```

### service.py

This is the script that runs the actual classifier and should start automatically if you're using the docker image.

#### Start the bentoml service manually

To start the service locally, run the following command:

```bash
bentoml serve service:svc --production
```

Simply open up a browser and navigate to [http://localhost:3000](http://localhost:3000) to test out the service manually.

The data that it takes is in `json` format and should be formated like this:

```json
{
  "state": "tx",
  "age_yrs": 52,
  "sex": "f",
  "disable": 0,
  "other_meds": 1,
  "cur_ill": 0,
  "history": 0,
  "prior_vax": 0,
  "ofc_visit": 0,
  "allergies": 0,
  "vax_name": "moderna",
  "vax_dose_series": 1
}
```

### predict.py

This script is used to test the service automatically.
Just make sure that the service is running.

```bash
python predict.py
actual=0 DANGER 0.6464744210243225
actual=1 DANGER 0.9937990307807922
actual=0 SAFE 0.003976976033300161
actual=1 SAFE 0.06304533779621124
actual=1 DANGER 0.9938003420829773
actual=0 CAUTION 0.3316843509674072
actual=0 DANGER 0.8416000604629517
actual=1 SAFE 0.030635036528110504
actual=0 SAFE 0.02638752944767475
actual=0 SAFE 0.0005494322977028787
```

### locusfile.py

This script is used to run a load tester to stress test the service and can be started with the following command:

```bash
locust -H http://localhost:3000
```

Then open a browser to [http://localhost:8089](http://localhost:8089).
Adjust the number of desired users and the spawn rate and start swarming.

## Building the classifier

Once you have a bentoml model, you are ready to build the classifier.
Simply run the following command:

```bash
bentoml build
Building BentoML service "covid_risk_classifier:t5kuzvk2jcrawdg5" from build context "C:\Users\clamy\Projects\mid-term"
Packing model "covid_risk_model:djsbjtk2jcaladg5"
Locking PyPI package versions..
C:\Users\clamy\anaconda3\envs\datasci\lib\site-packages\_distutils_hack\__init__.py:33: UserWarning: Setuptools is replacing distutils.
  warnings.warn("Setuptools is replacing distutils.")

██████╗░███████╗███╗░░██╗████████╗░█████╗░███╗░░░███╗██╗░░░░░
██╔══██╗██╔════╝████╗░██║╚══██╔══╝██╔══██╗████╗░████║██║░░░░░
██████╦╝█████╗░░██╔██╗██║░░░██║░░░██║░░██║██╔████╔██║██║░░░░░
██╔══██╗██╔══╝░░██║╚████║░░░██║░░░██║░░██║██║╚██╔╝██║██║░░░░░
██████╦╝███████╗██║░╚███║░░░██║░░░╚█████╔╝██║░╚═╝░██║███████╗
╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░░╚════╝░╚═╝░░░░░╚═╝╚══════╝

Successfully built Bento(tag="covid_risk_classifier:t5kuzvk2jcrawdg5")
```

### Confirm that your classifier has been created

```bash
bentoml list
 Tag                                      Size        Creation Time        Path
 covid_risk_classifier:t5kuzvk2jcrawdg5   769.15 KiB  2022-11-01 19:52:30  ~\bentoml\bentos\covid_risk_classifier…
 ```

To get more information about your classifier:

```yaml
bentoml get covid_risk_classifier:t5kuzvk2jcrawdg5
service: service:svc
name: covid_risk_classifier
version: 4ukkzsk2nocq6dg5
bentoml_version: 1.0.7
creation_time: '2022-11-02T05:05:00.478300+00:00'
labels:
  owner: Martin Uribe
  email: clamytoe@gmail.com
  stage: dev
models:
- tag: covid_risk_model:rgvdhgs2noldydg5
  module: bentoml.xgboost
  creation_time: '2022-11-02T05:02:23.599680+00:00'
runners:
- name: covid_risk_model
  runnable_type: XGBoostRunnable
  models:
  - covid_risk_model:rgvdhgs2noldydg5
  resource_config: null
apis:
- name: classify
  input_type: JSON
  output_type: JSON
docker:
  distro: debian
  python_version: '3.10'
  cuda_version: null
  env: null
  system_packages: null
  setup_script: null
  base_image: null
  dockerfile_template: null
python:
  requirements_txt: null
  packages:
  - pydantic
  - scikit-learn==1.1.2
  - xgboost
  lock_packages: true
  index_url: null
  no_index: null
  trusted_host: null
  find_links: null
  extra_index_url: null
  pip_args: null
  wheels: null
conda:
  environment_yml: null
  channels: null
  dependencies: null
  pip: null
  ```

## Build a docker image from your classifier

Now that you have your classifier and you are happy with it's performance, it's really easy to build a docker image from it.
Simply run the following command:

```bash
bentoml containerize covid_risk_classifier:t5kuzvk2jcrawdg5
Building docker image for Bento(tag="covid_risk_classifier:t5kuzvk2jcrawdg5")...
Successfully built docker image for "covid_risk_classifier:t5kuzvk2jcrawdg5" with tags "covid_risk_classifier:t5kuzvk2jcrawdg5"
To run your newly built Bento container, pass "covid_risk_classifier:t5kuzvk2jcrawdg5" to "docker run". For example: "docker run -it --rm -p 3000:3000 covid_risk_classifier:t5kuzvk2jcrawdg5 serve --production".
```

## Start your bentoml docker image

To start the service from the docker image, run the following command:

```bash
docker run -it --rm -p 3000:3000 covid_risk_classifier:t5kuzvk2jcrawdg5 serve --production
```

You can test your docker container with the `perdict.py` script, the same way you did for testing the bentoml service:

```bash
python predict.py
actual=0 DANGER 0.6464744210243225
actual=1 DANGER 0.9937990307807922
actual=0 SAFE 0.003976976033300161
actual=1 SAFE 0.06304533779621124
actual=1 DANGER 0.9938003420829773
actual=0 CAUTION 0.3316843509674072
actual=0 DANGER 0.8416000604629517
actual=1 SAFE 0.030635036528110504
actual=0 SAFE 0.02638752944767475
actual=0 SAFE 0.0005494322977028787
```

## Push your image to docker hub

First you will have to tag your image with your docker hub user name.
That can be done like this:

```bash
docker tag covid_risk_classifier:t5kuzvk2jcrawdg5 clamytoe/covid_risk_classifier:latest
```

> **NOTE:** Make sure to use your own docker hub user name.

Once your image has been properly named, you can now push it.

> Make sure that your docker desktop app is authenticated with Docker.

```bash
docker push clamytoe/covid_risk_classifier:latest
```

## Using your tagged docker image

Now that the image has been tagged with your user name the service can be started like this:

```bash
docker run -it --rm -p 3000:3000 clamytoe/covid_risk_classifier serve --production
```

## Load testing the service

I have included a locustfile.py script so that you can test the performance of your service.
To start it, simply run the following command:

```bash
locust -H http://localhost:3000
[2022-11-01 20:01:33,999] ROG-STRIX/INFO/locust.main: Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)
[2022-11-01 20:01:34,012] ROG-STRIX/INFO/locust.main: Starting Locust 2.12.2
[2022-11-01 20:02:09,923] ROG-STRIX/INFO/locust.runners: Ramping to 1000 users at a rate of 10.00 per second
[2022-11-01 20:03:49,041] ROG-STRIX/INFO/locust.runners: All users spawned: {"CovidRiskTestUser": 1000} (1000 total users)
```

Then simply open up your browser to [http://localhost:8089](http://localhost:8089) and play around with the settings.
To stop it, simply click on the red stop button and `Ctrl+C` on the terminal to stop the service.
