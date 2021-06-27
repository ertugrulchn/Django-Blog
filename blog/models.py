from enum import unique
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
DEFAULT = 'software'
CATEGORY = (
    ('software', 'yazilim'),
    ('product', 'urun'),
    ('game', 'oyun'),
    ('book', 'kitap'),
    ('movie', 'film'),
)

class Post(models.Model):
    user = models.ForeignKey(
        'auth.User', related_name='post', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name='Başlık')
    content = models.TextField(verbose_name='İçerik')
    publishing_date = models.DateTimeField(
        verbose_name='Yayınlanma Tarihi', auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='post')
    slug = models.SlugField(unique=True, editable=False, max_length=130)
    status = models.CharField(choices=CATEGORY, max_length=10, default=DEFAULT)

    def __str__(self):
        return self.title   

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug':self.slug})    

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))        
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-publishing_date', 'id']        