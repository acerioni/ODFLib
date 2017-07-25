# This file is part of ODFLib.
#
# ODFLib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ODFLib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ODFLib.  If not, see <http://www.gnu.org/licenses/>.

import logging
import xml.etree.cElementTree as ET
from xml.dom import minidom

#__all__ = ['infoitem']

class InfoItem():

    def __init__(self, name):
        # the name is mandatory, cf. http://www.opengroup.org/iot/odf/p2.htm#X_OX2dDF_Objects
        self.root = ET.Element("InfoItem", name=name)
        return

    def add_name(self, name):
        """Additional names for the same InfoItem. This feature may be used, for instance,
        if the same InfoItem is known under different names in different organizations or software.
        (cf. http://www.opengroup.org/iot/odf/p2.htm#X_OX2dDF_Objects)
        """
        ET.SubElement(self.root, "name").text = name
        return self.sort()

    def add_description(self, description):
        """
        Text that explains what the InfoItem represents, mainly intended for human users.
        (cf. http://www.opengroup.org/iot/odf/p2.htm#X_OX2dDF_Objects)
        """
        ET.SubElement(self.root, "description").text = description
        return self.sort()

    def add_metadata(self, infoitem):
        # N.B.: input metadata should be an infoitem ()

        try:
            # check whether a MetaData tag already exists
            insertion_point = self.getroot().findall('./MetaData')[0]
        except:
            # otherwise, let's create one!
            insertion_point = ET.SubElement(self.root, "MetaData")

        insertion_point.append(infoitem.getroot())

        return self.sort()

    def add_value(self, value, dateTime=None, unixTime=None, type="xsd:double"):
        if unixTime != None:
            ET.SubElement(self.root, "value", unixTime=unixTime, type=type).text = value
            # unixTime has priority over dateTime, which is not taken into account if unixTime != None
            return self.sort()
        elif dateTime != None:
            ET.SubElement(self.root, "value", dateTime=dateTime, type=type).text = value
            return self.sort()
        else:
            # the timestamp is optional, cf. http://www.opengroup.org/iot/odf/p2.htm#fig5
            #now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            #ET.SubElement(self.root, "value", dateTime=now, type=type).text = value
            ET.SubElement(self.root, "value", type=type).text = value
            return self.sort()

    def getroot(self):
        return ET.ElementTree(self.root).getroot()

    def sort(self):
        """
        Sorts an InfoItem's children so to comply with the O-DF schema used by the reference implementation.
        cf. https://github.com/AaltoAsia/O-MI/blob/master/O-MI%20Node/src/main/resources/odf.xsd
        """

        tag2rank = {'name': 0, 'description': 1, 'MetaData': 2, 'value': 3}

        tmp = [ (tag2rank[child.tag], child) for child in self.root ]
        tmp = sorted(tmp, key=lambda x: x[0])
        tmp = [ x[1] for x in tmp ]

        attrib_backup = self.root.items()

        # delete all children
        self.root.clear()
        # restore attributes
        [self.root.set(*attrib) for attrib in attrib_backup]
        # restore children in a proper order
        [ self.root.append(child) for child in tmp ]

        return self

    def __str__(self):
        return minidom.parseString( ET.tostring(self.getroot()) ).toprettyxml(indent=" "*3)


if __name__ == '__main__':

    from datetime import datetime
    myInfoItem = InfoItem('myInfoItem')
    #myInfoItem.add_name('myName')
    myInfoItem.add_value( "1.23", dateTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ') )
    myInfoItem.add_value( "4.56", unixTime = "2" )
    myInfoItem.add_value( "7.89" )
    myInfoItem.add_description('myDescription')

    myOtherInfoItem = InfoItem('myOtherInfoItem')
    myOtherInfoItem.add_value('3.14')

    myInfoItem.add_metadata( myOtherInfoItem )



    #for el in myInfoItem.get_element_tree().iter():
    #    print(el.tag, el.attrib, el.text)

    print(myInfoItem)
