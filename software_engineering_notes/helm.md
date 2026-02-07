# Helm

## Helm Charts

### Templating

A Kubernetes cluster is configured by Kubernetes objects, each of which is specified as a YAML file. A Kubernetes object can include a lot of configuration:

- The API version.
- The kind of object (e.g., a Deployment object).
- The name of the object.
- The number of replicas.
- Which containers should run in each replica, and their configurations.
- Secrets such as API keys and database credentials.

A Kubernetes cluster may be configured with multiple Kubernetes objects that may depend on other objects. There may be multiple Kubernetes clusters across different regions/datacenters. And there may be different configurations between development and production environments.

This would be too much configuration to maintain. If you wanted to create or reconfigure an object in all clusters, or create or reconfigure a cluster that has all objects, there would be a lot of copy-pasting. This would be tedious and error-prone. Git could be used to store configurations on a separate branch for each cluster or environment, but they would quickly diverge and become hard to reconcile.

There is likely a lot of configuration that is common across **all** or **almost all** objects, clusters, and environments. This means that a lot of configuration could be placed into a template that many Kubernetes objects can inherit from. This kind of templating is used by Helm Charts to make it easy to configure a Kubernetes cluster for a certain application.

In Helm Charts, one YAML file is used as a template for multiple Kubernetes objects by using placeholders for pieces of configuration therein that need to be set to certain values for each object. Values to fill in the placeholders are specified in a `values.yaml` file. A JSON schema may accompany the template to explicitly defines the format that a `values.yaml` file must follow in order to be compatible.

### Packaging

Helm Charts is a packaging system for Kubernetes configurations. Each chart is a package that contains the configuration, and other charts, required to run a certain application on a Kubernetes cluster. Each chart contains:

- A `Chart.yaml` file, which specifies the application name, version, and list of any dependencies (charts upon which the application depends).
- A `values.yaml` file, which specifies overridable defaults for the application.
- An optional JSON schema for compatible `values.yaml` files.
- Templates, in `templates/`.
- Any dependencies, in `charts/`.

The `values.yaml` file can be overridden:

- By a user of the chart, via `helm install --values=my-values.yaml <chart-name>`.
- When included in another chart.

Like any other software package, revisions to a Helm chart can be committed to a VCS (such as the Helm Charts repository) and new versions of the Helm chart can be released for installation by users. This allows changes to be tracked and allows rolling back to a previous version.
