from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Create your models here.
GRIND_CHOICES = (
    (0, "Whole Bean"),
    (1, "Coarse"),
    (2, "Medium"),
    (3, "Fine"),
    (4, "Extra Fine")
)

GRIND_CHOICES_DICT = dict(GRIND_CHOICES)


CONTINENT_CHOICES = (
    (0, "African"),
    (1, "Asian"),
    (2, "American"),
)


COUNTRY_CHOICES = (
    (0, "Ethiopia"),
    (1, "Kenya"),
    (2, "Uganda"),
    (3, "India"),
    (4, "Vietnam"),
    (5, "Brazil"),
    (6, "Colombia"),
    (7, "Guatemala"),
    (8, "Peru"),
)


REGION_CHOICES = (
    (0, "Sidamo"),
    (1, "Blue Mountain"),
    (2, "Agua Santa"),
    (3, "Excelso Popayan"),
    (4, "Huehuetenango"),
    (5, "Copaceyba"),
    (6, "Malabar"),
    (7, "-")
)

CURRENCY_CHOICES = (
    ("USD", "USD - US Dollar"),
    ("EUR", "EUR - Euro"),
    ("GBP", "GBP - British Pound Sterling"),
    ("JPY", "JPY - Japanese Yen"),
    ("AUD", "AUD - Australian Dollar"),
    ("CAD", "CAD - Canadian Dollar"),
    ("CHF", "CHF - Swiss Franc"),
    ("CNY", "CNY - Chinese Yuan"),
    ("SEK", "SEK - Swedish Krona"),
    ("NZD", "NZD - New Zealand Dollar"),
    ("MXN", "MXN - Mexican Peso"),
    ("SGD", "SGD - Singapore Dollar"),
    ("HKD", "HKD - Hong Kong Dollar"),
    ("NOK", "NOK - Norwegian Krone"),
    ("KRW", "KRW - South Korean Won"),
    ("TRY", "TRY - Turkish Lira"),
    ("INR", "INR - Indian Rupee"),
    ("RUB", "RUB - Russian Ruble"),
    ("ZAR", "ZAR - South African Rand"),
    ("BRL", "BRL - Brazilian Real"),
    ("ILS", "ILS - Israeli New Shekel"),
    ("PLN", "PLN - Polish Zloty"),
    ("THB", "THB - Thai Baht"),
    ("DKK", "DKK - Danish Krone"),
    ("HUF", "HUF - Hungarian Forint"),
    ("CZK", "CZK - Czech Koruna"),
    ("CLP", "CLP - Chilean Peso"),
    ("COP", "COP - Colombian Peso"),
    ("PEN", "PEN - Peruvian Sol"),
    ("ARS", "ARS - Argentine Peso"),
    ("MYR", "MYR - Malaysian Ringgit"),
    ("PHP", "PHP - Philippine Peso"),
    ("PKR", "PKR - Pakistani Rupee"),
    ("MAD", "MAD - Moroccan Dirham"),
    ("AED", "AED - United Arab Emirates Dirham"),
    ("BHD", "BHD - Bahraini Dinar"),
    ("KWD", "KWD - Kuwaiti Dinar"),
    ("OMR", "OMR - Omani Rial"),
    ("JOD", "JOD - Jordanian Dinar"),
    ("DZD", "DZD - Algerian Dinar"),
    ("TND", "TND - Tunisian Dinar"),
)

CURRENCY_SYMBOLS = (
    ("USD", "$"),
    ("EUR", "€"),
    ("GBP", "£"),
    ("JPY", "¥"),
    ("AUD", "A$"),
    ("CAD", "C$"),
    ("CHF", "CHF"),
    ("CNY", "¥"),
    ("SEK", "kr"),
    ("NZD", "NZ$"),
    ("MXN", "$"),
    ("SGD", "S$"),
    ("HKD", "HK$"),
    ("NOK", "kr"),
    ("KRW", "₩"),
    ("TRY", "₺"),
    ("INR", "₹"),
    ("RUB", "₽"),
    ("ZAR", "R"),
    ("BRL", "R$"),
    ("ILS", "₪"),
    ("PLN", "zł"),
    ("THB", "฿"),
    ("DKK", "kr"),
    ("HUF", "Ft"),
    ("CZK", "Kč"),
    ("CLP", "$"),
    ("COP", "$"),
    ("PEN", "S/"),
    ("ARS", "$"),
    ("MYR", "RM"),
    ("PHP", "₱"),
    ("PKR", "₨"),
    ("MAD", "د.م."),
    ("AED", "د.إ"),
    ("BHD", "ب.د."),
    ("KWD", "د.ك"),
    ("OMR", "ر.ع."),
    ("JOD", "د.أ"),
    ("DZD", "د.ج"),
    ("TND", "د.ت"),
)


class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    main_category = models.CharField(max_length=100)

    def __str__(self):
        return self.main_category


class CoffeeOrigin(models.Model):
    origin_id = models.AutoField(primary_key=True)
    continent = models.IntegerField(choices=CONTINENT_CHOICES)
    country = models.IntegerField(choices=COUNTRY_CHOICES)
    region = models.IntegerField(choices=REGION_CHOICES)

    def get_continent_display(self):
        return dict(CONTINENT_CHOICES).get(self.continent)

    def get_country_display(self):
        return dict(COUNTRY_CHOICES).get(self.country)

    def get_region_display(self):
        return dict(REGION_CHOICES).get(self.region)

    def __str__(self):
        return (
        f"{self.get_continent_display()}, "
        f"{self.get_country_display()}, "
        f"{self.get_region_display()}"
    )


class CoffeeGrind(models.Model):
    grind_id = models.AutoField(primary_key=True)
    grind = models.IntegerField(choices=GRIND_CHOICES)

    def get_grind_display(self):
        return dict(GRIND_CHOICES).get(self.grind)

    def __str__(self):
        return self.get_grind_display()


class CoffeeSize(models.Model):
    size_id = models.AutoField(primary_key=True)
    size = models.DecimalField(null=True, max_digits=10, decimal_places=0)
    unit = models.TextField()

    def __str__(self):
        return f"{self.size} {self.unit}"


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="products")
    origin = models.ForeignKey(CoffeeOrigin, on_delete=models.CASCADE,
                                  null=True,
                                  related_name="products")
    grind = models.ForeignKey(CoffeeGrind, on_delete=models.CASCADE,
                                 null=True,
                                 related_name="products")
    size = models.ForeignKey(CoffeeSize, on_delete=models.CASCADE,
                                null=True,
                                related_name="products")
    manufacturer = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def get_currency_symbol(self):
        currency_dict = dict(CURRENCY_CHOICES)
        symbol = next((symbol for code, symbol in CURRENCY_SYMBOLS
                      if code == self.currency), '')
        return symbol

    def get_currency_display(self):
        return self.get_currency_symbol()

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    description = models.TextField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='GBP')
    image = CloudinaryField('image')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name
