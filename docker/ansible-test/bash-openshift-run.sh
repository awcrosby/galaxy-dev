# NOTE: Don't use this block, below cannot copy entrypoint, think no build context on stdin
# echo 'Create from:Dockerfile buildconfig via Dockerfile'
# cat Dockerfile | oc new-build -D - --name ansible-test2

# NOTE: Don't use this block, use jobs instead
# # CrashLoopBackOff likely since no long running project
# echo 'Runs pod from image under openshift'
# oc run mytestapp5 --image=172.30.1.1:5000/myproject/mytest
# oc get deploymentconfig

# echo 'Create from:Binary buildconfig via Dockerfile'
# oc new-build \
#     --strategy docker \
#     --binary \
#     --docker-image centos:centos7 \
#     --name bin-ans-test

echo 'Start or rebuild binary build using local dir content'
oc start-build bin-ans-test --from-dir . --follow

# echo 'Get buildconfig and imagesstreams'
# oc get bc
# oc get is
# oc describe bc/bin-ans-test
# oc edit bc/bin-ans-test

echo 'Creating and running openshift job...'
echo 'apiVersion: batch/v1
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
      restartPolicy: Never
' >> job.yaml
oc create -f job.yaml
rm job.yaml

sleep 5

echo 'Getting logs from job'
oc logs jobs/bin-ans-test -f

# echo 'Deleting files...'
oc delete job/bin-ans-test

# # Get pod name and look at log output
# oc get pods
# oc logs bin-ans-test-k6lnj
# oc debug pod/mytestapp7-1-z6rk5  # shell into pod
