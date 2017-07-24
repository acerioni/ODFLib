from datetime import datetime
import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from odflib import *

print('version:', version.__version__)
print()

myObject = Object("test_object")
myObject.add_description('myDescription')

myInfoItem = InfoItem('myInfoitem')
myObject.add_id('myId')
myObject.add_id('myIdWithIdType', 'myIdType')
myObject.add_id('myIdWithIdTypeAndTagType', 'myIdType', 'myTagType')

myInfoItem.add_value( "1.23", dateTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ') )
myInfoItem.add_value( "4.56", unixTime = "2" )
myInfoItem.add_value( "7.89" )
myInfoItem.add_description('myDescription')

metadata1 = InfoItem('myMetaData1').add_value('myMetaData1', type='xsd:string')
metadata2 = InfoItem('myMetaData2').add_value('myMetaData2', type='xsd:string')
myInfoItem.add_metadata(metadata1)
myInfoItem.add_metadata(metadata2)

myObject.add_infoitem(myInfoItem)

myObjects = Objects()
myObjects.add_object(myObject)
myObjects.add_object(myObject)

myOMIEnvelope = OMIEnvelope(mode='write')
myOMIEnvelope.add_objects( myObjects )
print(myOMIEnvelope)

myOMIEnvelope.write_to_file('tmp.xml')
