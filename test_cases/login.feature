@login @happy_path
Scenario Outline: Login exitoso con usuarios válidos
Given que el usuario ingresa a: www.saucedemo.com
When completa el usuario "<usuario>"
And completa la contraseña "<password>"
And presiona el botón de login
Then el usuario accede correctamente al inventario
And visualiza la página de productos
Examples:
| usuario                | password     |
| standard_user          | secret_sauce |
| problem_user           | secret_sauce |
| error_user             | secret_sauce |
| visual_user            | secret_sauce |

@login @negative
Scenario Outline: Login con <case_name>
Given que el usuario ingresa a: www.saucedemo.com
When completa el usuario "<usuario>"
And completa la contraseña "<password>"
And presiona el botón de login
Then el sistema muestra el mensaje de error "<mensaje>"
Examples:
| usuario          | password           | mensaje                                                                   | case_name              |
| locked_out_user  | secret_sauce       | Epic sadface: Sorry, this user has been locked out.                       | usuario bloqueado      |
| standard_user    | incorrect_password | Epic sadface: Username and password do not match any user in this service | contraseña incorrecta  |
| incorrect_user   | secret_sauce       | Epic sadface: Username and password do not match any user in this service | usuario incorrecto     |
| standard_user    |                    | Epic sadface: Password is required                                        | campo contraseña vacio |
|                  | secret_sauce       | Epic sadface: Username is required                                        | campo usuario vacio    |
