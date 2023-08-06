=======
Logging
=======

Coiled stores instance, scheduler, and worker logs in your cloud provider account using Amazon CloudWatch and Google Cloud Logging (see the sections on :ref:`AWS <logs-aws>` and :ref:`GCP <logs-gcp>`). While you can use any of your existing log management systems to access your logs, Coiled also offers a few ways to make this easier.

.. note::
    This page covers cluster and instance logs. To learn more about understanding your Dask computations, see our documentation on :doc:`analytics` and :doc:`performance_reports`.

.. _coiled-cloud:

Coiled cloud
------------

Regardless of whether you are launching a Coiled cluster interactively or from a Python script, you can see your logs from the cluster dashboard page of your Coiled account at ``https://cloud.coiled.io/<account-name>/clusters``:

.. figure:: images/cloud-cluster-dashboard.png
    :width: 75%
    :alt: Cluster dashboard on the Coiled cloud web app with rows for each cluster and columns for cluster name, status, number of workers, software environment, last seen timestamp, and cost (in credits).

    Cluster dashboard (click to enlarge)

When you click on the name of a given cluster, you'll be redirected to the cluster details page at ``https://cloud.coiled.io/<account-name>/clusters/<cluster_id>/details>``:

.. figure:: images/cloud-cluster-details-panels.png
    :width: 85%
    :alt: Screenshot of the cluster details page on Coiled cloud.

    Cluster details (click to enlarge)

Here you can see the current cluster state and download instance-specific logs for the scheduler or workers by clicking "download logs".

.. note::
    You can also pull the logs for the scheduler and each worker using :func:`coiled.cluster_logs`.

As you scroll down, you can see the logs for the cluster state history:

.. figure:: images/cloud-cluster-details-state-history.png
    :width: 85%
    :alt: Screenshot of cluster state history.

    Cluster state history (click to enlarge)

Interactive session
-------------------

Within an interactive session, e.g. IPython or Jupyter Notebook, there is a dynamic widget loaded when you first create the cluster:

.. figure:: images/widget-gif.gif
       :alt: Terminal dashboard displaying the Coiled cluster status overview, configuration, and worker states.

The widget has three panels showing an overview of the Coiled cluster, the configuration, and Dask worker states with progress bars for how many workers have reached a given state. You can also use the link at the top to view the cluster details page mentioned above.

Python script
-------------

Coiled uses the `Python standard logging module <https://docs.python.org/3/library/logging.html>`_ for logging changes in cluster, scheduler, and worker state. The default level is ``WARNING``, but you can control the logging verbosity by setting the logging level, the ``DEBUG`` and ``INFO`` levels being the most verbose. See the `Python logging docs <https://docs.python.org/3/howto/logging.html#when-to-use-logging>`_ for more on logging levels. Here is an example for how this can be configured from within a Python script:

.. code-block:: python

   import logging
   from coiled import Cluster

   logging.basicConfig(level=logging.INFO)
   logging.getLogger("coiled").setLevel(logging.INFO)

   cluster = Cluster()
   cluster.close()

The above snippet will print the logs to the console, but you can also choose to save logs to a file by changing the parameters passed to ``basicConfig()`` (see `this tutorial on logging to a file <https://docs.python.org/3/howto/logging.html#logging-to-a-file>`_).

Next steps
----------

For more advanced options in debugging your Dask computations, see the `Dask documentation on logging <https://docs.dask.org/en/latest/how-to/debug.html#logs>`_.
