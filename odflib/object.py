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


import xml.etree.cElementTree as ET
from xml.dom import minidom

class Object():

    def __init__(self, type):
        # the type is mandatory, cf. http://www.opengroup.org/iot/odf/p2.htm#X_OX2dDF_Objects
        self.root = ET.Element("Object", type=type)
        return

    def add_description(self, description):
        # the description is optional, cf. http://www.opengroup.org/iot/odf/p2.htm#X_OX2dDF_Objects
        ET.SubElement(self.root, "description").text = description
        return self

    def add_id(self, id, idType=None, tagType=None, startDate=None, endDate=None):
        # at least one id should be present, cf. http://www.opengroup.org/iot/odf/p2.htm#X_OX2dDF_Objects
        sub_element = ET.SubElement(self.root, "id")
        sub_element.text = id

        if idType != None:
            sub_element.set('idType', idType)
        if tagType != None:
            sub_element.set('tagType', tagType)
        if startDate != None:
            sub_element.set('startDate', startDate)
        if endDate != None:
            sub_element.set('endDate', endDate)
        return self

    def add_infoitem(self, infoitem):

        self.root.append( infoitem.get() )

        return self

    def add_object(self, object):
        #insertion_point = ET.SubElement(self.root, "Object")
        self.root.append(object.get())
        return self

    def get(self):
        return ET.ElementTree(self.root).getroot()

    def __str__(self):
        return minidom.parseString( ET.tostring(self.get()) ).toprettyxml(indent=" "*3)


if __name__ == '__main__':

    from infoitem import  *

    myObject = Object("test_object")
    myObject.add_description('myDescription')
    myObject.add_id('myId')
    myObject.add_id('myIdWithIdType', 'myIdType')
    myObject.add_id('myIdWithIdTypeAndTagType', 'myIdType', 'myTagType')

    myInfoItem = InfoItem('myInfoitem')
    myInfoItem.add_value( "1.23", dateTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ') )
    myInfoItem.add_value( "4.56", unixTime = "2" )
    myInfoItem.add_value( "7.89" )
    myInfoItem.add_description('myDescription')

    myObject.add_infoitem(myInfoItem)

    print(myObject)
