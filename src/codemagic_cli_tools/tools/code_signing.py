import argparse
import json
import pathlib
import shlex
import shutil
from tempfile import NamedTemporaryFile
from typing import Counter
from typing import Generator
from typing import Optional
from typing import Sequence

from codemagic_cli_tools import cli
from codemagic_cli_tools.cli.colors import Colors
from codemagic_cli_tools.models import ProvisioningProfile
from .keychain import Keychain
from .mixins import PathFinderMixin


def _existing_file(path_str: str) -> pathlib.Path:
    path = pathlib.Path(path_str)
    if not path.exists():
        raise argparse.ArgumentTypeError(f'Path "{path}" does not exist')
    if not path.is_file():
        raise argparse.ArgumentTypeError(f'Path "{path}" is not a file')
    return path


class CodeSigningException(cli.CliAppException):
    pass


class CodeSigningArgument(cli.Argument):
    XCODE_PROJECT_PATTERN = cli.ArgumentProperties(
        key='xcode_project_pattern',
        flags=('--xcode-project-pattern',),
        type=pathlib.Path,
        description=(
            'Glob pattern to detect Xcode projects for which to apply the settings to, '
            'relative to working directory. Can be a literal path.'
        ),
        argparse_kwargs={'required': False, 'default': '**/*.xcodeproj'},
    )
    PROFILE_PATHS = cli.ArgumentProperties(
        key='profile_paths',
        flags=('--profiles',),
        type=_existing_file,
        description=(
            'Path to provisioning profile to be used for code signing. '
            f'If not provided, the profiles will be looked up from '
            f'{Colors.WHITE(shlex.quote(str(ProvisioningProfile.DEFAULT_LOCATION)))}.'
        ),
        argparse_kwargs={
            'required': False,
            'nargs': '+',
            'metavar': 'profile-path'
        }
    )


class CodeSigning(cli.CliApp, PathFinderMixin):
    """
    Utility to prepare iOS application code signing properties for build
    """

    @property
    def _code_signing_manager(self) -> str:
        if shutil.which('code_signing_manager.rb'):
            return 'code_signing_manager.rb'
        executable = pathlib.Path(__file__) / '..' / '..' / '..' / '..' / 'bin' / 'code_signing_manager.rb'
        return str(executable.resolve())

    @cli.action('use-profiles',
                CodeSigningArgument.XCODE_PROJECT_PATTERN,
                CodeSigningArgument.PROFILE_PATHS)
    def use_profiles(self,
                     xcode_project_pattern: pathlib.Path,
                     profile_paths: Optional[Sequence[pathlib.Path]] = None):
        """
        Set up code signing settings on specified Xcode project
        to use given provisioning profiles.
        """

        if profile_paths is None:
            profile_paths = list(ProvisioningProfile.DEFAULT_LOCATION.glob('*.mobileprovision'))
        try:
            serialized_profiles = json.dumps(list(self._serialize_profiles(profile_paths)))
        except (ValueError, IOError) as error:
            raise CodeSigningException(*error.args)

        for xcode_project in self._find_paths(xcode_project_pattern.expanduser()):
            used_profiles = self._use_profiles(xcode_project, serialized_profiles)
            # TODO: proper profile usage notice
            self.logger.info(f'Use profiles result: {used_profiles}')

    def _serialize_profiles(self, profile_paths: Sequence[pathlib.Path]) -> Generator:
        available_certs = Keychain(use_default=True) \
            .list_code_signing_certificates(should_print=False)

        for profile_path in profile_paths:
            profile = ProvisioningProfile.from_path(profile_path, cli_app=self)
            usable_certificates = profile.get_usable_certificates(available_certs)
            common_names = Counter[str](certificate.common_name for certificate in usable_certificates)
            most_popular_common = common_names.most_common(1)
            common_name = most_popular_common[0][0] if most_popular_common else ''
            yield {'certificate_common_name': common_name, **profile.dict()}

    def _use_profiles(self, xcode_project: pathlib.Path, json_serialized_profiles: str):
        with NamedTemporaryFile(mode='r', prefix='used_profiles_', suffix='.json') as used_profiles:
            cmd = (
                self._code_signing_manager,
                '--xcode-project', xcode_project,
                '--used-profiles', used_profiles.name,
                '--profiles', json_serialized_profiles,
                '--verbose'
            )
            process = self.execute(cmd)
            try:
                used_profiles_info = json.load(used_profiles)
            except ValueError:
                self.logger.debug(f'Failed to read used profiles info from {used_profiles.name}')
                used_profiles_info = {}
        if process.returncode != 0:
            error = f'Failed to set code signing settings for {xcode_project}'
            raise CodeSigningException(error, process)
        return used_profiles_info


if __name__ == '__main__':
    CodeSigning.invoke_cli()
