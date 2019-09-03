import logging

from canari.maltego.entities import Domain, IPv4Address, Phrase, Hash
from canari.maltego.transform import Transform
from OTX_transform.otx_transforms.transforms.common.entities import Pulse
from OTX_transform.otx_transforms.transforms.common.utils import gram,cores,type_hash
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
        logging.debug(url)
        r = requests.get(url, headers={'X-OTX-API-KEY': api_key})
        if r.status_code == 200:
            try:
                res = r.json()
            except:
                p = Phrase(url)
                response +=p
                return response

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

class PulsesHashes(Pulses):
    input_type = Hash
    namespace = 'Otx_Transform'

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

        url = '%s/pulses/%s/indicators' % (base_url, id_p)

        is_finish = False

        while not is_finish:
            if url:
                r = requests.get(url, headers={'X-OTX-API-KEY': api_key})
                res = r.json()
                for indicator in res['results']:
                    ind_maltego = cores[indicator['type']]()
                    if indicator['type'] in type_hash:
                        ind_maltego.type = type_hash[indicator['type']]
                    ind_maltego.value = indicator['indicator']
                    ind_maltego.link_label = indicator['created']
                    ind_maltego.url = 'https://otx.alienvault.com/indicator/%s/%s' \
                                      % (indicator['type'], indicator['indicator'])
                    response += ind_maltego
                url = res['next']
            else:
                is_finish = True
        return response


class PDNS(Transform):
    input_type = Domain
    namespace = "Otx_Transform"

    def do_transform(self, request, response, config):
        base_url = config['OTX_transform.local.otx_url']
        api_key = config['OTX_transform.local.api_key']
        host = request.entity.value
        url = '%s/indicators/hostname/%s/passive_dns' %\
              (base_url, host)
        r = requests.get(url, headers={'X-OTX-API-KEY': api_key})
        if r.status_code == 200:

            res = r.json()

            for pdns in res['passive_dns']:

                ip = IPv4Address(pdns['address'])
                ip.link_label = 'last: %s' % pdns['last']
                response += ip

        return response