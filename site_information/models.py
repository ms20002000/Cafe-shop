from django.db import models

class SiteInfo(models.Model):
    site_name = models.CharField(max_length=255, verbose_name="Site Name")
    logo = models.ImageField(upload_to="site_logo/", verbose_name="Logo")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Address")
    description = models.TextField(verbose_name="Site Description", blank=True, null=True)
    fav_icon = models.ImageField(upload_to="site_logo/", verbose_name="Fav Icon", blank=True, null=True)
    slogan = models.CharField(max_length=50, verbose_name="Slogan", blank=True, null=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Site Information"
        verbose_name_plural = "Site Information"
