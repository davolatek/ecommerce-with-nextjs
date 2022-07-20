from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Category(MPTTModel):
    """
    class implemented with MPTT Model

    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and Unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Category Safe url"), max_length=255, unique=True
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("ecommerce_api:category_detail", args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    This stores the various product type of a particular product
    """

    name = models.CharField(
        verbose_name=_("Product Type"), help_text=_("Required"), max_length=255
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    This contains specifications or features of the product type
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_("Name"), help_text=_("Required"), max_length=255
    )

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    This Table stores all product item and
    its details
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("title"), help_text=_("Required"), max_length=255
    )
    description = models.TextField(
        verbose_name=_("description"), help_text=_("Not required"), blank=True
    )
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular Price"),
        help_text=_("Maximum 999.99"),
        max_digits=5,
        decimal_places=2,
        error_messages={"name": {"Price must be between 0 and 999.99"}},
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount Price"),
        help_text=_("Maximum 999.99"),
        max_digits=5,
        decimal_places=2,
        error_messages={"name": {"Price must be between 0 and 999.99"}},
    )
    is_active = models.BooleanField(
        verbose_name=_("Product Visibility"),
        help_text=_("Change Product Visibility"),
        default=True,
    )
    created_at = models.DateTimeField(_("Created Time"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated Time"), auto_now=True)

    class Meta:
        ordering = "-created_at"
        verbose_name = _("Product")
        verbose_name_plural = _("products")

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    """
    The table store values associated with the Product sepcification
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Product Specification value"),
        help_text=_("Product Specification Value, Maximum length of 255"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = (
        models.ImageField(
            verbose_name=_("Images"),
            help_text=_("Upload Product Images"),
            upload_to="images/",
        ),
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text for Images"),
        help_text=_("Alternative text for Images"),
        blank=True,
        null=True,
        max_length=255,
    )
    is_feature = models.BooleanField(default=False)

    created_at = models.DateTimeField(_("Created Time"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated Time"), auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    
