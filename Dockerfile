# JupyterHub image for the PReSto2k PaleoBook (built by quay.io from GitHub).
# The environment itself lives in binder/environment.yml and binder/postBuild,
# so this file and repo2docker/Binder stay in sync.
FROM quay.io/jupyter/minimal-notebook:python-3.12.11

# Install the PaleoBook environment into the image's base conda env
# (the one JupyterHub launches), then clean caches to keep the image small.
COPY --chown=${NB_UID}:${NB_GID} binder/environment.yml /tmp/binder/environment.yml
RUN mamba env update -n base -f /tmp/binder/environment.yml && \
    mamba clean --all -f -y && \
    pip cache purge && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Build-time fixes (cfr annualize alias for pandas 3)
COPY --chown=${NB_UID}:${NB_GID} binder/postBuild /tmp/binder/postBuild
RUN bash /tmp/binder/postBuild && rm -rf /tmp/binder

# Notebooks and small data files
COPY --chown=${NB_UID}:${NB_GID} . /home/${NB_USER}/presto2k_cfr_pb
WORKDIR /home/${NB_USER}/presto2k_cfr_pb
