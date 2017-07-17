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

class ObjectList:

    def __init__(self):
        self.root = ET.Element('Objects')
        self.root.set('xmlns', 'http://www.opengroup.org/xsd/odf/1.0/')
        #self.root.set('xmlns:xs', 'http://www.w3.org/2001/XMLSchema')
        #self.root.set('xmlns:odf', 'http://www.opengroup.org/xsd/odf/1.0/')

    def add_object(self, object):
        self.root.append(object.get())
        return self

    def get(self):
        return ET.ElementTree(self.root).getroot()

    def __str__(self):
        return minidom.parseString( ET.tostring(self.get()) ).toprettyxml(indent=" "*3)


if __name__ == '__main__':

    from infoitem import  *
    from object import *

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

    print(myObjects)
