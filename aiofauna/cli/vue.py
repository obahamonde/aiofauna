import pathlib
from typing import Any, Dict, Generator, Tuple

import jinja2

from main import app

VUE_TEMPLATE = """
<script setup lang="ts">
  #{ if in == 'query' }
const @{ name } = ref < @{ type } > (@{ default });
  #{ else }
const @{ name } = ref < @{ type } > (@{ default });
  #{ endif }

  #{ if body }
  export interface @{ body.content['application/json'].schema.title } {
    #{ for k, v in body.content['application/json'].schema.properties.items() }
  @{ k }: @{ v.type };
    #{ endfor }
}
  #{ endif }

const url = computed(() => {
  let url = '@{ path }' + '?' + @{ params }.map(p => p.name + '=' + p.value).join('&');
  return url;
});

const trigger = ref(false);
</script>

<template>
  <Request method="@{ method }" :url="url" :headers="headers" :body="body" v-if="trigger">
    <slot :json="{ json }"></slot>

    <slot #actions="{ json }">
      <button @click="trigger = !trigger">Send</button>
    </slot>

    <slot #error="{ json }">
      <div v-if="json.error">
        <h3>Error</h3>
        <pre>{{ json.error }}</pre>
      </div>
    </slot>
  </Request>
</template>
"""


class Templater(object):
    def generator(self) -> Generator[Dict[str, Any], None, None]:
        """
        Generator that yields a dictionary of data for each endpoint.
        on the OpenAPI spec.
        """
        paths = app.openapi["paths"]
        for path in paths:
            for k, v in paths[path].items():
                method = k.upper()
                name = v["summary"]
                _body = v.get("requestBody")
                _params = v["parameters"]
                params = []
                for param in _params:
                    _in = param["in"]
                    name = param["name"]
                    required = param["required"]
                    _type = param["schema"]["type"]
                    default = param["schema"].get("default")

                    yield {
                        "path": path,
                        "method": method,
                        "in": _in,
                        "required": required,
                        "default": default,
                        "type": _type.__name__,
                        "name": name,
                        "params": params,
                        "body": _body,
                        "headers": {"Content-Type": "application/json"},
                    }

    @property
    def template(self) -> str:
        """The Base Vue Template with an slotted Request component."""
        template_str = (
            pathlib.Path(__file__)
            .parent.joinpath("templates", "__init__.vue")
            .read_text()
        )
        return template_str

    def render(self) -> Generator[Tuple[Any,str], None, None]:
        """
        Generator that yields a rendered template for each endpoint.
        on the OpenAPI spec.
        """
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath="templates"),
            variable_start_string="@{",
            variable_end_string="}",
            comment_start_string="##{",
            comment_end_string="}",
            block_start_string="#{",
            block_end_string="}",
        )
        template = env.from_string(self.template)
        for data in self.generator():
            yield data.get("name"), template.render(**data)


def generate_components() -> None:
    """Generate Vue Components for each endpoint on the OpenAPI spec."""
    for name, component in Templater().render():
        if not pathlib.Path("app/src/components").exists():
            pathlib.Path("app/src/components").mkdir(parents=True)
        pathlib.Path(f"app/src/components/{name}.vue").write_text(component)  
        print(f"Generated {name}.vue")
        
        
def main():
  number_of_components = len(list(Templater().generator()))
  print(f"{number_of_components} will be generated are you sure you want to continue? (y/n)")
  if input() == "y":
    generate_components()
    print("Done!")
  else:
    print("Aborted")
  
  
if __name__ == "__main__":
  main()