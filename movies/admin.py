from email.mime import message
from django.utils.safestring import mark_safe
from django.contrib import admin
from django import forms

from .models import (Category, Genre, Movie, MovieShots,
                     Actor, Rating, RatingStar, Review)

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание')

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)  # можно регистрировать в админке с помощью декоратора, указав в параметрах модель
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'name', 'url')  # позволяет в админке отображать колонки с названием, слагом и id
    list_display_links = ('name', )  # позволяет по нажатию на название категории переходить в детализацию


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')  # только для чтения, не позволит редактировать данные поля


class ReviewsInlines(admin.StackedInline):  # класс, для того, чтобы отзывы можно было прикрепить к отображению с другими элементами
# StackedInline - поля выстраиваются вертикально, TabularInline - горизонтально
    model = Review
    extra = 1  # указывает кол-во дополнительных пустых полей для заполнения
    readonly_fields = ('email', 'name')


class MovieShotsInline(admin.StackedInline):
    """ Отображение кадров в детатях фильма """
    model = MovieShots
    extra = 1

    readonly_fields = ('get_image', )  # отображение изображения в деталях

    def get_image(self, obj):  # метод для отображения изображения в админке
        return mark_safe(f'<img src={obj.image.url} width="150" height="auto"')

    get_image.short_description = "Изображение"  # название для столбца


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')  # фильтрация по категории
    search_fields = ('title', 'category__name', 'description')  # поиск
    inlines = [MovieShotsInline, ReviewsInlines]  # позволяет отображать также отзывы к фильму
    save_on_top = True  # выставляет панель со сохранением, удалением и редактированием сверху и снизу
    save_as = True  # появляется кнопка "Сохранить как новый объект", позволяя создавать быстро объекты со схожими полями и меняя только то, что нужно
    list_editable = ('draft',)  # позволяет редактировать графу "черновик" прямо в листинге
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    # fields = (('actors', 'directors', 'genres'), )  # позволяем выстроить поля в одну строку
    readonly_fields = ('get_image', )

    fieldsets = (  # еще один вариант группировки полей
        (None, {
            'fields': (('title', 'tagLine'), )
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actors', {
            'classes': ('collapse',),  # позволяет сворачивать данную группу
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):  # метод для отображения постера в админке
        return mark_safe(f'<img src={obj.poster.url} width="150" height="auto"')

    get_image.short_description = 'Постер'

    """ Добавление действий в админ панель """
    def unpublish(self, request, queryset):
        """ Снять с публикации """
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обновлены'
        self.message_user(request, f'{message_bit}')

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change', )

    def publish(self, request, queryset):
        """ Опубликовать """
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change', )



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )  # отображение изображения в деталях

    def get_image(self, obj):  # метод для отображения изображения в админке
        return mark_safe(f'<img src={obj.image.url} width="auto" height="80"')

    get_image.short_description = "Изображение"  # название для столбца



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'ip', 'star')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')

    readonly_fields = ('get_image', )  # отображение изображения в деталях

    def get_image(self, obj):  # метод для отображения изображения в админке
        return mark_safe(f'<img src={obj.image.url} width="auto" height="80"')

    get_image.short_description = "Изображение"  # название для столбца


# admin.site.register(Category, CategoryAdmin)  # либо можно регистрировать таким образом
# admin.site.register(Genre)
# admin.site.register(Movie)
# admin.site.register(MovieShots)
# admin.site.register(Actor)
# admin.site.register(Rating)
admin.site.register(RatingStar)
# admin.site.register(Reviews)


# Меняем заголовок админки
admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'

