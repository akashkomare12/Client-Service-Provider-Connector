from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Avg
from rest_framework.response import Response
from .models import Client, ServiceProvider, ServiceRecords
from .serializers import ClientSerializer, ServiceProviderSerializer, ServiceRecordsSerializer
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .forms import UpdateClientProfileForm


def home(request):
    return render(request, 'help/home.html')
# Register a new client------------------------------------------------------------------------------------------------------------------
def register_page(request):
    return render(request, 'help/client_register.html')
@csrf_exempt
@api_view(['POST', 'OPTIONS'])
def register_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(password=make_password(request.data.get('password')))
        return Response({"message": "Client registered successfully!"}, status=201)
    return Response(serializer.errors, status=400)

# Login client---------------------------------------------------------------------------------------------------------------------------
def login_page(request):
    return render(request, 'help/client_login.html')
@csrf_exempt
@api_view(['POST', 'OPTIONS'])
def login_client(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(f"Received username: {username}, password: {password}")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Logged in successfully!"}, status=200)
    else:
        return Response({"error": "Invalid credentials!"}, status=401)

@login_required
def client_service_page(request):
    # Fetch the logged-in client's profile
    client = Client.objects.get(username=request.user.username)
    # Fetch the logged-in client's service records
    services = ServiceRecords.objects.filter(u_id=client.client_id)

    context = {
        'client': client,
        'services': services
    }
    return render(request, 'help/client_service.html', context)
#client dashboard -----------------------------------------------------------------------------------------------------------------
@login_required
def client_dashboard(request):
    # Fetch the logged-in client's profile
    client = Client.objects.get(username=request.user.username)
    
    # Fetch the logged-in client's service records
    services = ServiceRecords.objects.filter(u_id=client.client_id)
    
    # Fetch all service providers and their average ratings
    service_providers = ServiceProvider.objects.all()
    provider_ratings = (
        ServiceRecords.objects
        .values('sp_id')  # Group by service provider ID
        .annotate(average_rating=Avg('ratings'))  # Compute average rating
    )

    # Create a dictionary for quick lookup of ratings by service provider ID
    ratings_dict = {entry['sp_id']: entry['average_rating'] for entry in provider_ratings}

    # Add average rating to each service provider
    for provider in service_providers:
        provider.average_rating = ratings_dict.get(provider.sp_id, 0)  # Default to 0 if no ratings

    context = {
        'client': client,
        'services': services,
        'service_providers': service_providers,
    }
    return render(request, 'help/client_dashboard.html', context)

#Service Provider dashboard -----------------------------------------------------------------------------------------------------------------
@login_required
def service_dashboard(request):
    # Fetch the logged-in client's profile
    service = ServiceProvider.objects.get(username=request.user.username)
    print(service.skills)
    # Fetch the logged-in client's service records
    services = ServiceRecords.objects.filter(sp_id=service.sp_id)

    context = {
        'service': service,
        'services': services,
    }
    return render(request, 'help/service_provider_dashboard.html', context)

def update_service_provider_page(request):
    service = ServiceProvider.objects.get(username=request.user.username)
    print(service.skills)
    # Fetch the logged-in client's service records
    services = ServiceRecords.objects.filter(sp_id=service.sp_id)

    context = {
        'service': service,
        'services': services,
    }
    return render(request, 'help/update_service_provider.html',context)

def update_client_page(request):
    client = Client.objects.get(username=request.user.username)
    # Fetch the logged-in client's service records
    context = {
        'client': client
    }
    return render(request, 'help/update_client.html',context)
#update client profile --------------------------------------------------------------------------------------------------------
@csrf_exempt
@api_view(['PUT'])
def update_client_profile(request):
    try:
        # Retrieve the client associated with the logged-in user
        client = Client.objects.get(username=request.user.username)
    except Client.DoesNotExist:
        return Response({"error": "Client not found."}, status=status.HTTP_404_NOT_FOUND)

    # Deserialize and validate the incoming data
    serializer = ClientSerializer(client, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return redirect('client_dashboard')
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

# Logout client------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@api_view(['POST'])
def logout_client(request):
    logout(request)
    return redirect('home')

# Register Service provider -----------------------------------------------------------------------------------------------------
def service_register_page(request):
    return render(request, 'help/service_provider_register.html')

@csrf_exempt
@api_view(['POST', 'OPTIONS'])
def register_service_provider(request):
    serializer = ServiceProviderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(password=make_password(request.data.get('password')))
        return Response({"message": "Service Provider registered successfully!"}, status=201)
    return Response(serializer.errors, status=400)



#login service provider ----------------------------------------------------------------------------------------------------------
def service_login_page(request):
    return render(request, 'help/service_provider_login.html')
@csrf_exempt
@api_view(['POST', 'OPTIONS'])
def login_service_provider(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(username,password)
    provider = authenticate(request, username=username, password=password)
    if provider is not None:
        login(request, provider)
        return Response({"message": "Logged in successfully!"}, status=200)
    return Response({"error": "Invalid credentials!"}, status=401)

#logout service provider ----------------------------------------------------------------------------------------------------------
@api_view(['POST'])
def logout_service_provider(request):
    logout(request)
    return Response({"message": "Logged out successfully!"}, status=200)

# Get list of service providers -----------------------------------------------------------------------------------------------------
@api_view(['GET'])
@login_required
def get_service_providers(request):
    service_providers = ServiceProvider.objects.all()
    serializer = ServiceProviderSerializer(service_providers, many=True)
    return Response(serializer.data, status=200)


# Book a service ------------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
@login_required
def book_service(request):
    # Ensure sp_id is passed as an integer ID
    sp_id = request.data.get('sp_id')
    if not sp_id:
        return Response({"error": "Service Provider ID (sp_id) is required."}, status=400)
    
    try:
        # Fetch the service provider using the sp_id
        service_provider = ServiceProvider.objects.get(sp_id=sp_id)
    except ServiceProvider.DoesNotExist:
        return Response({"error": "Service provider with this ID does not exist."}, status=404)

    try:
        # Fetch the logged-in client
        client = Client.objects.get(client_id=request.user.client_id)

        # Prepare the data for the ServiceRecordsSerializer
        data = {
            'u_id': client.client_id,  # Pass the client's ID
            'sp_id': service_provider.sp_id,  # Pass the service provider's ID
            'service': service_provider.skills,  # Retrieve the 'service' field from ServiceProvider
            'date': request.data.get('date'),
            'amount': request.data.get('amount'),
            'status': 'pending',  # Default status
        }
        print(data)
        # Serialize the data
        serializer = ServiceRecordsSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            # Save the service record
            serializer.save()
            return Response({"message": "Service booked successfully!"}, status=201)
        if not serializer.is_valid():
            print("Serializer Errors:", serializer.errors)

        return Response(serializer.errors, status=400)
    except Client.DoesNotExist:
        return Response({"error": "Client not found!"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

#update client ----------------------------------------------------------------------------------------------------------

@api_view(['PUT'])
@login_required
def update_client(request):
    client = Client.objects.get(client_id=request.user.client_id)
    serializer = ClientSerializer(client, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Client information updated successfully!"}, status=200)
    return Response(serializer.errors, status=400)

#update service provider -----------------------------------------------------------------------------------------------------------
@api_view(['PUT'])
@login_required
def update_service_provider(request):
    provider = ServiceProvider.objects.get(sp_id=request.user.sp_id)
    serializer = ServiceProviderSerializer(provider, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Service Provider information updated successfully!"}, status=200)
    return Response(serializer.errors, status=400)

#ger service records ---------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
@login_required
def get_service_records(request):
    try:
        # Get the logged-in user's client details
        client = Client.objects.get(client_id=request.user.client_id)

        # Retrieve all service records for the client
        records = ServiceRecords.objects.filter(u_id=client)

        # Serialize the records
        serializer = ServiceRecordsSerializer(records, many=True)

        # Return serialized data as a JSON response
        return Response(serializer.data, status=200)
    except Client.DoesNotExist:
        return Response({"error": "Client not found!"}, status=404)
    except Exception as e:
        return Response({"error": "Something went wrong!"}, status=500)

@login_required
def book_service_client(request):
    try:
        # Get the logged-in user's client details
        client = Client.objects.get(client_id=request.user.client_id)

        # Retrieve all service records for the client
        records = ServiceRecords.objects.filter(u_id=client)

        # Serialize the records
        serializer = ServiceRecordsSerializer(records, many=True)

        # Return serialized data as a JSON response
        return Response(serializer.data, status=200)
    except Client.DoesNotExist:
        return Response({"error": "Client not found!"}, status=404)
    except Exception as e:
        return Response({"error": "Something went wrong!"}, status=500)


#edit service record --------------------------------------------------------------------------------------------------------------------
def edit_service_page(request):
    return render(request, 'help/edit_service.html')
@login_required
def edit_service_record(request, record_id):
    # Fetch the service record with the given record_id
    service_record = get_object_or_404(ServiceRecords, pk=record_id, u_id=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_rating = request.POST.get('rating')

        if new_status in ['pending', 'completed', 'cancelled']:
            service_record.status = new_status

        if new_rating:
            try:
                new_rating = int(new_rating)
                if 1 <= new_rating <= 5:
                    service_record.ratings = new_rating
                else:
                    return render(request, 'help/edit_service.html', {
                        'service_record': service_record,
                        'error': "Rating must be between 1 and 5."
                    })
            except ValueError:
                return render(request, 'edit_service.html', {
                    'service_record': service_record,
                    'error': "Invalid rating. Please enter a number between 1 and 5."
                })

        service_record.save()
        return redirect('client_dashboard')

    return render(request, 'help/edit_service.html', {
        'service_record': service_record
    })