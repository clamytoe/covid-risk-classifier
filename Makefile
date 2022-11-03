# Makefile

USER= clamytoe
PROJECT= covid_risk
PICKLE= $(shell ls -alt xgboost*.bin | head -n1 | awk '{print $$9}')
BENTOML_MODEL= $(shell bentoml models list $(PROJECT)_model | grep -v Tag | head -n1 | awk '{print $$1}' | sed "s/:/\\\:/g")
BENTOML_CLASSIFIER= $(shell bentoml list $(PROJECT)_classifier | grep -v Tag | head -n1 | awk '{print $$1}' | sed "s/:/\\\:/g")
DOCKER_IMAGE= $(shell docker images $(PROJECT)_classifier | grep -v TAG | head -n1 | awk '{print $$1":"$$2}' | sed "s/:/\\\:/g")_docker
MY_IMAGE= $(USER)/$(PROJECT)_classifier\:latest

# Define the make commands
.PHONY: train model classifier docker tag push serve test load_test

# Define the rules
all: train model classifier docker tag serve

# Define each of the commands and specifying their outputs
$(PICKLE): train.py
	@echo Training and saving the model
	python train.py

train: $(PICKLE)

$(BENTOML_MODEL):
	@echo Generating bentoml model from $(PICKLE)
	python create_bento_model.py

model: $(BENTOML_MODEL)

$(BENTOML_CLASSIFIER):
	@echo Generating classifier from latest $(BENTOML_MODEL)
	bentoml build

classifier: $(BENTOML_CLASSIFIER)

$(DOCKER_IMAGE):
	@echo Creating docker image from $(BENTOML_CLASSIFIER)
	bentoml containerize $(BENTOML_CLASSIFIER)

docker: $(DOCKER_IMAGE)

$(MY_IMAGE):
	@echo Tagging $(BENTOML_CLASSIFIER) for user $(USER)
	docker tag $(BENTOML_CLASSIFIER) $(USER)/$(PROJECT)_classifier:latest

tag: $(MY_IMAGE)

serve:
	@echo Starting classifier service
	docker run -it --rm -p 3000:3000 $(BENTOML_CLASSIFIER) serve --production

test:
	@echo Running test
	python test_service.py

load_test:
	@echo Running load tester
	locust -H http://localhost:3000

push:
	@echo Pushing image $(MY_IMAGE) to docker hub
	docker push $(MY_IMAGE)

# Use debug rule to check that all of the variables were
# constructed properly.
debug:
	@echo 'Rule -> $@'
	@echo '              USER: $(USER)'
	@echo '           PROJECT: $(PROJECT)'
	@echo '     BENTOML_MODEL: $(BENTOML_MODEL)'
	@echo 'BENTOML_CLASSIFIER: $(BENTOML_CLASSIFIER)'
	@echo '      DOCKER_IMAGE: $(DOCKER_IMAGE)'
	@echo '          MY_IMAGE: $(MY_IMAGE)'
	@echo '            PICKLE: $(PICKLE)'

# Simple help menu showing what commands are available
# and what they do.
help:
	@echo 'Makefile for generating and deploying bentoml classification models       '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make help                           prints this message                '
	@echo '   make all                            runs through the whole process     '
	@echo '   make clean                          remove the generated files         '
	@echo '   make debug                          prints all of the variables used   '
	@echo '   make train                          (re)trains the model               '
	@echo '   make model                          creates a new bentoml model        '
	@echo '   make classifier                     creates a new bentoml classifier   '
	@echo '   make docker                         creates a new docker image         '
	@echo '   make tag                            tags the new docker image          '
	@echo '   make serve                          start the classification service   '
	@echo '   make push                           pushes docker image to docker hub  '
	@echo '   make -n                             prints the commands without        '
	@echo '                                       executing them                     '
	@echo '                                                                          '
	@echo 'Example:                                                                  '
	@echo '   make -n train                       would display the command for      '
	@echo '                                       training a new model               '
	@echo '                                                                          '

# Specify clean-up rules.
clean:
	@/bin/rm -f *.log *.bin .mypy_cache __pycache__

