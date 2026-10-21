# prison_core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Jail, Prisoner
from accounts.decorators import admin_required

# -- Jail Management Views (Admin Only) --

@login_required
@admin_required
def jail_list(request):
    """
    Displays a list of all jails. Only accessible by admins.
    """
    jails = Jail.objects.all()
    return render(request, 'prison_core/jail_list.html', {'jails': jails})

class JailCreateView(CreateView):
    """
    A view to create a new Jail.
    """
    model = Jail
    fields = ['name', 'location']
    template_name = 'prison_core/jail_form.html'
    success_url = reverse_lazy('jail_list')

    def form_valid(self, form):
        messages.success(self.request, "Jail created successfully.")
        return super().form_valid(form)

class JailUpdateView(UpdateView):
    """
    A view to update an existing Jail's details.
    """
    model = Jail
    fields = ['name', 'location']
    template_name = 'prison_core/jail_form.html'
    success_url = reverse_lazy('jail_list')

    def form_valid(self, form):
        messages.success(self.request, "Jail details updated successfully.")
        return super().form_valid(form)

class JailDeleteView(DeleteView):
    """
    A view to delete a Jail after confirmation.
    """
    model = Jail
    template_name = 'prison_core/jail_confirm_delete.html'
    success_url = reverse_lazy('jail_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Jail deleted successfully.")
        return super().delete(request, *args, **kwargs)

# -- Prisoner Management Views (Admin Only, Filtered by Jail) --

@login_required
@admin_required
def prisoner_list(request):
    """
    Lists all prisoners within the logged-in admin's assigned jail.
    """
    if not request.user.jail:
        messages.error(request, "You are not assigned to a jail. Please contact the super administrator.")
        return redirect('admin_dashboard') # Or some other appropriate page

    prisoners = Prisoner.objects.filter(jail=request.user.jail)
    return render(request, 'prison_core/prisoner_list.html', {'prisoners': prisoners, 'jail': request.user.jail})

from .forms import PrisonerForm # Add this import

@login_required
@admin_required
def prisoner_create(request):
    if request.method == 'POST':
        form = PrisonerForm(request.POST, request.FILES)
        if form.is_valid():
            prisoner = form.save(commit=False)
            prisoner.jail = request.user.jail # Assign the admin's jail
            prisoner.save()
            messages.success(request, "Prisoner created successfully.")
            return redirect('prisoner_list')
    else:
        form = PrisonerForm()
        
    return render(request, 'prison_core/prisoner_form.html', {'form': form})


@login_required
@admin_required
def prisoner_detail(request, pk):
    """
    Shows the detailed view of a single prisoner, ensuring they belong to the admin's jail.
    """
    prisoner = get_object_or_404(Prisoner, pk=pk, jail=request.user.jail)
    return render(request, 'prison_core/prisoner_detail.html', {'prisoner': prisoner})

# You would similarly create Update and Delete views for Prisoners,
# always ensuring to filter by request.user.jail for security.