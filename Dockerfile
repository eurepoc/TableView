# Base image with Conda installed
FROM continuumio/miniconda3

# Create a group and user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Setup app directories and permissions
RUN mkdir -p /app /app/.cache/huggingface/transformers
WORKDIR /app
RUN chown -R appuser:appuser /app /app/.cache/huggingface
RUN mkdir -p /home/appuser/
RUN chown -R appuser:appuser /home/appuser

# Copy the environment file to the container
COPY environment.yml ./environment.yml

# Create the Conda environment named "my_env"
RUN conda env create -f environment.yml -n my_env

# Copy the rest of your application files to the container
COPY . ./

# Add conda env binaries to PATH
ENV PATH /opt/conda/envs/my_env/bin:$PATH
ENV TRANSFORMERS_CACHE /app/.cache/huggingface/transformers

# Make sure the directory is created and has the correct ownership
RUN mkdir -p ${TRANSFORMERS_CACHE} && chown -R appuser:appuser ${TRANSFORMERS_CACHE}

# Download the sentence-transformer model using the created environment
# Adjusting the command here to make sure the model is downloaded with the correct user permissions
USER appuser
RUN conda run -n my_env python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"

# Change ownership of the application files to appuser
USER root
RUN chown -R appuser:appuser /app .cache/huggingface

# Use the new user to run the application
USER appuser

# Expose the desired port
EXPOSE 8081

# Set the entrypoint command to run the application
CMD ["conda", "run", "-n", "my_env", "python", "run_app.py"]