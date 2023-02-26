import json
import datetime
from beaker import sandbox

acl = sandbox.get_indexer_client()
print(acl.transaction("MGV3JEWBUBOGEJPM6ODJ4C27Q7FYSZ47LNKPS7X5BWG4CEPCO4WA")['transaction']['note'])