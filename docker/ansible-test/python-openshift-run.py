#!/usr/bin/env python3

import json
from pprint import pprint
import requests
import yaml

JOB_YAML = '''apiVersion: batch/v1
kind: Job
metadata:
  name: bin-ans-test
spec:
  parallelism: 1
  completions: 1
  activeDeadlineSeconds: 1800
  backoffLimit: 6
  template:
    metadata:
      name: bin-ans-test-metadata
    spec:
      containers:
      - name: bin-ans-test-container
        image: 172.30.1.1:5000/myproject/bin-ans-test
      restartPolicy: OnFailure
'''

# https://docs.openshift.com/container-platform/3.11/rest_api/examples.html
DOMAIN = 'https://192.168.99.100:8443'
SESSION_TOKEN = 'zQxlmkqnZv-RLJ4BOpPevOUZ6-zBkfU0aCORC15h1Dg'  # oc whoami --show-token
headers = {'Authorization': f'Bearer {SESSION_TOKEN}'}
NAMESPACE = 'myproject'

JOB_NAME = 'bin-ans-test'
jobs_post_url = f'{DOMAIN}/apis/batch/v1/namespaces/{NAMESPACE}/jobs'


def get_jobs():
    jobs_get_url = f'{DOMAIN}/apis/batch/v1/namespaces/{NAMESPACE}/jobs/{JOB_NAME}'
    jobs = requests.get(jobs_get_url, headers=headers, verify=False)
    pprint(jobs.json())


def create_job():
    data = yaml.load(JOB_YAML)
    requests.post(jobs_post_url, headers=headers, data=json.dumps(data), verify=False)


def output_log_with_pod_name(pod_name):
    # NOTE: pod logging, this works $ oc logs pod/bin-ans-test-z6c2q
    pod_log_url = f'{DOMAIN}/api/v1/namespaces/{NAMESPACE}/pods/{pod_name}/log'
    pod_logs = requests.get(pod_log_url, headers=headers, verify=False)
    print(pod_logs.text[:100])


def get_pod_name_of_job():
    # NOTE: trying to replicate: $ oc get pods -l job-name=bin-ans-test
    # TODO: see if can be done with ref from create_job()
    pods_ns_url = f'{DOMAIN}/api/v1/namespaces/{NAMESPACE}/pods'
    params = {'labelSelector': f'job-name={JOB_NAME}'}
    pods_ns = requests.get(pods_ns_url, headers=headers, params=params, verify=False)
    first_item = pods_ns.json()['items'][0]  # TODO: sort by recent?
    pod_name = first_item['metadata']['name']
    return pod_name


def delete_pod():
    pass


pod_name = get_pod_name_of_job()
print(f'pod_name={pod_name}')
output_log_with_pod_name(pod_name)

import pdb; pdb.set_trace()
