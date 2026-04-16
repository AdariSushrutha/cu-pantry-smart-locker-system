import requests


def lookup_barcode(barcode):
    """
    Look up a product by barcode using Open Food Facts API.
    Returns product details or None if not found.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    try:
        headers = {
    'User-Agent': 'CUPantryApp/1.0 (cupantry@clarkson.edu)'
}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()

        if data.get('status') == 1:
            product = data.get('product', {})

            name = (
                product.get('product_name_en') or
                product.get('product_name') or
                'Unknown Product'
            )

            categories = product.get('categories', '').lower()
            if any(word in categories for word in ['frozen', 'ice cream', 'freeze']):
                temperature_category = 'frozen'
            elif any(word in categories for word in ['refrigerated', 'dairy', 'meat', 'fresh']):
                temperature_category = 'refrigerated'
            else:
                temperature_category = 'ambient'

            return {
                'found': True,
                'barcode': barcode,
                'name': name,
                'image_url': product.get('image_url', ''),
                'brands': product.get('brands', ''),
                'quantity': product.get('quantity', ''),
            }
        else:
            return {
                'found': False,
                'barcode': barcode,
                'message': 'Product not found in database.'
            }

    except requests.exceptions.RequestException as e:
        return {
            'found': False,
            'barcode': barcode,
            'message': f'Error looking up barcode: {str(e)}'
        }