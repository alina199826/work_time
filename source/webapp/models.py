from django.db import models
from accounts.models import User
from django.urls import reverse
import qrcode
import io


class WorkTime(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=False, blank=False,
                                 related_name="user_worktime", verbose_name="Работник")
    start_time = models.DateTimeField(auto_now=True, null=False, blank=False,  verbose_name="Дата начала")
    end_time = models.DateTimeField(verbose_name="Дата конца")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания ")
    organization = models.ForeignKey('webapp.Organization',  null=False, blank=False,
                                     related_name='org_wt', on_delete=models.CASCADE,
                                     verbose_name='Организация')

    def __str__(self):
        return f'{self.pk}. {self.user}'


class Organization(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Название Организации")
    start_time = models.DateTimeField(auto_now_add=True, null=False, blank=False,  verbose_name="Дата начала")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Дата конца")
    email = models.EmailField(verbose_name="Почта")
    branch = models.ForeignKey('webapp.Branch', null=False, blank=False,
                                     related_name='org_wt', on_delete=models.CASCADE, verbose_name="Филиал организации")

    def __str__(self):
        return f'{self.pk}. {self.name}'


class Branch(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Название Филиала")

    def get_qr_code_svg(self):
        url = reverse('branch_detail',
                      args=[str(self.id)])
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        output = io.BytesIO()
        img.save(output)
        svg = output.getvalue().decode('ISO-8859-1')
        output.close()
        return svg

    def __str__(self):
        return f'{self.pk}. {self.name}'

