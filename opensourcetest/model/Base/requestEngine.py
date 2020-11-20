#!/user/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from typing import Text, Union
from opensourcetest.common.yamlOperation import YamlFileOption
from opensourcetest.common.urlOperation import url_replace
from opensourcetest.builtin.check import check_assertion
from opensourcetest.builtin.models import OSTReqRespData, OSTReqArgv
from opensourcetest.builtin.baseRequest import BaseRequest

# Read the conf.yml Global profile
conf_yaml_path = os.path.join(os.path.dirname(__file__).split("Base")[0], "Conf/conf.yml")
# According to the read conf.yml To obtain the testing website service and other information
conf_server_info = YamlFileOption.read_yaml(conf_yaml_path)["server_info"]

base_url = conf_server_info["protocol"] + '://' + conf_server_info["base_url"]
verify = conf_server_info["verify"]


def start_run_case(params_object, params_mark: Union[Text, int], checker=None, session_connection=None, params=None,
                   data=None, json=None, files=None, url_converter=None, **kwargs) -> OSTReqRespData:
    # Inject yaml request object
    params_obj = params_object()
    params_dict = params_obj.get_param_by_yaml(params_mark)
    req = BaseRequest()
    logging.info(params_dict)
    # Injection request data
    if session_connection:
        params_dict['headers'].update(session_connection)
    if url_converter:
        part_url = url_replace(params_dict['url'], url_converter)
    else:
        part_url = params_dict['url']
    if params:
        params_dict['params'].update(params)
    if data:
        params_dict['data'].update(data)
    if json:
        params_dict['json'].update(json)
    if files:
        params_dict['files'].update(files)
    # receive a request and response object
    ost_req_argv = OSTReqArgv(
        part_url=part_url,
        method=params_dict['method'].upper(),
        params=params_dict['params'],
        data=params_dict['data'],
        json=params_dict['json'],
        headers=params_dict['headers'],
        **kwargs
    )
    logging.error(ost_req_argv)

    ost_req_resp = req.send_request(url=base_url + part_url, method=params_dict['method'].upper(),
                                    send_params=params_dict['params'], send_data=params_dict['data'],
                                    send_json=params_dict['json'], headers=params_dict['headers'], verify=verify,
                                    **kwargs)
    if checker:
        # According to jmespath_rule and contrast value are used to judge, which needs to support multiple judgments
        check_assertion(ost_req_resp.response, checker)
    return ost_req_resp


if __name__ == "__main__":
    ...
