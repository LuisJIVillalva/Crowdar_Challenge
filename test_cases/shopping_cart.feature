 @carrito @happy_path
  Scenario Outline: Agregar un producto al carrito de compra
    Given que el usuario ingresa a : www.saucedemo.com
    And inicia sesión con el usuario "<usuario>" y la contraseña "secret_sauce"
    When agrega el producto "<producto>" al carrito
    And el ícono del carrito muestra "<cantidad>" producto
    Then el producto "<producto>" aparece en el carrito

    Examples:
      | usuario                 | producto                | cantidad |
      | standard_user           | Sauce Labs Backpack     | 1        |
      | performance_glitch_user | Sauce Labs Backpack     | 1        |

  @carrito @happy_path
  Scenario Outline: Agregar todos los productos al carrito
    Given que el usuario ingresa a : www.saucedemo.com
    And inicia sesión con el usuario "<usuario>" y la contraseña "secret_sauce"
    When agrega todos los productos existentes al carrito
    Then los productos seleccionados aparecen en el carrito

    Examples:
      | usuario                 |
      | standard_user           |
      | performance_glitch_user |

  @carrito @happy_path
  Scenario Outline: Agregar todos los productos y removerlos hasta dejar 1
    Given que el usuario ingresa a : www.saucedemo.com
    And inicia sesión con el usuario "<usuario>" y la contraseña "secret_sauce"
    When agrega todos los productos disponibles al carrito
    And remueve los siguientes productos:
      | producto                     |
      | Sauce Labs Backpack          |
      | Sauce Labs Bike Light        |
      | Sauce Labs Bolt T-Shirt      |
      | Sauce Labs Fleece Jacket     |
      | Sauce Labs Onesie            |
    Then el ícono del carrito muestra "1" producto
    And queda solo el producto "Test.allTheThings() T-Shirt (Red)" en el carrito

    Examples:
      | usuario                 |
      | standard_user           |
      | performance_glitch_user |

  @carrito @happy_path
  Scenario Outline: Agregar y remover un producto varias veces
    Given que el usuario ingresa a : www.saucedemo.com
    And inicia sesión con el usuario "<usuario>" y la contraseña "secret_sauce"
    When se agrega y elimina "<cantidad>" veces un producto
    Then el ícono del carrito muestra "1" producto
    And el producto "Sauce Labs Backpack" aparece en el carrito

    Examples:
      | usuario                 |cantidad|
      | standard_user           |2       |
      | standard_user           |5       |
      | standard_user           |10      |
      | performance_glitch_user |2       |
      | performance_glitch_user |13      |
      | performance_glitch_user |11      |

  @detalle @happy_path
  Scenario Outline: Agregar al carrito desde el detalle del producto
    Given que el usuario ingresa a : www.saucedemo.com
    And inicia sesión con el usuario "<usuario>" y la contraseña "secret_sauce"
    And ingresa al detalle de un producto
    When agrega el producto al carrito desde la pagina de detalle
    Then el ícono del carrito muestra "1" producto
    And el producto agregado aparece en el carrito

    Examples:
      | usuario                 |
      | standard_user           |
      | performance_glitch_user |

  @detalle @happy_path
  Scenario Outline: Agregar producto desde el inventario y removerlo desde la pagina de detalle
    Given que el usuario ingresa a : www.saucedemo.com
    And inicia sesión con el usuario "<usuario>" y la contraseña "secret_sauce"
    And agrega un producto al carrito
    When ingresa al detalle del producto agregado al carrito
    And remueve el producto
    Then el ícono del carrito no muestra productos
    And el carrito se encuentra vacío

    Examples:
      | usuario                 |
      | standard_user           |
      | performance_glitch_user |

  @carrito @happy_path
  Scenario Outline: Remover todos los productos desde el carrito
    Given que el usuario ingresa a : www.saucedemo.com
    And inicia sesión con el usuario "<usuario>" y la contraseña "secret_sauce"
    And agrega todos los productos disponibles al carrito
    And ingresa al carrito de compras
    When remueve todos los productos desde el carrito
    Then el carrito se encuentra vacío
    And el ícono del carrito no muestra productos

    Examples:
      | usuario                 |
      | standard_user           |
      | performance_glitch_user |
