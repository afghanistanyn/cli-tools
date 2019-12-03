from typing import List
from typing import Optional
from typing import Union

from codemagic_cli_tools.apple.app_store_connect.resource_manager import ResourceManager
from codemagic_cli_tools.apple.resources import BundleId
from codemagic_cli_tools.apple.resources import BundleIdCapability
from codemagic_cli_tools.apple.resources import BundleIdPlatform
from codemagic_cli_tools.apple.resources import LinkedResourceData
from codemagic_cli_tools.apple.resources import Profile
from codemagic_cli_tools.apple.resources import ResourceId
from codemagic_cli_tools.apple.resources import ResourceType


class BundleIdOrdering(ResourceManager.Ordering):
    ID = 'id'
    NAME = 'name'
    PLATFORM = 'platform'
    SEED_ID = 'seedId'


class BundleIds(ResourceManager):
    """
    Bundle IDs
    https://developer.apple.com/documentation/appstoreconnectapi/bundle_ids
    """

    def register(self,
                 identifier: str,
                 name: str,
                 platform: BundleIdPlatform,
                 seed_id: Optional[str] = None) -> BundleId:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/register_a_new_bundle_id
        """
        attributes = {
            'name': name,
            'identifier': identifier,
            'platform': platform.value,
        }
        if seed_id:
            attributes['seedId'] = seed_id
        response = self.client.session.post(
            f'{self.client.API_URL}/bundleIds',
            json=self._get_create_payload(ResourceType.BUNDLE_ID, attributes=attributes)
        ).json()
        return BundleId(response['data'])

    def modify(self, bundle_id: Union[LinkedResourceData, ResourceId], name: str) -> BundleId:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/modify_a_bundle_id
        """
        bundle_id_resource_id = self._get_resource_id(bundle_id)
        payload = self._get_update_payload(bundle_id_resource_id, ResourceType.BUNDLE_ID, {'name': name})
        response = self.client.session.patch(
            f'{self.client.API_URL}/bundleIds/{bundle_id_resource_id}', json=payload).json()
        return BundleId(response['data'])

    def delete(self, bundle_id: Union[LinkedResourceData, ResourceId]) -> None:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/delete_a_bundle_id
        """
        bundle_id_resource_id = self._get_resource_id(bundle_id)
        self.client.session.delete(f'{self.client.API_URL}/bundleIds/{bundle_id_resource_id}')

    def list(self, ordering=BundleIdOrdering.NAME, reverse=False) -> List[BundleId]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/list_bundle_ids
        """
        params = {'sort': ordering.as_param(reverse)}
        bundle_ids = self.client.paginate(f'{self.client.API_URL}/bundleIds', params=params)
        return [BundleId(bundle_id) for bundle_id in bundle_ids]

    def read(self, bundle_id: Union[LinkedResourceData, ResourceId]) -> BundleId:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/read_bundle_id_information
        """
        bundle_id_resource_id = self._get_resource_id(bundle_id)
        response = self.client.session.get(f'{self.client.API_URL}/bundleIds/{bundle_id_resource_id}').json()
        return BundleId(response['data'])

    def list_profile_ids(self, bundle_id: Union[BundleId, ResourceId]) -> List[LinkedResourceData]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/get_all_profile_ids_for_a_bundle_id
        """
        if isinstance(bundle_id, BundleId):
            url = bundle_id.relationships.profiles.links.self
        else:
            url = f'{self.client.API_URL}/bundleIds/{bundle_id}/relationships/profiles'
        return [LinkedResourceData(bundle_id_profile) for bundle_id_profile in self.client.paginate(url)]

    def list_profiles(self, bundle_id: Union[BundleId, ResourceId]) -> List[Profile]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/list_all_profiles_for_a_bundle_id
        """
        if isinstance(bundle_id, BundleId):
            url = bundle_id.relationships.profiles.links.related
        else:
            url = f'{self.client.API_URL}/bundleIds/{bundle_id}/profiles'
        return [Profile(profile) for profile in self.client.paginate(url)]

    def list_capabilility_ids(self, bundle_id: Union[BundleId, ResourceId]) -> List[LinkedResourceData]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/get_all_capabilility_ids_for_a_bundle_id
        """
        if isinstance(bundle_id, BundleId):
            url = bundle_id.relationships.bundleIdCapabilities.links.self
        else:
            url = f'{self.client.API_URL}/bundleIds/{bundle_id}/relationships/bundleIdCapabilities'
        return [LinkedResourceData(capabilility) for capabilility in self.client.paginate(url, page_size=None)]

    def list_capabilities(self, bundle_id: Union[BundleId, ResourceId]) -> List[BundleIdCapability]:
        """
        https://developer.apple.com/documentation/appstoreconnectapi/list_all_capabilities_for_a_bundle_id
        """
        if isinstance(bundle_id, BundleId):
            url = bundle_id.relationships.bundleIdCapabilities.links.related
        else:
            url = f'{self.client.API_URL}/bundleIds/{bundle_id}/bundleIdCapabilities'
        return [BundleIdCapability(capabilility) for capabilility in self.client.paginate(url, page_size=None)]