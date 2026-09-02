import qrcode

def generate_account_qr(account):

    data = f"""
Account Number: {account.account_number}
Name: {account.customer.user.get_full_name()}
IFSC: {account.ifsc}
"""

    img = qrcode.make(data)

    img.save(f"media/qrcode/{account.account_number}.png")