from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,FormView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .filters import NippoModelFilter
from .models import NippoModel
from .forms import  NippoFormClass,NippoModelForm
from accounts.models import Profile
from utils.access_restrictions import OwnerOnly     # モジュール化したアクセス制限

# リスト　クラスベースビュー
class NippoListView(ListView):
    template_name = "nippo/nippo-list.html"
    model = NippoModel 

    def get_queryset(self):
        q = self.request.GET.get("search")
        qs = NippoModel.objects.search(query=q)
        # 自分の日報なら下書きを見れる
        if self.request.user.is_authenticated:
            qs = qs.filter(Q(public=True)|Q(user=self.request.user))
        else:
            qs = qs.filter(public=True)
        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter"] = NippoModelFilter(self.request.GET, queryset=self.get_queryset())
        profile_id = self.request.GET.get("profile")
        q = Profile.objects.filter(id=profile_id)
        if q.exists():
            ctx["profile"] = q.first()
        return ctx

# 詳細
class NippoDetailView(DetailView):
    template_name = "nippo/nippo-detail.html"
    model = NippoModel

# 新規作成　モデルフォームビュー
# (LoginRequiredMixinでログインユーザーのみアクセスできる)
class NippoCreateModelFormView(LoginRequiredMixin,CreateView):
    # CreateViewを継承しているので保存までできる
    template_name = "nippo/nippo-form.html"
    form_class = NippoModelForm
    success_url = reverse_lazy("nippo-list")

    # 紐づくフォームに辞書型で値を送る
    def get_form_kwargs(self):
        kwgs = super().get_form_kwargs()
        kwgs["user"] = self.request.user    # アクセスしているユーザーの情報を取得
        return kwgs


# 更新　モデルフォームビュー
class NippoUpdateModelFormView(OwnerOnly,UpdateView):
    template_name = "nippo/nippo-form.html"
    model = NippoModel
    form_class = NippoModelForm
    success_url = reverse_lazy("nippo-list")

# 削除
class NippoDeleteView(OwnerOnly,DeleteView):
    template_name = "nippo/nippo-delete.html"
    model = NippoModel
    success_url = reverse_lazy("nippo-list")



#### 以下未使用

def nippoListView(request):
    template_name = "nippo/nippo-list.html"
    ctx = {}
    qs = NippoModel.objects.all()
    ctx["object_list"] = qs
    ctx["something"] = "1"
    return render(request, template_name, ctx)

# 新規作成
def nippoCreateView(request):
    template_name = "nippo/nippo-form.html"
    form = NippoFormClass(request.POST or None)
    ctx = {"form": form}

    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj = NippoModel(title=title, content=content)
        obj.save()
        return redirect("nippo-list")

    return render(request,template_name,ctx)

# 更新
def nippoUpdateView(request, pk):
    template_name = "nippo/nippo-form.html"
    # obj = NippoModel.objects.get(pk=pk)
    obj = get_object_or_404(NippoModel, pk=pk)
    initial_values = {"title": obj.title, "content":obj.content}
    form = NippoFormClass(request.POST or initial_values)
    ctx = {"form": form}
    ctx["object"] = obj

    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj.title = title
        obj.content = content
        obj.save()
        if request.POST:
            return redirect("nippo-list")
        
    return render(request, template_name, ctx)

# 削除
def nippoDeleteView(request, pk):
    template_name = "nippo/nippo-delete.html"
    obj = get_object_or_404(NippoModel, pk=pk)
    ctx = {"object": obj}
    if request.POST:
        obj.delete()
        return redirect("nippo-list")
    return render(request, template_name, ctx)

# フォーム
class NippoCreateFormView(FormView):
    template_name = "nippo/nippo-form.html"
    form_class = NippoFormClass
    success_url = reverse_lazy("nippo-list")     # リダイレクト先(ページ名からurlを取得)

    def form_valid(self, form):
        data = form.cleaned_data     # 辞書型でフォームの入力値を取得
        obj = NippoModel(**data)     # formsとmodelsのフィールド名が同じなので、**で展開して入れられる
        obj.save()
        return super().form_valid(form)
    
