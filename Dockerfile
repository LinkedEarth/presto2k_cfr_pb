# Environment image for the PReSto2k PaleoBook, built by quay.io from GitHub
# (quay.io/linkedearth/presto2k_cfr_pb). The environment itself lives in
# docker/environment.yml and docker/postBuild. Notebooks are NOT baked in:
# binder/Dockerfile starts FROM this image and copies the repo content.
FROM quay.io/jupyter/minimal-notebook:python-3.12.11

# Install the PaleoBook environment into the image's base conda env
# (the one JupyterHub launches), then clean caches to keep the image small.
COPY --chown=${NB_UID}:${NB_GID} docker/environment.yml /tmp/docker/environment.yml
RUN mamba env update -n base -f /tmp/docker/environment.yml && \
    mamba clean --all -f -y && \
    pip cache purge && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Build-time fixes (cfr annualize alias for pandas 3)
COPY --chown=${NB_UID}:${NB_GID} docker/postBuild /tmp/docker/postBuild
RUN bash /tmp/docker/postBuild && rm -rf /tmp/docker

WORKDIR /home/${NB_USER}
