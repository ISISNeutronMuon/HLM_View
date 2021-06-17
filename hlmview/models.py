# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# managed = False in the model’s Meta class tells Django not to manage each table’s creation, modification, and deletion.

class GamCoordinate(models.Model):
    coo_id = models.AutoField(db_column='COO_ID', primary_key=True)
    coo_x = models.DecimalField(db_column='COO_X', max_digits=5, decimal_places=0, blank=True, null=True)
    coo_y = models.DecimalField(db_column='COO_Y', max_digits=5, decimal_places=0, blank=True, null=True)
    coo_ob = models.ForeignKey('GamObject', models.DO_NOTHING, db_column='COO_OB_ID')
    coo_img = models.ForeignKey('GamImage', models.DO_NOTHING, db_column='COO_IMG_ID')

    class Meta:
        managed = False
        db_table = 'gam_coordinate'


class GamDisplayformat(models.Model):
    df_id = models.IntegerField(db_column='DF_ID', primary_key=True)
    df_upperlimit = models.DecimalField(db_column='DF_UPPERLIMIT', max_digits=10, decimal_places=4, blank=True, null=True)
    df_lowerlimit = models.DecimalField(db_column='DF_LOWERLIMIT', max_digits=10, decimal_places=4, blank=True, null=True)
    df_alarmhigh = models.DecimalField(db_column='DF_ALARMHIGH', max_digits=10, decimal_places=4, blank=True, null=True)
    df_alarmlow = models.DecimalField(db_column='DF_ALARMLOW', max_digits=10, decimal_places=4, blank=True, null=True)
    df_ratetype = models.DecimalField(db_column='DF_RATETYPE', max_digits=1, decimal_places=0, blank=True, null=True)
    df_decimalplaces = models.DecimalField(db_column='DF_DECIMALPLACES', max_digits=1, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gam_displayformat'


class GamDisplaygroup(models.Model):
    dg_id = models.AutoField(db_column='DG_ID', primary_key=True)
    dg_name = models.CharField(db_column='DG_NAME', max_length=50, blank=True, null=True)
    dg_outofoperation = models.DecimalField(db_column='DG_OUTOFOPERATION', max_digits=1, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'gam_displaygroup'


class GamFunction(models.Model):
    of_id = models.AutoField(db_column='OF_ID', primary_key=True)
    of_name = models.CharField(db_column='OF_NAME', max_length=50, blank=True, null=True)
    of_comment = models.CharField(db_column='OF_COMMENT', max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gam_function'


class GamImage(models.Model):
    img_id = models.AutoField(db_column='IMG_ID', primary_key=True)
    img_blob = models.TextField(db_column='IMG_BLOB', blank=True, null=True)
    img_name = models.CharField(db_column='IMG_NAME', max_length=50)
    img_comment = models.CharField(db_column='IMG_COMMENT', max_length=1000)
    img_diameter = models.IntegerField(db_column='IMG_DIAMETER', blank=True, null=True)
    img_outofoperation = models.DecimalField(db_column='IMG_OUTOFOPERATION', max_digits=1, decimal_places=0)
    img_nw = models.ForeignKey('GamNetwork', models.DO_NOTHING, db_column='IMG_NW_ID')

    class Meta:
        managed = False
        db_table = 'gam_image'


class GamMeasurement(models.Model):
    mea_id = models.AutoField(db_column='MEA_ID', primary_key=True)
    mea_object = models.ForeignKey('GamObject', models.DO_NOTHING, db_column='MEA_OBJECT_ID')
    mea_date = models.DateTimeField(db_column='MEA_DATE')
    mea_date2 = models.DateTimeField(db_column='MEA_DATE2', blank=True, null=True)
    mea_status = models.DecimalField(db_column='MEA_STATUS', max_digits=3, decimal_places=0, blank=True, null=True)
    mea_comment = models.CharField(db_column='MEA_COMMENT', max_length=1000, blank=True, null=True)
    mea_value1 = models.DecimalField(db_column='MEA_VALUE1', max_digits=12, decimal_places=3, blank=True, null=True)
    mea_value2 = models.DecimalField(db_column='MEA_VALUE2', max_digits=12, decimal_places=3, blank=True, null=True)
    mea_value3 = models.DecimalField(db_column='MEA_VALUE3', max_digits=12, decimal_places=3, blank=True, null=True)
    mea_value4 = models.DecimalField(db_column='MEA_VALUE4', max_digits=12, decimal_places=3, blank=True, null=True)
    mea_value5 = models.DecimalField(db_column='MEA_VALUE5', max_digits=12, decimal_places=3, blank=True, null=True)
    mea_valid = models.DecimalField(db_column='MEA_VALID', max_digits=1, decimal_places=0, blank=True, null=True)
    mea_bookingcode = models.DecimalField(db_column='MEA_BOOKINGCODE', max_digits=1, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gam_measurement'
        indexes = [
            models.Index(fields=['mea_object_id'])
        ]


class GamNetwork(models.Model):
    nw_id = models.AutoField(db_column='NW_ID', primary_key=True)
    nw_name = models.CharField(db_column='NW_NAME', max_length=50)
    nw_comment = models.CharField(db_column='NW_COMMENT', max_length=1000, blank=True, null=True)
    nw_outofoperation = models.DecimalField(db_column='NW_OUTOFOPERATION', max_digits=1, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'gam_network'


class GamObject(models.Model):
    ob_id = models.AutoField(db_column='OB_ID', primary_key=True)
    ob_objecttype = models.ForeignKey('GamObjecttype', models.DO_NOTHING, db_column='OB_OBJECTTYPE_ID')
    ob_name = models.CharField(db_column='OB_NAME', max_length=50)
    ob_address = models.CharField(db_column='OB_ADDRESS', max_length=20, blank=True, null=True)
    ob_comment = models.CharField(db_column='OB_COMMENT', max_length=1000, blank=True, null=True)
    ob_posinformation = models.CharField(db_column='OB_POSINFORMATION', max_length=1000, blank=True, null=True)
    ob_status = models.DecimalField(db_column='OB_STATUS', max_digits=3, decimal_places=0, blank=True, null=True)
    ob_lasttimeactive = models.DateTimeField(db_column='OB_LASTTIMEACTIVE', blank=True, null=True)
    ob_endofoperation = models.DateTimeField(db_column='OB_ENDOFOPERATION', blank=True, null=True)
    ob_active = models.DecimalField(db_column='OB_ACTIVE', max_digits=1, decimal_places=0, blank=True, null=True)
    ob_ip = models.CharField(db_column='OB_IP', max_length=20, blank=True, null=True)
    ob_volume = models.DecimalField(db_column='OB_VOLUME', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_value = models.DecimalField(db_column='OB_VALUE', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_minvalue = models.DecimalField(db_column='OB_MINVALUE', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_maxvalue = models.DecimalField(db_column='OB_MAXVALUE', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_critvalue = models.DecimalField(db_column='OB_CRITVALUE', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_comport = models.CharField(db_column='OB_COMPORT', max_length=10, blank=True, null=True)
    ob_tare = models.DecimalField(db_column='OB_TARE', max_digits=7, decimal_places=3, blank=True, null=True)
    ob_enabled1 = models.DecimalField(db_column='OB_ENABLED1', max_digits=1, decimal_places=0, blank=True, null=True)
    ob_substance1 = models.CharField(db_column='OB_SUBSTANCE1', max_length=20, blank=True, null=True)
    ob_span1 = models.DecimalField(db_column='OB_SPAN1', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_zero1 = models.DecimalField(db_column='OB_ZERO1', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_enabled2 = models.DecimalField(db_column='OB_ENABLED2', max_digits=1, decimal_places=0, blank=True, null=True)
    ob_substance2 = models.CharField(db_column='OB_SUBSTANCE2', max_length=20, blank=True, null=True)
    ob_span2 = models.DecimalField(db_column='OB_SPAN2', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_zero2 = models.DecimalField(db_column='OB_ZERO2', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_enabled3 = models.DecimalField(db_column='OB_ENABLED3', max_digits=1, decimal_places=0, blank=True, null=True)
    ob_substance3 = models.CharField(db_column='OB_SUBSTANCE3', max_length=20, blank=True, null=True)
    ob_span3 = models.DecimalField(db_column='OB_SPAN3', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_zero3 = models.DecimalField(db_column='OB_ZERO3', max_digits=10, decimal_places=4, blank=True, null=True)
    ob_shortinterval = models.IntegerField(db_column='OB_SHORTINTERVAL', blank=True, null=True)
    ob_longinterval = models.IntegerField(db_column='OB_LONGINTERVAL', blank=True, null=True)
    ob_quenchtime = models.IntegerField(db_column='OB_QUENCHTIME', blank=True, null=True)
    ob_quenchcurrent = models.IntegerField(db_column='OB_QUENCHCURRENT', blank=True, null=True)
    ob_waittime = models.IntegerField(db_column='OB_WAITTIME', blank=True, null=True)
    ob_meascurrent = models.IntegerField(db_column='OB_MEASCURRENT', blank=True, null=True)
    ob_adcloop = models.IntegerField(db_column='OB_ADCLOOP', blank=True, null=True)
    ob_filltimeout = models.IntegerField(db_column='OB_FILLTIMEOUT', blank=True, null=True)
    ob_cellcount = models.DecimalField(db_column='OB_CELLCOUNT', max_digits=1, decimal_places=0, blank=True, null=True)
    ob_installed = models.DateTimeField(db_column='OB_INSTALLED', blank=True, null=True)
    ob_serno = models.CharField(db_column='OB_SERNO', max_length=50, blank=True, null=True)
    ob_offset_value = models.DecimalField(db_column='OB_OFFSET_VALUE', max_digits=10, decimal_places=3, blank=True, null=True)
    ob_offset_volume = models.DecimalField(db_column='OB_OFFSET_VOLUME', max_digits=10, decimal_places=3, blank=True, null=True)
    ob_offset_corrvolume = models.DecimalField(db_column='OB_OFFSET_CORRVOLUME', max_digits=10, decimal_places=3, blank=True, null=True)
    ob_send_delta_v = models.DecimalField(db_column='OB_SEND_DELTA_V', max_digits=10, decimal_places=3, blank=True, null=True)
    ob_send_delta_p = models.DecimalField(db_column='OB_SEND_DELTA_P', max_digits=4, decimal_places=0, blank=True, null=True)
    ob_displaygroup = models.ForeignKey(GamDisplaygroup, models.DO_NOTHING, db_column='OB_DISPLAYGROUP_ID', blank=True, null=True)
    ob_nw = models.ForeignKey(GamNetwork, models.DO_NOTHING, db_column='OB_NW_ID', blank=True, null=True)
    ob_aliasname = models.CharField(db_column='OB_ALIASNAME', max_length=10, blank=True, null=True)
    ob_df_id_1 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='object_display_format_1', db_column='OB_DF_ID_1', blank=True, null=True)
    ob_df_id_2 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='object_display_format_2', db_column='OB_DF_ID_2', blank=True, null=True)
    ob_df_id_3 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='object_display_format_3', db_column='OB_DF_ID_3', blank=True, null=True)
    ob_df_id_4 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='object_display_format_4', db_column='OB_DF_ID_4', blank=True, null=True)
    ob_df_id_5 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='object_display_format_5', db_column='OB_DF_ID_5', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gam_object'
        indexes = [
            models.Index(fields=['ob_objecttype_id'])
        ]


class GamObjectclass(models.Model):
    oc_id = models.IntegerField(db_column='OC_ID', primary_key=True)
    oc_function = models.ForeignKey(GamFunction, models.DO_NOTHING, db_column='OC_FUNCTION_ID')
    oc_name = models.CharField(db_column='OC_NAME', max_length=50)
    oc_positiontype = models.DecimalField(db_column='OC_POSITIONTYPE', max_digits=2, decimal_places=0)
    oc_comment = models.CharField(db_column='OC_COMMENT', max_length=1000, blank=True, null=True)
    oc_measuretype1 = models.CharField(db_column='OC_MEASURETYPE1', max_length=100, blank=True, null=True)
    oc_measuretype2 = models.CharField(db_column='OC_MEASURETYPE2', max_length=100, blank=True, null=True)
    oc_measuretype3 = models.CharField(db_column='OC_MEASURETYPE3', max_length=100, blank=True, null=True)
    oc_measuretype4 = models.CharField(db_column='OC_MEASURETYPE4', max_length=100, blank=True, null=True)
    oc_measuretype5 = models.CharField(db_column='OC_MEASURETYPE5', max_length=100, blank=True, null=True)
    oc_icon0 = models.CharField(db_column='OC_ICON0', max_length=500, blank=True, null=True)
    oc_icon20 = models.CharField(db_column='OC_ICON20', max_length=500, blank=True, null=True)
    oc_icon40 = models.CharField(db_column='OC_ICON40', max_length=500, blank=True, null=True)
    oc_icon60 = models.CharField(db_column='OC_ICON60', max_length=500, blank=True, null=True)
    oc_icon80 = models.CharField(db_column='OC_ICON80', max_length=500, blank=True, null=True)
    oc_icon_alarm = models.CharField(db_column='OC_ICON_ALARM', max_length=500, blank=True, null=True)
    oc_displaypriority = models.DecimalField(db_column='OC_DISPLAYPRIORITY', max_digits=1, decimal_places=0, blank=True, null=True)
    oc_df_id_1 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='class_display_format_1', db_column='OC_DF_ID_1', blank=True, null=True)
    oc_df_id_2 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='class_display_format_2', db_column='OC_DF_ID_2', blank=True, null=True)
    oc_df_id_3 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='class_display_format_3', db_column='OC_DF_ID_3', blank=True, null=True)
    oc_df_id_4 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='class_display_format_4', db_column='OC_DF_ID_4', blank=True, null=True)
    oc_df_id_5 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='class_display_format_5', db_column='OC_DF_ID_5', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gam_objectclass'


class GamObjectrelation(models.Model):
    or_id = models.AutoField(db_column='OR_ID', primary_key=True)
    or_primary = models.DecimalField(db_column='OR_PRIMARY', max_digits=1, decimal_places=0, blank=True, null=True)
    or_object = models.ForeignKey(GamObject, models.DO_NOTHING, related_name='relation_object_id', db_column='OR_OBJECT_ID')
    or_object_id_assigned = models.ForeignKey(GamObject, models.DO_NOTHING,  related_name='relation_assigned_object_id', db_column='OR_OBJECT_ID_ASSIGNED')
    or_date_assignment = models.DateTimeField(db_column='OR_DATE_ASSIGNMENT')
    or_date_removal = models.DateTimeField(db_column='OR_DATE_REMOVAL', blank=True, null=True)
    or_outflow = models.DecimalField(db_column='OR_OUTFLOW', max_digits=1, decimal_places=0, blank=True, null=True)
    or_bookingrequest = models.DecimalField(db_column='OR_BOOKINGREQUEST', max_digits=1, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gam_objectrelation'
        indexes = [
            models.Index(fields=['or_date_removal', 'or_object'])
        ]


class GamObjecttype(models.Model):
    ot_id = models.AutoField(db_column='OT_ID', primary_key=True)
    ot_objectclass = models.ForeignKey(GamObjectclass, models.DO_NOTHING, db_column='OT_OBJECTCLASS_ID')
    ot_name = models.CharField(db_column='OT_NAME', max_length=50)
    ot_outofoperation = models.DecimalField(db_column='OT_OUTOFOPERATION', max_digits=1, decimal_places=0)
    ot_volume = models.DecimalField(db_column='OT_VOLUME', max_digits=10, decimal_places=4, blank=True, null=True)
    ot_substance = models.CharField(db_column='OT_SUBSTANCE', max_length=20, blank=True, null=True)
    ot_comment = models.CharField(db_column='OT_COMMENT', max_length=1000, blank=True, null=True)
    ot_producer = models.CharField(db_column='OT_PRODUCER', max_length=200, blank=True, null=True)
    ot_model = models.CharField(db_column='OT_MODEL', max_length=200, blank=True, null=True)
    ot_internal_tcomp = models.DecimalField(db_column='OT_INTERNAL_TCOMP', max_digits=1, decimal_places=0, blank=True, null=True)
    ot_temp_norm = models.DecimalField(db_column='OT_TEMP_NORM', max_digits=10, decimal_places=4, blank=True, null=True)
    ot_internal_pcomp = models.DecimalField(db_column='OT_INTERNAL_PCOMP', max_digits=1, decimal_places=0, blank=True, null=True)
    ot_press_norm = models.DecimalField(db_column='OT_PRESS_NORM', max_digits=10, decimal_places=4, blank=True, null=True)
    ot_step = models.DecimalField(db_column='OT_STEP', max_digits=6, decimal_places=4, blank=True, null=True)
    ot_calib_npoints = models.IntegerField(db_column='OT_CALIB_NPOINTS', blank=True, null=True)
    ot_calib_x = models.CharField(db_column='OT_CALIB_X', max_length=1000, blank=True, null=True)
    ot_calib_y = models.CharField(db_column='OT_CALIB_Y', max_length=1000, blank=True, null=True)
    ot_calib_name = models.CharField(db_column='OT_CALIB_NAME', max_length=200, blank=True, null=True)
    ot_df_id_1 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='type_display_format_1', db_column='OT_DF_ID_1', blank=True, null=True)
    ot_df_id_2 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='type_display_format_2', db_column='OT_DF_ID_2', blank=True, null=True)
    ot_df_id_3 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='type_display_format_3', db_column='OT_DF_ID_3', blank=True, null=True)
    ot_df_id_4 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='type_display_format_4', db_column='OT_DF_ID_4', blank=True, null=True)
    ot_df_id_5 = models.ForeignKey(GamDisplayformat, models.DO_NOTHING, related_name='type_display_format_5', db_column='OT_DF_ID_5', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gam_objecttype'
