from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUser, LoginUser, ProfileImgForm, UserRoleForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/'
    template_name = 'polls/index.html'
    # for override automatic creating context name
    context_object_name = 'lastest_question'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(question)
    print(request.POST)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {'question': question, 'error_msg': "You didn't selected the choice"}
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.vote += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('p:results', args=(question.id,)))


def signup(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        p_form = ProfileImgForm(request.POST, request.FILES)
        role_form = UserRoleForm(request.POST)
        if form.is_valid() and p_form.is_valid() and role_form.is_valid():
            user = form.save()
            user.save()
            role = role_form.save(commit=False)
            profile = p_form.save(commit=False)
            profile.user = user
            role.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                print(profile.picture.url)
                role.save()
            else:
                print('Picture is not Saved')
    form = CreateUser()
    p_form = ProfileImgForm()
    role_form = UserRoleForm
    context = {'form': form, 'p_form': p_form, 'role_form': role_form}

    return render(request, 'polls/signup.html', context)


def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_1 = User.objects.filter(username=username).first()
    p = User.objects.filter(username='pranish1').first()
    user = authenticate(request, username=username, password=password)
    print(user_1)
    # print(f'{user} under user')
    if user is not None:
        if user_1.userrole.role == 'admin':
            login(request, user)
            return redirect('p:adminview')
        elif user_1.userrole.role == 'user':
            print(p)
            print(f'{user} inside user')
            print(user_1.userrole.role)
            login(request, user)
            return redirect('p:index')
    form = LoginUser()
    context = {'form': form}
    return render(request, 'polls/login.html', context)


class AdminView(LoginRequiredMixin, generic.ListView):
    login_url = '/'
    template_name = 'polls/admin.html'
    context_object_name = 'all_user'

    # fetching all user from database except admin user
    def get_queryset(self):
        return [user for user in User.objects.all() if user.userrole.role == 'user']


# for logout user from the app
def user_logout(request):
    logout(request)
    return redirect('p:login')


# for editing user from the app
def edit(request, user_id):
    edit_user = User.objects.get(id=user_id)
    # instance is used for displaying fields
    form = CreateUser(instance=edit_user, initial={'password1': edit_user.password})
    if request.method == 'POST':
        form = CreateUser(request.POST, instance=edit_user, initial={'password1': edit_user.password})
        if form.is_valid():
            print('form is valid')
            form.save()
            return redirect('p:adminview')
        else:
            print('Nothing updated')
    context = {
        'edit_user': edit_user,
        'form': form
    }
    # data =
    # return JsonResponse(edit_user)
    return render(request, 'polls/signup.html', context)


# user deleting from the app
def delete_user(request, user_id):
    user_del = User.objects.get(id=user_id)
    print(user_del)
    if request.method == 'POST':
        user_del.delete()
        return redirect('p:adminview')
    context = {
        'user_del': user_del
    }
    return render(request, 'polls/delete.html', context)
    # return JsonResponse(user_del)
