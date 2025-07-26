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
        form = YfCaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            case.save()
            messages.success(request, '案件建立成功！')
            return redirect('cases:case_detail', pk=case.pk)
    else:
        form = YfCaseForm()
    
    return render(request, 'cases/case_form.html', {
        'form': form,
        'title': '建立新案件'
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
        form = YfCaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, '案件更新成功！')
            return redirect('cases:case_detail', pk=case.pk)
    else:
        form = YfCaseForm(instance=case)
    
    return render(request, 'cases/case_form.html', {
        'form': form,
        'case': case,
        'title': '編輯案件'
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
    city_id = request.GET.get('city_id')
    if city_id:
        townships = Township.objects.filter(city_id=city_id)
        data = [{'id': t.id, 'name': t.name} for t in townships]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)
