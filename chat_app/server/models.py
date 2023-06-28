from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .mixins import DeleteImageOnModelDeleteMixin
from .validators import validate_icon_image_size, validate_image_file_extension


def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"


def server_channel_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icons/{filename}"


def server_channel_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banners/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon_upload_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if updating or saving category for icon image
        if self.id:
            existing_category = get_object_or_404(Category, id=self.id)
            if existing_category.icon != self.icon:
                existing_category.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def _category_delete_icon_receiver(sender, instance, **kwargs):
        # To delete category icon file connected to Category when deleting its instance.
        for field in instance._meta.fields:
            # Find icon field in fields if exists
            if field.name == "icon":
                icon_file = getattr(instance, field.name)
                # Check if icon image is defined and delete it.
                if icon_file:
                    icon_file.delete(save=False)

    def __str__(self) -> str:
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="server_category")
    description = models.CharField(max_length=250, blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self) -> str:
        return self.name


class Channel(DeleteImageOnModelDeleteMixin, models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channel_server")
    banner = models.ImageField(
        upload_to=server_channel_banner_upload_path,
        null=True,
        blank=True,
        validators=[
            validate_image_file_extension,
        ],
    )
    icon = models.ImageField(
        upload_to=server_channel_icon_upload_path,
        null=True,
        blank=True,
        validators=[
            validate_icon_image_size,
            validate_image_file_extension,
        ],
    )

    def save(self, *args, **kwargs):
        # save lowercase names to database
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
