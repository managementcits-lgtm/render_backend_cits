import cloudinary.uploader
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import (
    GalleryImage,
    MOU,
    CareerApplication,
    CommunityItem,
)

def get_public_id(field_file):
    if not field_file:
        return None
    return field_file.name.rsplit(".", 1)[0]


@receiver(post_delete, sender=GalleryImage)
def delete_gallery_image(sender, instance, **kwargs):
    pid = get_public_id(instance.image)
    if pid:
        cloudinary.uploader.destroy(pid)


@receiver(post_delete, sender=MOU)
def delete_mou_pdf(sender, instance, **kwargs):
    pid = get_public_id(instance.pdf)
    if pid:
        cloudinary.uploader.destroy(pid)


@receiver(post_delete, sender=CareerApplication)
def delete_resume(sender, instance, **kwargs):
    pid = get_public_id(instance.resume)
    if pid:
        cloudinary.uploader.destroy(pid)


@receiver(post_delete, sender=CommunityItem)
def delete_community_image(sender, instance, **kwargs):
    pid = get_public_id(instance.image)
    if pid:
        cloudinary.uploader.destroy(pid)



@receiver(pre_save, sender=GalleryImage)
def replace_gallery_image(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = GalleryImage.objects.filter(pk=instance.pk).first()
    if old and old.image != instance.image:
        pid = get_public_id(old.image)
        if pid:
            cloudinary.uploader.destroy(pid)


@receiver(pre_save, sender=MOU)
def replace_mou_pdf(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = MOU.objects.filter(pk=instance.pk).first()
    if old and old.pdf != instance.pdf:
        pid = get_public_id(old.pdf)
        if pid:
            cloudinary.uploader.destroy(pid)


@receiver(pre_save, sender=CommunityItem)
def replace_community_image(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = CommunityItem.objects.filter(pk=instance.pk).first()
    if old and old.image != instance.image:
        pid = get_public_id(old.image)
        if pid:
            cloudinary.uploader.destroy(pid)