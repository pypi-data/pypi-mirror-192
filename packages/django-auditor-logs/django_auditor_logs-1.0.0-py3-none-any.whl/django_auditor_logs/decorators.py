import json

def set_metadata_mutation(model=None, id_field_name=None, session_manager=None, validate_method_name=None, index_tuple_user_session=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            assert model is not None, 'model is required'
            assert id_field_name is not None, 'id_field_name is required'
            # get the instance of the model
            if id_field_name in kwargs:
                instance = model.objects.get(id=kwargs[id_field_name])
            else:
                instance = model.objects.get(id=kwargs['input'][id_field_name])
            # set user_metadata
            if session_manager is not None and validate_method_name is not None and index_tuple_user_session is not None:
                validate_method=getattr(session_manager, validate_method_name)
                session_data = validate_method(kwargs['info'].context)
                if session_data is not None:
                    user=session_data[index_tuple_user_session]
                    user_metadata = {}
                    for field in user._meta.get_fields():
                        if not field.is_relation:
                            user_metadata[field.name] = str(getattr(user, field.name))
                    instance.__user_metadata__ = json.dumps(user_metadata)
            # set request_metadata
            request_metadata = {
                'ip':kwargs['info'].context.META.get('REMOTE_ADDR'),
                'user_agent':kwargs['info'].context.META.get('HTTP_USER_AGENT'),
                'method':kwargs['info'].context.META.get('REQUEST_METHOD'),
                'path':kwargs['info'].context.META.get('PATH_INFO'),
                'query_string':kwargs['info'].context.META.get('QUERY_STRING'),
                'content_type':kwargs['info'].context.META.get('CONTENT_TYPE'),
                'content_length':kwargs['info'].context.META.get('CONTENT_LENGTH'),
            }
            instance.__request_metadata__ = json.dumps(request_metadata)
            return func(*args, instance=instance, **kwargs)
        return wrapper
    return decorator

