# -*- coding: utf-8 -*-
"""
Script reads an XML file, converts and saves to JSON with the same file name in the working directory.
"""

import json
import os
import sys
import xml.etree.ElementTree as ET


class XmlToJson:
    """Base class that implements the required functionality to convert XML to JSON.
    """
    def __init__(self, file) -> None:
        """Initialise class object.
        Args:
            file ([str]): file path for input XML file
        """
        self.file = file
        tree = ET.parse(file)
        self.tree = tree

    def _get_attributes(self, element) -> dict:
        """Get attributes for a node element.
        Args:
            element [ET.element]: The element object to extract attributes from.

        Returns:
            attributes [dict]: Returns a dictionary with keys as the attribute name and value as attribute value.
        """
        attributes = element.attrib
        if attributes == {}:
            attributes['no-attrib'] = True
        attributes['xml_element_type'] = element.tag
        return attributes

    def _unpack_node(self, current_node) -> dict:
        """Take a node element and extract its child elements.
        Args:
            current_node [ET.element]: Current node whose child elements we want to extract.

        Returns:
            result [dict]: Returns a dict where each list type node is the key and the list elements are the values for that key.
        """
        result = self._get_attributes(current_node)
        if list(current_node) == []:
            pass
        else:
            for child in current_node:
                child_xml_tag = child.tag.upper()
                if child_xml_tag not in result.keys():
                    result[child_xml_tag] = []
                result[child_xml_tag].append(self._unpack_node(child))
        return result

    def generate_json(self):
        """Generate dictionary from the XML file provided as argument.
        Returns:
            result [dict]: Returns the final parsed dictionary object.
        """
        root = self.tree.getroot()
        result = self._unpack_node(root)
        return result

    def save_json(self, content):
        """Save the dictionary to a JSON file with same name in the working directory.
        Args:
            content [dict]: The final parsed dictionary to be saved.
        """
        filename = os.path.split(os.path.splitext(self.file)[0])[-1]
        with open(f'{filename}.json', 'w') as fwrite:
            json.dump(content, fwrite)


if __name__ == "__main__":
    file = sys.argv[1]
    worker = XmlToJson(file)
    result = worker.generate_json()
    worker.save_json(result)
