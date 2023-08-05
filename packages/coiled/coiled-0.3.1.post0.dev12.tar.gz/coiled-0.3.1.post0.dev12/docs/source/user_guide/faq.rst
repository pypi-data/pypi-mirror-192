:notoc:

===
FAQ
===

Usage
-----

.. dropdown:: Can I use Coiled to do machine learning, data science, etc.?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes! Coiled builds on the popular PyData ecosystem of tools, and Dask in
    particular. Refer to the following resources to learn more about what you
    can do with Dask and Python:

    - `Dask <https://dask.org>`_
    - `Dask Examples <https://examples.dask.org>`_
    - :doc:`Dask Examples on Coiled <examples>`

    You may also want to check out our `YouTube channel
    <https://youtube.com/c/Coiled>`_ for interviews with community members that
    are using Python at scale.


.. dropdown:: Does Coiled support Jupyter notebooks?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, you can use Coiled from anywhere that you can run Python, including a
    Jupyter Notebook on your laptop, a cloud-hosted Jupyter Notebook, or a
    multi-user JupyterHub instance.

    And if you're using JupyterLab, you can learn more about
    :doc:`some extensions <examples/jupyterlab>` that we recommend trying to make JupyterLab
    even better when working with Coiled and Dask.


.. dropdown:: Can I use Coiled from Sagemaker, VS Code, PyCharm, etc.?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, in addition to using Coiled from Jupyter Notebooks, you can use Coiled
    from anywhere that you can run Python. Coiled is agnostic to any specific
    user environment, editor, or IDE.

    Coiled was built for the purpose of making it easy to work with remote Dask
    clusters from anywhere, and most of our users work with Jupyter Notebooks or
    their favorite Python IDE to work with Coiled and Dask.


.. dropdown:: Does Coiled support GPUs?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes! See :doc:`gpu` for more details.

.. dropdown:: Can I use a container registry other than DockerHub or ECR?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, you can use any Docker registry that supports the Docker Registry API
    V2. Get in touch with our support team at support@coiled.io if you encounter
    any issues.


Data
----

.. dropdown:: How do I access my data from Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When you run computations on Dask clusters managed by Coiled, you can access
    many different file formats using the typical approaches used by Dask,
    Python, and related libraries.

    -   `Tabular data <https://docs.dask.org/en/latest/dataframe-create.html>`_
    -   `Array data <https://docs.dask.org/en/latest/array-creation.html>`_
    -   `Text data <https://docs.dask.org/en/latest/bag-creation.html>`_

    Coiled can provision Dask clusters on different cloud providers. Therefore,
    large datasets should be stored on the cloud using services such as Amazon
    S3 to avoid large data transfer costs. Be sure to also consider which region
    you are running Coiled in compared to which region the data resides in.


.. dropdown:: Do I need to migrate my data to Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    No, Coiled does not store any of your data. Rather, your data can remain in
    its current location. Coiled manages computation and helps you load data
    from your existing data sources, process it, and write results to those same
    (or other) data sources.


.. dropdown:: Does Coiled collect logs from my cluster?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    If you have configured Coiled to run within your own cloud provider account
    on AWS or GCP, then Coiled doesn't collect or store cluster or server logs.
    In these cases, Coiled uses a token to access the logs in your account to
    display them from within the cluster dashboard.


.. dropdown:: Why does Coiled need permissions for my container registry?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled stores built software environments as Docker images in the container
    registry in your cloud provider account based on your pip/conda dependencies
    and uses these images when you create a cluster. Even if you don't plan to
    install any dependencies, Coiled still needs the permissions to access your
    container registries when creating container-only software environments.


Libraries
---------

.. dropdown:: How do I install libraries on my Coiled clusters?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled helps you manage software environments both on your local machine and
    on cloud providers. You can specify custom environments using pip or conda
    environment files with the :func:`coiled.create_software_environment` function
    and Coiled will manage building Docker images that can then be used as
    software environments in Dask clusters on the cloud.

    Refer to the documentation on :doc:`software_environment` for more
    information.


.. _why-local-software:


