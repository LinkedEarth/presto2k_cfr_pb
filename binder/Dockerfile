FROM quay.io/tanaya_g/presto2k_cfr_pb:update_C03_b

# Set working directory
WORKDIR /home/jovyan

# Copy repository files into the container
COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan/

# Set the default command to start Jupyter
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
