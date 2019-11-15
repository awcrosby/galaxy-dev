FROM centos:7

ENV PYTHONUNBUFFERED=1 \
    LANG=en_US.UTF-8 \
    VENV=/venv

RUN yum -y install epel-release \
    && yum -y install \
        python36 \
        python36-devel \
    && yum -y clean all

RUN python3.6 -m venv "${VENV}" \
    && source "${VENV}/bin/activate" \
    && pip --no-cache-dir install -U \
        "pip<19.0" \
        wheel \
    && pip install ansible \
        cryptography \
        jinja2 \
        pycodestyle \
        pylint \
        pyyaml \
        rstcheck \
        virtualenv \
        voluptuous \
        yamllint

RUN useradd user1 \
        --uid 1000 \
        --no-create-home \
        --gid root \
    && mkdir -m 0775 /archive \
    && mkdir -p -m 0775 /ansible_collections \
    && chown user1:root /ansible_collections

# Update dir and permissions for where ansible-test sanity writes files
# NOTE: if a sanity cli tool conditionally writes to a diff dir, it will fail
RUN mkdir -m 0775 /.pylint.d \
    && mkdir -m 0775 /.ansible \
    && chmod -R 0775 "${VENV}"/lib64/python*

COPY entrypoint.sh /entrypoint
RUN chmod +x /entrypoint

ENV HOME /
USER 1000

ENTRYPOINT ["/entrypoint"]

COPY google-gcp-1.0.0.tar.gz /archive
