FROM python:3.11

# Install system dependencies required for PaddlePaddle and OpenCV
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgcc-s1 \
    libgfortran5 \
    libgl1 \
    libx11-6 \
    libxrender1 \
    libgthread-2.0-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libgtk-3-0 \
    libavcodec58 \
    libavformat58 \
    libavutil56 \
    libswscale5 \
    libswresample3 \
    libx264-164 \
    libx265-199 \
    libvpx7 \
    libmp3lame0 \
    libopus0 \
    libtheora0 \
    libvorbis0a \
    libvorbisenc2 \
    libxvidcore4 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY ./pyproject.toml ./README.md ./poetry.lock* ./

COPY ./package[s] ./packages

RUN poetry install  --no-interaction --no-ansi --no-root

COPY ./app ./app

RUN poetry install --no-interaction --no-ansi

# Set environment variables to prevent PaddlePaddle segmentation faults
ENV PADDLE_INFERENCE_BACKEND=cpu
ENV FLAGS_allocator_strategy=auto_growth
ENV FLAGS_fraction_of_gpu_memory_to_use=0.1
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1

EXPOSE 8080

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080
