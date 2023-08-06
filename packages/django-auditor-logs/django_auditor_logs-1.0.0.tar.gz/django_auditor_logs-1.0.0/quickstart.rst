Django Auditor Logs is a Django app that provides a simple way to log events CREATE, UPDATE AND DELETE in your Django project. It is designed to be used with the Graphene Django package or Django Graphbox, but can be used with any Django project.

Installation
--------------------------------
    .. code-block:: bash

        pip install django-auditor-logs

Quick start
--------------------------------
1. Add "django_auditor_logs" to your INSTALLED_APPS setting like this::
    .. code-block:: python3

        INSTALLED_APPS = [
            ...
            'django_auditor_logs',
        ]

2. Configure AUDIT_APPS in your settings.py file like this::
    .. code-block:: python3
        
        AUDIT_APPS = [
            'app1',
            'app2',
        ]

3. Run `python manage.py migrate` to create the django_auditor_logs models.

4. Optionally you can change MIGRATION_MODULES in your settings.py file like this::
    .. code-block:: python3

        MIGRATION_MODULES = {
            'django_auditor_logs': 'app1.migrations',
        }

5. User and request metadare must be added on __user_metadata__ and __request_metadata__ fields in the model instance. On Django Graphbox from 1.1.0 version, this fields are added automatically.

6. There is a decorator to set user and request metadata on the model instance when it use Graphene Django uson a session_manager authentication style. the decorator set_metadata_mutation(model=None, id_field_name=None, session_manager=None, validate_method_name=None, index_tuple_user_session=0) must be used on the mutation class. The decorator parameters are:

    - model: The model class to set metadata.
    - id_field_name: The id field name of the model class ( same as the argument of Mutation that points to the id field of the model class)
    - session_manager: The session manager class to validate session and has a validation method that returns a tuple with the user instance.
    - validate_method_name: The method name to validate the session.
    - index_tuple_user_session: The index of the tuple returned by the session_manager.validate_method_name method that contains the user instance.