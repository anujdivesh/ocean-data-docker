FROM python:3.12.3-slim

RUN apt-get update && apt-get -y upgrade \
  && apt-get install -y --no-install-recommends \
    git \
    wget \
    g++ \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && echo "Running $(conda --version)" && \
    conda init bash && \
    . /root/.bashrc && \
    conda update conda

WORKDIR /app

COPY environment2.yml /app/environment2.yml
RUN conda env create -n ocean -f /app/environment2.yml

#RUN . /root/miniconda3/bin/activate && conda env update --name base --file /app/environment.yml


RUN echo "conda activate ocean" >> ~/.bashrc

ENTRYPOINT ["bash", "-l", "-c"]
CMD ["/bin/bash"]

