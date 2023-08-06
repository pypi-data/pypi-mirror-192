==========================
Coiled Cloud Release Notes
==========================

These release notes are related to updates for `cloud.coiled.io <https://cloud.coiled.io>`_.

.. _v2023.02.13:

2023.02.13
==========

Released on February 13, 2023

- Scheduler dashboards now have HTTPS (encryption) plus authentication. This will not be enabled if you're
  using a private IP address for the scheduler.

  Currently `Dask JupyterLab Extension <https://github.com/dask/dask-labextension>`_ won't work
  if you have auth on the scheduler dashboard, so you may wish to disable HTTPS and authentication
  if you're using the JupyterLab extension to see your dashboard.
  You can disable HTTPS and authentication for the Scheduler dashboard using the ``use_dashboard_https``
  keyword argument when creating a cluster.

- You may now see "flags" on the web dashboard with information about your clusters' performance
  (high memory usage, disk usage, etc).


.. _v2023.02.08:

2023.02.08
==========

Released on February 08, 2023

- Added cpu/memory charts to the cluster overview page


.. _v2023.01.11:

2023.01.11
==========

Released on January 11, 2023

- By default, you'll just see Dask logs for your (new) cluster, not all system logs. To retrieve full
  logs, you can use the ``coiled cluster better-logs`` CLI.
- You can now invite people to join your Coiled team by email address, instead of only by 
  Coiled username. This is especially useful for inviting people who do not have Coiled 
  accounts yet.

.. _v2022.11.28:

2022.11.28
==========

Released on November 28, 2022

- Package sync build logs are now available in the software tab of the cluster details page
- Resolved an issue with displaying team roles
- Disabled AWS GPUs that are not compatible with the CUDA version used on clusters
- Cluster details page now shows the zone of the cluster

.. _v2022.10.27:

2022.10.27
===========

Released on October 27, 2022

