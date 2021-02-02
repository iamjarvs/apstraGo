"""
==========================================
 Title:  ApstraGo
 Author: Adam Jarvis
 Date:   2021
==========================================

"""
from rich import print
import requests
import json 
    
class errors():

    def __init__(self):
        super().__init__() 

    """
    Error Catch
    """
    def customError(self, response: bytes) -> print:
        print("#" * 120)
        if isinstance(response, requests.models.Response):
            print(f"""\n[bold red]Error[/]:\n     {str(response.json()['errors'])} \n     {response.reason} \n     {response.text} \n     {response.url} \n     {response.status_code}\n""")
        elif isinstance(response, str):
            print(f'''[bold red]Error[/]:\n     {response}''')
        elif isinstance(response, dict):
            print(f'''\n[bold red]Error: YAML Input Issue[/]\n     {json.dumps(response, indent=4)}\n''')
        print("#" * 120)
        print('\n')

    def customSuccess(self, response: bytes) -> print:
        print("#" * 120)
        if isinstance(response, requests.models.Response):
            print(f"""\n[bold green]Success[/]:\n     {response.reason} \n     {response.text} \n     {response.url} \n     {response.status_code}\n""")
        elif isinstance(response, str):
            print(f"""\n[bold green]Success[/]:\n     {response}""")    
        print("#" * 120)
        print('\n')