.. dropdown:: Why do I need a local software environment?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When performing distributed computations with Dask, you’ll create a
    :class:`distributed.Client` object which connects your local Python process
    (e.g., your laptop) to your remote Dask cluster (e.g., running on the
    cloud). The Dask ``Client`` is the user-facing entry point for submitting
    tasks to a Dask cluster. When using a ``Client`` to submit tasks to your
    cluster, Dask will package up and send data, functions, and other Python
    objects needed for your computations *from* your local Python process where
    your ``Client`` is running *to* your remote Dask cluster in order for them
    to be executed.

    This means that if you want to run a function on your Dask cluster, for
    example NumPy’s :func:`numpy.mean` function, then you must have NumPy
    installed in your local Python process so Dask can send the ``numpy.mean``
    function from your local Dask ``Client`` to the workers in your Dask
    cluster. For this reason, it’s recommended to have the same
    libraries/versions installed on both your local machine and on the remote
    workers in your cluster.

    Refer to the documentation on :doc:`software_environment` for more details
    on how to easily synchronize your local and remote software environments
    using Coiled.


.. _faq-version-mismatch:

.. dropdown:: Why do I get Version Mismatch warnings?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When running cloud computations from your local machine, we need to ensure
    some level of consistency between your local and remote environments. For
    example, your Python versions should match, and if you want to use a library
    like PyTorch or Pandas remotely, then you should probably also install it
    locally. When Coiled detects a mismatch, it will inform you with a warning.

    Matching versions can be challenging if handled manually. Fortunately,
    Coiled provides functionality to help build and maintain software
    environments that match across local and remote environments. Refer to the
    documentation on :doc:`software_environment_local` for more information.

.. _faq-deployment:

Deployment
----------

.. dropdown:: Which cloud providers does Coiled support?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled currently supports running within your AWS or GCP account.
    See :doc:`backends` for more information on configuration, supported
    regions, and GPUs.

.. dropdown:: Can I run Coiled on-premises?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    If you want to run Coiled on your own machines in your own data center, we
    would love to hear from you. Please contact sales@coiled.io to start a
    conversation with us.

Availability
------------

.. dropdown:: How do I invite colleagues, students, etc.?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    We're glad that you're enjoying Coiled and want to invite colleagues or
    students. Coiled is currently open access, so your colleagues can join on
    their own without any additional steps.

    If you want to work within a team account with a group of users from your
    organization, then you can send an e-mail to sales@coiled.io with a team
    name and we'll set you up as an administrator for your new team. Refer to
    the documentation on :doc:`teams` for more information.


Security
--------

.. dropdown:: Can I use Coiled to read private data on AWS?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes. If you create a Coiled cluster from an environment that has AWS
    credentials defined, then Coiled will generate a secure token from those
    credentials and forward it to your Dask workers. The Dask workers will have
    the same rights and permissions that you have by default.

    For additional control, Coiled can be deployed within your own AWS or GCP
    account where you can specify and manage IAM roles directly. Refer to the
    documentation on :doc:`security` for more information.


.. dropdown:: Are my computations and data secure?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled provides end-to-end network security by the use of both cloud
    networking policies and with SSL/TLS encryption. Coiled does not persist or
    store any of your data, data only resides in memory as long as you are
    performing computations.

    For additional control, Coiled can be deployed within your own AWS account
    where you can specify and manage data access controls directly. Refer to the
    documentation on :doc:`security` for more information.

Connect with us
---------------

.. dropdown:: How can I submit a bug report, feature request, or other question?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    First, thank you! Your feedback is highly valuable and will help influence
    the future of Coiled.

    For **bug reports, feature requests, or other usability feedback**, we'd love to hear from
    you! Please `submit an issue <https://github.com/coiled/feedback/issues/new/choose>`_.

    For **other questions**, please join our
    `Coiled Community Slack <https://join.slack.com/t/coiled-users/shared_invite/zt-hx1fnr7k-In~Q8ui3XkQfvQon0yN5WQ>`_
    where you can ask questions and interact with our engineers as well as the
    Coiled community.


.. dropdown:: How can I keep up with the latest news about Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    To stay up to date with Coiled, you can
    `subscribe to our newsletter <https://coiled.io>`_ and follow us on
    `Twitter <https://twitter.com/coiledhq>`_,
    `YouTube <https://youtube.com/c/Coiled>`_, and
    `LinkedIn <https://www.linkedin.com/company/coiled-computing/>`_.
