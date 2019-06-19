from canari.maltego.entities import Domain, IPv4Address, Phrase
from canari.maltego.transform import Transform
from OTX_transform.otx_transforms.transforms.common.entities import Pulse
from OTX_transform.otx_transforms.transforms.common.utils import gram,cores
import requests


class Pulses(Transform):
    namespace = "Otx_Transform"
    description = "Get Pulses linked with otx"

    def do_transform(self, request, response, config):
        base_url = config['OTX_transform.local.otx_url']
        api_key = config['OTX_transform.local.api_key']

        entity_type = gram[request.entity.type]
        entity_value = request.entity.value

        url = '%s/indicators/%s/%s/general' % (base_url, entity_type, entity_value)

        r = requests.get(url, headers={'X-OTX-API-KEY': api_key})
        if r.status_code == 200:

            res = r.json()

            for pulse in res['pulse_info']['pulses']:
                p = Pulse()
                p.URL = 'https://otx.alienvault.com/pulse/%s' % pulse['id']
                p.ID = pulse['id']
                p.value = pulse['name']
                p.link_label = pulse['modified']
                response += p
        return response

        pass

    def on_terminate(self):
        pass


class PulsesDomain(Pulses):
    input_type = Domain
    namespace = "Otx_Transform"

class PulsesIP(Pulses):
    input_type = IPv4Address
    namespace = "Otx_Transform"

class Tags(Transform):

    input_type = Pulse
    namespace = "Otx_Transform"

    def do_transform(self, request, response, config):
        base_url = config['OTX_transform.local.otx_url']
        api_key = config['OTX_transform.local.api_key']

        id_p = request.entity.ID
        url = '%s/pulses/%s' % (base_url, id_p)

        r = requests.get(url, headers={'X-OTX-API-KEY': api_key})

        if r.status_code == 200:
            res = r.json()

            for ind in res['industries']:

                p = Phrase(ind)

                response += p
            for t in res['tags']:
                p = Phrase(t)
                response += p

            for coun in res['targeted_countries']:
                p = Phrase(coun)
                response += p

        return response


class Related_Pulses(Transform):
    input_type = Pulse
    namespace = "Otx_Transform"

    def do_transform(self, request, response, config):
        base_url = config['OTX_transform.local.otx_url']
        api_key = config['OTX_transform.local.api_key']

        id_p = request.entity.ID

        url = '%s/pulses/%s/related' % (base_url, id_p)

        r = requests.get(url, headers={'X-OTX-API-KEY': api_key})

        if r.status_code==200:
            res = r.json()['results']
            for pulse in res:
                p = Pulse()
                p.URL = 'https://otx.alienvault.com/pulse/%s' % pulse['id']
                p.ID = pulse['id']
                p.value = pulse['name']
                p.link_label = pulse['modified']
                response += p

            return response

class Indicators(Transform):

    input_type = Pulse
    namespace = "Otx_Transform"

    def do_transform(self, request, response, config):
        base_url = config['OTX_transform.local.otx_url']
        api_key = config['OTX_transform.local.api_key']

        id_p = request.entity.ID
        id_p = "5cfe6b9d0ecf65e404ef4f85"
        url = '%s/pulses/%s/indicators' % (base_url, id_p)

        r = requests.get(url, headers={'X-OTX-API-KEY': api_key})
        res = r.json()
        is_finish = False

        while not is_finish:
            next_url = res['next']

            if next_url:
                r = requests.get(next_url, headers={'X-OTX-API-KEY': api_key})
                res = r.json()
                for indicator in res['results']:
                    ind_maltego = cores[indicator['type']]()
                    ind_maltego.value = indicator['indicator']
                    ind_maltego.link_label = indicator['created']
                    response += ind_maltego
            else:
                is_finish = True
        return response
