#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_health_monitor_method_http
description:
    - HTTP type
short_description: Configures A10 health.monitor.method.http
author: A10 Networks 2018 
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
        - present
        - absent
        required: True
    a10_host:
        description:
        - Host for AXAPI authentication
        required: True
    a10_username:
        description:
        - Username for AXAPI authentication
        required: True
    a10_password:
        description:
        - Password for AXAPI authentication
        required: True
    partition:
        description:
        - Destination/target partition for object/command
    monitor_name:
        description:
        - Key to identify parent object
    http_url:
        description:
        - "Specify URL string, default is GET /"
        required: False
    text_regex:
        description:
        - "Specify text expected  with Regex"
        required: False
    http_maintenance_code:
        description:
        - "Specify response code for maintenance (Format is xx,xx-xx (xx between [100, 899]))"
        required: False
    http_kerberos_auth:
        description:
        - "Http Kerberos Auth"
        required: False
    http_postfile:
        description:
        - "Specify the HTTP post data (Input post data file name here)"
        required: False
    response_code_regex:
        description:
        - "Specify response code range with Regex (code with Regex, such as [2-5][0-9][0-9])"
        required: False
    uuid:
        description:
        - "uuid of the object"
        required: False
    post_type:
        description:
        - "'postdata'= Specify the HTTP post data; 'postfile'= Specify the HTTP post data; "
        required: False
    http_password_string:
        description:
        - "Specify password, '' means empty password"
        required: False
    url_path:
        description:
        - "Specify URL path, default is '/'"
        required: False
    http_response_code:
        description:
        - "Specify response code range (e.g. 200,400-430) (Format is xx,xx-xx (xx between [100, 899]))"
        required: False
    http_host:
        description:
        - "Specify 'Host=' header used in request (enclose IPv6 address in [])"
        required: False
    http:
        description:
        - "HTTP type"
        required: False
    url_type:
        description:
        - "'GET'= HTTP GET method; 'POST'= HTTP POST method; 'HEAD'= HTTP HEAD method; "
        required: False
    http_postdata:
        description:
        - "Specify the HTTP post data (Input post data here)"
        required: False
    http_text:
        description:
        - "Specify text expected"
        required: False
    http_encrypted:
        description:
        - "Do NOT use this option manually. (This is an A10 reserved keyword.) (The ENCRYPTED password string)"
        required: False
    http_kerberos_realm:
        description:
        - "Specify realm of Kerberos server"
        required: False
    http_password:
        description:
        - "Specify the user password"
        required: False
    http_kerberos_kdc:
        description:
        - "Field http_kerberos_kdc"
        required: False
        suboptions:
            http_kerberos_hostipv6:
                description:
                - "Server's IPV6 address"
            http_kerberos_port:
                description:
                - "Specify the kdc port"
            http_kerberos_portv6:
                description:
                - "Specify the kdc port"
            http_kerberos_hostip:
                description:
                - "Kdc's hostname(length=1-31) or IP address"
    http_expect:
        description:
        - "Specify what you expect from the response message"
        required: False
    post_path:
        description:
        - "Specify URL path, default is '/'"
        required: False
    http_username:
        description:
        - "Specify the username"
        required: False
    http_port:
        description:
        - "Specify HTTP Port (Specify port number (default 80))"
        required: False

