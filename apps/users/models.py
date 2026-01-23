from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Kengaytirilgan foydalanuvchi modeli
    """
    ROLE_CHOICES = [
        ('doctor', 'Shifokor'),
        ('nurse', 'Hamshira'),
        ('lab_tech', 'Laborant'),
        ('admin', 'Administrator'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='doctor',
        verbose_name='Rol'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telefon'
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Bo\'lim'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan sana'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yangilangan sana'
    )

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
