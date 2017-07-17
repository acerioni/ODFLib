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

class OMIEnvelope:
    def __init__(self, mode="read"):
        self.root = ET.Element("omiEnvelope", xmlns="http://www.opengroup.org/xsd/omi/1.0/", version="1.0", ttl="0")

        if mode == 'read':
            self.sub = ET.SubElement(self.root, "read", msgformat="odf")

        else:
            self.sub = ET.SubElement(self.root, "write", msgformat="odf")

        self.msg = ET.SubElement(self.sub, "msg")

    def add_objects(self, objects):
        self.msg.append(objects.get())
        return self

    def get(self):
        return ET.ElementTree(self.root).getroot()

    def __str__(self):
        return minidom.parseString(ET.tostring(self.get())).toprettyxml(indent=" "*3)

    def write_to_file(self, filename):
        ET.ElementTree(self.root).write(filename)
        return



if __name__ == '__main__':

    from infoitem import *
    from object import *
    from objectlist import *

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

    myObjects = ObjectList()
    myObjects.add_object(myObject)
    myObjects.add_object(myObject)

    myOMIEnvelope = OMIEnvelope(mode='write')
    myOMIEnvelope.add_objects( myObjects )
    print(myOMIEnvelope)

    myOMIEnvelope.write_to_file('tmp.xml')
