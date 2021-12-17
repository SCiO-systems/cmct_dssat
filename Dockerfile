FROM public.ecr.aws/lambda/python:3.8

ARG AWS_KEY
ARG AWS_SECRET

ENV AWS_KEY ${AWS_KEY}
ENV AWS_SECRET ${AWS_SECRET}

RUN yum install gcc-gfortran cmake git glibc-static gcc gcc-c++ make wget -y

# DSSAT environment preparation
RUN mkdir -p DSSAT47/src

# DSSAT compiler installtion
RUN git clone https://github.com/DSSAT/dssat-csm-os.git && \
    cd dssat-csm-os && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make

# DSSAT data repository 
RUN git clone https://github.com/DSSAT/dssat-csm-data.git

# Adjusting filesystem to DSSAT compiler requirements
RUN cp dssat-csm-os/build/bin/dscsm047 DSSAT47/dscsm047
RUN cp -r dssat-csm-data/* DSSAT47/
RUN cp -r dssat-csm-os/Data/. DSSAT47/

RUN rm -rf DSSAT47/DSSATPRO.L47
RUN wget https://qvantum-crop-models.s3.eu-central-1.amazonaws.com/dssat/DSSATPRO.L47 -P DSSAT47/

# AWS CLI installation
RUN yum install aws-cli -y

RUN aws configure set aws_access_key_id ${AWS_KEY}
RUN aws configure set aws_secret_access_key ${AWS_SECRET}

COPY . ./

RUN pip3 install -r requirements.txt

CMD ["dssat.lambda_handler"]
