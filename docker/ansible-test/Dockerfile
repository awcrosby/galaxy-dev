FROM quay.io/ansible/default-test-container

RUN useradd user1 \
        --uid 1000 \
        --no-create-home \
        --gid root \
    && mkdir -m 0775 /archive \
    && mkdir -p -m 0775 /ansible_collections \
    && chown user1:root /ansible_collections \
    && pip install ansible

# Update dir and permissions for where ansible-test sanity writes files
# NOTE: if a sanity test conditionally writes to a different dir, it will fail
RUN touch /usr/local/lib/python3.6/dist-packages/ansible.egg-info \
    && chmod 0775 /usr/local/lib/python3.6/dist-packages/ansible.egg-info \
    && mkdir -m 0775 /.ansible \
    && mkdir -m 0775 /.pylint.d

COPY entrypoint.sh /entrypoint
RUN chmod +x /entrypoint

ENV HOME /
USER 1000

ENTRYPOINT ["/entrypoint"]

COPY archive /archive
