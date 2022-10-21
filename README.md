# Overview
This sample demonstrates how to change Python logging level configured using Kubernetes ConfigMap without restarting the pod.

## How to test
### Run on a local machine

1. Create a Python venv and activate, for example,

```bash
python -m venv log_env
source log_env/bin/activate
```

2. Install [watchdog](https://python-watchdog.readthedocs.io/en/stable/index.html): `pip install watchdog`.
3. Run the main program: `python main.py`.
4. Change [logging level in dynamic-config\logging.conf](./dynamic-config/logging.conf#L16), and watch the output change accordingly.

### Run in Kubernetes

1. Build a docker container: `docker build -t {your_docker_registry}/{your_image_name}:{your_image_tag}`.
2. Push the image to your docker registry.
3. Update the [image url in k8s\deployment.yaml](./k8s/deployment.yaml#L19).
4. Deploy to your Kubernetes cluster: `kubectl apply -f k8s`.
5. Check the log of the pod: `kubectl logs <pod_name> -f`, leave this command running.
6. Change the [logging level in k8s\configmap.yaml](./k8s/configmap.yaml#L22).
7. Deploy to your Kubernetes cluster again: `kubectl apply -f k8s`.
8. The output of #5 should continue, indicating that the pod has not been restarted. After a few minutes, logging level will change accordingly.

## How it works

This sample leverages [Python Watchdog](https://github.com/gorakhargosh/watchdog) to monitor ConfigMap changes.
Here are a few things specific to ConfigMap change as compared to normal file system change:

- ConfigMap change doesn't change the file itself, but symbolic link the file points to.
 For this reason, using file name pattern matching or filtering `src_path` of the change event to
 the file of interest doesn't work. You must monitor the whole directory.
- The ConfigMap must be mounted without Subpath, otherwise, [ConfigMap will not be updated](https://kubernetes.io/docs/concepts/storage/volumes/#configmap).
- It could take minutes for `watchdog` to pick up the change. 
