from django.db import models
from django.dispatch import receiver


class DeleteImageOnModelDeleteMixin(models.Model):
    # Mixin to delete image fields from models.
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        for field in self._meta.fields:
            # Find image fields in the model
            if isinstance(field, models.ImageField):
                image_file = getattr(self, field.name)
                # Check if image field is defined and delete it
                if image_file:
                    image_file.delete(save=False)
        super().delete(*args, **kwargs)

    @receiver(models.signals.pre_delete)
    def delete_image_on_model_receiver(sender, instance, **kwargs):
        if issubclass(sender, DeleteImageOnModelDeleteMixin):
            instance.delete()
