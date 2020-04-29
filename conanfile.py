from conans import ConanFile, tools
import os


class SmlConan(ConanFile):
    name = "sml"
    description = "[Boost].SML: C++14 State Machine Library"
    topics = ("conan", "sml", "state-machine")
    url = "https://github.com/bincrafters/conan-sml"
    homepage = "https://github.com/boost-experimental/sml"
    license = "BSL-1.0"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    no_copy_source = True

    _source_subfolder = "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)

    def package_id(self):
        self.info.header_only()
