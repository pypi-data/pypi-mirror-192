"""Defines the PSquared class"""

from typing import List, Optional, Tuple, Union

import os
from pathlib import Path
import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET

import requests

from .request_error import RequestError
from .response_error import ResponseError

_DEBUG_SEPARATOR = "--------"
_HEADERS = {"Content-Type": "application/xml", "Accept": "application/xml"}


def _eprint(*args, **kwargs):
    """Prints to standard error"""
    print(*args, file=sys.stderr, **kwargs)


def _get_client_dir() -> str:
    home = os.getenv("HOME")
    if None is home:
        raise ValueError("$HOME is not defined")
    return home + "/.psquared/client"


def _check_status(url: str, response: requests.Response, expected: int) -> None:
    """
     Checks the return status of a request to a URL

    :param url: the URL to which the request was made
    :param response: the response to the request
    :param expected: the expected response code
    """
    if expected == response.status_code:
        return
    if 400 == response.status_code:
        raise ResponseError(
            'Application at "' + url + '" can not process this request as it is bad',
            response.status_code,
            response.text,
        )
    if 401 == response.status_code:
        raise ResponseError(
            'Not authorized to execute commands for Application at "' + url,
            response.status_code,
            response.text,
        )
    if 404 == response.status_code:
        raise ResponseError(
            'Application at "' + url + '" not found',
            response.status_code,
            response.text,
        )
    raise ResponseError(
        "Unexpected status ("
        + str(response.status_code)
        + ') returned from "'
        + url
        + '"',
        response.status_code,
        response.text,
    )


def _extract_text(element: ET.Element, name: str) -> str:
    """
    Extracts a uri from the supplied element

    :param element: the element from which the uri shoud be extracted
    :param name: the name of the contain element from which the text
        should be extracted
    """
    uri_element = element.find(name)
    if None is uri_element:
        return "UNKNOWN"
    result = uri_element.text
    if None is result:
        return "MISSING"
    return result


def _extract_default_version(config: str, element: ET.Element, url: str) -> str:
    """
    Extracts the name of the default element for the supplied configuration
    """
    default_version = element.find("default-version")
    if None is default_version or None is default_version.text:
        raise RequestError(
            'No default version of configuration "'
            + config
            + '" is not available from '
            + url
        )
    known_default = element.findall(
        'known-versions/known-version/[uri="' + default_version.text + '"]'
    )
    if None is known_default:
        raise RequestError(
            'Default version of configuration "'
            + config
            + '" is not available from '
            + url
        )
    default_element = known_default[0]
    if None is not default_element:
        raise RequestError(
            'Default version of configuration "'
            + config
            + '" from '
            + url
            + " has no name"
        )
    name_element = default_element.find("name")
    if None is not name_element and None is not name_element.text:
        raise RequestError(
            'Default version of configuration "'
            + config
            + '" from '
            + url
            + " has no name"
        )
    return name_element.text


def _prepare_items(items):
    """
    Prepares a set of items for a selection or submission document
    """

    if None is items:
        return None
    items_element = ET.Element("items")
    for item in items:
        item_element = ET.Element("item")
        item_element.text = item
        items_element.append(item_element)
    return items_element


def _prepare_scheduler_uri(
    application: ET.Element, element, scheduler: Optional[str] = None
):
    """
    Prepares a Scheduler element containing its URI for a submission
    document containing the specified scheduler, if any

    :param application the application document to which to send the
        submission
    :param element the name of the element to contain the scheduler
    :param scheduler the name of the scheduler to prepare
    """
    if None is scheduler:
        return None
    result = ET.Element(element)
    scheduler_element = application.find(
        'schedulers/scheduler/[name="' + scheduler + '"]'
    )
    if None is scheduler_element:
        raise RequestError(
            'Scheduler "'
            + scheduler
            + '" is not available from '
            + _extract_text(application, "uri")
        )
    result.text = _extract_text(scheduler_element, "uri")
    return result


def _prepare_submission(
    application: ET.Element,
    items: List[str],
    message: Optional[str] = None,
    scheduler: Optional[str] = None,
) -> ET.Element:
    """
    Prepares a Submission document containing the specified items

    :param application the application document to which to send the
        submission
    :param items: the items that should be submitted.
    :param message: any message associated with the submission
    (default None).
    :param scheduler: the name of the scheduler that should schedule
    """
    result = ET.Element("submission")
    result.append(_prepare_items(items))
    if None is not message:
        msg = ET.Element("message")
        msg.text = message
        result.append(msg)
    scheduler_element = _prepare_scheduler_uri(application, "scheduler", scheduler)
    if None is not scheduler_element:
        result.append(scheduler_element)
    return result


