# FactoryBoy typing issue due to missing `__all__`

Using the documented `import factory` pattern causes VSCode and pyright errors under strict mode because `factory/__init__.py` does not define `__all__`. As a result, pyright cannot resolve the exported names (e.g. `factory.Factory`, `factory.Faker`) and reports them as unknown.

Looks like this is being tracked here: <https://github.com/FactoryBoy/factory_boy/pull/1114>

## Example

```python
import factory

class UserFactory(factory.Factory):  # error: Cannot access attribute "Factory" for class "ModuleType"
    class Meta:
        model = User

    name = factory.Faker("name")  # error: Cannot access attribute "Faker" for class "ModuleType"
    email = factory.Faker("email")
```

## Steps to reproduce

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Install project packages: `uv sync`
- Run `pyright`:

    ```shell
    uv run pyright .
    ```

    Produces type errors:

    ```txt
    /Users/gregbrown/Development/personal/bug-reports/factory-boy-typing-issue/main.py
    /Users/gregbrown/Development/personal/bug-reports/factory-boy-typing-issue/main.py:11:19 - error: Expected type arguments for generic class "Factory" (reportMissingTypeArgument)
    /Users/gregbrown/Development/personal/bug-reports/factory-boy-typing-issue/main.py:11:27 - error: "Factory" is not exported from module "factory" (reportPrivateImportUsage)
    /Users/gregbrown/Development/personal/bug-reports/factory-boy-typing-issue/main.py:12:11 - error: "Meta" overrides symbol of same name in class "Factory"
        "main.UserFactory.Meta" is not assignable to "factory.base.Factory.Meta"
        Type "type[main.UserFactory.Meta]" is not assignable to type "type[factory.base.Factory.Meta]" (reportIncompatibleVariableOverride)
    /Users/gregbrown/Development/personal/bug-reports/factory-boy-typing-issue/main.py:15:20 - error: "Faker" is not exported from module "factory" (reportPrivateImportUsage)
    /Users/gregbrown/Development/personal/bug-reports/factory-boy-typing-issue/main.py:16:21 - error: "Faker" is not exported from module "factory" (reportPrivateImportUsage)
  ```

- Open the project in VS Code with the following setting:

    ```json
    "python.analysis.typeCheckingMode": "strict"
    ```

    This produces errors in the IDE.

Note: there are no runtime issues with these imports, showing type-checking is inconsistent:

```shell
uv run python -m main                    
# User(name='Michael Castro', email='oliversheila@example.com')
```

## Expected behaviour

No errors. The symbols exported in `factory/__init__.py` are accessible via `import factory`.

## Actual behaviour

Pyright reports errors on all attribute accesses on the `factory` module because `__all__` is not defined, causing strict mode to treat the module's public API as unknown.

## Fix

Add `__all__` to `factory/__init__.py` listing all publicly exported names.
