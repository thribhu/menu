FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Copy project
COPY . /code/

# Install dependencies
RUN echo "Upgrading pip version"
RUN pip install pip -U

RUN echo "Installing dependencies"
RUN pip install -r requirements.txt -U


