from django.db import models
from users.models import CustomUser

class City(models.Model):
    name = models.CharField(u'縣市名稱', max_length=50, unique=True)
    
    class Meta:
        verbose_name = u'縣市'
        verbose_name_plural = u'縣市'
    
    def __str__(self):
        return self.name

class Township(models.Model):
    name = models.CharField(u'鄉鎮區里名稱', max_length=50)
    city = models.ForeignKey(City, verbose_name=u'所屬縣市', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = u'鄉鎮區里'
        verbose_name_plural = u'鄉鎮區里'
        unique_together = ['name', 'city']
    
    def __str__(self):
        return f"{self.city.name} - {self.name}"

class YfCase(models.Model):
    yfcaseCaseNumber = models.CharField(u'案號(*)', max_length=100)
    yfcaseCompany = models.CharField(u'所屬公司', max_length=50)
    yfcaseCity = models.ForeignKey(City, verbose_name=u'縣市', on_delete=models.SET_NULL, null=True)
    yfcaseTownship = models.ForeignKey(Township, verbose_name=u'鄉鎮區里', on_delete=models.SET_NULL, null=True)
    yfcaseBigSection = models.CharField(u'段號', max_length=10, null=True, blank=True)
    yfcaseSmallSection = models.CharField(u'小段', max_length=10, null=True, blank=True)
    yfcaseVillage = models.CharField(u'村里', max_length=100, null=True, blank=True)
    yfcaseNeighbor = models.CharField(u'鄰', max_length=100, null=True, blank=True)
    yfcaseStreet = models.CharField(u'街路', max_length=100, null=True, blank=True)
    yfcaseSection = models.CharField(u'段', max_length=100, null=True, blank=True)
    yfcaseLane = models.CharField(u'巷', max_length=100, null=True, blank=True)
    yfcaseAlley = models.CharField(u'弄', max_length=100, null=True, blank=True)
    yfcaseNumber = models.CharField(u'號', max_length=100)
    yfcaseFloor = models.CharField(u'樓(含之幾)', max_length=100, null=True, blank=True)
    yfcaseCaseStatus = models.CharField(u'案件狀態', max_length=10)
    yfcaseUpdated = models.DateTimeField(u'案件最後更新時間', auto_now=True, auto_now_add=False)
    yfcaseTimestamp = models.DateTimeField(u'案件建立時間', auto_now=False, auto_now_add=True)
    user = models.ForeignKey(CustomUser, verbose_name=u'區域負責人', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = u'案件'
        verbose_name_plural = u'案件'
        ordering = ['-yfcaseTimestamp']
    
    def __str__(self):
        return self.yfcaseCaseNumber
    
    def get_full_address(self):
        """取得完整地址"""
        address_parts = []
        if self.yfcaseCity:
            address_parts.append(self.yfcaseCity.name)
        if self.yfcaseTownship:
            address_parts.append(self.yfcaseTownship.name)
        if self.yfcaseStreet:
            address_parts.append(self.yfcaseStreet)
        if self.yfcaseLane:
            address_parts.append(f"{self.yfcaseLane}巷")
        if self.yfcaseAlley:
            address_parts.append(f"{self.yfcaseAlley}弄")
        if self.yfcaseNumber:
            address_parts.append(f"{self.yfcaseNumber}號")
        if self.yfcaseFloor:
            address_parts.append(self.yfcaseFloor)
        
        return ''.join(address_parts)
