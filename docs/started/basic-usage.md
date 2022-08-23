
Using `PyI18n` in your application is pretty easy, all you need to do before is create your `locale` files.

!!! info
    By default `PyI18n` will look for your `locale` files in `./locale` directory.

## Create loacle files

You can create as many files as you need for the languages in your application, `PyI18n` will handle it.

```sh
$ mkdir locale
$ touch locale/en.yml
$ touch locale/pl.yml
```

Those files have to be in YAML format, for e.g. you're creating online shop

??? example "Example `pl` locale file"
    ```yaml
    pl:
        labels:
            products: Produkty
            cart: Koszyk
            checkout: Złóż zamówienie
        messages:
            cart:
                empty: Koszyk jest pusty
                total: "Łącznie: {total}"
            checkout:
                title: Złóż zamówienie
                name: Imię
                surname: Nazwisko
                email: Email
                phone: Telefon
                address: Adres
                city: Miasto
                zip: Kod pocztowy
                country: Kraj
                payment: Metoda płatności
                payment_method_card: Karta
                payment_method_cash: Gotówka
                payment_method_transfer: Przelew
                payment_method_paypal: PayPal
                payment_method_other: Inne
                payment_method_other_description: Opis płatności
    ```

??? example "Example `en` locale file"

    ```yaml
    en:
        labels:
            products: Products
            cart: Cart
            checkout: Checkout
        messages:
            cart:
                empty: Cart is empty
                total: "Total: {total}"
            checkout:
                title: Checkout
                name: Name
                surname: Surname
                email: Email
                phone: Phone
                address: Address
                city: City
                zip: Zip
                country: Country
                payment: Payment method
                payment_method_card: Card
                payment_method_cash: Cash
                payment_method_transfer: Transfer
                payment_method_paypal: PayPal
                payment_method_other: Other
                payment_method_other_description: Payment method description
    ```

## Integrate with your application

Application structure
```sh
.
├── locales
│   ├── en.yml
│   └── pl.yml
└── store.py
```

```py
products = {
    '1': {
        'name': 'Chocolate',
        'price': '$2.00',
        'description': 'A delicious chocolate',
    },
    '2': {
        'name': 'Coffee',
        'price': '$3.00',
        'description': 'A delicious coffee',
    },
    '3': {
        'name': 'Tea',
        'price': '$1.00',
        'description': 'A delicious tea',
    },
}

if __name__ == "__main__":
    available_locales: Tuple[str] = ('en', 'pl')

    user_locale: str = input('Enter your locale: ')
    if user_locale.lower() not in available_locales:
        print('Locale not supported, please select another one')
        sys.exit(1)

    i18n: PyI18n = PyI18n(available_locales)
    _ = i18n.gettext

    print(_(user_locale, 'messages.welcome'))
    print("============================")
    print(_(user_locale, 'labels.products') + ": \n")

    if not products:
        print(_(user_locale, 'messages.product_list.empty'))
    else:
        for product in products:
            print(f"{product} - {products[product]['name']} - {products[product]['price']}")
```

## Json format files

Lets take a look at the example above, we can use json format files as well.

!!! info
    In this example we're using `PyI18nJsonLoader` to load translations from `translations/` directory.

!!! tip
    Don't pass `load_path` argument to `PyI18n` constructor if you're using loader other than `PyI18nYamlLoader` (build-in). You should specify `load_path` argument in your loader instead.

```py

from pyi18n import PyI18n
from pyi18n.loaders import PyI18nJsonLoader

if __name__ == "__main__":
    available_locales: Tuple[str] = ('en', 'pl')
    loader: PyI18nJsonLoader = PyI18nJsonLoader('translations/')
    i18n: PyI18n = PyI18n(available_locales, loader=loader)
    _ = i18n.gettext

```

