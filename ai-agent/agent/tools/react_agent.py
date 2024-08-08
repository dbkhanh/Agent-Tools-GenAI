#Apply react agent
class ReActAgent:
    def __init__(self, tools):
        self.tools = tools

    def run(self, tool_name, message):
        for tool in self.tools:
            if tool['name'] == tool_name:
                return tool['func'](message)
        return "Tool not found!"