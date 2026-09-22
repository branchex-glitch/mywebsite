from django.core.management.base import BaseCommand
from shop.models import Product

PRODUCTS = [
    ('Minimalist Cashmere Blend Trench', 'outerwear', 249, 4.9, 128, 'https://images.unsplash.com/photo-1544441893-675973e31985?q=80&w=800&auto=format&fit=crop', ['#2c221e', '#d1c7bd', '#000000'], ['S', 'M', 'L', 'XL'], ['Luxury', 'Winter', 'Bestseller'], 'Best Seller'),
    ('Oversized Organic Cotton Tee', 'women', 45, 4.7, 94, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=800&auto=format&fit=crop', ['#ffffff', '#2c221e', '#a3a3a3'], ['XS', 'S', 'M', 'L'], ['Casual', 'Basics'], 'Sustainable'),
    ('Tailored Linen Blazer', 'men', 185, 4.8, 56, 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=800&auto=format&fit=crop', ['#1e293b', '#e2e8f0'], ['M', 'L', 'XL'], ['Formal', 'Summer'], 'Selling Fast'),
    ('Ribbed Knit Midi Dress', 'women', 110, 4.6, 82, 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?q=80&w=800&auto=format&fit=crop', ['#881337', '#000000'], ['XS', 'S', 'M'], ['Trendy', 'New'], 'New'),
    ('Italian Leather Crossbody Bag', 'accessories', 195, 5.0, 210, 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?q=80&w=800&auto=format&fit=crop', ['#78350f', '#000000'], ['One Size'], ['Leather', 'Bestseller'], 'Best Seller'),
    ('Heavyweight Utility Jacket', 'outerwear', 160, 4.7, 43, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?q=80&w=800&auto=format&fit=crop', ['#3f6212', '#18181b'], ['S', 'M', 'L', 'XL'], ['Streetwear'], ''),
    ('Classic Wool Fedora Hat', 'accessories', 68, 4.5, 31, 'https://images.unsplash.com/photo-1514327605112-b887c0e61c0a?q=80&w=800&auto=format&fit=crop', ['#27272a', '#78350f'], ['M', 'L'], ['Accessories'], ''),
    ('Pleated Wide-Leg Trousers', 'women', 125, 4.8, 77, 'https://images.unsplash.com/photo-1509631179647-0177331693ae?q=80&w=800&auto=format&fit=crop', ['#0f172a', '#d1d5db'], ['S', 'M', 'L'], ['Workwear'], ''),
]


class Command(BaseCommand):
    help = 'Load the AURA product catalog into the database.'

    def handle(self, *args, **options):
        for title, category, price, rating, reviews, image, colors, sizes, tags, badge in PRODUCTS:
            Product.objects.update_or_create(
                title=title,
                defaults={
                    'category': category, 'price': price, 'rating': rating, 'reviews': reviews,
                    'image': image, 'colors': colors, 'sizes': sizes, 'tags': tags, 'badge': badge,
                    'description': f'{title}, designed for everyday AURA elegance.',
                },
            )
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(PRODUCTS)} products.'))
