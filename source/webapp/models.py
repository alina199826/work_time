from django.db import models
from django.urls import reverse
import qrcode
import io


class WorkTime(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=False, blank=False,
                             related_name="work_times", verbose_name="Работник")
    start_time = models.DateTimeField(auto_now=True, null=False, blank=False, verbose_name="Дата начала")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Дата конца")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    organization = models.ForeignKey('webapp.Organization', null=False, blank=False,
                                     related_name='work_times', on_delete=models.CASCADE,
                                     verbose_name='Организация')
    branch = models.ForeignKey('webapp.Branch', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Филиал')

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f'{self.user} - {self.start_time.strftime("%d.%m.%Y %H:%M:%S")}'

    @property
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        else:
            return None


class Organization(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Название Организации")
    start_time = models.DateTimeField(auto_now_add=True, null=False, blank=False,  verbose_name="Дата начала")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Дата конца")
    email = models.EmailField(verbose_name="Почта")
    admin = models.ManyToManyField('accounts.User',
                                    related_name='admin_organization',
                                     )

    def __str__(self):
        return f'{self.pk}. {self.name}'


class Branch(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Название Филиала")
    organization = models.ForeignKey('webapp.Organization', null=False, blank=False,
                               related_name='org_branch', on_delete=models.CASCADE, verbose_name="Oрганизациz")
    qr_code = models.TextField(blank=True, null=True, verbose_name='QRcode')

    def get_qr_code_svg(self):
        url = reverse('branch_detail', args=[str(self.id)])
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        output = io.BytesIO()
        img.save(output)
        svg = output.getvalue().decode('ISO-8859-1')
        output.close()
        self.qr_code = svg
        self.save()
        return svg

    def __str__(self):
        return f'{self.pk}. {self.name}'

