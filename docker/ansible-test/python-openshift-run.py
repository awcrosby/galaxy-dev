#!/usr/bin/env python3
"""Creates openshift job and outputs log from pod

Uses openshift rest api:
https://docs.openshift.com/container-platform/3.11/rest_api/examples.html

For concurrent jobs, may need jobname in yaml to be unique
- create by name, then look for pod(s) via jobname label
- create by name, then delete by name

get_job_pod_names(): $ oc get pods -l job-name=$JOB_NAME
SESSION_TOKEN via: $ oc whoami --show-token

bash env needs to have $ oc get pods working

"""

from pprint import pprint
import requests
import time
import yaml

DOMAIN = 'https://192.168.99.100:8443'
SESSION_TOKEN = 'zQxlmkqnZv-RLJ4BOpPevOUZ6-zBkfU0aCORC15h1Dg'
NAMESPACE = 'myproject'

JOB_NAME = 'bin-ans-test'
IMAGE = '172.30.1.1:5000/myproject/bin-ans-test'

JOB_YAML = f'''apiVersion: batch/v1
kind: Job
metadata:
  name: {JOB_NAME}
spec:
  parallelism: 1
  completions: 1
  activeDeadlineSeconds: 1800
  backoffLimit: 6
  template:
    metadata:
      name: {JOB_NAME}
    spec:
      containers:
      - name: {JOB_NAME}
        image: {IMAGE}
      restartPolicy: Never
'''

HEADERS = {'Authorization': f'Bearer {SESSION_TOKEN}'}
JOBS_URL = f'{DOMAIN}/apis/batch/v1/namespaces/{NAMESPACE}/jobs'
JOB_NAME_URL = f'{JOBS_URL}/{JOB_NAME}'
PODS_URL = f'{DOMAIN}/api/v1/namespaces/{NAMESPACE}/pods'
pod_url = '{pods_url}/{pod_name}'
log_url = '{pods_url}/{pod_name}/log'


def get_jobs():
    DOMAIN = 'https://192.168.99.100:8443'
    NAMESPACE = 'myproject'
    SESSION_TOKEN = 'zQxlmkqnZv-RLJ4BOpPevOUZ6-zBkfU0aCORC15h1Dg'
    HEADERS = {'Authorization': f'Bearer {SESSION_TOKEN}'}
    JOBS_URL = f'{DOMAIN}/apis/batch/v1/namespaces/{NAMESPACE}/jobs'
    JOB_NAME = 'bin-ans-test'
    JOB_NAME_URL = f'{JOBS_URL}/{JOB_NAME}'
    jobs = requests.get(JOB_NAME_URL, headers=HEADERS, verify=False)
    pprint(jobs.json())


# def watch_or_status_job():
#     url = f'{DOMAIN}/apis/batch/v1/watch/namespaces/{NAMESPACE}/jobs'
#     # url = f'{DOMAIN}/apis/batch/v1/namespaces/{NAMESPACE}/jobs/{JOB_NAME}/status'
#     r = requests.get(url, headers=HEADERS, verify=False, timeout=5)
#     # pprint(r.json())
#     for chunk in r.iter_content(chunk_size=256, decode_unicode=True):
#         print(chunk.rstrip())


def create_job():
    requests.post(JOBS_URL, headers=HEADERS, json=yaml.load(JOB_YAML), verify=False)


def get_job_pod_names():
    params = {'labelSelector': f'job-name={JOB_NAME}'}
    r = requests.get(PODS_URL, headers=HEADERS, params=params, verify=False)
    if not r.json()['items']:
        return []
    return [item['metadata']['name'] for item in r.json()['items']]


def get_pod_logs(pod_name):
    r = requests.get(
            url=f'{PODS_URL}/{pod_name}/log',
            headers=HEADERS,
            params=dict(follow='true'),
            stream=True,
            verify=False,
        )
    return r.iter_content(chunk_size=256, decode_unicode=True)


def cleanup_job():
    pod_names = get_job_pod_names()
    requests.delete(JOB_NAME_URL, headers=HEADERS, verify=False)
    for pod_name in pod_names:
        requests.delete(f'{PODS_URL}/{pod_name}', headers=HEADERS, verify=False)
        print(f'Deleted pod_name={pod_name}')


def main():
    requests.packages.urllib3.disable_warnings()

    # TODO: handle unsuccessful create?
    create_job()

    # TODO: remove sleep and wait until pod ready via:
    # watch job endpoint (but doesn't change)
    # or status of job (but docs api endpoint may be wrong)
    # or retry get_job_pod_names until not None and within a timeout
    time.sleep(5)
    pod_names = get_job_pod_names()

    if not pod_names:
        print('WARNING: could not find pod assocated with job')
        cleanup_job()
        return
    if len(pod_names) > 1:
        print('WARNING: expected one pod associated with job, found multiple')
        pprint(pod_names)

    logs = get_pod_logs(pod_names[0])
    for chunk in logs:
        print(chunk.rstrip())

    cleanup_job()


if __name__ == '__main__':
    main()
