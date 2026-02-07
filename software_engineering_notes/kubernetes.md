# Kubernetes (k8s)

Kubernetes, or k8s for short, is a container orchestration system.

It enables declaratively configuring how many instances (replicas) of a service you want running, rather than having to manually set up the desired number of instances on each VM and monitor them.

In a deployment, one or more containers can run on one VM, and one or more VMs can run on one server, of which there can be many. In a Kubernetes deployment, the VMs are called *pods*, the servers are called *worker nodes*, and the group of nodes is called a *cluster*. The are orchestrated by a *control plane* (controllers), mot of which runs on a separate, non-worker node within the cluster.

- The controllers constantly monitor the deployment, and if a pod crashes, will start a replacement instance on another, healthy pod in the cluster, ensuring zero downtime.

- Containers running on the same pod can share that pod's disk and network resources.

- Usually there is one main container per pod.

- Each node runs `kubelet` and `kube-proxy`.

The computational tasks performed by a system are called its *load*. A cloud deployment may have thousands of requests per second, each representing a computational task. A single container or pod can handle only so many requests, or traffic, before one of its resources (network I/O, CPU, memory) either becomes a bottleneck (slowing the system's response time) or crashes the container or pod. To avoid this, requests are sent to a *load balancer* which then delegates to a container or pod that has available resources. The load balancer tries to evenly distribute the load, for example, using 80% of resources on five machines rather than 100% of resources on only four of them.

When the system load increases or decreases, Kubernetes will scale by creating or removing extra pods as necessary. This means that pods are *ephemeral* (short-lived). Because pods are just VMs, every time one is created, it will have a new IP address. The load balancer keeps track of which pod IP addresses to send requests to, and provides a stable API endpoint for each service for requests to be sent to.

When a new version of the software is deployed, the container image is updated. Kubernetes handles rolling updates, in containers are gradually redeployed from the new image, ensuring zero downtime. With rolling updates, the container image can be rolled back if the new version is failing.

## Scaling

Horizontal Pod Autoscaling (HPA) means more pods. Configuration includes:

- Minimum and maximum number of replicas.
- Average utilization target for a resource (e.g., try to keep average CPU utilization at 50%).

Vertical Pod Autoscaling (VPA) means pods that have more resources. This is required for:

- Load consisting of fewer, larger tasks that cannot be broken up / parallelized.
- Databases.

Cluster Autoscaling means more nodes, and is invoked when existing nodes are at their limits. Configuration includes:

- Whether scaling back down is enabled and, if so, how long to wait after scaling up or after load decreases before considering scaling down.
- Minimum and maximum number of nodes can be configured.
- Minimum and maximum amount of memory and CPU cores for extra nodes.

## The Control Plane

The control plane consists of a number of components:

- API Server: Communicates with `etcd`, the Scheduler, and the Controller Manager, as well as the `kubectl` CLI on a dev/admin machine.

- `etcd`: Database (distributed key-value store) storing the state of the cluster (up-to-date information about nodes and pods).

- Scheduler: Assigns new pods to nodes based on what resources the new pod needs (e.g., how much memory) and what resources the node has available. The scheduler writes the node-to-pod assignment to `etcd`, which the node's `kubelet` instance picks up on.

- Controller Manager: Contains controllers:

    - Deployment Controller.
    - ReplicaSet Controller: Ensures the correct number of pods/replicas exist.
    - Node Controller: Monitors node health and moves pods to a different node if their current node starts to fail.
    - Service Controller: Creates a load balancer for each service.

- `kubelet`:

    - Starts pods.
    - Starts containers via a *container runtime*.
    - Does *liveness and readiness probes*, and reports node and pod status to the API Server.

## References

- [What on earth is Kubernetes?](https://kylejeong.com/blog/what-is-kubernetes)
