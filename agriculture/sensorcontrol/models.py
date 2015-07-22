#encoding=utf-8
from django.db import models
from django.core.validators import ValidationError
from django.contrib import admin


class User(models.Model):                           #用户
    username = models.CharField(primary_key=True, max_length=20, unique=True)
    password = models.CharField(max_length=20)
    mail = models.EmailField(max_length=255, unique=True, null=True)
    #license = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'user'


class Storage(models.Model):                        #库房
    index = models.PositiveIntegerField(primary_key=True, unique=True)
    owner = models.ForeignKey(User, db_column='owner')
    num_air=models.PositiveIntegerField()
    num_soilt=models.PositiveIntegerField()
    num_soilm=models.PositiveIntegerField()
    num_sunlight=models.PositiveIntegerField()
    num_coz=models.PositiveIntegerField()
    class Meta:
        db_table = 'storage'


class Sensor(models.Model):                         #传感器
    sensor_index = models.PositiveIntegerField()
    location = models.CharField( max_length=20)
    type = models.CharField( max_length=20)
    storage = models.ForeignKey(Storage, db_column='storage')

    class Meta:
        db_table = 'sensor'
        unique_together = ("sensor_index", "storage")


class Air(models.Model):                            #空气温湿度
    sensor_index = models.ForeignKey(Sensor, db_column='sensor_index')
    temp = models.FloatField()
    hum = models.FloatField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'air_temp'


class SoilMoist(models.Model):                          #土壤湿度
    sensor_index=models.ForeignKey(Sensor, db_column='sensor_index')
    temp=models.FloatField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'soil_moist'


class SoilTemp(models.Model):                             #土壤温度
    sensor_index=models.ForeignKey(Sensor, db_column='sensor_index')
    temp=models.FloatField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'soil_temp'


class SunLight(models.Model):                               #光照
    sensor_index=models.ForeignKey(Sensor, db_column='sensor_index')
    light=models.FloatField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'sun_light'


class COZ(models.Model):                                    #二氧化碳
    sensor_index=models.ForeignKey(Sensor,  db_column='sensor_index')
    content=models.FloatField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'coz'


class IP(models.Model):
    ip = models.GenericIPAddressField(unpack_ipv4=False)

    class Meta:
        db_table ='ip'



def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    创建指定model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label必须用Meta内部类来设定
        setattr(Meta, 'app_label', app_label)

    # 若提供了options参数，就要用更新Meta类
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # 创建一个字典来模拟类的声明，module和当前所在的module对应
    attrs = {'__module__': module, 'Meta': Meta}

    # 加入所有提供的字段
    if fields:
        attrs.update(fields)

    # 创建这个类，这会触发ModelBase来处理
    model = type(name, (models.Model,), attrs)

    # 如果提供了admin参数，那么创建Admin类
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model



class MyApp(models.Model):
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MyModel(models.Model):
    app = models.ForeignKey(MyApp, related_name='mymodels')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_django_model(self):
        "Returns a functional Django model based on current data"
        # Get all associated fields into a list ready for dict()
        fields = [(f.name, f.get_django_field()) for f in self.myfields.all()]

        # Use the create_model function defined above
        return create_model(self.name, dict(fields), self.app.name, self.app.module)

    class Meta:
        unique_together = (('app', 'name'),)

def is_valid_field(self, field_data, all_data):
    if hasattr(models, field_data) and issubclass(getattr(models, field_data), models.Field):
        # It exists and is a proper field type
        return
    raise ValidationError("This is not a valid field type.")

class MyField(models.Model):
    model = models.ForeignKey(MyModel, related_name='myfields')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, validators=[is_valid_field])

    def get_django_field(self):
        "Returns the correct field type, instantiated with applicable settings"
        # Get all associated settings into a list ready for dict()
        settings = [(s.name, s.value) for s in self.mysettings.all()]

        # Instantiate the field with the settings as **kwargs
        return getattr(models, self.type)(*dict(settings))

    class Meta:
        unique_together = (('model', 'name'),)

class MySetting(models.Model):
    field = models.ForeignKey(MyField, related_name='mysettings')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = (('field', 'name'),)