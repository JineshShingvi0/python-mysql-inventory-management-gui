from invoice import generate_invoice

cart = [
    {
        "name":"Groundnut Oil",
        "quantity":2,
        "price":600,
        "subtotal":1200
    },
    {
        "name":"Mustard Oil",
        "quantity":2,
        "price":300,
        "subtotal":600
    }
]

path = generate_invoice(
    sale_id=1,
    customer_name="Jinesh Shingvi",
    phone="9881353330",
    payment_method="UPI",
    cart=cart,
    subtotal=1800,
    gst=324,
    discount=0,
    grand_total=2124
)

print(path)