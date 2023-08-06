import glob
import os
import traceback

from uetools.core.plugin import discover_plugins

try:
    import uetools.plugins

    PLUGINS = True

except ModuleNotFoundError:
    PLUGINS = False

except ImportError:
    PLUGINS = False


def fetch_factories(registry, base_module, base_file_name, function_name="COMMANDS"):
    """Loads all the defined commands"""
    module_path = os.path.dirname(os.path.abspath(base_file_name))

    for module_path in glob.glob(
        os.path.join(module_path, "[A-Za-z]*"), recursive=False
    ):
        module_file = module_path.split(os.sep)[-1]

        if module_file == base_file_name:
            continue

        module_name = module_file.split(".py")[0]

        try:
            module = __import__(".".join([base_module, module_name]), fromlist=[""])
        except ImportError:
            print(traceback.format_exc())
            continue

        if hasattr(module, function_name):
            cmd = getattr(module, function_name)
            registry.insert_commands(cmd)


def discover_from_plugins_commands(registry, module, function_name="COMMANDS"):
    """Imports all commands for the plugins we found"""
    plugins = discover_plugins(module)

    for _, plugin in plugins.items():

        if hasattr(plugin, function_name):
            plugin_commands = getattr(plugin, function_name)
            registry.insert_commands(plugin_commands)


#: pylint: disable=too-few-public-methods
class CommandRegistry:
    """Simple class to keep track of all the commands we find"""

    def __init__(self):
        self.found_commands = {}

    def insert_commands(self, cmds):
        """Insert a command into the registry makes sure it is unique"""
        if not isinstance(cmds, list):
            cmds = [cmds]

        for cmd in cmds:
            if cmd.name != cmd.name.strip():
                print(f"Warning: {cmd.name} has white space before or after the name")

            assert (
                cmd.name not in self.found_commands
            ), f"Duplicate command name: {cmd.name}"
            self.found_commands[cmd.name] = cmd


def discover_commands():
    """Discover all the commands we can find (plugins and built-in)"""
    registry = CommandRegistry()
    fetch_factories(registry, "uetools.commands", __file__)

    if PLUGINS:
        discover_from_plugins_commands(registry, uetools.plugins)

    return registry.found_commands


commands = discover_commands()


def find_command(name):
    return commands.get(name)
