import json
import PyPDF2, os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from zipfile import ZipFile
from .forms import CreateUser, LoginUser, ProfileImgForm, UserRoleForm, EditForm, PdfFileUpload
from .models import Question, Choice, UploadPdf


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/'
    template_name = 'polls/index.html'
    # for override automatic creating context name
    context_object_name = 'lastest_question'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class CalenderView(generic.TemplateView):
    template_name = 'polls/calender.html'


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


class SquareForm(generic.TemplateView):
    template_name = 'square/sqform.html'


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
        return HttpResponseRedirect(reverse('polls:results', args=question.id))


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
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user_1.userrole.role == 'admin':
            login(request, user)
            return redirect('polls:table')
        elif user_1.userrole.role == 'user':
            login(request, user)
            return redirect('polls:index')
    form = LoginUser()
    context = {'form': form}
    return render(request, 'polls/login.html', context)


# mixinins for adminview
class UserGetMixin:
    model = User

    def get_queryset(self):
        return User.objects.all()


class AdminView(UserGetMixin, LoginRequiredMixin, generic.DetailView):
    # model = User
    login_url = '/'
    template_name = 'polls/admin.html'

    # def get_queryset(self):
    #     return User.objects.all()


class TableView(generic.ListView):
    template_name = 'polls/table.html'
    context_object_name = 'all_user'

    # fetching all user from database except admin user
    def get_queryset(self):
        return [user for user in User.objects.all()]


# for logout user from the app
def user_logout(request):
    logout(request)
    return redirect('polls:login')


# for editing user from the app
def edit(request, user_id):
    edit_user = User.objects.get(id=user_id)
    # instance is used for displaying fields
    form = EditForm(initial={'password1': edit_user.password, 'username': edit_user.username,
                             'first_name': edit_user.first_name, 'last_name': edit_user.last_name})
    context = {
        'edit_user': edit_user,
        'form': form
    }
    return render(request, 'polls/signup.html', context)


# user deleting from the app
def delete_user(request, user_id):
    user_del = User.objects.get(id=user_id)
    print(user_del)
    if request.method == 'POST':
        user_del.delete()
        return redirect('polls:adminview', pk=user_id)
    context = {
        'user_del': user_del
    }
    return render(request, 'polls/delete.html', context)
    # return JsonResponse(user_del)


# class AjaxRequest(generic.View):
def ajax_request(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    form_value = request.POST.get('formData')
    data = dict()
    if request.is_ajax():
        if action == "DELETE":
            qs = User.objects.get(id=user_id)
            qs.delete()
            all_user = User.objects.all()
            data['html_view'] = render_to_string('polls/table.html', {'all_user': all_user})
            return JsonResponse(data)
        elif action == "EDIT":
            edit_user = User.objects.get(id=user_id)
            if request.method == "POST":
                form = EditForm(request.POST,
                                initial={'password1': edit_user.password, 'username': edit_user.username,
                                         'first_name': edit_user.first_name, 'last_name': edit_user.last_name})
                if form.is_valid():
                    json_for = json.loads(form_value)
                    first_name = json_for[1]['value']
                    last_name = json_for[2]['value']
                    username = json_for[3]['value']
                    edit_user.first_name = first_name
                    edit_user.last_name = last_name
                    edit_user.username = username
                    edit_user.save()
                    all_user = User.objects.all()
                    data['table_view'] = render_to_string('polls/table.html', {'all_user': all_user})
                    return HttpResponse(json.dumps(data), content_type="application/json")
        elif action == "payment":
            from square.client import Client
            import uuid
            client = Client(
                access_token='EAAAEKGHC9ln1ADjUHupUnQH3F5yd7OwCrLsc9DLRQxrs2OF1qgHNOTL_NYFycne',
                environment='sandbox',
            )

            data['action'] = request.POST.get('action')
            price = request.POST.get('price')
            nonce = request.POST.get('nonce')
            print(f"nonce:{nonce}")
            idempotency_key = uuid.uuid4().hex[:16]
            body = {
                "source_id": nonce,
                "idempotency_key": idempotency_key,
                "amount_money": {
                    "amount": int(price),
                    "currency": "USD"
                },
            }
            if nonce:
                print('nonce is found')
                payment_api = client.payments
                result = payment_api.create_payment(body)
                if result.is_success():
                    print(result.body)
            else:
                payment_api = client.payments
                result = payment_api.create_payment(body)
                try:
                    err_code = str(result.errors[0].get("category"))
                    err_detail = str(result.errors[0].ge("detail"))

                except:
                    err_code = ""
                    err_detail = str(result.errors[0].get("detail"))
                data['status'] = False
                data['message'] = "Payment Failed: ERROR CODE  {}".format(err_code)
                data['detail'] = f"{err_detail}"
                print(result.is_error)

            return HttpResponse(json.dumps(data), content_type="application/json")


def pdf_file(request):
    if request.method == 'POST':
        form = PdfFileUpload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('polls:pdf')
    else:
        form = PdfFileUpload()
        qs = UploadPdf.objects.all()
        context = {
            'form': form,
            'qs': qs
        }
        return render(request, 'polls/pdf_view.html', context)


def pdf_view(request, pdf_id):
    qs = UploadPdf.objects.get(id=pdf_id)
    zip_r = UploadPdf.objects.get(id=pdf_id)
    media_path = os.path.abspath('.')
    zip_location = media_path + zip_r.zip_file.url
    with ZipFile(zip_location, 'r') as zip:
        zip.extractall(path=f'{media_path}/extract/')
    extracted_dir = media_path + '/extract/'
    all_extracted_pdfs = (os.listdir(extracted_dir))
    print(all_extracted_pdfs)
    for file in all_extracted_pdfs:
        print(file)
        pdf_file_name = file
        text_file_name = file[:-4]
        pdf_open = open(extracted_dir + pdf_file_name, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_open)
        pdf_pages = pdf_reader.numPages
        pdf_html = [pdf_reader.getPage(pdf).extractText() for pdf in range(pdf_pages)]
        pdf_text_file = open(media_path + f'/media/{text_file_name}.txt', 'x')
        [pdf_text_file.writelines(str(pdf)) for pdf in pdf_html]
        pdf_text_file.close()
    return render(request, 'polls/pdftext.html')

# if not media_path + f'/media/{qs.pdf_name}.txt' else os.remove(
#              media_path + f'/media/{qs.pdf_name}.txt')
