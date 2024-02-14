Demo of virtual QA engineer agents

Have 2 commands

Converts open github repository  to swagger spec files, require org repo branch

```bash
git2swagger -t "Use repository spring-petclinic/spring-framework-petclinic with branch main It is Java Spring application, please create swagger spec. Deployment URL is https://petclinic.example.com"
```

Converts swagger files to gherkin test cases

```bash
swagger2gherkin
```

Environment requirements

```bash
AZURE_LLM_ENDPOINT=
OPENAI_API_KEY=
OPENAI_API_VERSION=
DEPLOYMENT_NAME=
MAX_TOKEN=
RESULT_PATH=
GHERKIN_PATH=
```