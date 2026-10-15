from datetime import date

class Product:
    def __init__(self, product_id, name, price, stock, expiration_date):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.expiration_date = expiration_date 


class Store:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.products = {} 

    @property
    def total_items(self):
        return sum(p.stock for p in self.products.values())

    def add_product(self, product):
        if product.product_id in self.products:
            raise ValueError(f"Το προϊόν με id {product.product_id} υπάρχει ήδη.")
        if product.stock < 0 or product.price < 0:
            raise ValueError("Η τιμή και το απόθεμα δεν μπορούν να είναι αρνητικά.")
        if self.total_items + product.stock > self.capacity:
            raise ValueError(f"Το κατάστημα είναι γεμάτο! Δεν χωράνε τα {product.stock} τεμάχια του '{product.name}'.")
        self.products[product.product_id] = product

    def remove_product(self, product_id):
        if product_id not in self.products:
            raise ValueError("Το προϊόν δεν βρέθηκε στο κατάστημα.")
        return self.products.pop(product_id)


class Customer:
    def __init__(self, name):
        self.name = name
        self.cart = []

    def add_to_cart(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Η ποσότητα πρέπει να είναι θετική.")
        if quantity > product.stock:
            raise ValueError(f"Το '{product.name}' έχει μόνο {product.stock} τεμάχια (ζητήσατε {quantity}).")
        if product.expiration_date < date.today():
            raise ValueError(f"Το '{product.name}' έχει λήξει.")
        self.cart.append([product, quantity])

    def checkout(self):
        for product, quantity in self.cart:
            if quantity > product.stock:
                raise ValueError(f"Δεν υπάρχει πια αρκετό απόθεμα για '{product.name}'.")
        total = 0
        for product, quantity in self.cart:
            product.stock -= quantity  
            total += product.price * quantity
        self.cart = []
        return round(total, 2)


if __name__ == "__main__":
    store = Store("Super Market Central", 40)

 
    milk = Product(1, "Γάλα", 1.50, 10, date(2026, 10, 30))
    bread = Product(2, "Ψωμί", 1.20, 15, date(2026, 10, 20))
    cheese = Product(3, "Τυρί", 4.50, 5, date(2026, 11, 15))

    for p in (milk, bread, cheese):
        store.add_product(p)
    print("Τεμάχια στο κατάστημα:", store.total_items)

    maria = Customer("Maria")
    try:
        maria.add_to_cart(milk, 2)
        maria.add_to_cart(bread, 3)
        maria.add_to_cart(cheese, 99)
    except ValueError as error:
        print("Σφάλμα:", error)

    total = maria.checkout()
    print(f"Συνολικό ποσό: {total}€")
    print("Τεμάχια που απέμειναν:", store.total_items)
