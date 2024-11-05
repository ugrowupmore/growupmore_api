# utils/image_utils.py

import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

def generate_image_path(instance, filename, folder_name, field_name):
    """
    Generate the image path based on the given folder name and field name.
    """
    extension = filename.split('.')[-1]
    filename = f"{getattr(instance, field_name)}.{extension}"
    return os.path.join(folder_name, filename)

def delete_old_image_on_save(instance, field_name):
    """
    Deletes the old image file from the filesystem when updating the image field.
    """
    if instance.pk:
        model_class = instance.__class__
        try:
            old_instance = model_class.objects.get(pk=instance.pk)
            old_image = getattr(old_instance, field_name)
            new_image = getattr(instance, field_name)
            if old_image and old_image.name != new_image.name and old_image.name != 'na.png':
                old_image.delete(save=False)
        except model_class.DoesNotExist:
            pass  # If the instance does not exist, no action is needed

def delete_image_on_delete(instance, field_name):
    """
    Deletes the image file from the filesystem when the corresponding instance is deleted.
    """
    image = getattr(instance, field_name)
    if image and image.name != 'na.png':
        file_path = image.path
        if os.path.isfile(file_path):
            os.remove(file_path)

def register_image_delete_signal(model_class, field_name):
    """
    Registers a signal to delete the image file when an instance of the model is deleted.
    """
    @receiver(post_delete, sender=model_class)
    def _delete_image_on_delete(sender, instance, **kwargs):
        delete_image_on_delete(instance, field_name)
