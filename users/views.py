from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from .forms import UserRegistrationForm,UserLoginForm,UserUpdateForm,SetPasswordForm,PasswordResetForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from .models import Song,Watchlater,History, Channel, Likedsongs
from django.db.models import Case, When

# Create Your Models Here
def update_song(request, song_id):
    # Retrieve the song by its ID
    song = get_object_or_404(Song, song_id=song_id)

    if request.method == "POST":
        # Update song details
        song.name = request.POST.get('name', song.name)
        song.singer = request.POST.get('singer', song.singer)
        song.tags = request.POST.get('tag', song.tags)
        song.movie = request.POST.get('movie', song.movie)
        song.credit = request.POST.get('credit', song.credit)

        # If a new image is uploaded, update it
        if 'image' in request.FILES:
            song.image = request.FILES['image']

        # If a new song file is uploaded, update it
        if 'file' in request.FILES:
            song.song = request.FILES['file']

        # Save the updated song
        song.save()

        messages.success(request, 'Your audio is Updated sucessfully')
        # Redirect to the channel or song page after updating
        return redirect('channel', channel=request.user.username)  # Change 'channel' to your actual URL name

    # If the request method is GET, show the form to update the song
    return render(request, 'users/update_song.html', {'song': song})


def search(request):
    query = request.GET.get("query")
    song = Song.objects.all()
    qs = song.filter(name__icontains=query)

    return render(request, 'users/search.html', {"songs":qs, "query":query})

def upload(request):
    if request.method == "POST":
        name = request.POST['name']
        singer = request.POST['singer']
        tag = request.POST['tag']
        image = request.FILES['image']
        movie = request.POST['movie']
        credit = request.POST['credit']
        song1 = request.FILES['file']

        song_model = Song(name=name, singer=singer, tags=tag, image=image, movie=movie, credit=credit, song=song1)
        song_model.save()

        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name=str(request.user))
        print(channel_find)

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()
        messages.success(request, 'Your audio is sucessfully Uploaded')
    return render(request, "users/upload.html")

def channel(request, channel):
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    song = Song.objects.filter(song_id__in=video_ids).order_by(preserved)    

    return render(request, "users/channel.html", {"channel": chan, "song": song})

def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user, music_id=music_id)
        history.save()

        return redirect(f"/users/songs/{music_id}")
    
    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)
    return render(request, 'users/history.html', {"history":song})

def remove_from_watchlater(request):
    if request.method == "POST":
        video_id = request.POST['video_id']
        user = request.user

        # Try to find the Watchlater entry for the given user and video_id
        try:
            watchlater_entry = Watchlater.objects.get(user=user, video_id=video_id)
            watchlater_entry.delete()  # Delete the entry from Watchlater
            messages.success(request, 'Your audio has been removed from Watch Later.')
        except Watchlater.DoesNotExist:
            messages.warning(request, 'This audio is not in your Watch Later list.')

    # After removing, redirect back to the Watch Later page without changing its content
    return redirect('watchlater')

def watchlater(request):
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        watch = Watchlater.objects.filter(user=user)
        
        for i in watch:
            if video_id == i.video_id:
                #message = "Your Video is Already Added"
                messages.warning(request, 'Your audio is already added in listen later!')
                break
        else:
            watchlater = Watchlater(user=user, video_id=video_id)
            watchlater.save()
            messages.success(request, 'Your audio is sucessfully added')
           # message = "Your Video is Succesfully Added"

        song = Song.objects.filter(song_id=video_id).first()
        return render(request, f"users/songpost.html", {'song': song, "message": messages})

    wl = Watchlater.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "users/watchlater.html", {'song': song})

def remove_from_likedsongs(request):
    if request.method == "POST":
        video_id = request.POST['video_id']
        user = request.user

        # Try to find the Watchlater entry for the given user and video_id
        try:
            watchlater_entry = Likedsongs.objects.get(user=user, video_id=video_id)
            watchlater_entry.delete()  # Delete the entry from Watchlater
            messages.success(request, 'Your audio has been removed from Liked Songs.')
        except Likedsongs.DoesNotExist:
            messages.warning(request, 'This audio is not in your Liked Song list.')

    # After removing, redirect back to the Watch Later page without changing its content
    return redirect('likedsongs')

def likedsongs(request):
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        watch = Likedsongs.objects.filter(user=user)
        
        for i in watch:
            if video_id == i.video_id:
                #message = "Your Video is Already Added"
                messages.warning(request, 'Your audio is already added in listen later!')
                break
        else:
            watchlater = Likedsongs(user=user, video_id=video_id)
            watchlater.save()
            messages.success(request, 'Your audio is sucessfully added')
           # message = "Your Video is Succesfully Added"

        song = Song.objects.filter(song_id=video_id).first()
        return render(request, f"users/songpost.html", {'song': song, "message": messages})

    wl = Likedsongs.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "users/likedsongs.html", {'song': song})


def songpost(request, id):
    song = Song.objects.filter(song_id=id).first()
    return render(request, 'users/songpost.html', {'song': song})

def songs(request):
    song = Song.objects.all()
    return render(request, 'users/songs.html', {'song': song})

def homepage(request):
    song = Song.objects.all()[0:3]

    if request.user.is_authenticated:
        wl = Watchlater.objects.filter(user=request.user)
        ids = []
        for i in wl:
            ids.append(i.video_id)

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        watch = Song.objects.filter(song_id__in=ids).order_by(preserved)
        watch = reversed(watch)
    else:
        watch = Song.objects.all()[0:3]

    return render(request, 'users/home.html', {'song': song, 'watch': watch})


def about(request):
    return render(request, 'users/about.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('homepage')

# Create your views here.
def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

    messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
...

@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            
            channel = Channel(name=user.username)
            channel.save()

            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('homepage')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()
    # in rendering we are giving path to our register.html
    return render(
        request=request,
        template_name = "users/register.html",
        context={"form": form}
    )

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")

@user_not_authenticated
def custom_login(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)

                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("homepage")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(request, error)

    form = UserLoginForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form}
        )


def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, 'users/profile.html', context={'form': form})

    return redirect("homepage")

def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})

@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])    
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")
            else:
                messages.error(request, "The email address you provided is not associated with any account.")
            return redirect('password_reset')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("login")

