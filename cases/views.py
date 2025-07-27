from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import YfCase, City, Township
from .forms import YfCaseForm, CaseSearchForm

@login_required
def case_list(request):
    """案件列表頁面，包含搜尋、篩選、排序和分頁"""
    form = CaseSearchForm(request.GET)
    cases = YfCase.objects.all()
    
    # 搜尋功能
    if form.is_valid():
        search = form.cleaned_data.get('search')
        if search:
            cases = cases.filter(
                Q(yfcaseCaseNumber__icontains=search) |
                Q(yfcaseStreet__icontains=search) |
                Q(yfcaseLane__icontains=search) |
                Q(yfcaseAlley__icontains=search) |
                Q(yfcaseNumber__icontains=search) |
                Q(yfcaseFloor__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(yfcaseCity__name__icontains=search) |
                Q(yfcaseTownship__name__icontains=search)
            )
        
        # 狀態篩選
        status = form.cleaned_data.get('status')
        if status:
            cases = cases.filter(yfcaseCaseStatus=status)
        
        # 縣市篩選
        city = form.cleaned_data.get('city')
        if city:
            cases = cases.filter(yfcaseCity=city)
        
        # 排序（預設按建立時間遞減）
        sort_by = request.GET.get('sort_by')
        if sort_by == 'yfcaseCaseNumber':
            cases = cases.order_by('yfcaseCaseNumber')
        elif sort_by == '-yfcaseCaseNumber':
            cases = cases.order_by('-yfcaseCaseNumber')
        else:
            cases = cases.order_by('-yfcaseTimestamp')
    
    # 分頁
    paginator = Paginator(cases, 10)  # 每頁10筆
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_count': cases.count(),
    }
    return render(request, 'cases/case_list.html', context)

@login_required
def case_detail(request, pk):
    """案件詳細頁面"""
    case = get_object_or_404(YfCase, pk=pk)
    return render(request, 'cases/case_detail.html', {'case': case})

@login_required
def case_create(request):
    """建立新案件"""
    if request.method == 'POST':
        # 先處理縣市和鄉鎮區里資料
        city_name = request.POST.get('yfcaseCity')
        township_name = request.POST.get('yfcaseTownship')
        
        # 創建一個修改過的 POST 資料副本
        post_data = request.POST.copy()
        
        # 將縣市和鄉鎮區里欄位設為空，避免表單驗證錯誤
        post_data['yfcaseCity'] = ''
        post_data['yfcaseTownship'] = ''
        
        form = YfCaseForm(post_data)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            
            # 處理縣市和鄉鎮區里的外鍵關聯
            if city_name:
                try:
                    city = City.objects.get(name=city_name)
                    case.yfcaseCity = city
                except City.DoesNotExist:
                    pass
            
            if township_name and city_name:
                try:
                    township = Township.objects.get(name=township_name, city__name=city_name)
                    case.yfcaseTownship = township
                except Township.DoesNotExist:
                    pass
            
            case.save()
            messages.success(request, '案件建立成功！')
            return redirect('cases:case_detail', pk=case.pk)
    else:
        form = YfCaseForm()
    
    # 取得所有縣市資料供下拉選單使用
    cities = City.objects.all().order_by('name')
    
    return render(request, 'cases/case_form.html', {
        'form': form,
        'title': '建立新案件',
        'cities': cities
    })

@login_required
def case_update(request, pk):
    """更新案件"""
    case = get_object_or_404(YfCase, pk=pk)
    
    # 檢查權限（只有案件負責人或管理員可以編輯）
    if case.user != request.user and not request.user.is_staff:
        messages.error(request, '您沒有權限編輯此案件！')
        return redirect('cases:case_detail', pk=case.pk)
    
    if request.method == 'POST':
        # 先處理縣市和鄉鎮區里資料
        city_name = request.POST.get('yfcaseCity')
        township_name = request.POST.get('yfcaseTownship')
        
        # 創建一個修改過的 POST 資料副本
        post_data = request.POST.copy()
        
        # 將縣市和鄉鎮區里欄位設為空，避免表單驗證錯誤
        post_data['yfcaseCity'] = ''
        post_data['yfcaseTownship'] = ''
        
        form = YfCaseForm(post_data, instance=case)
        if form.is_valid():
            case = form.save(commit=False)
            
            # 處理縣市和鄉鎮區里的外鍵關聯
            if city_name:
                try:
                    city = City.objects.get(name=city_name)
                    case.yfcaseCity = city
                except City.DoesNotExist:
                    pass
            
            if township_name and city_name:
                try:
                    township = Township.objects.get(name=township_name, city__name=city_name)
                    case.yfcaseTownship = township
                except Township.DoesNotExist:
                    pass
            
            case.save()
            messages.success(request, '案件更新成功！')
            return redirect('cases:case_detail', pk=case.pk)
    else:
        form = YfCaseForm(instance=case)
    
    # 取得所有縣市資料供下拉選單使用
    cities = City.objects.all().order_by('name')
    
    return render(request, 'cases/case_form.html', {
        'form': form,
        'case': case,
        'title': '編輯案件',
        'cities': cities
    })

@login_required
def case_delete(request, pk):
    """刪除案件"""
    case = get_object_or_404(YfCase, pk=pk)
    
    # 檢查權限
    if case.user != request.user and not request.user.is_staff:
        messages.error(request, '您沒有權限刪除此案件！')
        return redirect('cases:case_detail', pk=case.pk)
    
    if request.method == 'POST':
        case.delete()
        messages.success(request, '案件刪除成功！')
        return redirect('cases:case_list')
    
    return render(request, 'cases/case_confirm_delete.html', {'case': case})

def get_townships(request):
    """AJAX: 根據縣市取得鄉鎮區里選項"""
    city_name = request.GET.get('city_id')  # 參數名稱保持不變，但實際傳遞的是縣市名稱
    if city_name:
        try:
            city = City.objects.get(name=city_name)
            townships = Township.objects.filter(city=city)
            data = [{'id': t.name, 'name': t.name} for t in townships]  # 使用鄉鎮名稱作為ID
            return JsonResponse(data, safe=False)
        except City.DoesNotExist:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)
