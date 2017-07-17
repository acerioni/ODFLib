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