class PSquared:
    """
    This class provides programatic access to a PSquared instance
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        url: str = "http://localhost:8080/psquared/local/report/",
        dump: bool = False,
        cert: Optional[str] = None,
        key: Optional[str] = None,
        cacert: Optional[Path] = None,
    ):
        """
        An Object that talks to the specified **PSquared** server.

        :param url: the URL of the PSquared instance.
        :param dump: True if the raw XML exchanges should be dumped.
        :param cert: path to the file containing the client\'s x509
                certificate, (default
                ``${HOME}/.psquared/client/cert/psquared_client.pem`` ).
        :param key: path to the file containing path to the client\'s
                private x509 key (default
                ``${HOME}/.psquared/client/private/psquared_client.key``
                ).
        :param cacert: path to the file containing one or more CA
                x509 certificates, (default
                ``${HOME}/.psquared/client/cert/cacert.pem``).

        The ``cert`` and ``key`` will only be used if the files
        containing them exist, otherwise they are ignored.

        The alternate ``cacert`` location is only used if the specified
        directory exists.
        """

        self.__url = url
        self.__debug = dump
        self.__session = requests.Session()
        if None is cert:
            cert = _get_client_dir() + "/cert/psquared_client.pem"  # Client certificate
        if None is key:
            key = (
                _get_client_dir() + "/private/psquared_client.key"
            )  # Client private key
        if None is cacert:
            cacert = Path(_get_client_dir() + "/cert/cacert.pem")  # CA certificate file
        if os.path.exists(cert) and os.path.exists(key):
            self.__session.cert = (cert, key)
        if os.path.exists(cacert):
            self.__session.verify = str(cacert)

    def __debug_separator(self) -> None:
        _eprint(_DEBUG_SEPARATOR)

    def get_application(self) -> ET.Element:
        """

        :return: the application document at the URL
        :rtype:

        :raises ResponseError: if the server response in not OK.
        """

        response = self.__session.get(self.__url)
        _check_status(self.__url, response, 200)
        application = ET.fromstring(response.text)
        self.__pretty_print(self.__url, ET.tostring(application))
        return application

    def get_configuration(self, name: str, **kwargs) -> Tuple[ET.Element, ET.Element]:
        """

        :param str name: the name of the configuration that should be
        returned.
        :param options: an optional dictionary of options determining
        how much detail to include in the returned configuration.

        :return: the configuration document the named configuration.

        :raises ResponseError: if the server response is not OK.
        """
        configuration_url, application = self.__get_configuration_url(name)
        url_to_use = configuration_url + self.__prepare_query(kwargs)
        response = self.__session.get(url_to_use)
        _check_status(url_to_use, response, 200)
        configuration = ET.fromstring(response.text)
        self.__pretty_print(url_to_use, ET.tostring(configuration))
        return configuration, application

    def __get_configuration_url(self, name: str) -> Tuple[str, ET.Element]:
        """

        :param name: the name of the configuration whose URL should be returned.

        :return: the URL of the named configuration, the application document at the URL

        :raises ResponseError: if the server response in not OK.
        """

        application = self.get_application()
        configurations = application.findall("configurations/configuration")
        for configuration in configurations:
            name_element = configuration.find("name")
            if None is not name_element and name == name_element.text:
                config_element = configuration.find("uri")
                if None is not config_element:
                    configuration_url = config_element.text
                    if None is configuration_url:
                        raise RequestError(
                            'Configuration "'
                            + name
                            + '" has no URL for "'
                            + _extract_text(application, "uri")
                            + '"'
                        )
                    return configuration_url, application
        raise RequestError(
            'Configuration "'
            + name
            + '" is not available from "'
            + _extract_text(application, "uri")
            + '"'
        )

    def __get_named_resource_url(
        self, config: str, vers: str, xpath: str, name: str
    ) -> Tuple[str, str, ET.Element]:
        """

        :param config: the name of the configuration to which the Named
        Resource should belong.
        :param vers: the version of the named configuration to which the
        Named Resource should belong.
        :param xpath: the xpath to the Named Resources within a Named
        Resource group that contains the Named Resource.
        :param name: the name of the resource whose URL should be
        returned.

        :return: the URI of a Named Resource for the specified
        configuration/version, the name of the version used and the
        application's document.
        :rtype: str, str, ElementTree

        :raises ResponseError: if the server response in not OK.
        """

        version, _, application = self.get_version(
            config, vers, options=("details", "full")
        )
        version_name = _extract_text(version, "name")
        cmd = version.find(xpath + '/[name="' + name + '"]')
        if None is cmd:
            raise ResponseError(
                'The version, "'
                + version_name
                + '", of configuration "'
                + config
                + '" does not support the "'
                + name
                + '" command',
                2,
                ET.tostring(version),
            )
        uri = _extract_text(cmd, "uri")
        return uri, version_name, application

    def get_version(  # pylint: disable=too-many-locals
        self, config: str, vers: Optional[str] = None, **kwargs
    ) -> Tuple[ET.Element, ET.Element, ET.Element]:
        """

        :param str config: the name of the configuration who version
        should be returned.
        :param str vers: the name of the version of the specified
        configuration to be returned.
        :param options: an optional dictionary of options determining
        how much detail to include in the returned version.

        :return: the version document the named configuration/version.

        :raises ResponseError: if the server response is not OK.
        """

        configuration, application = self.get_configuration(
            config, options=("details", "full")
        )
        url = _extract_text(application, "uri")
        if None is vers:
            vers_to_use = _extract_default_version(config, configuration, url)
        else:
            vers_to_use = vers
        version_element = configuration.find(
            'known-versions/known-version/[name="' + vers_to_use + '"]'
        )
        if None is version_element:
            raise RequestError(
                'Version "'
                + vers_to_use
                + '" of configuration "'
                + config
                + '" is not available from '
                + url
            )
        uri = _extract_text(version_element, "uri")
        uri_to_use = uri + self.__prepare_query(kwargs)
        response = self.__session.get(uri_to_use)
        _check_status(uri_to_use, response, 200)
        version = ET.fromstring(response.text)
        self.__pretty_print(uri_to_use, ET.tostring(version))
        return version, configuration, application

    def __prepare_query(self, options):
        """

        :param options: an optional dictionary of options determining
        how much detail to include in the returned configuration.

        :return: the query string to be added to a URL.
        """
        query = ""
        if None is not options and 0 != len(options):
            conjunction = "?"
            for _, value in options.items():
                query = query + conjunction + value[0] + "=" + value[1]
        return query

    def __pretty_print(
        self,
        url: Union[bytes, str],
        document: Union[bytes, str],
        is_response: bool = True,
    ) -> None:
        """
        Prints out a formatted version of the supplied XML

        :param url: the URL to which the request was made.
        :param document: the XML document to print.
        :param is_response: True is the XML is the reponse to a request.
        """
        if self.__debug:
            if None is not url:
                if is_response:
                    _eprint("URL : Response : " + str(url))
                else:
                    _eprint("URL : Request :  " + str(url))
            _eprint(xml.dom.minidom.parseString(document).toprettyxml())
            self.__debug_separator()

    def submit_items(  # pylint: disable=too-many-arguments
        self,
        configuration: str,
        version: str,
        items: List[str],
        message: Optional[str] = None,
        quiet: Optional[bool] = None,
        scheduler: Optional[str] = None,
        veto: Optional[str] = None,
    ) -> Tuple[Optional[ET.Element], Optional[str]]:
        """
        Submits the list of items for processing with the specified
        version of the named configuration

        :param configuration: the name of the configuration whose
        command URL should be returned.
        :param version: the version of the named configuration whose
        command URL should be returned.
        :param items: the items that should be submitted.
        :param message: any message associated with the submission
        (default None).
        :param quiet: True if no detailed response is required (default
        None).
        :param scheduler: the name of the scheduler that should schedule
        the execution. (default None)
        :param veto: the name of the veto, is any, to apply to the
        submission (default None).

        :return: the current report for the list of items for the
        specified configuration/version, and the name of the version
        used.

        :raises ResponseError: if the server response in not OK.
        """

        submit_url, vers, application = self.__get_named_resource_url(
            configuration, version, 'actions/[name="submission"]/action', "submit"
        )
        query_string = "?"
        if quiet:
            query_string = query_string + "details=None"
        if None is not veto:
            query_string = query_string + "veto=" + veto
        if 1 != len(query_string):
            submit_url = submit_url + query_string
        submission = _prepare_submission(application, items, message, scheduler)
        self.__pretty_print(submit_url, ET.tostring(submission), False)
        response = self.__session.post(
            submit_url, data=ET.tostring(submission), headers=_HEADERS
        )
        _check_status(submit_url, response, 200)
        if "" == response.text:
            return None, None
        report = ET.fromstring(response.text)
        self.__pretty_print(submit_url, ET.tostring(report))
        return report, vers
