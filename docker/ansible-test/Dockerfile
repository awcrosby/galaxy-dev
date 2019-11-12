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
        yamllint \
    && chmod -R a+rwX "${VENV}"/lib64/python*

# NOTE: https://stackoverflow.com/questions/42363105/permission-denied-mkdir-in-container-on-openshift
RUN adduser user1 -G root

# Needed?
# RUN chmod -R 775 /home/user1
# RUN chown -R user1:root /home/user1

VOLUME /collection_volume

# Needed?
# RUN chmod 775 /collection_volume

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

USER 1000

ENTRYPOINT ["/entrypoint.sh"]