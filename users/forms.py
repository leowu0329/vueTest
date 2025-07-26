from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from cases.models import City, Township

User = get_user_model()

class ProfileForm(forms.ModelForm):
    # 設定日期輸入格式
    userBirthday = forms.DateField(
        label=u'生日',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    # 自定義下拉式選單欄位
    userWorkArea = forms.ChoiceField(
        label=u'工作轄區',
        choices=[
            ('', '請選擇工作轄區'),
            ('雙北桃竹苗', '雙北桃竹苗'),
            ('中彰投', '中彰投'),
            ('雲嘉南', '雲嘉南'),
            ('高高屏', '高高屏'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    userPublicOrPrivate = forms.ChoiceField(
        label=u'身分別',
        choices=[
            ('', '請選擇身分別'),
            ('公務', '公務'),
            ('私人', '私人'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    userCountry = forms.ModelChoiceField(
        label=u'縣市',
        required=False,
        queryset=City.objects.all(),
        empty_label='請選擇縣市',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    userTownship = forms.ModelChoiceField(
        label=u'鄉鎮',
        required=False,
        queryset=Township.objects.all(),
        empty_label='請選擇鄉鎮',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'userFirstName', 'userLastName', 'userFullName', 'userWorkArea', 'userRole',
            'userIdentityCard', 'userBirthday', 'userLocalPhone', 'userMobilePhone',
            'userCountry', 'userTownship', 'userVillage', 'userNeighbor', 'userStreet',
            'userSection', 'userLane', 'userAlley', 'userNumber', 'userFloor',
            'userPublicOrPrivate'
        ]
        widgets = {
            'userFirstName': forms.TextInput(attrs={'class': 'form-control'}),
            'userLastName': forms.TextInput(attrs={'class': 'form-control'}),
            'userFullName': forms.HiddenInput(),  # 隱藏全名欄位
            'userRole': forms.NumberInput(attrs={'class': 'form-control'}),
            'userIdentityCard': forms.TextInput(attrs={'class': 'form-control'}),
            'userLocalPhone': forms.TextInput(attrs={'class': 'form-control'}),
            'userMobilePhone': forms.TextInput(attrs={'class': 'form-control'}),
            'userVillage': forms.TextInput(attrs={'class': 'form-control'}),
            'userNeighbor': forms.TextInput(attrs={'class': 'form-control'}),
            'userStreet': forms.TextInput(attrs={'class': 'form-control'}),
            'userSection': forms.TextInput(attrs={'class': 'form-control'}),
            'userLane': forms.TextInput(attrs={'class': 'form-control'}),
            'userAlley': forms.TextInput(attrs={'class': 'form-control'}),
            'userNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'userFloor': forms.TextInput(attrs={'class': 'form-control'}),
        } 