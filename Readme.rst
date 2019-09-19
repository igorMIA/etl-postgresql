etl-postgresql
===============

basic etl using Django and PostgreSQL

:License: MIT


Deploying
--------------

Using make
^^^^^^^^^^^^^^^^^^^^^

later

*  to load data run::

    $ make loaddata

*  to run tests run::

    $ make run_tests

*  to start application(load data automatically start application)::

    $ make start_server

*  to stop server run::

    $ make stop_server

Note
----

Before loaddata command, you should place data files to the ``input_file`` directory.
Proper file names are:

* Encounter.ndjson.txt
* Observation.ndjson.txt
* Patient.ndjson.txt
* Procedure.ndjson.txt
