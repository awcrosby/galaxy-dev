# NOTE: below cannot copy entrypoint, think no build context on stdin
# echo 'Create openshift buildconfig and image...'
# cat Dockerfile | oc new-build -D - --name ansible-test2

# echo 'Create binary buildconfig via Dockerfile'
# oc new-build \
#     --strategy docker \
#     --binary \
#     --docker-image centos:centos7 \
#     --name bin-ans-test
# echo 'Start (or redo) binary build using local dir content'
# oc start-build bin-ans-test --from-dir . --follow

# echo 'Get buildconfig and imagesstreams'
# oc get bc
# oc get is

echo 'apiVersion: batch/v1
kind: Job
metadata:
  name: bin-ans-test3
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
        # command: ["ls"]
      restartPolicy: OnFailure
' >> job.yaml
echo 'Create openshift job'
oc create -f job.yaml
rm job.yaml

# # Get pod name and look at log output
# oc get pods
# oc logs bin-ans-test-k6lnj

