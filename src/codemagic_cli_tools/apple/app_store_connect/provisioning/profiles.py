from typing import List
from typing import Optional
from typing import Union

from codemagic_cli_tools.apple.app_store_connect.resource_manager import ResourceManager
from codemagic_cli_tools.apple.resources import BundleId
from codemagic_cli_tools.apple.resources import Certificate
from codemagic_cli_tools.apple.resources import Device
from codemagic_cli_tools.apple.resources import LinkedResourceData
from codemagic_cli_tools.apple.resources import Profile
from codemagic_cli_tools.apple.resources import ProfileState
from codemagic_cli_tools.apple.resources import ProfileType
from codemagic_cli_tools.apple.resources import ResourceId
from codemagic_cli_tools.apple.resources import ResourceType


class ProfileOrdering(ResourceManager.Ordering):
    ID = 'id'
    NAME = 'name'
    PROFILE_STATE = 'profileState'
    PROFILE_TYPE = 'profileType'


class Profiles(ResourceManager):
    """
    Profiles
    https://developer.apple.com/documentation/appstoreconnectapi/profiles
    """

    def create(self,
               name: str,
               profile_type: ProfileType,
               bundle_id: Union[ResourceId, BundleId],
               certificates: List[Union[ResourceId, Certificate]],
               devices: List[Union[ResourceId, Device]]) -> Profile:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/create_a_profile
        """
        if devices is None:
            devices = []
        attributes = {
            'name': name,
            'profileType': profile_type.value
        }
        relationships = {
            'bundleId': {
                'data': self._get_attribute_data(bundle_id, ResourceType.BUNDLE_ID)
            },
            'certificates': {
                'data': [self._get_attribute_data(c, ResourceType.CERTIFICATES) for c in certificates]
            },
            'devices': {
                'data': [self._get_attribute_data(d, ResourceType.DEVICES) for d in devices]
            }
        }
        payload = self._get_create_payload(
            ResourceType.PROFILES, attributes=attributes, relationships=relationships)
        response = self.client.session.post(f'{self.client.API_URL}/profiles', json=payload).json()
        return Profile(response['data'])

    def delete(self, profile: Union[LinkedResourceData, ResourceId]) -> None:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/delete_a_profile
        """
        profile_id = self._get_resource_id(profile)
        self.client.session.delete(f'{self.client.API_URL}/profiles/{profile_id}')

    def list(self,
             filter_id: Optional[Union[str, ResourceId]] = None,
             filter_name: Optional[str] = None,
             filter_profile_state: Optional[ProfileState] = None,
             filter_profile_type: Optional[ProfileType] = None,
             ordering=ProfileOrdering.NAME,
             reverse=False) -> List[Profile]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/list_and_download_profiles
        """
        params = {'sort': ordering.as_param(reverse)}
        if filter_id is not None:
            params['filter[id]'] = filter_id
        if filter_profile_state is not None:
            params['filter[profileState]'] = filter_profile_state.value
        if filter_profile_type is not None:
            params['filter[profileType]'] = filter_profile_type.value
        if filter_name is not None:
            params['filter[name]'] = filter_name

        profiles = self.client.paginate(f'{self.client.API_URL}/profiles', params=params)
        return [Profile(profile) for profile in profiles]

    def read(self, profile: Union[LinkedResourceData, ResourceId]) -> Profile:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/read_and_download_profile_information
        """
        profile_id = self._get_resource_id(profile)
        response = self.client.session.get(f'{self.client.API_URL}/profiles/{profile_id}').json()
        return Profile(response['data'])

    def read_bundle_id(self, profile: Union[Profile, ResourceId]) -> BundleId:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/read_the_bundle_id_in_a_profile
        """
        if isinstance(profile, Profile):
            url = profile.relationships.bundleId.links.related
        else:
            url = f'{self.client.API_URL}/profiles/{profile}/bundleId'
        response = self.client.session.get(url).json()
        return BundleId(response['data'])

    def get_bundle_id_resource_id(self, profile: Union[Profile, ResourceId]) -> LinkedResourceData:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/get_the_bundle_resource_id_in_a_profile
        """
        if isinstance(profile, Profile):
            url = profile.relationships.bundleId.links.self
        else:
            url = f'{self.client.API_URL}/profiles/{profile}/relationships/bundleId'
        response = self.client.session.get(url).json()
        return LinkedResourceData(response['data'])

    def list_certificates(self, profile: Union[Profile, ResourceId]) -> List[Certificate]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/list_all_certificates_in_a_profile
        """
        if isinstance(profile, Profile):
            url = profile.relationships.profiles.links.related
        else:
            url = f'{self.client.API_URL}/profiles/{profile}/certificates'
        return [Certificate(certificate) for certificate in self.client.paginate(url)]

    def list_certificate_ids(self, profile: Union[Profile, ResourceId]) -> List[LinkedResourceData]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/get_all_certificate_ids_in_a_profile
        """
        if isinstance(profile, Profile):
            url = profile.relationships.profiles.links.self
        else:
            url = f'{self.client.API_URL}/profiles/{profile}/relationships/certificates'
        return [LinkedResourceData(certificate) for certificate in self.client.paginate(url)]

    def list_devices(self, profile: Union[Profile, ResourceId]) -> List[Device]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/list_all_devices_in_a_profile
        """
        if isinstance(profile, Profile):
            url = profile.relationships.profiles.links.related
        else:
            url = f'{self.client.API_URL}/profiles/{profile}/devices'
        return [Device(device) for device in self.client.paginate(url)]

    def list_device_ids(self, profile: Union[Profile, ResourceId]) -> List[LinkedResourceData]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/get_all_device_resource_ids_in_a_profile
        """
        if isinstance(profile, Profile):
            url = profile.relationships.profiles.links.self
        else:
            url = f'{self.client.API_URL}/profiles/{profile}/relationships/devices'
        return [LinkedResourceData(device) for device in self.client.paginate(url)]