"""

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["http","http_encrypted","http_expect","http_host","http_kerberos_auth","http_kerberos_kdc","http_kerberos_realm","http_maintenance_code","http_password","http_password_string","http_port","http_postdata","http_postfile","http_response_code","http_text","http_url","http_username","post_path","post_type","response_code_regex","text_regex","url_path","url_type","uuid",]

# our imports go at the top so we fail fast.
try:
    from a10_ansible import errors as a10_ex
    from a10_ansible.axapi_http import client_factory, session_factory
    from a10_ansible.kwbl import KW_IN, KW_OUT, translate_blacklist as translateBlacklist

except (ImportError) as ex:
    module.fail_json(msg="Import Error:{0}".format(ex))
except (Exception) as ex:
    module.fail_json(msg="General Exception in Ansible module import:{0}".format(ex))


def get_default_argspec():
    return dict(
        a10_host=dict(type='str', required=True),
        a10_username=dict(type='str', required=True),
        a10_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=["present", "absent", "noop"]),
        a10_port=dict(type='int', required=True),
        a10_protocol=dict(type='str', choices=["http", "https"]),
        partition=dict(type='str', required=False),
        get_type=dict(type='str', choices=["single", "list"])
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        http_url=dict(type='bool',),
        text_regex=dict(type='str',),
        http_maintenance_code=dict(type='str',),
        http_kerberos_auth=dict(type='bool',),
        http_postfile=dict(type='str',),
        response_code_regex=dict(type='str',),
        uuid=dict(type='str',),
        post_type=dict(type='str',choices=['postdata','postfile']),
        http_password_string=dict(type='str',),
        url_path=dict(type='str',),
        http_response_code=dict(type='str',),
        http_host=dict(type='str',),
        http=dict(type='bool',),
        url_type=dict(type='str',choices=['GET','POST','HEAD']),
        http_postdata=dict(type='str',),
        http_text=dict(type='str',),
        http_encrypted=dict(type='str',),
        http_kerberos_realm=dict(type='str',),
        http_password=dict(type='bool',),
        http_kerberos_kdc=dict(type='dict',http_kerberos_hostipv6=dict(type='str',),http_kerberos_port=dict(type='int',),http_kerberos_portv6=dict(type='int',),http_kerberos_hostip=dict(type='str',)),
        http_expect=dict(type='bool',),
        post_path=dict(type='str',),
        http_username=dict(type='str',),
        http_port=dict(type='int',)
    ))
   
    # Parent keys
    rv.update(dict(
        monitor_name=dict(type='str', required=True),
    ))

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/health/monitor/{monitor_name}/method/http"

    f_dict = {}
    f_dict["monitor_name"] = module.params["monitor_name"]

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/health/monitor/{monitor_name}/method/http"

    f_dict = {}
    f_dict["monitor_name"] = module.params["monitor_name"]

    return url_base.format(**f_dict)

def list_url(module):
    """Return the URL for a list of resources"""
    ret = existing_url(module)
    return ret[0:ret.rfind('/')]

def build_envelope(title, data):
    return {
        title: data
    }

def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")

def _build_dict_from_param(param):
    rv = {}

    for k,v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        elif isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv

def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            elif isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if x in params and params.get(x) is not None])
    
    errors = []
    marg = []
    
    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc,msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc,msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc,msg = REQUIRED_VALID
    
    if not rc:
        errors.append(msg.format(", ".join(marg)))
    
    return rc,errors

def get(module):
    return module.client.get(existing_url(module))

def get_list(module):
    return module.client.get(list_url(module))

def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return False

def create(module, result):
    payload = build_json("http", module)
    try:
        post_result = module.client.post(new_url(module), payload)
        if post_result:
            result.update(**post_result)
        result["changed"] = True
    except a10_ex.Exists:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def update(module, result, existing_config):
    payload = build_json("http", module)
    try:
        post_result = module.client.post(existing_url(module), payload)
        if post_result:
            result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def present(module, result, existing_config):
    if not exists(module):
        return create(module, result)
    else:
        return update(module, result, existing_config)

def absent(module, result):
    return delete(module, result)

def replace(module, result, existing_config):
    payload = build_json("http", module)
    try:
        post_result = module.client.put(existing_url(module), payload)
        if post_result:
            result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def run_command(module):
    run_errors = []

    result = dict(
        changed=False,
        original_message="",
        message="",
        result={}
    )

    state = module.params["state"]
    a10_host = module.params["a10_host"]
    a10_username = module.params["a10_username"]
    a10_password = module.params["a10_password"]
    a10_port = module.params["a10_port"] 
    a10_protocol = module.params["a10_protocol"]
    
    partition = module.params["partition"]

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        for ve in validation_errors:
            run_errors.append(ve)
    
    if not valid:
        err_msg = "\n".join(run_errors)
        result["messages"] = "Validation failure: " + str(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)
    if partition:
        module.client.activate_partition(partition)

    existing_config = exists(module)

    if state == 'present':
        result = present(module, result, existing_config)
        module.client.session.close()
    elif state == 'absent':
        result = absent(module, result)
        module.client.session.close()
    elif state == 'noop':
        if module.params.get("get_type") == "single":
            result["result"] = get(module)
        elif module.params.get("get_type") == "list":
            result["result"] = get_list(module)
    return result

def main():
    module = AnsibleModule(argument_spec=get_argspec())
    result = run_command(module)
    module.exit_json(**result)

# standard ansible module imports
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()