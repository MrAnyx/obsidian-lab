import frontmatter
from yaml import CSafeDumper as SafeDumper
import yaml


class FrontmatterHandler(frontmatter.YAMLHandler):
    def export(self, metadata, **kwargs):
        kwargs.setdefault("Dumper", SafeDumper)
        kwargs.setdefault("default_flow_style", False)
        kwargs.setdefault("allow_unicode", True)
        kwargs.setdefault("sort_keys", True)

        SafeDumper.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:null", ""),
        )

        metadata = yaml.dump(metadata, **kwargs).strip()
        return metadata
