FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    libzbar0 \
    make \
    wget \
    perl \
    gdal-bin \
    libgdal-dev && \
    rm -rf /var/lib/apt/lists/*

# Install exiftool
RUN wget https://cpan.metacpan.org/authors/id/E/EX/EXIFTOOL/Image-ExifTool-12.15.tar.gz \
    && tar -xvzf Image-ExifTool-12.15.tar.gz \
    && cd Image-ExifTool-12.15 \
    && perl Makefile.PL && make test && make install \
    && cd .. 

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda \
    && rm Miniconda3-latest-Linux-x86_64.sh

# Add Miniconda to PATH
ENV PATH="/opt/miniconda/bin:$PATH"

# Copy project files
COPY micasense_conda_env.yml /tmp/requirements.yml

# Install Conda environment
RUN conda env create -f /tmp/requirements.yml

# Activate environment and run tests
RUN echo "source activate micasense" > ~/.bashrc
ENV PATH /opt/miniconda/envs/micasense/bin:$PATH

# Set working directory
WORKDIR /app

COPY . .

# Run pytest
#RUN conda run -n micasense pytest tests/

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run Flask app
CMD ["conda", "run", "-n", "micasense", "python", "src/app.py"]
