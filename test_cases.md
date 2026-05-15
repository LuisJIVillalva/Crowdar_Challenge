# Casos de Prueba — saucedemo.com

## Funcionalidad 1: Inicio de Sesión

| ID | Descripción | Datos de entrada | Resultado esperado |
|----|-------------|-----------------|-------------------|
| TC-L01 | Login exitoso | user: `standard_user` / pass: `secret_sauce` | Redirige a `/inventory.html` |
| TC-L02 | Contraseña incorrecta | user: `standard_user` / pass: `mal_password` | Mensaje de error "do not match" |
| TC-L03 | Usuario bloqueado | user: `locked_out_user` / pass: `secret_sauce` | Mensaje de error "locked out" |
| TC-L04 | Campos vacíos | Sin datos | Mensaje de error "Username is required" |
| TC-L05 | Solo contraseña vacía | user: `standard_user` / pass: vacío | Mensaje de error "Password is required" |

---

## Funcionalidad 2: Carrito de Compras

| ID | Descripción | Precondición | Resultado esperado |
|----|-------------|-------------|-------------------|
| TC-C01 | Agregar un producto | Sesión iniciada | Badge del carrito muestra "1" |
| TC-C02 | Agregar múltiples productos | Sesión iniciada | Badge muestra cantidad correcta |
| TC-C03 | Producto aparece en vista del carrito | Producto agregado | El nombre del producto figura en el carrito |
| TC-C04 | Eliminar producto del carrito | Producto en carrito | El carrito queda vacío |
| TC-C05 | Botón cambia a "Remove" al agregar | Sesión iniciada | El botón del producto cambia de texto |

---

## Funcionalidad 3: API Mercado Libre

| ID | Descripción | Endpoint | Resultado esperado |
|----|-------------|---------|-------------------|
| TC-API01 | Status 200 | `GET /menu/departments` | HTTP 200 |
| TC-API02 | Respuesta contiene departamentos | `GET /menu/departments` | Body contiene palabras clave de categorías |

