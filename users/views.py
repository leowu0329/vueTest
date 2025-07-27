from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from cases.models import City

# Create your views here.

@login_required
def profile_edit(request):
    """編輯個人資料"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # 自動合併姓氏和名字到全名欄位
            first_name = form.cleaned_data.get('userFirstName', '').strip()
            last_name = form.cleaned_data.get('userLastName', '').strip()
            
            if first_name or last_name:
                full_name = f"{first_name}{last_name}".strip()
                form.instance.userFullName = full_name
            else:
                form.instance.userFullName = ''
            
            form.save()
            messages.success(request, '個人資料更新成功！')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    # 取得所有縣市資料供下拉選單使用
    cities = City.objects.all().order_by('name')
    
    return render(request, 'account/profile.html', {
        'form': form,
        'title': '修改個人資料',
        'cities': cities
    })
