from importlib import import_module, util
from re import sub

#
# script files should be snake_case.
# the Class in these file should be PascalCase 
#

class Script:
    STATUS_OK = 0
    STATUS_WARNING = 1
    STATUS_CRITICAL = 2
    STATUS_UNKNOWN = 3

    @classmethod
    def run(self):
        print("hello world.")

    @staticmethod
    def factory(snakeCasetype):
        snake_str = Script.to_snake_case(snakeCasetype)
        strClass = 'scripts.' + snake_str + '.' + Script.to_pascal_case(snake_str)

        module_path, class_name = strClass.rsplit('.', 1)

        m_spec = util.find_spec(module_path)
        found = m_spec is not None

        if (found):
            module = import_module(module_path)
            return getattr(module, class_name)()
    

    # Static methode to convert snake_case to CamelCase
    @staticmethod
    def to_camel_case(snake_str):
        components = snake_str.split('_')
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
        return components[0] + ''.join(x.title() for x in components[1:])


    @staticmethod
    def to_pascal_case(snake_str):
        components = snake_str.split('_')
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
        return ''.join(x.title() for x in components)


    # Static method to convert to snake_case
    @staticmethod
    def to_snake_case(s):
        return '_'.join(
            sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
            s.replace('-', ' '))).split()).lower()
