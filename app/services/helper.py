__author__ = 'Tarun'

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Helper():

    def __init__(self):
        pass

    @staticmethod
    def params_satisfied(request, params_list):
        """
            Checks for params from params_list in the http_request object.
        """
        response_dict = dict()
        for param in params_list:
            if not request.get(param):
                response_dict.update(msg="Missing parameter '%s'" % param, is_satisfied=False)
                break
        if not response_dict:
            response_dict.update(msg="Parameters satisfied.", is_satisfied=True)

        return response_dict

    @staticmethod
    def fetch_entity(entity_name, **kwargs):
        query = entity_name.query()
        for _property in kwargs:
            query = query.filter(entity_name._properties[_property] == kwargs[_property])
        log.info(query)
        entity = query.fetch()
        if entity:
            return True

        return False