- Coiled now attempts to gracefully shutdown AWS spot instances when there's a scheduled "interruption"
  in the next two minutes, and by default Coiled also requests a replacement instance.
  If you don't want Coiled to request a replacement, set ``"spot_replacement"=False`` in ``backend_options``.
  (Note that when you're okay paying for on-demand instances when you can't get as many spot instances as
  you've requested, you can set ``"spot_on_demand_fallback"=True`` in ``backend_options``.)

.. _v2022.10.03:

2022.10.03
==========

Released on October 3, 2022

- Added an overview tab to the cluster details page with cluster status and a consolidated list of potential warnings or errors.

.. figure:: images/cloud-cluster-alerts.png
      :width: 75%
      :alt: Cluster alerts page in web application

.. _v2022.09.21:

2022.09.21
==========

Released on September 21, 2022

- Show upcoming bill amounts on the billing page
- PAYG customers can set monthly spend limits

.. _v2022.09.14:

2022.09.14
==========

Released on September 14, 2022

Enhancements
++++++++++++

- Added tabs to the cluster details page and the cluster analytics page to make it easier for you to navigate
  between one page or the other.
- Tweaks to improve cluster start time.
- Experimental support for ARM (Graviton) instances on AWS. This isn't production ready yet
  but let us know if you're interesting in giving it a try and we'd be happy to chat!

.. _v2022.06.29:

2022.06.29
==========

Released on June 29, 2022

Enhancements
++++++++++++

- The default persistent disk size for most instances types is now smaller, which will reduce cost and help avoid
  running into cloud provider quotas. Previously we attached a 100GB disk to every instance, now the default size
  will be between 30GB and 100GB and depends on how much memory (RAM) the instance has. If you know that your workload
  requires larger disks, you can either specify a larger disk with the ``worker_disk_size`` keyword argument when
  creating a cluster, or on AWS you can use an instance type such as the ``i3.large`` with a local NVMe
  (Coiled will configure the NVMe to be used by Dask for temporary storage).

.. _v2022.06.01:

2022.06.01
==========

Released on June 1, 2022

Enhancements
++++++++++++

- We've fixed an issue with running ``xgboost`` training on v2 clusters.

Deprecated
+++++++++++

- For new customers, Coiled-hosted is no longer offered; you'll be able to sign up for Coiled and use your own
  AWS or GCP account for your clusters.

.. _v2022.05.26:

2022.05.26
===========

Released on May 26, 2022

Enhancements
++++++++++++

- Coiled v2 supports spot instances on GCP (AWS spot instances were already supported).

.. _v2022.05.20:

2022.05.20
===========

Released on May 20, 2022

Enhancements
++++++++++++

- Coiled v2 now supports GPU instances on both AWS and GCP. Only a single GPU per instance is currently utilized.
  For AWS, simple use an instance type with attached GPU; for GCP, you'll need to use ``n1`` family instance and
  attach guess accelerator using ``worker_gpu_type`` keyword when creating a cluster.
  See :doc:`gpu` for more information.

.. _v2022.04.28:

2022.04.28
==========

Released on April 28, 2022

Enhancements
++++++++++++

- Coiled v2 Beta clusters now accept the ``environ`` and ``worker_class`` keyword argument.
- Fixed a bug in v2 clusters affecting instance type selection while creating clusters in an account that's different from your user's default account.
- You can now specify an extra service account when configuring your GCP cloud backend. For Coiled v2, this service account will be attached to the instances that Coiled 
  creates so it can access resources in your GCP account.

.. _v2022.03.29:

2022.03.29
==========

Released on March 29, 2022

Enhancements
++++++++++++
- Signing up for a pro account now requires account verification

.. _v2022.03.22:

2022.03.22
==========

Released on March 3, 2022

Deprecated
++++++++++

- Creating cluster configurations from the UI are longer available in preparation for deprecation

Documentation
+++++++++++++

- Documentation related to creating cluster configuration has been removed in preparation for the deprecation of custom cluster configurations

.. _v2022.03.17:

2022.03.17
==========

Released on March 17, 2022

Enhancements
++++++++++++

- Some internal changes to improve stability and reliability.

.. _v2022.03.09:

2022.03.09
==========

Released on March 9, 2022

Enhancements
++++++++++++

- Updated style and wording in the activation banner that new accounts see when they login to Coiled and their account
  isn't activated yet.
- You can now request your account activation directly from the activation banner, by clicking the `Activate Coiled Now!`
  button.

.. _v2022.02.23:

2022.02.23
==========

Released on February 23, 2022

Enhancements
++++++++++++

- Improved error message when asking for a Cluster that's over your account node limit. This error message will now
  contain the number of nodes requested, the account limit, and the cores limit for that account.

Fixes
+++++

- Fixed issue where accounts created using social login could get an invalid slug. Accounts created using social login
  will now always get a valid slug.
- Fixed issue where the core count in the usage tab of the clusters dashboard wouldn't update once the cluster scales up/down.

.. _v2022.02.09:

2022.02.09
==========

Released on February 9, 2022

Fixes
+++++

- Fixed issue where the core count wasn't being appropriately counted if users specified instance types.

Enhancements
++++++++++++

- Core count will now get the number of cores from the instance vCPU and update the count as workers start
  connecting to the scheduler.

Documentation
+++++++++++++

- Added section for the new keyword argument :ref:`wait_for_workers <wait-for-workers>` that the ``coiled.Cluster()`` constructor
  is using. This argument is used to make sure that the Cluster is ready to start a computation and return more information
  back to the user when the Cluster can't get workers.
- Added a section on :ref:`custom-docker` to be used with Coiled when creating software environments.

.. _v2022.01.26:

2022.01.26
==========

Released on January 26, 2022

Fixes
+++++

- Fixed an issue that was causing the ``reset password`` page to reload continuously, preventing users from choosing a new password.
- Fixed issue that was causing clusters not to stop when requested by the user, if the cluster was created in a different availability
  zone than the default one.

Enhancements
++++++++++++

- You are now able to specify any instance type available from your cloud provider of choice. You might wish to run the command 
  ``coiled.get_notifications(level="ERROR")`` if you have issues creating clusters with the specified instance types.

Documentation
+++++++++++++

- Updated activation email for users requiring account activation to activate@coiled.io.

.. _v2022.01.12:

2022.01.12
==========

Released on January 12, 2022

Fixes
+++++

- Fixed issue where setting ``nthreads`` when launching a cluster wasn't respected. You can override worker
  ``worker_options={"nthreads": <number of threads>}`` passed to the ``coiled.Cluster`` constructor.
- Removed references to Azure from Coiled Cloud

Enhancements
++++++++++++

- For AWS, VPC creation that runs when you set your backend options to run Coiled on your cloud provider of choice will now
  create one subnet for each Availability Zone in the region you chose to run Coiled.
- You can now specify an Availability Zone when creating a cluster (you might need to rerun the VPC creation process).
- Periodic cleanup will now cleanup resources in different Availability Zones.

Documentation
+++++++++++++

- Added warning in the Firewall and Networking section of the cloud providers documentation that this feature is under
  active development and is in an experimental phase.

.. _v2021.12.15:

2021.12.15
==========

Released on December 15, 2021

Fixes
+++++

- Fixed a frontend issue where a customer's payment info was not showing up even though it had been entered.
- Fixed an intermittent issue where users for some credit cards were unable to enter their security code. This has
  been fixed and all credit cards should work consistently.

Enhancements
++++++++++++

- Dask workers now use public IPs so that NAT Gateway is no longer needed;
  ingress to workers is still blocked. :doc:`tutorials/bring_your_own_network` can disable
  public IPs for workers by setting the the `give_workers_public_ip` option.
- Added a UI for :doc:`bring your own network <tutorials/bring_your_own_network>` so
  network options can also be configured through the UI when selecting your backend.
- Free tier account usage is still on an opt-in model.
  If you are a new user please contact support@coiled.io to enable software
  environments and cluster creations.
- Azure functionality has been removed and disabled for users. Users previously
  hosted on Coiled-hosted Azure have been migrated to the AWS backend.

Documentation
+++++++++++++

- Fixed a couple of broken links in the documentation on teams :doc:`teams`.
- Added more examples to the :doc:`bring your own network <tutorials/bring_your_own_network>`
  documentation.

.. _v2021.12.01:

2021.12.01
==========

Released on December 1, 2021

Enhancements
++++++++++++

- Added ability to manage API access tokens using (optional) expiration dates or
  manual revocation. Added support for managing API tokens via the Coiled Python
  client.
- Added account limit alert when 99% of the quota is used and when your account
  has reached its quota limit.
- Changed the default to use on-demand VMs for Dask workers as opposed to ``spot`` or ``preemptible`` instances.
  Backend options can still be set to use ``spot`` or ``preemptible`` instances, see
  :ref:`AWS backend options<aws_backend_options>` or :ref:`GCP backend options<gcp_backend_options>`.
- Added ability to use pre-existing cloud resources (e.g., VPC, subnets,
  security groups) when running Coiled in your own cloud provider account.

Deprecated
++++++++++

- Coiled Notebooks and Coiled Jobs have been deprecated.

Documentation
+++++++++++++

- As part of upcoming deprecation of the Azure cloud provider backend, the
  documentation related to Azure has been removed.
- Coiled client version of 0.0.55 or higher is required - please update your client if needed.

.. _v2021.11.10:

2021.11.10
==========

Released on November 10, 2021

Fixes
+++++

- Dask workers will now use all CPU/Memory available for the instance type in which they have
  been created. In the past, workers would be limited by your CPU/Memory specification.


Enhancements
++++++++++++

- Moved the **Coiled Subscription** tab up on the account settings page to make it easier
  for you to see how many credits you have used so far.
- If you are using Coiled on your cloud provider, you can now
  customize ingress rules for the firewall/security group created by Coiled
  by specifying ingress ports and a CIDR block.

Deprecated
++++++++++

- Coiled Notebooks and Coiled Jobs were an experimental feature which is being deprecated.
  After December 1, 2021, these will no longer be available.


Documentation
+++++++++++++

- Updated the list of dependencies in the documentation page :doc:`software_environment_creation`
  to include ``dask[complete]`` while creating a software environment with pip.
- Added troubleshooting article for :doc:`repeated cluster timeout errors.
  <troubleshooting/repeated_timeout_errors>`.
- Embedded tutorial videos for `cluster configuration`
  and :ref:`software environments <software-envs>` documentation.

.. _v2021.10.27:

2021.10.27
==========

Released on October 27, 2021

Fixes
+++++

- The route table for the private subnet that is created when Coiled creates a VPC
  in your AWS account, is now called ``coiled-vm-private-router`` instead of
  ``coiled-vm-public-router``.
- Mitigate Rate Limit exceptions when performing some actions like scaling clusters,
  which should improve cluster reliability.
- Software environment names must now be lowercase only.


Enhancements
++++++++++++

- Removed experimental warnings for GCP and Azure in the UI when choosing a
  backend option for an account.
- Removed fallback option to fetch logs from instances via SSH.


Documentation
+++++++++++++

- Removed experimental notes for GCP and Azure in the respective section of
  the documentation for these backends.
- Updated default ``worker_memory`` to ``8GiB`` in a few pages where it was
  saying that the default was ``16GiB``.
- Added a section about network architecture to the :doc:`security` page.
- Added a tutorial on :doc:`tutorials/select_instance_types`.
- Added a tutorial on :doc:`gpu`.
- Added section on selecting instance types in the documentation page
  :doc:`cluster_creation`.
- Added a Networking section on the documentation page for the :doc:`aws_reference`
  that explains how you can specify your AWS security groups using the new arguments
  ``enable_public_http``, ``enable_public_ssh`` and ``disable_public_ingress``.

.. _v2021.10.13:

2021.10.13
==========

Released on October 13, 2021

Fixes
+++++

* Environment variables sent to the Cluster with the keyword argument
  ``environ=`` are now being converted to strings, which fixes
  occasional failures when sending non-string values to the Cluster.

Enhancements
++++++++++++

* You can now use Coiled in your own GCP account. Please refer to the
  :doc:`gcp_configure` documentation.
* You can now use Coiled in your own Azure account.
* You can now select a ``region`` or ``zone`` when launching clusters in GCP.
* You can now create software environments using Docker images stored in your
  private ECR (AWS), ACR (Azure) or GAR (GCP) container registries, in addition
  to Docker Hub and other registries, by calling
  ``coiled.create_software_environment(container="<URI>")``.
* Coiled now collects statistical profiling data from your Dask clusters.
  This data is visualized as a flame graph on the Analytics page for
  individual clusters.
* You can now hide/show columns in the Clusters Dashboard. The options are: Id,
  Cluster Name, Created By, Status, Num Workers, Software Environment,
  Cost (current), Cost(total), Last Seen, Backend, Runtime, Spot/Preemptible.
* Improve log filtering for AWS when viewing logs in the Coiled UI.


Documentation
+++++++++++++

* Added a new example on using the Dask Snowflake connector.
* Fix link to Coiled's privacy policy in the :doc:`security` page.
* Added new section in the :doc:`gpu` documentation to demonstrate the use how
  of GPUs with the Afar library to run remote commands.

.. _v2021.09.28:

2021.09.28
==========

Released on September 28, 2021

Fixes
+++++

* Resolve error that was throwing an "Unable to stop cluster" error message in the Clusters
  Dashboard for users using the Azure backend.
* Fix issue with workers not being created when users create a new Cluster using the AWS backend.
* Resolve error that was causing Clusters to shut down immediately upon creation for users using the AWS backend.
* Fix issue that was causing the Cluster Dashboard table to show zero workers count even though the workers were
  created and connected to the scheduler.


Enhancements
++++++++++++

* Add label containing the instance name to notification when running ``coiled.get_notifications()``.


Documentation
+++++++++++++

* Fix typo in CLI command, documentation mentioned ``coiled inspect`` but the right command is ``coiled env inspect``.
* Update :doc:`teams` page to better explain the distinction between Accounts and Teams.
