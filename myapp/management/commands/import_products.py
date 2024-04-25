import os
import csv
from decimal import Decimal
from datetime import datetime
from django.core.management.base import BaseCommand
from myapp.models import Product

class Command(BaseCommand):
    help = 'Import products from a tab-separated CSV file'

    def handle(self, *args, **kwargs):
        csv_file = os.path.join('myapp', 'management', 'commands', 'merged_dataset.csv')
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    name = row.get('Book_Name', '')
                    price_str = row.get('Book_Price', '')
                    author = row.get('Book_Author', '')
                    rating_str = row.get('Book_Rating', '')
                    release_date_str = row.get('Book_release_date', '')
                    image_url = row.get('Book_Image', '')
                    
                    # Check if all required fields are not empty
                    if name and price_str and author and rating_str and release_date_str and image_url:
                        # Convert string price to Decimal
                        price = Decimal(price_str)
                        
                        # Convert string date to datetime object
                        release_date = datetime.strptime(release_date_str, '%d-%b-%y').date()
                        
                        # Convert string rating to int
                        rating = int(rating_str)
                        
                        # Create Product object
                        Product.objects.create(
                            name=name,
                            price=price,
                            author=author,
                            rating=rating,
                            release_date=release_date,
                            image_url=image_url
                        )
                    else:
                        self.stdout.write(self.style.WARNING('Skipping row due to missing data'))
            self.stdout.write(self.style.SUCCESS('Products imported successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File '{csv_file}' not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
