# Makefile

USER= clamytoe
PROJECT= covid_risk
PICKLE= $(shell ls -alt xgboost*.bin | head -n1 | awk '{print $$9}')
BENTOML_MODEL= $(shell bentoml models list -o json | grep 'tag' | grep $(PROJECT)_model | head -n1 | awk -F": \"" '{print $$2}' | sed s/\",//g | sed "s/:/\\\:/g")
BENTOML_CLASSIFIER= $(shell bentoml list -o json | grep 'tag' | grep $(PROJECT)_classifier | head -n1 | awk -F": \"" '{print $$2}' | sed s/\",//g | sed "s/:/\\\:/g")
DOCKER_IMAGE= $(shell docker images $(PROJECT)_classifier | grep -v TAG | head -n1 | awk '{print $$1":"$$2}' | sed "s/:/\\\:/g")_docker
CONTAINER= $(shell docker container ls | grep covid | rev | awk '{print $$1}' | rev)
MY_IMAGE= $(USER)/$(PROJECT)_classifier\:latest
EPHEMERAL_FILES= *.log *.tmp *.bin .mypy_cache __pycache__
RM= /bin/rm -rf

# Define the make commands
.PHONY: classifier docker load_test model predict push serve serve-docker shell tag train

# Define the rules
all: train model classifier docker tag serve-docker
dev: train model classifier serve

# Define each of the commands and specifying their outputs
classifier:
	@echo Generating classifier from latest $(BENTOML_MODEL)...
	bentoml build

docker:
	@echo Creating docker image from $(BENTOML_CLASSIFIER)...
	bentoml containerize $(BENTOML_CLASSIFIER)

load_test:
	@echo Running load tester...
	locust -H http://localhost:3000

model:
	@echo Generating bentoml model from $(PICKLE)...
	python create_bento_model.py

predict:
	@echo Running the prediction test...
	python predict.py

push:
	@echo Pushing image $(MY_IMAGE) to docker hub...
	docker push $(MY_IMAGE)

serve:
	@echo Starting classifier service for development...
	bentoml serve service:svc --reload

serve-docker:
	@echo Starting classifier service from the docker image for production...
	docker run -it --rm -p 3000:3000 $(BENTOML_CLASSIFIER) serve --production

shell:
	@echo Gaining shell access to running container...
	docker exec -it $(CONTAINER) bash

tag:
	@echo Tagging $(BENTOML_CLASSIFIER) for user $(USER)...
	docker tag $(BENTOML_CLASSIFIER) $(USER)/$(PROJECT)_classifier:latest

train:
	@echo Training and saving the model...
	python train.py

# Use debug rule to check that all of the variables were
# constructed properly.
debug:
	@echo 'Rule -> $@'
	@echo '              USER: $(USER)'
	@echo '           PROJECT: $(PROJECT)'
	@echo '     BENTOML_MODEL: $(BENTOML_MODEL)'
	@echo 'BENTOML_CLASSIFIER: $(BENTOML_CLASSIFIER)'
	@echo '      DOCKER_IMAGE: $(DOCKER_IMAGE)'
	@echo '         CONTAINER: $(CONTAINER)'
	@echo '          MY_IMAGE: $(MY_IMAGE)'
	@echo '            PICKLE: $(PICKLE)'

# Simple help menu showing what commands are available
# and what they do.
help:
	@echo 'Makefile for generating and deploying the covid risk classifier model     '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make help                           prints this message                '
	@echo '   make all                            runs through the whole process and '
	@echo '                                       starts production server           '
	@echo '   make dev                            runs through the initial process   '
	@echo '   make dev                            and starts local dev server        '
	@echo '   make classifier                     creates a new bentoml classifier   '
	@echo '   make clean                          remove the generated files         '
	@echo '   make debug                          prints all of the variables used   '
	@echo '   make docker                         creates a new docker image         '
	@echo '   make model                          creates a new bentoml model        '
	@echo '   make predict                        tests some sample predictions      '
	@echo '   make push                           pushes docker image to docker hub  '
	@echo '   make serve                          start the server for development   '
	@echo '   make serve-docker                   start the server from docker image '
	@echo '   make shell                          open a shell in running container  '
	@echo '   make tag                            tags the new docker image          '
	@echo '   make train                          (re)trains the model               '
	@echo '   make -n                             prints the commands without        '
	@echo '                                       executing them                     '
	@echo '                                                                          '
	@echo 'Example:                                                                  '
	@echo '   make -n train                       would display the command for      '
	@echo '                                       training a new model               '
	@echo '                                                                          '

# Specify clean-up rules.
clean:
	$(RM) $(EPHEMERAL_FILES)
