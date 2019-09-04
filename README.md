# Presentation

Oxt_maltego is a rewritten in python 3 and canari (https://github.com/redcanari/canari3) a framework of transforms Maltego (https://www.paterva.com/)
 

# Installation

Import in Maltego the entities file named entities.mtz

pip install -r requirements.txt

canari create-profile OTX_transform

Configure  OTX_transform.conf to set _otx_url=https://otx.alienvault.com/api/v1_
and _api_key_

Import OTX_transform.mtz in maltego


# Custom Entities
* Pulse: a pulse in entry in Otx Alienvault. 
* CVE
* Yara: name of Yara rule (https://yara.readthedocs.io/) in a pulsdr