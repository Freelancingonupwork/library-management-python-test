from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from datetime import timedelta

from .models import Book, BookItem, Author


def books_list_view(request):
    """User-friendly HTML view for displaying books"""
    # Get search query
    search_query = request.GET.get('search', '').strip()
    
    # Get filter parameters
    author_filter = request.GET.get('author', '')
    subject_filter = request.GET.get('subject', '')
    
    # Base queryset with prefetch for performance
    queryset = Book.objects.prefetch_related(
        'author',
        Prefetch(
            'book_items',
            queryset=BookItem.objects.select_related('book')
        )
    ).annotate(
        total_copies=Count('book_items'),
        available_copies=Count('book_items', filter=Q(book_items__status=BookItem.STATUS_AVAILABLE))
    ).order_by('title')
    
    # Apply filters
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(isbn__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(author__name__icontains=search_query)
        ).distinct()
    
    if author_filter:
        queryset = queryset.filter(author__name__icontains=author_filter)
    
    if subject_filter:
        queryset = queryset.filter(subject__icontains=subject_filter)
    
    # Pagination
    paginator = Paginator(queryset, 12)  # Show 12 books per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get all authors and subjects for filter dropdowns
    all_authors = Author.objects.all().order_by('name')
    all_subjects = Book.objects.values_list('subject', flat=True).distinct().order_by('subject')
    
    context = {
        'books': page_obj,
        'search_query': search_query,
        'author_filter': author_filter,
        'subject_filter': subject_filter,
        'all_authors': all_authors,
        'all_subjects': all_subjects,
        'user': request.user,
    }
    
    return render(request, 'library/books_list.html', context)


def book_detail_view(request, book_id):
    """User-friendly HTML view for displaying a single book's details"""
    try:
        book = Book.objects.prefetch_related(
            'author',
            'book_items'
        ).annotate(
            total_copies=Count('book_items'),
            available_copies=Count('book_items', filter=Q(book_items__status=BookItem.STATUS_AVAILABLE)),
            borrowed_copies=Count('book_items', filter=Q(book_items__status=BookItem.STATUS_BORROWED)),
            reserved_copies=Count('book_items', filter=Q(book_items__status=BookItem.STATUS_RESERVED))
        ).get(id=book_id)
        
        # Get available book items
        available_items = book.book_items.filter(status=BookItem.STATUS_AVAILABLE)
        
        context = {
            'book': book,
            'available_items': available_items,
            'user': request.user,
        }
        
        # Check if user is a member and has already borrowed this book
        is_member = False
        has_borrowed = False
        if request.user.is_authenticated:
            from accounts.models import Member
            try:
                member = Member.objects.get(user=request.user)
                is_member = True
                # Check if member has already borrowed any copy of this book
                from borrowing.models import BorrowedBook
                has_borrowed = BorrowedBook.objects.filter(
                    borrower=member,
                    book_item__book=book
                ).exists()
            except Member.DoesNotExist:
                pass
        
        context['is_member'] = is_member
        context['has_borrowed'] = has_borrowed
        
        return render(request, 'library/book_detail.html', context)
    except Book.DoesNotExist:
        from django.http import Http404
        raise Http404("Book not found")


@require_http_methods(["POST"])
def borrow_book_view(request, book_id):
    """Handle book borrowing request"""
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to borrow books.")
        return redirect('account-login')
    
    # Check if user is a member
    from accounts.models import Member
    try:
        member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        messages.error(request, "You must be a registered member to borrow books.")
        return redirect('account-register')
    
    # Get the book
    book = get_object_or_404(Book, id=book_id)
    
    # Check if member has already borrowed this book
    from borrowing.models import BorrowedBook
    if BorrowedBook.objects.filter(borrower=member, book_item__book=book).exists():
        messages.warning(request, f"You have already borrowed '{book.title}'. Please return it before borrowing again.")
        return redirect('library-book-detail', book_id=book_id)
    
    # Find an available book item
    available_item = book.book_items.filter(status=BookItem.STATUS_AVAILABLE).first()
    
    if not available_item:
        messages.error(request, f"Sorry, '{book.title}' is currently not available. All copies are borrowed.")
        return redirect('library-book-detail', book_id=book_id)
    
    # Calculate due date (default 14 days from now)
    due_date = timezone.now().date() + timedelta(days=14)
    
    # Create borrow record
    try:
        BorrowedBook.objects.create(
            book_item=available_item,
            borrower=member,
            due_date=due_date
        )
        messages.success(
            request, 
            f"Successfully borrowed '{book.title}'! Due date: {due_date.strftime('%B %d, %Y')}"
        )
    except Exception as e:
        messages.error(request, f"Error borrowing book: {str(e)}")
    
    return redirect('library-book-detail', book_id=book_id)

