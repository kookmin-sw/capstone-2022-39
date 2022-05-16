from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import PostForm


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'board/board_form.html', {
        'form': form,
    })


# class PostListView(ListView):
#     model = Post
#     paginate_by = 10
#
# post_list = PostListView.as_view()

def post_list(request):
    qs = Post.objects.all()
    q = request.GET.get('q', '')  # key가 없을 때 반환할 값 지정

    if q:
        qs = qs.filter(title__icontains=q)
    return render(request, 'board/post_list.html', {
        'post_list': qs,
        'q': q,
    })


class PostDetailView(DetailView):
    model = Post
    # queryset = Post.objects.filter(is_public=True)

    def get_queryset(self):
        qs = super().get_queryset()
        # if not self.request.user.is_authenticated:
        #     qs = qs.filter(is_public=True)
        return qs

post_detail = PostDetailView.as_view()