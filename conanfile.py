from conans import ConanFile, tools
import os


class SmlConan(ConanFile):
    name = "sml"
    description = "[Boost].SML: C++14 State Machine Library"
    topics = ("conan", "sml", "state-machine")
    url = "https://github.com/bincrafters/conan-sml"
    homepage = "https://github.com/boost-experimental/sml"
    license = "BSL-1.0"
    settings = "compiler"
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return os.path.join(self.source_folder, "source_subfolder")

    def configure(self):
        minimal_cpp_standard = "14"
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, minimal_cpp_standard)
        minimal_version = {
            "gcc": "5",
            "clang": "3.4",
            "apple-clang": "10",
            "Visual Studio": "14"
        }
        compiler = str(self.settings.compiler)
        if compiler not in minimal_version:
            self.output.warn(
                "%s recipe lacks information about the %s compiler standard version support." % (self.name, compiler))
            self.output.warn(
                "%s requires a compiler that supports at least C++%s." % (self.name, minimal_cpp_standard))
            return
        version = tools.Version(self.settings.compiler.version)
        if version < minimal_version[compiler]:
            raise ConanInvalidConfiguration("%s requires a compiler that supports at least C++%s." % (self.name, minimal_cpp_standard))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _extract_license(self):
        header = tools.load(os.path.join(self._source_subfolder, "include", "boost", "sml.hpp"))
        license_contents = header[0:header.find("#", 2)]
        tools.save("LICENSE", license_contents)

    def package(self):
        self._extract_license()
        self.copy("LICENSE", dst="licenses")
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)

    def package_id(self):
        self.info.header_only()
