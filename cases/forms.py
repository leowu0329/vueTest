from django import forms
from .models import YfCase, City, Township

class YfCaseForm(forms.ModelForm):
    # 自定義下拉式選單欄位
    yfcaseCaseStatus = forms.ChoiceField(
        label=u'案件狀態(*)',
        choices=[
            ('', '請選擇案件狀態'),
            ('在途', '在途'),
            ('結案', '結案'),
        ],
        initial='在途',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    yfcaseCompany = forms.ChoiceField(
        label=u'所屬公司(*)',
        choices=[
            ('', '請選擇所屬公司'),
            ('揚富開發有限公司', '揚富開發有限公司'),
            ('鉅鈦開發有限公司', '鉅鈦開發有限公司'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = YfCase
        fields = [
            'yfcaseCaseNumber', 'yfcaseCompany', 'yfcaseCity', 'yfcaseTownship',
            'yfcaseBigSection', 'yfcaseSmallSection', 'yfcaseVillage', 'yfcaseNeighbor',
            'yfcaseStreet', 'yfcaseSection', 'yfcaseLane', 'yfcaseAlley',
            'yfcaseNumber', 'yfcaseFloor', 'yfcaseCaseStatus'
        ]
        widgets = {
            'yfcaseCaseNumber': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'yfcaseCity': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'yfcaseTownship': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'yfcaseBigSection': forms.TextInput(attrs={'class': 'form-control'}),
            'yfcaseSmallSection': forms.TextInput(attrs={'class': 'form-control'}),
            'yfcaseVillage': forms.TextInput(attrs={'class': 'form-control'}),
            'yfcaseNeighbor': forms.TextInput(attrs={'class': 'form-control'}),
            'yfcaseStreet': forms.TextInput(attrs={'class': 'form-control'}),
            'yfcaseSection': forms.TextInput(attrs={'class': 'form-control'}),
            'yfcaseLane': forms.TextInput(attrs={'class': 'form-control'}),
            'yfcaseAlley': forms.TextInput(attrs={'class': 'form-control'}),
            'yfcaseNumber': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'yfcaseFloor': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CaseSearchForm(forms.Form):
    search = forms.CharField(
        label='搜尋',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '模糊比對(案號、住址、負責人...等)'
        })
    )
    status = forms.ChoiceField(
        label='狀態',
        required=False,
        choices=[('', '全部')] + [
            ('在途', '在途'),
            ('結案', '結案'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    city = forms.ModelChoiceField(
        label='縣市',
        required=False,
        queryset=City.objects.all(),
        empty_label='全部縣市',
        widget=forms.Select(attrs={'class': 'form-control'})
    ) 